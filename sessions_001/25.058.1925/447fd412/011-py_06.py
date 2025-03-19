import numpy as np

def find_blue_cross_center(grid):
    blue_pixels = np.argwhere(grid == 1)
    if blue_pixels.size == 0:
        return None
    center_row = int(np.mean(blue_pixels[:, 0]))
    center_col = int(np.mean(blue_pixels[:, 1]))
    return (center_row, center_col)

def analyze_example(input_grid, expected_output, actual_output):
    cross_center = find_blue_cross_center(input_grid)
    red_pixels = np.argwhere(input_grid == 2)
    diff = expected_output != actual_output

    print("Cross Center:", cross_center)
    print("Red Pixels:", red_pixels)
    print("Differences:", np.argwhere(diff))
    print("Difference values (expected, actual):", [(expected_output[r,c], actual_output[r,c]) for r, c in np.argwhere(diff)])

# Example data (replace with actual data from the task)
example_inputs = [
np.array([[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0]]),
np.array([[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[1,1,1,1,1,1,1],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0]]),
np.array([[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[1,1,1,1,1,1,1,1,1],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0]]),
]
example_outputs = [
np.array([[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0]]),
np.array([[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[1,1,1,1,1,1,1],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0]]),
np.array([[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[1,1,1,1,1,1,1,1,1],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0,0]]),
]
#Assuming transform is previously defined.

actual_outputs = []
for i, ex_input in enumerate(example_inputs):
    actual_outputs.append(transform(ex_input))
for i, (ex_input, ex_output, act_output) in enumerate(zip(example_inputs, example_outputs, actual_outputs)):
    print(f"--- Example {i+1} ---")
    analyze_example(ex_input, ex_output, act_output)
