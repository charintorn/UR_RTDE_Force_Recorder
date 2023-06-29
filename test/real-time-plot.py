import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Create a figure and axes for the plot
fig, ax = plt.subplots()
x = []
y = []


new_x = 0  # Define new_x as a global variable

# Create an empty line object
(line,) = ax.plot(x, y)

# Set up the plot axes
ax.set_xlim(0, 10)
ax.set_ylim(0, 100)


# Function to generate new data
def generate_data():
    global new_x  # Use the global new_x variable
    new_x = len(x) + 1
    new_y = np.random.randint(0, 100)
    x.append(new_x)
    y.append(new_y)


# Function to update the plot
def update(frame):
    generate_data()
    line.set_data(x, y)
    ax.set_xlim(max(0, new_x - 10), new_x)


# Create the animation
ani = FuncAnimation(fig, update, interval=100)  # Update every 1 second (1000 milliseconds)

# Show the plot
plt.show()
