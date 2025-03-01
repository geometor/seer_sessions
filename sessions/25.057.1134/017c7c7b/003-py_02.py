import numpy as np

def analyze_grids(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    blue_positions_input = np.argwhere(input_grid == 1).tolist()
    red_positions_output = np.argwhere(output_grid == 2).tolist()
    added_rows = output_shape[0] - input_shape[0]

    return {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "blue_positions_input": blue_positions_input,
        "red_positions_output": red_positions_output,
        "added_rows": added_rows,
    }

# Example grids (replace with actual data from the task)
# input_grid, output_grid, result_grid

#example_data provided below

analysis_results = []
for i, (input_grid, output_grid) in enumerate(example_data):
    result = analyze_grids(np.array(input_grid), np.array(output_grid))
    analysis_results.append(f"Example {i+1}:\n{result}")

print("\n".join(analysis_results))
