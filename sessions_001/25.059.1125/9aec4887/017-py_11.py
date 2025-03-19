import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    """Analyzes a single example and returns relevant metrics."""

    input_pixels = input_grid.size
    output_pixels = output_grid.size
    predicted_pixels = predicted_output.size if predicted_output is not None else 0
    
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    predicted_colors = np.unique(predicted_output) if predicted_output is not None else []

    correct = np.array_equal(output_grid, predicted_output) if predicted_output is not None else False

    metrics = {
        "input_pixels": int(input_pixels),
        "output_pixels": int(output_pixels),
        "predicted_pixels": int(predicted_pixels),
        "input_colors": [int(c) for c in input_colors],
        "output_colors": [int(c) for c in output_colors],
        "predicted_colors": [int(c) for c in predicted_colors],
        "correct": bool(correct)
    }
    return metrics

def find_object(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size > 0:
         return coords
    return None

def get_bounding_box(grid):

    orange_line = find_object(grid, 7)
    blue_line =  find_object(grid, 1)
    yellow_line = find_object(grid, 4)
    magenta_line = find_object(grid, 6)
    azure_shape = find_object(grid,8)

    min_row = orange_line[0][0] if orange_line is not None else 0
    max_row = blue_line[0][0] if blue_line is not None else grid.shape[0] -1
    min_col = yellow_line[0][1] if yellow_line is not None else 0
    max_col = magenta_line[0][1] if magenta_line is not None else grid.shape[1] - 1

    if azure_shape is not None:
        min_azure_row = np.min(azure_shape[:, 0])
        max_azure_row = np.max(azure_shape[:, 0])
        min_azure_col = np.min(azure_shape[:, 1])
        max_azure_col = np.max(azure_shape[:, 1])

        min_row = min(min_row, min_azure_row)
        max_row = max(max_row, max_azure_row)
        min_col = min(min_col, min_azure_col)
        max_col = max(max_col, max_azure_col)


    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Get the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid)

    # Extract the subgrid
    subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]

    #Remove 0 columns
    
    # Find indices of columns that contain non-zero values.
    non_zero_cols = np.any(subgrid != 0, axis=0)
    # Use boolean indexing to select only columns with non-zero values.
    output_grid = subgrid[:, non_zero_cols]
    
    return output_grid