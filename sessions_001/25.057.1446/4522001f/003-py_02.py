def code_execution(inputs, outputs, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(zip(inputs, outputs)):
        try:
            predicted_output = transform_function(input_grid)
            results.append({
                "example_index": i,
                "success": predicted_output == expected_output,
                "input_shape": (len(input_grid), len(input_grid[0]) if input_grid else 0),
                "output_shape": (len(expected_output), len(expected_output[0]) if expected_output else 0),
                "predicted_output_shape": (len(predicted_output), len(predicted_output[0]) if predicted_output else 0)
            })
        except Exception as e:
            results.append({
                "example_index": i,
                "success": False,
                "error": str(e),
                "input_shape": (len(input_grid), len(input_grid[0]) if input_grid else 0),
                "output_shape": (len(expected_output), len(expected_output[0]) if expected_output else 0),
                "predicted_output_shape": None,

            })
    return results

#Example Use (Replace with the actual inputs and outputs, and transform function)
inputs = [
    [[0, 2, 0], [0, 0, 0], [0, 0, 0]],
    [[2, 0, 0], [0, 0, 0], [0, 0, 2]],
    [[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
]
outputs = [
    [[3, 3, 3, 3, 0, 0, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
    [[3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3]],
    [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 0, 0, 0], [0, 3, 3, 3, 3, 0, 0, 0], [0, 3, 3, 3, 3, 0, 0, 0], [0, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
]


import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    input_grid = np.array(input_grid)

    # Replace red (2) with green (3)
    modified_input = np.where(input_grid == 2, 3, input_grid)

    # Initialize output grid with zeros, making it 4 times the size of the input - NOT 3.
    output_grid = np.zeros((input_grid.shape[0] * 4, input_grid.shape[1] * 4), dtype=int)

    # Iterate through the modified input grid
    for i in range(modified_input.shape[0]):
        for j in range(modified_input.shape[1]):
            if modified_input[i, j] == 3:
                # Create a 4x4 block of green (3) pixels in the output grid
                output_grid[i * 4 : i * 4 + 4, j * 4: j * 4 + 4] = 3 # Use 4, not 3.

    return output_grid.tolist()

results = code_execution(inputs, outputs, transform)
for result in results:
    print(result)
