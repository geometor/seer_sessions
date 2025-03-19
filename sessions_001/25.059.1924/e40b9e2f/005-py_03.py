import numpy as np

def get_shape_bounds(grid):
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def analyze_example(input_grid, output_grid):
    input_bounds = get_shape_bounds(input_grid)
    output_bounds = get_shape_bounds(output_grid)

    print(f"  Input Bounds: {input_bounds}")
    print(f"  Output Bounds: {output_bounds}")

    if input_bounds and output_bounds:
        input_shape = input_grid[input_bounds[0]:input_bounds[1]+1, input_bounds[2]:input_bounds[3]+1]
        output_shape = output_grid[output_bounds[0]:output_bounds[1]+1, output_bounds[2]:output_bounds[3]+1]

        print(f"Input shape: {input_shape.shape}")
        print(f"Output shape: {output_shape.shape}")

        # Check if color swap is consistent
        unique_input_colors = np.unique(input_shape[input_shape != 0])
        unique_output_colors = np.unique(output_shape[output_shape != 0])

        if len(unique_input_colors) == len(unique_output_colors):
            color_swap_consistent = "Yes"
        else:
            color_swap_consistent = "No"

        print(f"Color Swap Consistent: {color_swap_consistent}")

# Example data grids (replace with actual data)
examples = [
    (np.array([[0, 0, 0, 0, 0],
              [0, 4, 4, 4, 0],
              [0, 4, 7, 4, 0],
              [0, 4, 4, 4, 0],
              [0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0],
              [0, 7, 7, 7, 0],
              [0, 7, 4, 7, 0],
              [0, 7, 7, 7, 0],
              [0, 0, 0, 0, 0]])),
    (np.array([[0, 0, 4, 4, 0, 0],
               [0, 0, 4, 4, 0, 0],
               [0, 0, 7, 7, 0, 0],
               [0, 0, 7, 7, 0, 0],
               [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0],
               [0, 0, 7, 7, 0, 0],
               [0, 0, 7, 7, 0, 0],
               [0, 0, 4, 4, 0, 0],
               [0, 0, 4, 4, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0],
              [0, 4, 4, 7, 7, 0],
              [0, 4, 4, 7, 7, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 7, 7, 4, 4, 0],
              [0, 7, 7, 4, 4, 0],
              [0, 0, 0, 0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0],
              [0, 7, 7, 0, 0, 0],
              [0, 7, 7, 0, 0, 0],
              [0, 4, 4, 0, 0, 0],
              [0, 4, 4, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 4, 4, 0, 0, 0],
              [0, 4, 4, 0, 0, 0],
              [0, 7, 7, 0, 0, 0],
              [0, 7, 7, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]))
]
for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)