import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from mischbares.db.user import Users  # Import your Users class
import webbrowser
import inspect
import subprocess
from mischbares.procedures.autolab_procedures import AutolabProcedures
from flask import jsonify

import logging
logging.basicConfig(level=logging.INFO)


app = Flask(__name__, template_folder='templates')  # Initialize the Flask app
app.secret_key = 'mischbares2023'  # Set a secret key for session management
app.config['TESTING'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.json.sort_keys = False

SIGNED_IN_USER_ID = None

# Initialize your Users class
#users_db = Users()
@app.route('/login', methods=['GET', 'POST'])
def login():
    global SIGNED_IN_USER_ID
    if request.method == 'POST':
        # username = request.form['username']
        # password = request.form['password']
        # if username == '' or password == '':
        #     flash('Please enter a username and password!', 'danger')
        #     return redirect(url_for('login'))
        #if users_db.login_user(username, password):
        #     # User authenticated
        #     SIGNED_IN_USER_ID = users_db.user_id
        #     #flash('Login successful!', 'success')
        SIGNED_IN_USER_ID = 1	
        return redirect(url_for('main'))  # Redirect to the main page or dashboard

        #else:
        #    flash('Invalid username or password! \n Contact your administrator', 'danger')
    return render_template('login.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'icon.ico')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if SIGNED_IN_USER_ID is None:
        return redirect(url_for('login'))
    general_settings = {}
    experiment_settings = {}
    if request.method == 'GET':
        general_settings, experiment_settings = load_all_settings()

    return render_template('main.html', general_settings=general_settings, experiment_settings=experiment_settings)


@app.route('/save-experiment-settings', methods=['POST'])
def save_experiment_settings():
    experiment_settings = request.json
    with open('saved_config/experiment_config.json', 'w') as f:
        json.dump(experiment_settings, f)
    return jsonify({'success': True, 'message': 'Experiment settings saved successfully!', 'category': 'success'})


@app.route('/load-experiment-settings', methods=['GET'])
def load_experiment_settings():
    general_settings, experiment_settings = load_all_settings()
    flash('Experiment settings loaded successfully!', 'success')
    return render_template('main.html', general_settings =general_settings, experiment_settings=experiment_settings)


@app.route('/save-general-settings', methods=['POST'])
def save_general_settings():
    general_settings = request.json
    with open('saved_config/general_config.json', 'w') as f:
        json.dump(general_settings, f)
    return jsonify({'success': True, 'message': 'General settings saved successfully!', 'category': 'success'})

@app.route('/load-general-settings', methods=['GET'])
def load_general_settings():
    general_settings, experiment_settings = load_all_settings()
    flash('General settings loaded successfully!', 'success')
    return render_template('main.html', general_settings=general_settings, experiment_settings=experiment_settings)




def load_all_settings():
    """
    Load general and experiment settings from JSON files.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the loaded general settings and experiment settings.
    """
    try:
        with open('saved_config/general_config.json', 'r') as f:
            general_settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        general_settings = {}
        flash('No saved general settings found or invalid file format.', 'warning')

    try:
        with open('saved_config/experiment_config.json', 'r') as f:
            experiment_settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        experiment_settings = {}
        flash('No saved experiment settings found or invalid file format.', 'warning')

    return general_settings, experiment_settings


@app.route('/load-batch-settings', methods=['GET'])
def load_batch_settings():
    with open('saved_config/batch_config.json', 'r') as file:
        batch_config = json.load(file)

    prepared_batch_data = prepare_batch_data(batch_config)
    num_batches = len(batch_config)
    num_experiments_per_batch = {batch: len(experiments) for batch, experiments in batch_config.items()}
    
    return jsonify({'num_batches': num_batches, 
                    'num_experiments_per_batch': num_experiments_per_batch, 
                    'batch_data': prepared_batch_data})

def prepare_batch_data(batch_config):
    prepared_data = {}
    for batch, experiments in batch_config.items():
        experiment_data = {}
        for exp_id, settings in experiments.items():
            experiment_data[exp_id] = settings
        prepared_data[batch] = experiment_data
    return prepared_data


@app.route('/save-batch-settings', methods=['POST'])
def save_batch_settings():
    batch_settings = request.json
    with open('saved_config/batch_config.json', 'w') as f:
        json.dump(batch_settings, f)
    return jsonify({'success': True, 'message': 'Batch settings saved successfully!', 'category': 'success'})




@app.route('/render-status', methods=['GET'])
def render_status():
    return render_template('status.html')

@app.route('/run-mischbares', methods=['GET'])
def run_mischbares():
    print("Starting Mischbares...")
    try:
        subprocess.Popen(['python', 'main.py', str(SIGNED_IN_USER_ID)])
        return jsonify({'success': True, 'message': "Starting Mischbares..."})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Error running Mischbares: {str(e)}"}), 500

def parse_motor_positions(motor_pos_str):
    # Converts string input to list of tuples
    return [tuple(map(float, pos.split(','))) for pos in motor_pos_str.split(';') if pos.strip()]


@app.route('/get-function-names')
def get_function_names_route():
    function_names = get_function_names()

    return jsonify(function_names)

@app.route('/get-function-args')
def get_function_args_route():
    function_args = get_functions_args()
    return jsonify(function_args)

def get_functions_args():
    """Get the arguments of all the functions in the AutolabProcedures class

    Returns:
        dict: dictionary with the function names as keys and the arguments as values
    """
    excluded_args = ['self']
    function_args = {}
    for func in get_function_names():
        # Get the arguments of the function excluding the self
        args = inspect.getfullargspec(getattr(AutolabProcedures, func)).args[1:]
        if args and args[0] not in excluded_args:
            function_args[func] = args
    return function_args


def get_function_names():
    function_names = [func for func in dir(AutolabProcedures) if callable(getattr(AutolabProcedures, func)) and not func.startswith("_")][::-1]
    return function_names

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return 'Main Page or Dashboard'  # Replace with actual main page
    return redirect(url_for('login'))

def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Create a folder for saving the config files
    #subprocess.Popen(['mkdir', '-p', 'saved_config'])
    try:
        os.mkdir('saved_config', exist_ok=True)
    except:
        pass
    #open_browser()
    app.run(debug=True)
