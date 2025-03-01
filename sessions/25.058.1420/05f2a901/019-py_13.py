import numpy as np

def code_execution(input_grid, output_grid, predicted_output):
    def get_object_details(grid, color):
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            return "Absent", None, None, None, None
        min_row, min_col = coords.min(axis=0)
        max_row, max_col = coords.max(axis=0)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        return "Present", min_row, min_col, height, width

    results = {}

    results["input_grid_shape"] = input_grid.shape
    results["output_grid_shape"] = output_grid.shape
    results["predicted_output_shape"] = predicted_output.shape
    results["grids_match"] = np.array_equal(output_grid, predicted_output)

    for color, color_name in [(8, "azure"), (2, "red")]:
        results[f"{color_name}_input"] = get_object_details(input_grid, color)
        results[f"{color_name}_output"] = get_object_details(output_grid, color)
        results[f"{color_name}_predicted"] = get_object_details(predicted_output, color)
    return results

# Example Usage (replace with actual data from the task)
# Provide the input and output grid as numpy arrays

input_grids = [np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 8, 8, 8, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 2, 2, 2, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
               np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0]]),
               np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 8, 8, 8, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])]
output_grids = [np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 8, 8, 8, 5, 5, 5],
        [5, 5, 5, 5, 2, 2, 2, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
                np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0]]),
                np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 8, 8, 8, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5]])]

predicted_outputs = [transform(input_grid) for input_grid in input_grids]

for i in range(len(input_grids)):
    results = code_execution(input_grids[i], output_grids[i], predicted_outputs[i])
    print(f"Example {i+1}:")
    for key, value in results.items():
        print(f"  {key}: {value}")