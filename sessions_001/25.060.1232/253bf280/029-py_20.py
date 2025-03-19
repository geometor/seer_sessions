# Hypothetical data (replace with actual data from the task)
# This is for executing code, not intended to be complete examples
# This is just to get sizes correct
import numpy as np

example_inputs = [
    np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]]),
    np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]]),
    np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]]),
]
example_outputs = [
    np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]]),
    np.array([[2, 2, 2], [3, 3, 3]]),
    np.array([[2, 2, 2], [2, 2, 2], [3, 3, 3]]),
]

def check_identity(input_grid, output_grid):
    return np.array_equal(input_grid, output_grid)

def check_cropping(input_grid, output_grid):
    #checks to see if output is a cropped version
    if input_grid.shape[0] > output_grid.shape[0] or input_grid.shape[1] > output_grid.shape[1]:
        return True
    else: return False

def check_color_change(input_grid, output_grid, color_in, color_out):
    # Check if the output is the same as the input, but with a color change
    temp_grid = np.copy(input_grid)
    temp_grid[temp_grid == color_in] = color_out
    return np.array_equal(temp_grid, output_grid)

results = []
for i, (input_grid, output_grid) in enumerate(zip(example_inputs, example_outputs)):
    identity_holds = check_identity(input_grid, output_grid)
    cropping_possible = check_cropping(input_grid, output_grid)

    color_change_1_to_2 = False

    if not identity_holds and not cropping_possible:
        color_change_1_to_2 = check_color_change(input_grid, output_grid, 1, 2)
    
    results.append({
        "example": i + 1,
        "identity_holds": identity_holds,
        "cropping_possible": cropping_possible,
        "color_change_1_to_2": color_change_1_to_2
    })

for result in results:
    print(result)