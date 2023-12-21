"""orcestrator, higherst level of the framework"""
#pylint: disable=global-variable-undefined
#pylint: disable=global-variable-not-assigned
#pylint: disable=no-self-argument
#pylint: disable=cell-var-from-loop
#pylint: disable=line-too-long
#pylint: disable=consider-using-set-comprehension
#pylint: disable=consider-iterating-dictionary
#pylint: disable=consider-using-dict-items
#pylint: disable=use-a-generator
#pylint: disable=no-else-break
#pyint: disable=use-implicit-booleaness-not-comparison
#pylint: disable=too-many-branches
#pylint: disable=use-implicit-booleaness-not-comparison
#pylint: disable=consider-using-generator
#pylint: disable=dangerous-default-value

import os
import sys
import datetime
from copy import copy
import time
import json
from typing import Union,Optional
from pathlib import Path
import asyncio
import requests

import uvicorn
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel, validator

import numpy
import h5py

from mischbares.logger import logger
from mischbares.utils import orchestrator_utils
from mischbares.config.main_config import config


log = logger.get_logger("orchestrator")

SERVERKEY = "orchestrator"


app = FastAPI(title="Orchestrator",description="Orchestrator for the mischbares framework",
              version="2.1.0")


class Experiment(BaseModel):
    """ validation class
    """
    soe: list
    params: dict
    meta: Optional[dict]

    @validator('soe')
    def native_command_ordering(cls, experiments):
        """ check if the soe is in the right order

        Args:
            experiments (list): list of experiments

        Returns:
            retc (ReturnClass): return class with the parameters and the data
        """
        for i in experiments:
            if i.count('_') > 1:
                raise ValueError("too many underscores in function name")
        for i in experiments:
            if i.count('/') != 1 or i[0] == '/' or i[-1] == '/':
                raise ValueError("action must consist of a server name and a function name separated by '/'")

        # check inappropriate experiments
        parsed_v = [i.split('_')[0] for i in experiments]
        if parsed_v.count("orchestrator/start") > 1:
            raise ValueError("cannot have multiple calls to orchestrator/start in single soe")
        if "orchestrator/start" in parsed_v and parsed_v[0] != "orchestrator/start":
            raise ValueError("orchestrator/start must be first action in soe")
        if parsed_v.count("orchestrator/finish") > 1:
            raise ValueError("cannot have multiple calls to orchestrator/finish in single soe")
        if "orchestrator/finish" in parsed_v and parsed_v[-1] != "orchestrator/finish":
            raise ValueError("orchestrator/start must be last action in soe")
        if parsed_v.count("orchestrator/repeat") > 1:
            raise ValueError("cannot have multiple calls to orchestrator/repeat in single soe")
        if "orchestrator/repeat" in parsed_v and not (parsed_v[-1] == "orchestrator/repeat" or\
            parsed_v[-2] == "orchestrator/repeat" and parsed_v[-1] == "orchestrator/finish"):
            raise ValueError("orchestrator/repeat can only be followed \
                by orchestrator/finish in soe")
        return experiments


    @validator('params')
    def parameter_correspondence(cls, experiment, values):
        """ check if the parameters are in the right order

        Args:
            experiment (dict): dict of experiments
            experiment_values (list): list of experiments

        returns:
            experiment (dict): dict of experiments
        """
        action = set([i.split('/')[-1] for i in values['soe']])
        if action != set(experiment.keys()):
            raise ValueError("soe and params are not perfectly corresponding. \n \
                must be params entry for every action in soe, and vice-versa")
        if len(action) != len(values['soe']):
            raise ValueError("duplicate entries in soe")
        return experiment


@app.get("/health")
def health_check():
    """ health check to see if the server is up and running
    Returns:
        dict: status
    """
    return {"status": "healthy"}

@app.post("/orchestrator/addExperiment")
async def send_measurement(experiment: str, thread: int = 0, priority: int = 10):
    """ Add sequence of experiment to the queue of the orchestrator

    Args:
        experiment (str): experiment to be added to the queue
        thread (int): thread to which the experiment is added
        priority (int): priority of the experiment in the queue
    """
    global INDEX
    # load experiment and run it through pydantic validation
    experiment = dict(Experiment(**json.loads(experiment)))
    await SCHEDULER_QUEUE.put((priority,INDEX,experiment,thread))
    INDEX += 1


async def scheduler():
    """ Receives all experiments, creates new threads, and sends experiments
    to the appropriate thread"""
    global EXPERIMENT_QUEUES,EXPERIMENT_TASKS,LOOP,TRACKING
    while True:
        priority,index,experiment,thread = await SCHEDULER_QUEUE.get()
        if thread not in EXPERIMENT_QUEUES.keys():
            EXPERIMENT_QUEUES.update({thread:asyncio.PriorityQueue()})
             # several instances of the infinite loop , one for each thread
            EXPERIMENT_TASKS.update({thread:LOOP.create_task(infl(thread))})
            # get the status that initializing the thread
            TRACKING[thread] = {'path':None, 'run':None,'experiment':None,\
                'current_action':None,'status':'uninitialized','history':[]}
        await EXPERIMENT_QUEUES[thread].put((priority,index,experiment))


async def infl(thread: int):
    """ Executes a single thread of experiments"""
    while True:
        *_,experiment = await EXPERIMENT_QUEUES[thread].get()
        if TRACKING[thread]['status'] == 'clear':
            #await update_tracking(thread,'running','status')
            TRACKING[thread]['status'] = 'running'
        await do_measurement(experiment, thread)
        if EXPERIMENT_QUEUES[thread].empty() and TRACKING[thread]['status'] == 'running':
            #await update_tracking(thread,'clear','status')
            TRACKING[thread]['status'] = 'clear'

async def do_measurement(experiment: dict, thread: int):
    """ Executes a single experiment"""
    global TRACKING,LOOP,FILELOCKS,SERVERLOCKS,TASK
    log.info(f'experiment: {experiment} on thread {thread}')
    # add header for new experiment if you already have an initialized, nonempty experiment
    if isinstance(TRACKING[thread]['experiment'],int):
        async with FILELOCKS[TRACKING[thread]['path']]:
            with h5py.File(TRACKING[thread]['path'], 'r') as session:
                if len(list(session[f"/run_{TRACKING[thread]['run']}/experiment_{TRACKING[thread]['experiment']}:{thread}"].keys())) > 0:
                    TRACKING[thread]['experiment'] += 1

    # put thread in experiment for native commands
    experiment['meta']['thread'] = thread

    # handling unset-up threads and couple to the thread directly below if it exists
    # raise a flag and skip the experiment if it doesn't
    if experiment['soe'] != [] and all([TRACKING[thread][i] is None \
                                    for i in ['path','run','experiment','current_action']])  \
                                    and experiment['soe'][0].split('_')[0] != 'orchestrator/start':
        log.info(f"thread {thread} for experiment {experiment} has not been set up")
        if thread-1 in TRACKING.keys() and all([TRACKING[thread][i] is not None for i in \
            ['path','run','experiment','current_action']]):
            TRACKING[thread]['path'] = TRACKING[thread-1]['path']
            TRACKING[thread]['run'] = TRACKING[thread-1]['run']
            TRACKING[thread]['experiment'] = 0
            log.info(f"thread {thread} bound to thread {thread-1}")
        else:
            experiment = {'soe':[],'params':{},'meta':{}}
            log.info("experiment has been blanked")

    for action_str in experiment['soe']:
         # example: action is'movement' and the function is 'moveToHome_0
        server, fnc = action_str.split('/')
        while TRACKING[thread]['status'] != 'running' and server != 'orchestrator':
            await asyncio.sleep(.1)
        TRACKING[thread]['current_action'] = fnc
        action = fnc.split('_')[0]
        params = experiment['params'][fnc]
        servertype = server.split(':')[0]
        if server not in SERVERLOCKS.keys() and servertype != "orchestrator":
            SERVERLOCKS[server] = asyncio.Lock()

        # a placeholder for the appropriate conditional.
        if servertype != 'orchestrator':
            while True:
                async with SERVERLOCKS[server]:
                    res = await LOOP.run_in_executor(None,lambda x: requests.get(x, params=params, timeout=None),
                    f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/{action}")

                #ensure that action completed successfully
                if 200 <= res.status_code < 300:
                    res = res.json()
                    break
                else:
                    log.info(f"Orchestrator has received an invalid response attempting \
                        action {action_str} with parameters {params}.")
                    input('Fix the problem, and press Enter to try the action again.')
        elif servertype == '':
            pass
        elif servertype == 'orchestrator':
            if params is None:
                params = {}

            # crash or fail on native command due to an unsafe state.
            experiment = await process_native_command(action,experiment,**params)
            continue

        elif servertype == 'analysis':
            add = list(filter(lambda s: s.split('_')[-1] == 'address',params.keys()))
            if add != []:
                analysis_time = int(params[add[0]].split('/')[0].split(':')[1])
                if TRACKING[analysis_time]['path'] is not None:
                    async with FILELOCKS[TRACKING[analysis_time]['path']]:
                        await LOOP.run_in_executor(None,lambda x: \
                            requests.get(x,params=dict(path=TRACKING[analysis_time]['path'], \
                                run=TRACKING[analysis_time]['run'], \
                                    addresses=json.dumps({a:params[a] for a in add})), \
                                        timeout=None),\
                                f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/receiveData")
                else:
                    for history in TRACKING[thread]['history']:
                        async with FILELOCKS[history['path']]:
                            if orchestrator_utils.paths_in_hdf5(history['path'],[params[a] for a in add]):
                                await LOOP.run_in_executor(None,lambda x: \
                                    requests.get(x,params=dict(path=history['path'],\
                                        run=history['run'], \
                                        addresses=json.dumps({a:params[a] for a in add})), \
                                            timeout=None), \
                                        f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/receiveData")
                                break
            async with SERVERLOCKS[server]:
                res = await LOOP.run_in_executor(None,lambda x: requests.get(x,params=params, \
                    timeout=None).json(), \
                    f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/{action}")
        elif servertype == 'ml':
            if "address" in params.keys():
                analysis_time = int(params['address'].split('/')[0].split(':')[1])
                if TRACKING[analysis_time]['path'] is not None:
                    async with SERVERLOCKS[server]:
                        async with FILELOCKS[TRACKING[analysis_time]['path']]:
                            if 'modelid' in params.keys():
                                await LOOP.run_in_executor(None,lambda x: \
                                    requests.get(x,params=dict(path=TRACKING[analysis_time]['path'],\
                                        run=TRACKING[analysis_time]['run'],\
                                            address=params['address'], \
                                                modelid=params['modelid']), timeout=None), \
                                    f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/receiveData")
                            else:
                                await LOOP.run_in_executor(None,lambda x: requests.get(x, \
                                    params=dict(path=TRACKING[analysis_time]['path'], \
                                        run=TRACKING[analysis_time]['run'],address=params['address']), \
                                            timeout=None), \
                                    f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/receiveData")
                else:
                    for history in TRACKING[thread]['history']:
                        async with SERVERLOCKS[server]:
                            async with FILELOCKS[history['path']]:
                                if orchestrator_utils.paths_in_hdf5(history['path'],params['address']):
                                    if 'modelid' in params.keys():
                                        await LOOP.run_in_executor(None,lambda x: requests.get(x, \
                                            params=dict(path=history['path'], \
                                            run=history['run'],address=params['address'], \
                                                modelid=params['modelid']), timeout=None), \
                                            f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/receiveData")
                                    else:
                                        await LOOP.run_in_executor(None,lambda x: requests.get(x, \
                                            params=dict(path=history['path'],run=history['run'], \
                                            address=params['address']), timeout=None), \
                                            f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/receiveData")
                                    break
            async with SERVERLOCKS[server]:
                res = await LOOP.run_in_executor(None,lambda x: requests.get(x,params=params, \
                    timeout=None).json(), \
                    f"http://{config['servers'][server]['host']}:{config['servers'][server]['port']}/{servertype}/{action}")

        async with FILELOCKS[TRACKING[thread]['path']]:
            res.update({'meta':{'measurement_time':datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}})
            orchestrator_utils.save_dict_to_hdf5({fnc:res},TRACKING[thread]['path'], \
                path=f"/run_{TRACKING[thread]['run']}/experiment_{TRACKING[thread]['experiment']}:{thread}/",mode='a')
            #add metadata to experiment
            with h5py.File(TRACKING[thread]['path'], 'r') as session:
                session_list = list(session[f"/run_{TRACKING[thread]['run']}/experiment_{TRACKING[thread]['experiment']}:{thread}"].keys())
                if len(session_list) > 0 and 'meta' not in session_list:
                    session.close()
                    orchestrator_utils.save_dict_to_hdf5({'meta':experiment['meta']}, \
                                                        TRACKING[thread]['path'],\
                        path=f"/run_{TRACKING[thread]['run']}/experiment_{TRACKING[thread]['experiment']}:{thread}/",mode='a')
        log.info(f"function {fnc} in thread {thread} completed at {time.time()}")
        log.info(f"function operating in run {TRACKING[thread]['run']} \
            in file {TRACKING[thread]['path']}")

async def process_native_command(command: str,experiment: dict,**params):
    """ process a command that is native to the orchestrator """
    if command in ['start','finish','modify','wait','repeat']:
        return await getattr(sys.modules[__name__],command)(experiment,**params)
    raise Exception("native command not recognized")


async def start(experiment: dict,collectionkey:str,meta:dict={}):
    """ Ensure appropriate folder, file, and all keys and tracking variables are appropriately
        initialized at the beginning of a run

    Args:
        experiment (dict): experiment dictionary
        collectionkey (str): determines folder and file names for session, may correspond to key
            of experiment['meta'], in which case name will be indexed by that value.
        meta (dict, optional): will be placed as metadata under the header of the run set up by
            this command. Defaults to {}.
    """
    global TRACKING,FILELOCKS,SERVERLOCKS
    thread = experiment['meta']['thread']
    # give the directory an index if one is provided
    if collectionkey in experiment['meta'].keys():
        h5dir = os.path.join(config[SERVERKEY]['path'], \
            f"{collectionkey}_{experiment['meta'][collectionkey]}")
    # name the directory without an index if not.
    else:
        h5dir = os.path.join(config[SERVERKEY]['path'],f"{collectionkey}")
    # ensure that the directory in which this session should be saved exists
    h5dirlist = str(Path(h5dir)).split('\\')
    for folder in ['\\'.join(h5dirlist[:i+1]) for f,i in zip(h5dirlist,range(len(h5dirlist)))]:
        if not os.path.exists(folder):
            os.mkdir(folder)
     # create a session, if there is no current session to load
    if list(filter(lambda s: s[-3:]=='.h5',os.listdir(h5dir))) == []:
        TRACKING[thread]['path'] = \
            os.path.join(h5dir,config['instrument']+'_'+os.path.basename(h5dir)+'_session_0.h5')
        #add a lock to a file if it does not already exist
        if TRACKING[thread]['path'] not in FILELOCKS.keys():
            FILELOCKS[TRACKING[thread]['path']] = asyncio.Lock()
        async with FILELOCKS[TRACKING[thread]['path']]:
            orchestrator_utils.save_dict_to_hdf5(dict(meta=dict(date=datetime.date.today().strftime("%d/%m/%Y"))),TRACKING[thread]['path'])

    # otherwise grab most recent session in dir
    else:
        TRACKING[thread]['path'] = os.path.join(h5dir, \
        orchestrator_utils.highest_name(list(filter(lambda s: s[-3:]=='.h5',os.listdir(h5dir)))))
        if TRACKING[thread]['path'] not in FILELOCKS.keys():
            FILELOCKS[TRACKING[thread]['path']] = asyncio.Lock()
    async with FILELOCKS[TRACKING[thread]['path']]:
        with h5py.File(TRACKING[thread]['path'], 'r') as session:
            # assigns date to this session if necessary, or replaces session if too old
            if 'meta' not in session.keys():
                orchestrator_utils.save_dict_to_hdf5(dict(meta=dict(date=datetime.date.today().strftime("%d/%m/%Y"))),TRACKING[thread]['path'], path='/',mode='a')
            elif 'date' not in session['meta'].keys():
                session.close()
                orchestrator_utils.save_dict_to_hdf5(dict(date=datetime.date.today().strftime("%d/%m/%Y")),TRACKING[thread]['path'], path='/meta/',mode='a')
            elif session['meta/date/'][()] != datetime.date.today().strftime("%d/%m/%Y"):
                log.info('current session is old, saving current session and creating new session')
                session.close()
                if "orch_kadi" not in SERVERLOCKS.keys():
                    SERVERLOCKS["orch_kadi"] = asyncio.Lock()
                try:
                    async with SERVERLOCKS["orch_kadi"]:
                        print(requests.get(f"{config[SERVERKEY]['kadiurl']}/kadi/uploadhdf5",
                            params=dict(filename=os.path.basename(TRACKING[thread]['path']), \
                                filepath=os.path.dirname(TRACKING[thread]['path'])), \
                                    timeout=None).json())
                except:
                    log.info('not connected to kadi4mat and did not upload the session there')
                TRACKING[thread]['path'] = os.path.join(h5dir, \
                    orchestrator_utils.increment_name(os.path.basename(TRACKING[thread]['path'])))
                if TRACKING[thread]['path'] not in FILELOCKS.keys():
                    FILELOCKS[TRACKING[thread]['path']] = asyncio.Lock()
                async with FILELOCKS[TRACKING[thread]['path']]:
                    orchestrator_utils.save_dict_to_hdf5(dict(meta= \
                        dict(date=datetime.date.today().strftime("%d/%m/%Y"))),\
                            TRACKING[thread]['path'])

    async with FILELOCKS[TRACKING[thread]['path']]:
        #adds a new run to session to receive incoming data
        with h5py.File(TRACKING[thread]['path'], 'r') as session:
            if "run_0" not in session.keys():
                session.close()
                orchestrator_utils.save_dict_to_hdf5({"run_0":{f"experiment_0:{thread}":None}, \
                    "meta":meta},TRACKING[thread]['path'],mode='a')
                TRACKING[thread]['run'] = 0
            else:
                run = orchestrator_utils.increment_name(orchestrator_utils.highest_name(list(filter(lambda k: k[:4]=="run_",list(session.keys())))))
                session.close()
                orchestrator_utils.save_dict_to_hdf5({run:{f"experiment_0:{thread}":None,\
                    "meta":meta}},TRACKING[thread]['path'],mode='a')
                TRACKING[thread]['run'] = int(run[4:])
        TRACKING[thread]['experiment'] = 0
        orchestrator_utils.save_dict_to_hdf5({'meta':None},\
            TRACKING[thread]['path'],path=f'/run_{TRACKING[thread]["run"]}/experiment_0:{thread}/',\
                mode='a')
    TRACKING[thread]['status'] = 'running'
    return experiment


async def finish(experiment: dict):
    """ Ensure tracking variables are appropriately reset at the end of a run,
            and upload the finished session
    Args:
     experiment (dict): dictionary containing experiment metadata
    """
    global TRACKING,FILELOCKS,SERVERLOCKS
    thread = experiment['meta']['thread']
    log.info(f'thread {thread} finishing')
    # get the number of the threads
    working_threads = sum([1 if TRACKING[k]['path'] == TRACKING[thread]['path'] else 0 for k in TRACKING.keys()])
    if working_threads == 1:
        print('attempting to upload session')
        if "orch_kadi" not in SERVERLOCKS.keys():
            SERVERLOCKS["orch_kadi"] = asyncio.Lock()
        try:
            async with SERVERLOCKS["orch_kadi"]:
                log.info(requests.get(f"{config[SERVERKEY]['kadiurl']}/kadi/uploadhdf5",
                    params=dict(filename=os.path.basename(TRACKING[thread]['path']), \
                        filepath=os.path.dirname(TRACKING[thread]['path'])), timeout=None).json())
        except:
            log.info('no kadi4mart connection, did not upload the session there')

        # adds a new hdf5 file which will be used for the next incoming data
        newpath = os.path.join(os.path.dirname(TRACKING[thread]['path']), \
            orchestrator_utils.increment_name(os.path.basename(TRACKING[thread]['path'])))
        FILELOCKS[newpath] = asyncio.Lock()
        async with FILELOCKS[TRACKING[thread]['path']]:
            orchestrator_utils.save_dict_to_hdf5(dict(meta=None),newpath)

        # clear history relating to this file from all threads
        for tracking in TRACKING.values():
            for tracking_history in tracking['history']:
                if tracking_history['path'] == TRACKING['thread']['path']:
                    del tracking_history
    else:
        log.info(f'{working_threads-1} threads still operating on {TRACKING[thread]["path"]}')
        #free up the thread
        TRACKING[thread] = {'path':None,'run':None,'experiment':None, \
            'current_action':None,'status':'uninitialized', \
            'history':[{'path':TRACKING[thread]['path'], \
                'run':TRACKING[thread]['run']}]+TRACKING[thread]['history']}
    return experiment


async def modify(experiment: dict, addresses:Union[str,list], pointers:Union[str,list]):
    """ Set undefined values under experiment parameter dict.
        Values must come from currently running threads

    Args:
        experiment (dict): dictionary containing experiment metadata
        addresses (Union[str,list]): within a run, address(es) of the value(s)
                    that should be transmitted to parameter(s)
        pointers (Union[str,list]): within param dict of experiment,
                    addresses to transmit values to.
                    parameter must have previously been initialized as "?"

    Returns:
        dict: dictionary containing experiment
    """
    global TRACKING,FILELOCKS
    mainthread = experiment['meta']['thread']
    if not isinstance(addresses, list):
        addresses = [addresses]
    if not isinstance(pointers, list):
        pointers = [pointers]
    assert len(addresses) == len(pointers)
    threads = [int(address.split('/')[0].split(':')[1]) for address in addresses]
    for address, pointer, thread in zip(addresses, pointers, threads):
        if orchestrator_utils.dict_address(pointer, experiment['params']) != "?":
            raise Exception(f"pointer {pointer} is not intended to be written to")
        if TRACKING[thread]['path'] is not None:
            async with FILELOCKS[TRACKING[thread]['path']]:
                with h5py.File(TRACKING[thread]['path'], 'r') as session:
                    val = session[f'run_{TRACKING[thread]["run"]}/'+address][()]
                    orchestrator_utils.dict_address_set(pointer, experiment['params'],val)
                    log.info(f'pointer {pointer} in params for experiment \
                        {TRACKING[mainthread]["experiment"]} in thread {mainthread} set to {val}')
        else:
            for history_track in TRACKING[thread]['history']:
                if history_track['path'] == TRACKING[thread]['path']:
                    async with FILELOCKS[history_track['path']]:
                        with h5py.File(history_track['path'], 'r') as session:
                            try:
                                val = session[f'run_{history_track["run"]}/'+address][()]
                            except:
                                continue
                            orchestrator_utils.dict_address_set(pointer, experiment['params'],val)
                            print(f'pointer {pointer} in params for experiment \
                                {TRACKING[mainthread]["experiment"]} in thread {mainthread} \
                                    set to {val} from history')
                            break
            if orchestrator_utils.dict_address(pointer,experiment['params']) == '?':
                raise Exception('modify failed to find address in history')
    return experiment



async def wait(experiment: dict, addresses: Union[str,list]):
    """ Pause experiment until given thread(s) complete(s) given action(s)

    Args:
        experiment (dict): dictionary containing experiment metadata
        addresses (Union[str,list]): path(s) below run to awaited address(es),
                    i.e "experiment/action"

    Returns:
        experiment: dictionary containing experiment metadata
    """
    global TRACKING,FILELOCKS
    log.info(f"waiting on {addresses}")
    if not isinstance(addresses, list):
        addresses = [addresses]
    threads = [int(address.split('/')[0].split(':')[1]) for address in addresses]
    while addresses != []:
        await asyncio.sleep(.1)
        address_and_thread = list(zip(range(len(addresses)),copy(addresses), copy(threads)))
        for i,address,thread in address_and_thread:
            if TRACKING[thread]['path'] is not None:
                async with FILELOCKS[TRACKING[thread]['path']]:
                    with h5py.File(TRACKING[thread]['path'], 'r') as session:
                        exp = address.split('/')[0]
                        action = address.split('/')[1]
                        if exp in session[f'run_{TRACKING[thread]["run"]}/'].keys():
                            if action in session[f'run_{TRACKING[thread]["run"]}/{exp}'].keys():
                                log.info(f"{addresses[i]} found")
                                del addresses[i]
                                del threads[i]
                                break
            # waiting on the results of a session that already finished,
            # check history for path & run
            else:
                for exp_history in TRACKING[thread]['history']:
                    if exp_history['path'] == TRACKING[thread]['path']:
                        async with FILELOCKS[exp_history['path']]:
                            with h5py.File(exp_history['path'], 'r') as session:
                                exp = address.split('/')[0]
                                action = address.split('/')[1]
                                if exp in session[f'run_{exp_history["run"]}/'].keys():
                                    if action in session[f'run_{exp_history["run"]}/{exp}'].keys():
                                        print(f"{addresses[i]} found in history")
                                        del addresses[i]
                                        del threads[i]
    return experiment

# submit an experiment identical to the current one to the orchestrator thread.
# will have higher-than default priority, and will go before any intervening experiments
# that may have been submitted.
# an experiment should only have one call of repeat, and it should only be at the end of
# the experiment (unless followed by a finish command)
async def repeat(experiment: dict, number_of_repeat: int = 0, priority: int = 5):
    """ Submit an experiment identical to the current one to the orchestrator thread.

    Args:
        experiment (dict): dictionary containing experiment metadata
        n (int, optional): number of times to repeat after 1st experiment,
                            or 0 to repeat until forced to stop. Defaults to 0.
        priority (int, optional): priority of experiment. Defaults to 5.

    Returns:
        _type_: _description_
    """
    global INDEX
    #copy current experiment
    new_exp = experiment
    if number_of_repeat == 1: #if n=1, repeating is finished.
        del new_exp['params']['repeat']
        del new_exp['soe'][-1]
    elif number_of_repeat != 0: #else, decrement repeats left to go
        new_exp['params']['repeat'] -= 1
    #and of course, for n==0, we do nothing and it repeats forever
    #then the new experiment is added to the appropriate queue with a higher-than-default priority
    await EXPERIMENT_QUEUES[experiment['meta']['thread']].put((priority,INDEX,new_exp))
    INDEX += 1
    return experiment

@app.on_event("startup")
async def memory():
    """ Initialize memory for orchestrator
    """
    global TRACKING
    # a dict of useful variables to keep track of
    # every single experiment will have a tracking key here.
    TRACKING = {}
    global SCHEDULER_QUEUE
    SCHEDULER_QUEUE = asyncio.PriorityQueue()
    global TASK
    TASK = asyncio.create_task(scheduler())

    global EXPERIMENT_QUEUES
    EXPERIMENT_QUEUES = {}
    global EXPERIMENT_TASKS
    EXPERIMENT_TASKS = {}

    # two thread can access to the same file and same server at the same time
    global FILELOCKS
    FILELOCKS = {}
    global SERVERLOCKS
    SERVERLOCKS = {}

    global LOOP
    # for fixing the error handling
    LOOP = asyncio.get_event_loop()
    global ERROR
    ERROR = LOOP.create_task(raise_exceptions())

    global INDEX #assign a number to each experiment to retain order within priority queues
    INDEX = 0


@app.on_event("shutdown")
def disconnect():
    """ Disconnect from orchestrator
    """
    global TASK, ERROR
    if not ERROR.cancelled():
        ERROR.cancel()
    if not TASK.cancelled():
        TASK.cancel()
    for exp_task in EXPERIMENT_TASKS.values():
        if not exp_task.cancelled():
            exp_task.cancel()


@app.post("/orchestrator/clear")
def clear(thread: Optional[int] = None):
    """ Empty queue for thread, or for all threads if no thread specified.

    Args:
        thread (Optional[int], optional): thread to clear. Defaults to None.
    """
    global EXPERIMENT_QUEUES
    if thread is None:
        for k in EXPERIMENT_QUEUES.keys():
            while not EXPERIMENT_QUEUES[k].empty():
                EXPERIMENT_QUEUES[k].get_nowait()
    elif thread in EXPERIMENT_QUEUES.keys():
        while not EXPERIMENT_QUEUES[thread].empty():
            EXPERIMENT_QUEUES[thread].get_nowait()
    else:
        print(f"thread {thread} not found")

# TODO add it to thinker having different buttons for each
# can not stop the action that is currently running , just after the action is done
@app.post("/orchestrator/kill")
def kill(thread: Optional[int] = None):
    """ Empty queue and cancel current experiment for thread,
            or for all threads if no thread specified

    Args:
        thread (Optional[int], optional): thread to kill. Defaults to None.
    """
    global EXPERIMENT_TASKS,TRACKING
    global EXPERIMENT_TASKS,TRACKING
    clear(thread)
    if thread is None:
        for k in EXPERIMENT_TASKS.keys():
            EXPERIMENT_TASKS[k].cancel()
            del EXPERIMENT_TASKS[k]
            EXPERIMENT_TASKS.update({k:LOOP.create_task(infl(k))})
            exp_history = {'path':TRACKING[k]['path'],'run':TRACKING[k]['run']}
            TRACKING[k] = {'path':None,'run':None,'experiment':None,'current_action':None,'status':'uninitialized','history':[exp_history]+TRACKING[k]['history']}
    elif thread in EXPERIMENT_TASKS.keys():
        EXPERIMENT_TASKS[thread].cancel()
        del EXPERIMENT_TASKS[thread]
        EXPERIMENT_TASKS.update({thread:LOOP.create_task(infl(thread))})
        exp_history = {'path':TRACKING[thread]['path'],'run':TRACKING[thread]['run']}
        TRACKING[thread] = {'path':None,'run':None,'experiment':None,'current_action':None,'status':'uninitialized','history':[exp_history]+TRACKING[thread]['history']}
    else:
        print(f"thread {thread} not found")


@app.post("/orchestrator/pause")
def pause(thread: Optional[int] = None):
    """ Pause current experiment for thread, or for all threads if no thread specified

    Args:
        thread (Optional[int], optional): thread to pause. Defaults to None.
    """
    global TRACKING
    if thread is None:
        for k in TRACKING.keys():
            if TRACKING[k]['status'] == 'running':
                TRACKING[k]['status'] = 'paused'
                log.info(f"thread {k} paused")
            else:
                log.info(f'attempted to pause thread {k}, but status was {TRACKING[k]["status"]}')
    elif thread in TRACKING.keys():
        if TRACKING[thread]['status'] == 'running':
            TRACKING[thread]['status'] = 'paused'
            log.info(f"thread {thread} paused")
        else:
            log.info(f'attempted to pause thread {thread}, but status was {TRACKING[thread]["status"]}')
    else:
        log.info(f"thread {thread} not found")


@app.post("/orchestrator/resume")
def resume(thread: Optional[int] = None):
    """ Resume current experiment for thread, or for all threads if no thread specified

    Args:
        thread (Optional[int], optional): thread to resume. Defaults to None.
    """
    global TRACKING
    if thread is None:
        for k in TRACKING.keys():
            if TRACKING[k]['status'] == 'paused':
                TRACKING[k]['status'] = 'running'
                log.info(f"thread {k} resumed")
            else:
                log.info(f'attempted to resume thread {k}, but status was {TRACKING[k]["status"]}')
    elif thread in TRACKING.keys():
        if TRACKING[thread]['status'] == 'paused':
            TRACKING[thread]['status'] = 'running'
            log.info(f"thread {thread} resumed")
        else:
            log.info(f'attempted to resume thread {thread}, but status was {TRACKING[thread]["status"]}')
    else:
        log.info(f"thread {thread} not found")


@app.post("/orchestrator/getStatus")
def get_status():
    """ Get status of all threads

    Returns:
        dict: status of all threads
    """
    return TRACKING


async def raise_exceptions():
    """ Check for exceptions. If found, print stack trace and cancel the infinite loop
        Error handing within the infinite loop
    """
    global TASK,EXPERIMENT_TASKS,ERROR
    while True:
        # check for errors every second (maybe this should be a different number?)
        await asyncio.sleep(1)
        try:
            TASK.exception()
            TASK.print_stack()
            break
        except:
            pass
        task_check = None
        for task in EXPERIMENT_TASKS.values():
            try:
                task.exception()
                task.print_stack()
                task_check = task
                break
            except:
                pass
        try:
            task_check.exception()
            break
        except:
            pass
    #if an error shows up anywhere, bring the whole house down.
    # cancel all tasks
    for task_value in EXPERIMENT_TASKS.values():
        try:
            task_value.cancel()
        except:
            pass
    try:
        TASK.cancel()
    except:
        pass
    try:
        ERROR.cancel()
    except:
        pass


@app.get("/orchestrator/getData")
async def get_data(thread:int, addresses:str ,mode:str, wait_time:float=.01):
    """ Get data from the specified addresses

    Args:
        thread (int): thread to get data from
        addresses (str): addresses to get data from
        mode (str): mode to get data in
        wait (float, optional): time to wait between requests. Defaults to .01.

    Raises:
        ValueError: _description_

    Returns:
        dict: data from the specified addresses
    """

    await asyncio.sleep(wait_time)
    data = []
    try:
        addresses = json.loads(addresses)
    except:
        addresses = [addresses]
    if mode not in ['list','group','next']:
        raise ValueError('invalid mode for getData')
    path = TRACKING[thread]['path'] if \
        TRACKING[thread]['path'] is not None else TRACKING[thread]['history'][0]['path']
    run = TRACKING[thread]['run'] if \
        TRACKING[thread]['path'] is not None else TRACKING[thread]['history'][0]['run']
    if mode == 'list':
        async with FILELOCKS[path]:
            with h5py.File(path, 'r') as session:
                experiments = list(session[f'run_{run}'].keys())
                for experiment in experiments:
                    subdata = []
                    for address in addresses:
                        dpath = f'run_{run}/'+experiment+'/'+address
                        if orchestrator_utils.paths_in_hdf5(session,dpath):
                            datum = orchestrator_utils.hdf5_group_to_dict(session,dpath)
                            if isinstance(datum,numpy.ndarray):
                                datum = datum.tolist()
                            subdata.append(datum)
                        else:
                            log.info(f'address {address} not found in file')
                    if subdata != []:
                        data.append(subdata if len(subdata) != 1 else subdata[0])
    elif mode == 'group':
        async with FILELOCKS[path]:
            with h5py.File(path, 'r') as session:
                for address in addresses:
                    data.append(orchestrator_utils.hdf5_group_to_dict(session,f'run_{run}/{address}'))
    elif mode == 'next':
        new_exp = f'experiment_{TRACKING[thread]["experiment"]}:{thread}'
        log.info(f'awaiting data at {new_exp}')
        present = False
        while not present:
            async with FILELOCKS[path]:
                with h5py.File(path, 'r') as session:
                    present = orchestrator_utils.paths_in_hdf5(path,[f'run_{run}/{new_exp}/{address}' for address in addresses])
                await asyncio.sleep(.1)
        for address in addresses:
            async with FILELOCKS[path]:
                with h5py.File(path, 'r') as session:
                    datum = orchestrator_utils.hdf5_group_to_dict(session,f'run_{run}/{new_exp}/{address}')
            if isinstance(datum,numpy.ndarray):
                datum = datum.tolist()
            data.append(datum)
    return data

def main():
    """Main entry point of the application."""
    uvicorn.run(app, host= config['servers'][SERVERKEY]['host'], port= config['servers'][SERVERKEY]['port'])

if __name__ == "__main__":
    main()
