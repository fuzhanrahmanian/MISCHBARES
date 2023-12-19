import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from mischbares.db.user import Users  # Import your Users class
import webbrowser
import inspect
import subprocess
from mischbares.procedures.autolab_procedures import AutolabProcedures
from flask import jsonify

app = Flask(__name__, template_folder='templates')  # Initialize the Flask app
app.secret_key = 'mischbares2023'  # Set a secret key for session management
app.config['TESTING'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.json.sort_keys = False

# Initialize your Users class
users_db = Users()
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = "test_username"#request.form['username']
        password = "test_password"#request.form['password']
        if users_db.login_user(username, password):
            # User authenticated
            flash('Login successful!', 'success')
            return redirect(url_for('main'))  # Redirect to the main page or dashboard
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
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
    return jsonify({'success': True})

@app.route('/save-general-settings', methods=['POST'])
def save_general_settings():
    general_settings = request.json
    with open('saved_config/general_config.json', 'w') as f:
        json.dump(general_settings, f)
    return jsonify({'success': True})

@app.route('/load-general-settings', methods=['GET'])
def load_general_settings():
    general_settings, experiment_settings = load_all_settings()
    return render_template('main.html', general_settings=general_settings, experiment_settings=experiment_settings)

@app.route('/load-experiment-settings', methods=['GET'])
def load_experiment_settings():
    general_settings, experiment_settings = load_all_settings()
    return render_template('main.html', general_settings =general_settings, experiment_settings=experiment_settings)


def load_all_settings():
    try:
        with open('saved_config/general_config.json', 'r') as f:
            general_settings = json.load(f)
            #general_settings['motor_pos'] = format_motor_positions(general_settings['motor_pos'])
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


@app.route('/get-batch-settings', methods=['GET'])  # Adjusted route name
def get_batch_settings():
    try:
        with open('saved_config/batch_config.json', 'r') as f:
            batch_settings = json.load(f)
        return jsonify(batch_settings)
    except FileNotFoundError:
        return jsonify({"error": "Batch config file not found."}), 404

@app.route('/save-batch-settings', methods=['POST'])
def save_batch_settings():
    batch_settings = request.json
    with open('saved_config/batch_config.json', 'w') as f:
        json.dump(batch_settings, f)
    return jsonify({'success': True})


@app.route('/run-mischbares', methods=['POST'])
def run_mischbares():
    try:
        # Replace the command with the correct way to execute your main.py
        result = subprocess.run(['python', 'path/to/main.py'], check=True, stdout=subprocess.PIPE)
        return jsonify({"message": "Mischbares run successfully", "output": result.stdout.decode()})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Error running Mischbares", "details": str(e)}), 500

def format_motor_positions(motor_pos_list):
    # Converts list of tuples back to the original input string format
    return '; '.join(','.join(map(str, pos)) for pos in motor_pos_list)


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
    app.run(debug=True)