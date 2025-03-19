import numpy as np

def code_execution(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    input_objects = {}
    expected_objects = {}
    actual_objects = {}

    for color in range(10):  # Check all colors
        input_objects[color] = np.sum(input_grid == color)
        expected_objects[color] = np.sum(expected_output == color)
        actual_objects[color] = np.sum(actual_output == color)

    rightmost_input = 0
    for c in range(input_grid.shape[1]):
        if np.any(input_grid[:, c] != 0):
            rightmost_input = c

    rightmost_expected = 0
    for c in range(expected_output.shape[1]):
        if np.any(expected_output[:, c] != 0):
            rightmost_expected = c
    
    rightmost_actual = 0
    for c in range(actual_output.shape[1]):
        if np.any(actual_output[:,c] != 0):
            rightmost_actual = c
            

    print("Pixel Counts:")
    print(f"  Input: {input_objects}")
    print(f"  Expected: {expected_objects}")
    print(f"  Actual:   {actual_objects}")
    print(f"Rightmost Column (non-white):")
    print(f"  Input: {rightmost_input}")
    print(f"  Expected: {rightmost_expected}")
    print(f"  Actual: {rightmost_actual}")
    print(f"Shapes: Input {input_grid.shape} Expected {expected_output.shape} Actual {actual_output.shape}")
    print("Object comparison (Input vs Expected)")

    #check alignment of objects
    match = np.array_equal(actual_output, expected_output)
    print(f"Objects match exactly: {match}")

# Example Usage (replace with actual data from each example)
# i will prepare this data then call the function
example_data = [
    {
     "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 2, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
     "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 3, 2, 2, 2, 2, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 7, 0], [0, 3, 2, 2, 3, 0, 0, 0, 0, 0, 7, 0], [0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 0], [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 0], [0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 7, 0], [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    }
]

for i, example in enumerate(example_data):
    print(f"Example {i + 1}:")
    code_execution(example["input"], example["output"], transform(np.array(example["input"])))
    print("-" * 40)
