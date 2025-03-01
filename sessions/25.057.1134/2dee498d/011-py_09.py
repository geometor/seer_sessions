import numpy as np

def analyze_column_inclusion(input_grid, output_grid):
    """
    Analyzes which columns from the input grid are present in the output grid.

    Args:
        input_grid: The input grid as a 2D list or numpy array.
        output_grid: The output grid as a 2D list or numpy array.

    Returns:
        A dictionary where keys are column indices from the input grid,
        and values are booleans indicating if the column is present in
        the output grid.  Also prints analysis to the console.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_cols = input_grid.shape[1]
    output_cols = output_grid.shape[1]

    print(f"Input grid shape: {input_grid.shape}")
    print(f"Output grid shape: {output_grid.shape}")

    column_inclusion = {}

    for i in range(input_cols):
        input_col = input_grid[:, i]
        is_present = False
        for j in range(output_cols):
            output_col = output_grid[:, j]
            if np.array_equal(input_col, output_col):
                is_present = True
                break
        column_inclusion[i] = is_present
        print(f"Column {i} from input present in output: {is_present}")

    return column_inclusion