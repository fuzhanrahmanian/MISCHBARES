var functionArgs = {};

window.onload = function () {
    // Fetch function arguments
    fetch('/get-function-args')
        .then(response => response.json())
        .then(args => {
            functionArgs = args;
            createBatchSections(); // Move createBatchSections call here, after functionArgs are set
        })
        .catch(error => console.error('Error fetching function arguments:', error));

    // Hide flash messages after 3 seconds
    var flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(flashMessage) {
        setTimeout(function () {
            flashMessage.style.display = 'none';
        }, 3000);
    });
};


// Function to handle showing flash messages
function showFlashMessage(message, category) {
    var flashMessageDiv = document.createElement('div');
    flashMessageDiv.id = 'flashMessage';
    flashMessageDiv.className = 'flash-message ' + category;
    flashMessageDiv.textContent = message;

    document.body.appendChild(flashMessageDiv);

    setTimeout(function () {
        flashMessageDiv.remove();
    }, 3000); // Adjust the time as needed
}


function updateExperimentSettingsVisibility() {
    var material = document.getElementById('material').value;
    var number_of_electrons = document.getElementById('number_of_electrons').value;
    var electrode_area = document.getElementById('electrode_area').value;
    var concentration_of_active_material = document.getElementById('concentration_of_active_material').value;
    var mass_of_active_material = document.getElementById('mass_of_active_material').value;

    var experimentSettings = document.getElementById('experiment_settings');
    if (material && number_of_electrons && electrode_area && concentration_of_active_material && mass_of_active_material) {
        experimentSettings.style.display = 'block';
    } else {
        experimentSettings.style.display = 'none';
    }
}

function createBatchSections() {
    return new Promise((resolve, reject) => {
        var numBatches = parseInt(document.getElementById('num_of_batch').value) || 0;
        var numExperiments = parseInt(document.getElementById('num_of_experiment_in_each_batch').value) || 0;
        var batchContainer = document.getElementById('batch-container');

        // Preserve current state before clearing content
        var currentState = preserveCurrentState(batchContainer);

        batchContainer.innerHTML = ''; // Clear previous content

        fetch('/get-function-names')
            .then(response => response.json())
            .then(functionNames => {
                for (var i = 0; i < numBatches; i++) {
                    var batchSection = document.createElement('div');
                    batchSection.className = 'batch-section';

                    var batchTitle = document.createElement('h3');
                    batchTitle.className = 'batch-title';
                    batchTitle.textContent = 'Batch ' + (i + 1);
                    batchSection.appendChild(batchTitle);

                    for (var j = 0; j < numExperiments; j++) {
                        var experimentContainer = document.createElement('div');
                        experimentContainer.className = 'experiment-container';

                        var label = document.createElement('label');
                        label.textContent = 'Experiment ' + (j + 1) + ':';
                        label.setAttribute('for', 'batch_' + (i + 1) + '_experiment_' + (j + 1));

                        var select = document.createElement('select');
                        select.id = 'batch_' + (i + 1) + '_experiment_' + (j + 1);
                        select.name = 'batch_' + (i + 1) + '_experiment_' + (j + 1);
                        select.className = 'experiment-dropdown';

                        experimentContainer.appendChild(label);
                        experimentContainer.appendChild(select);

                        functionNames.forEach(name => {
                            var option = document.createElement('option');
                            option.value = name;
                            option.textContent = name;
                            select.appendChild(option);
                        });

                        // Attach event listener to handle function selection
                        select.addEventListener('change', function() {
                            var selectedFunction = this.value;
                            var argsContainer = this.parentNode;
                            updateArgumentFields(argsContainer, functionArgs[selectedFunction]);
                        });

                        // Dispatch change event right after populating the dropdown
                        select.dispatchEvent(new Event('change'));

                        batchSection.appendChild(experimentContainer);
                    }

                    batchContainer.appendChild(batchSection);
                }

                // Trigger change event for each dropdown to create argument inputs
                document.querySelectorAll('.experiment-dropdown').forEach(dropdown => {
                    if (currentState[dropdown.id]) {
                        // Only update if there's a saved function for this dropdown
                        if (currentState[dropdown.id].selectedFunction) {
                            dropdown.value = currentState[dropdown.id].selectedFunction;
                            dropdown.dispatchEvent(new Event('change'));
                        }

                        // Restore argument input values if they exist
                        if (currentState[dropdown.id].arguments) {
                            let argsContainer = dropdown.closest('.experiment-container').querySelector('.args-container');
                            Object.entries(currentState[dropdown.id].arguments).forEach(([argName, argValue]) => {
                                let input = argsContainer.querySelector(`[data-arg-name="${argName}"]`);
                                if (input) {
                                    input.value = argValue;
                                }
                            });
                        }
                    }
                });

                // After all dropdown change events are triggered, restore argument input values
                restoreState(currentState, batchContainer);

                resolve();
            }).catch(error => {
                console.error('Error in createBatchSections:', error);
                reject(error);
            });
    });
}

function preserveCurrentState(container) {
    var state = {};
    container.querySelectorAll('.experiment-dropdown').forEach(dropdown => {
        var args = Array.from(dropdown.closest('.experiment-container').querySelectorAll('.arg-field'))
            .map(input => input.value);
        state[dropdown.id] = {
            selectedFunction: dropdown.value,
            arguments: args
        };
    });
    return state;
}

function restoreState(state, container) {
    for (const [dropdownId, dropdownState] of Object.entries(state)) {
        let dropdown = container.querySelector('#' + dropdownId);
        if (dropdown) {
            dropdown.value = dropdownState.selectedFunction;
            // Trigger change event to recreate argument fields
            dropdown.dispatchEvent(new Event('change'));

            // Restore argument field values
            let argFields = dropdown.closest('.experiment-container').querySelectorAll('.arg-field');
            dropdownState.arguments.forEach((value, index) => {
                if (argFields[index]) {
                    argFields[index].value = value;
                }
            });
        }
    }
}


function saveGeneralSettings() {
    // Collect data from general settings fields
    var generalSettingsData = {
        material: document.getElementById('material').value,
        number_of_electrons: document.getElementById('number_of_electrons').value,
        electrode_area: document.getElementById('electrode_area').value,
        concentration_of_active_material: document.getElementById('concentration_of_active_material').value,
        mass_of_active_material: document.getElementById('mass_of_active_material').value,
        row: document.getElementById('row').value,
        column: document.getElementById('column').value,
        height: document.getElementById('height').value,
        stepsize: document.getElementById('stepsize').value,
        motor_pos: document.getElementById('motor_pos').value,
        save_dir: document.getElementById('save_dir').value,
    };

    // Send data to the server
    fetch('/save-general-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(generalSettingsData)
    })
        .then(response => response.json())
        .then(data => {
            console.log('General settings saved:', data)
            showFlashMessage(data.message, data.category);
        }
        )
        .catch(error => {
            showFlashMessage('An error occurred. Please try again.', 'error');
            console.error('Error saving general settings:', error)
        });
}

function saveExperimentSettings() {
    var experimentSettingsData = {
        num_of_batch: document.getElementById('num_of_batch').value,
        num_of_experiment_in_each_batch: document.getElementById('num_of_experiment_in_each_batch').value,
    };

    // Send data to the server
    fetch('/save-experiment-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(experimentSettingsData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show the flash message
                showFlashMessage(data.message, data.category);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showFlashMessage('An error occurred. Please try again.', 'error');
        });
}

document.getElementById('saveGeneralSettings').addEventListener('click', saveGeneralSettings);


function saveBatchSettings() {
    var batchData = {};

    // Iterate over each batch section
    document.querySelectorAll('.batch-section').forEach((batchSection, batchIndex) => {
        var batchId = 'batch_' + (batchIndex + 1);
        batchData[batchId] = {};

        // Iterate over each experiment dropdown in the current batch
        batchSection.querySelectorAll('.experiment-dropdown').forEach((dropdown, expIndex) => {
            var expId = 'experiment_' + (expIndex + 1);
            var selectedFunction = dropdown.value;
            var argsData = {};
            // Find the container of argument inputs for this experiment
            var argsContainer = dropdown.closest('.experiment-container').querySelector('.args-container');
            if (argsContainer) {
                argsContainer.querySelectorAll('.arg-field').forEach(input => {
                    var argName = input.getAttribute('data-arg-name'); // Retrieve the original argument name
                    // Only save the arguments if they have a value
                    if (input.value) {
                        argsData[argName] = input.value; // Capture the value
                    }
                });
            }
            if (Object.keys(argsData).length > 0) {
                batchData[batchId][expId] = { [selectedFunction]: argsData };
            } else {
                // Optionally handle the case where there are no arguments for a function
                batchData[batchId][expId] = { [selectedFunction]: {} };
            }
        });
    });

    // Send this data to the server to be saved
    fetch('/save-batch-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(batchData)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Batch settings saved:', data);
            showFlashMessage(data.message, data.category);
            document.getElementById('runMischbares').style.display = 'block';
        })
        .catch(error => console.error('Error saving batch settings:', error));
}


function updateArgumentFields(dropdown, args) {
    var experimentContainer = dropdown.closest('.experiment-container');

    // Extract experimentIndex from the dropdown's ID
    var dropdownIdParts = dropdown.id.split('_');
    var experimentIndex = dropdownIdParts[dropdownIdParts.length - 2] + '_' + dropdownIdParts[dropdownIdParts.length - 1];

    // Remove existing argument fields container if it exists
    var existingArgsContainer = experimentContainer.querySelector('.args-container');
    if (existingArgsContainer) {
        existingArgsContainer.remove();
    }

    // Create a new container for argument fields
    var argsContainer = document.createElement('div');
    argsContainer.className = 'args-container';

    // Add new fields for each argument
    args.forEach((arg, index) => {
        var input = document.createElement('input');
        input.type = 'text';
        input.setAttribute('data-arg-name', arg);
        input.id = 'arg_' + experimentIndex + '_' + index; // Construct a valid ID
        input.className = 'arg-field';
        input.placeholder = arg;
        argsContainer.appendChild(input); // Append to the args container
    });

    // Append the args container after the dropdown
    experimentContainer.appendChild(argsContainer);
}

// JavaScript to enable button when all fields are filled
document.addEventListener('input', function() {
    var row = document.getElementById('row').value;
    var column = document.getElementById('column').value;
    var height = document.getElementById('height').value;
    var stepsize = document.getElementById('stepsize').value;
    var motorPos = document.getElementById('motor_pos').value;
    var button = document.getElementById('generate_meshgrid');
    // Check if all meshgrid fields are filled
    var allMeshgridFieldsFilled = row && column && height && stepsize;
    // Enable the button if all meshgrid fields are filled and position is not filled
    if (allMeshgridFieldsFilled && !motorPos) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }
    var material = document.getElementById('material').value;
    var number_of_electrons = document.getElementById('number_of_electrons').value;
    var electrode_area = document.getElementById('electrode_area').value;
    var concentration_of_active_material = document.getElementById('concentration_of_active_material').value;
    var mass_of_active_material = document.getElementById('mass_of_active_material').value;
    var experimentSettings = document.getElementById('experiment_settings');
    if (material && number_of_electrons && electrode_area && concentration_of_active_material && mass_of_active_material) {
        experimentSettings.style.display = 'block';
    } else {
        experimentSettings.style.display = 'none';
    }
});

document.getElementById('generate_meshgrid').onclick = function () {
    var row = parseInt(document.getElementById('row').value);
    var column = parseInt(document.getElementById('column').value);
    var height = parseFloat(document.getElementById('height').value);
    var stepsize = parseFloat(document.getElementById('stepsize').value);
    var motorPos = '';
    for (var i = 0; i < row; i++) {
        for (var j = 0; j < column; j++) {
            motorPos += (i * stepsize) + ',' + (j * stepsize) + ',' + height + '; ';
        }
    }
    document.getElementById('motor_pos').value = motorPos.trim();
};

document.getElementById('runMischbares').addEventListener('click', function (event) {
    event.preventDefault();
    fetch('/run-mischbares', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/render-status'; // Redirect to the status page
            } else {
                showFlashMessage(data.message, 'error');
            }
        })
        .catch(error => {
            showFlashMessage('Error starting Mischbares: ' + error, 'error');
        });
});


document.getElementById('loadBatchSettings').addEventListener('click', function (event) {
    event.preventDefault();
    fetch('/load-batch-settings', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('num_of_batch').value = data.num_batches;
            document.getElementById('num_of_experiment_in_each_batch').value = Object.values(data.num_experiments_per_batch)[0];

            createBatchSections().then(() => {
                fillExperimentInputs(data.batch_data);
            });
            document.getElementById('runMischbares').style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading batch settings:', error);
        });
});

function fillExperimentInputs(batchData) {
    for (const [batchId, experiments] of Object.entries(batchData)) {
        for (const [expId, settings] of Object.entries(experiments)) {
            const selectId = batchId + '_' + expId;
            const selectElement = document.getElementById(selectId);

            if (selectElement) {
                // Assuming each experiment has a single setting representing the selected function name
                const selectedFunction = Object.keys(settings)[0];
                selectElement.value = selectedFunction;
                selectElement.dispatchEvent(new Event('change'));

                // Assuming settings[selectedFunction] contains arguments to be filled
                const args = settings[selectedFunction];
                const argsContainer = selectElement.closest('.experiment-container').querySelector('.args-container');
                if (argsContainer) {
                    Object.entries(args).forEach(([argName, argValue]) => {
                        const input = argsContainer.querySelector(`[data-arg-name="${argName}"]`);
                        if (input) {
                            input.value = argValue;
                        }
                    });
                }
            }
        }
    }
}


// document.getElementById('loadBatchSettings').addEventListener('click', loadBatchSettings);
document.addEventListener('DOMContentLoaded', updateExperimentSettingsVisibility);
document.addEventListener('input', updateExperimentSettingsVisibility);
isProgrammaticChange = true;
document.getElementById('num_of_batch').addEventListener('change', createBatchSections);
document.getElementById('num_of_experiment_in_each_batch').addEventListener('change', createBatchSections);
isProgrammaticChange = false;
document.getElementById('saveBatchSettings').addEventListener('click', function (event) {
    event.preventDefault();
    saveBatchSettings();
});
document.getElementById('saveExperimentSettings').addEventListener('click', function (event) {
    event.preventDefault();
    saveExperimentSettings();
});
document.getElementById('saveGeneralSettings').addEventListener('click', function (event) {
    event.preventDefault();
    saveGeneralSettings();
});
