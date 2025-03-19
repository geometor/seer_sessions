import numpy as np

example_inputs = [
    [[3, 3, 3], [0, 0, 0], [0, 0, 0]],  # Example 1 input
    [[0, 0, 0, 0], [0, 5, 5, 5], [0, 0, 0, 0]],  # Example 2 input
    [[0, 0, 0, 0, 8], [0, 0, 0, 8, 0], [0, 0, 8, 0, 0], [0, 8, 0, 0, 0]],  # Example 3 input
]
example_outputs = [
    [[0, 0, 3], [0, 0, 3], [0, 0, 3]],  # Example 1 output
    [[0, 0, 0], [0, 5, 0], [0, 5, 0], [0, 5, 0]],  # Example 2 output
    [[0, 0, 0, 0, 0], [0, 0, 0, 0, 8], [0, 0, 0, 8, 0], [0, 0, 8, 0, 0]], # Example 3 output
]

def analyze_changes(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    rotated_input = np.rot90(input_grid)
    changes = []

    for r in range(rotated_input.shape[0]):
        for c in range(rotated_input.shape[1]):
            original_value = input_grid[input_grid.shape[0] - 1 - c, r] # Corrected indexing for pre-rotation
            rotated_value = rotated_input[r, c]
            output_value = output_grid[r,c]
            
            if rotated_value != output_value:
                changes.append(
                    {
                        "rotated_row": r,
                        "rotated_col": c,
                        "original_value": original_value,
                        "rotated_value": rotated_value,
                        "output_value": output_value,
                    }
                )
    return changes

for i in range(len(example_inputs)):
  results = analyze_changes(example_inputs[i], example_outputs[i])
  print(f"Example {i+1} Changes:")
  print(results)
