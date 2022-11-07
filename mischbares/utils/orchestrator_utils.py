""" A collection of functions for working with hdf5 files and generally with orchestrator data."""
import numpy as np
import h5py


def increment_name(name:str):
    """ Increment the number at the end of a string.

    Args:
        name (str): name of file

    Returns:
        str: Incremented name of file
    """
    segments = name.split('_')
    if '.' in segments[-1]:
        #so that we can increment filenames too
        subsegment = segments[-1].split('.')
        subsegment[0] = str(int(subsegment[0])+1)
        segments[-1] = '.'.join(subsegment)
    else:
        segments[-1] = str(int(segments[-1])+1)
    return '_'.join(segments)

def highest_name(names:list):
    """ Tke in a list of strings which differ only by an integer,
    and return the one for which that integer is highest

    Args:
        names (list): list of strings

    Returns:
        str: highest name
    """
    if len(names) == 1:
        return names[0]
    slen = min([len(i) for i in names])
    leftindex = None
    rightindex = None
    for i in range(slen):
        for name in names:
            if name[i] != names[0][i]:
                leftindex = i
                break
        if leftindex is not None:
            break
    for i in range(-1,-slen-1,-1):
        for name in names:
            if name[i] != names[0][i]:
                rightindex = i
                break
        if rightindex is not None:
            break
    numbers = [int(s[leftindex:rightindex+1] if rightindex != -1 else s[leftindex:]) for s in names]
    return names[numbers.index(max(numbers))]


def dict_address(address,dict_keys):
    """ For a string of dict keys seperated by '/', get the value of d under that series

    Args:
        address (str): address of value
        dict_keys: dictionary to search

    Returns:
        dict: value at address
    """
    address = address.split('/')
    if len(address) == 1:
        return dict_keys[address[0]]
    return dict_address('/'.join(address[1:]),dict_keys[address[0]])


def dict_address_set(address,dict_keys,val):
    """ For a string of dict keys seperated by '/', set the value of dictionary d at that address to val

    Args:
        address (str): address of value
        dict_keys (dict): dictionary to search
        val (int): value to set
    """
    address = address.split('/')
    if len(address) == 1:
        dict_keys[address[0]] = val
    else:
        dict_address_set('/'.join(address[1:]),dict_keys[address[0]],val)


def save_dict_to_hdf5(dict_keys, filename, path='/', mode='w'):
    """ Save a dictionary to an hdf5 file.

    Args:
        dict (dict): dictionary to save
        filename (str): name of file
        path (str, optional): path where the hdf5 is saved. Defaults to '/'.
        mode (str, optional): mode to open the file. Defaults to 'w'.
    """
    with h5py.File(filename, mode) as h5file:
        recursively_save_dict_contents_to_group(h5file, path, dict_keys)


def recursively_save_dict_contents_to_group( h5file, path, dict_keys):
    """ Save a dictionary to an hdf5 file.

    Args:
        h5file (h5py._hl.files.File): hdf5 file to save to
        path (str): path to save to
        dict_keys (dict): dictionary to save
    """
    # pylint: disable=protected-access
    # argument type checking
    if not isinstance(dict_keys, dict):
        raise ValueError("must provide a dictionary")
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    if not isinstance(h5file, h5py._hl.files.File):
        raise ValueError("must be an open h5py file")
    # save items to the hdf5 file
    for key, item in dict_keys.items():
        key = str(key)
        if isinstance(item, list):
            item = np.array(item)
        if not isinstance(key, str):
            raise ValueError("dict keys must be strings to save to hdf5")
        # save strings, numpy.int64, and numpy.float64 types
        if isinstance(item, (np.int64, np.float64, str, np.float, float, np.float32,int)):
            h5file[path + key] = item
        # save numpy arrays
        elif isinstance(item, np.ndarray):
            try:
                h5file[path + key] = item
            except:
                item = np.array(item).astype('|S9')
                h5file[path + key] = item
            if not np.array_equal(h5file[path + key][()], item):
                raise ValueError('The data representation in the HDF5 file does not match the original dict.')
        elif isinstance(item, list):
            h5file[path + key] = np.array(item)
            if not h5file[path + key] == np.array(item):
                raise ValueError('The data representation in the HDF5 file does not match the original dict.')
        # save dictionaries
        elif isinstance(item, dict):
            recursively_save_dict_contents_to_group(h5file, path + key + '/', item)
        elif item is None:
            h5file.create_group(path + key)
        # other types cannot be saved and will result in an error
        else:
            raise ValueError('Cannot save %s type.' % type(item))


def hdf5_group_to_dict(h5file, path):
    """ Take a group from somewhere within an hdf5 file, convert it to a dict, and return it.

    Args:
        h5file (str): hdf5 file to read from
        path (str): path to group

    Raises:
        ValueError: if the group is not a dictionary

    Returns:
        dict: dictionary of group
    """
    # pylint: disable=protected-access
    data = {}
    for key in h5file[path].keys():
        if isinstance(h5file[path+key+'/'],h5py._hl.group.Group):
            data.update({key:hdf5_group_to_dict(h5file,path+key+'/')})
        elif isinstance(h5file[path+key+'/'],h5py._hl.dataset.Dataset):
            data.update({key:h5file[path+key+'/'][()]})
        else:
            raise ValueError(f'somehow {h5file[key]} is neither an hdf5 group nor dataset')
    return data


def paths_in_hdf5(h5path, paths):
    """ Check if the input path or list of paths are valid for the input hdf5 file.

    Args:
        h5path (str): path to hdf5 file
        paths (str or list): path or list of paths to check

    Returns:
        bool : True if path is in hdf5, False if not.
    """
    if isinstance(paths,str):
        paths = [paths]
    with h5py.File(h5path, 'r') as h5file:
        for path in paths:
            try:
                h5file[path]
            except:
                return False
    return True
