import numpy as np

def describe_grid(grid, name):
    """Provides a description of the grid's shape and color distribution."""
    shape = grid.shape
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_description = ", ".join([f"{color}: {count}" for color, count in zip(unique_colors, counts)])
    print(f"{name} - Shape: {shape}, Colors: {color_description}")

# Load the example grids (Replace with your actual grid data)
train_inputs = [
    np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),  # input grid from first example
    np.array([[5, 5], [5, 5]]),
    np.array([[7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7]]),
    np.array([[2, 2, 2], [2, 2, 2]]),
    np.array([[8]])
]
train_outputs = [
    np.array([[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5]]), # output grid for first example
    np.array([[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]),
    np.array([[7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7]]),
    np.array([[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]]),
    np.array([[8, 8], [8, 8]])

]

# Describe each grid
for i, (inp, outp) in enumerate(zip(train_inputs, train_outputs)):
    describe_grid(inp, f"Train Input {i+1}")
    describe_grid(outp, f"Train Output {i+1}")
