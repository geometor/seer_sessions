import numpy as np

def analyze_example(input_grid, output_grid, result_grid):
    input_non_white = np.sum(input_grid != 0)
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape
    result_rows, result_cols = result_grid.shape if result_grid is not None else (0, 0)
    output_non_white = np.sum(output_grid != 0)
    result_non_white = np.sum(result_grid != 0) if result_grid is not None else 0
    match = np.array_equal(output_grid, result_grid) if result_grid is not None else False

    # Check for removed rows
    removed_rows = []
    for i in range(input_rows):
        if not np.any(np.isin(input_grid[i], output_grid)):
           if not np.all(input_grid[i] == 0):
                removed_rows.append(i)

    # Check for removed columns
    removed_cols = []
    for j in range(input_cols):
        if not np.any(np.isin(input_grid[:, j], output_grid)):
            if not np.all(input_grid[:,j] == 0):
                removed_cols.append(j)
    
    print(f"""
    Input:
        shape: {input_rows}x{input_cols}
        non-white pixels: {input_non_white}
        removed_rows: {removed_rows}
        removed_cols: {removed_cols}
    Output:
        shape: {output_rows}x{output_cols}
        non-white pixels: {output_non_white}
        expected == result : {match}
    Result:
        shape: {result_rows}x{result_cols}
        non-white-pixels: {result_non_white}
    """)
    return

# Example Usage with dummy data (replace with your actual data)
input_grid = np.array([[0, 0, 0], [0, 0, 0], [1, 2, 0]])
output_grid = np.array([[1, 2, 0], [0, 0, 0], [0, 0, 0]])
result_grid = np.array([[1, 2, 0], [0, 0, 0], [0, 0, 0]])
analyze_example(input_grid, output_grid, result_grid)

input_grid = np.array([[0, 0, 0, 0], [0, 5, 0, 0], [1, 0, 3, 0],[0, 0, 0, 0]])
output_grid = np.array([[1, 0, 3], [0, 0, 0], [0, 0, 0]])
result_grid = np.array([[5, 0, 0], [0, 0, 0], [0, 0, 0]])
analyze_example(input_grid, output_grid, result_grid)

input_grid = np.array([[7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7],[7, 7, 7, 7]])
output_grid = np.array([[7, 7, 7], [7, 7, 7], [7, 7, 7]])
result_grid = np.array([[7, 7, 7], [7, 7, 7], [7, 7, 7]])
analyze_example(input_grid, output_grid, result_grid)

input_grid = np.array([[0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 5, 0], [2, 0, 8, 0, 0, 6],[0, 0, 0, 0, 0, 0]])
output_grid = np.array([[2, 0, 8], [0, 0, 6], [0, 0, 0]])
result_grid = np.array([[5, 0, 5], [0, 0, 0], [0, 0, 0]])
analyze_example(input_grid, output_grid, result_grid)