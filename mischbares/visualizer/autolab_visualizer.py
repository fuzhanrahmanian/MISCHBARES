##### NEEDED FOR DEBUGGING #####
# import ptvsd
# ptvsd.enable_attach(address=('localhost', 5678))
# print("Waiting for debugger attach")
# ptvsd.wait_for_attach()
import websockets
import json
import collections
from functools import partial
import socket

from bokeh.models import ColumnDataSource, CheckboxButtonGroup, RadioButtonGroup, Div
from bokeh.plotting import figure, curdoc
from tornado.ioloop import IOLoop

# Initialize the IP address and WebSocket URI
ip_address = socket.gethostbyname(socket.gethostname())
autolabDriver = dict(host=ip_address, port=15111)
uri = f"ws://{autolabDriver['host']}:{autolabDriver['port']}/ws"

# Initialize the document and time stamp
doc = curdoc()
time_stamp = 0
pids = collections.deque(10*[0], 10)

# Initialize the data source
source = ColumnDataSource(data=dict(t_s=[], freq=[], Ewe_V=[], Z_real=[], Z_imag=[], phase=[], modulus=[], I_A=[]))

# Create the plot
plot = figure(height=300) # title="Initial Plot"
plot.title.align = "center"
plot.title.text_font_size = "24px"

# Define the layout for checkbox and radio buttons with user-friendly labels
labels = ["Time [s]", "Frequency [Hz]", "Potential [V]", "Z_real [Ohm]", "Z_imag [Ohm]", "Phase Shift [degree]", "Modulus [Ohm]", "Current [A]"]
variable_names = ["t_s", "freq", "Ewe_V", "Z_real", "Z_imag", "phase", "modulus", "I_A"]
label_to_variable = dict(zip(labels, variable_names))

checkbox_button_group = CheckboxButtonGroup(labels=labels, active=[0])
radio_button_group = RadioButtonGroup(labels=labels, active=0)

x_axis_label_text = Div(text="X-axis:")
y_axis_label_text = Div(text="Y-axis:")

current_measurement_id = None
source = ColumnDataSource(data={})

def reset_plot(new_measurement_id):
    global plot, source
    # Clear the data source
    source = ColumnDataSource(data=dict(t_s=[], freq=[], Ewe_V=[], Z_real=[], Z_imag=[], phase=[], modulus=[], I_A=[]))
    # Remove the last root (the current plot) from the document
    if len(doc.roots) > 0:
        last_root = doc.roots[-1]
        doc.remove_root(last_root)
    plot = figure(title=f"Measurement ID: {new_measurement_id}", height=300)
    plot.title.align = "center"
    plot.title.text_font_size = "18px"
    # Add a new line renderer
    plot.line(x='x', y='y', source=source)
    doc.add_root(plot)


# Function to update the plot based on the selected buttons
def update_plot():
    global plot, source, checkbox_button_group, radio_button_group

    # Clear existing lines
    plot.renderers = []

    x_axis_label = label_to_variable[checkbox_button_group.labels[checkbox_button_group.active[0]]]
    y_axis_label = label_to_variable[radio_button_group.labels[radio_button_group.active]]

    # Update axis titles
    plot.xaxis.axis_label = checkbox_button_group.labels[checkbox_button_group.active[0]]
    plot.yaxis.axis_label = radio_button_group.labels[radio_button_group.active]

    # Add new line based on the selection
    plot.line(x=x_axis_label, y=y_axis_label, source=source)

# Callbacks for button groups
checkbox_button_group.on_change('active', lambda attr, old, new: update_plot())
radio_button_group.on_change('active', lambda attr, old, new: update_plot())


# Function to stream new data to the plot
def update(new_data):
    global source
    source.stream(new_data, rollover=100)
    update_plot()

# Async function to receive and process data
async def loop():
    global current_measurement_id
    async with websockets.connect(uri) as ws:
        while True:
            new_data = await ws.recv()
            new_data = json.loads(new_data)

            # Check if new_data is measurement_id
            if isinstance(new_data, dict) and 'measurement_id' in new_data:
                new_measurement_id = new_data['measurement_id']
                new_data.pop('measurement_id')
                if new_measurement_id != current_measurement_id:
                    current_measurement_id = new_measurement_id
                    # Update the plot title and reset the plot
                    doc.add_next_tick_callback(partial(reset_plot, new_measurement_id))
                    doc.add_next_tick_callback(partial(update, new_data))
                else:
                    doc.add_next_tick_callback(partial(update, new_data))

# Add the plot and widgets to the document
doc.add_root(x_axis_label_text)
doc.add_root(checkbox_button_group)
doc.add_root(y_axis_label_text)
doc.add_root(radio_button_group)
doc.add_root(plot)

# Start the data receiving loop
IOLoop.current().spawn_callback(loop)
