import numpy as np

def find_azure_cross(grid):
    """Finds the center coordinates of the azure cross, defined by longest lines."""
    rows, cols = grid.shape
    azure_pixels = np.where(grid == 8)
    
    # Find longest horizontal line
    row_counts = np.bincount(azure_pixels[0])
    central_row_index = np.argmax(row_counts)

    # Find longest vertical line
    col_counts = np.bincount(azure_pixels[1])
    central_col_index = np.argmax(col_counts)
    
    return central_row_index, central_col_index

def flood_fill(grid, start_row, start_col, fill_color, boundary_color):
    """Fills a region bounded by a specific color."""
    rows, cols = grid.shape
    if grid[start_row, start_col] == boundary_color or grid[start_row, start_col] == fill_color:
        return

    stack = [(start_row, start_col)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < rows and 0 <= c < cols and grid[r, c] != boundary_color and grid[r,c] != fill_color:
            grid[r, c] = fill_color
            stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the azure cross
    central_row_index, central_col_index = find_azure_cross(output_grid)

    # Fill Above (Red)
    flood_fill(output_grid, central_row_index - 1, central_col_index, 2, 8)

    # Fill Left Below (Magenta)
    flood_fill(output_grid, central_row_index + 1, central_col_index - 1, 6, 8)

    # Fill Top-Left, First Row (Yellow)
    if central_row_index + 1 < rows:
        for c in range(central_col_index -1, -1, -1):
             if output_grid[central_row_index+1, c] == 8:
                break
             output_grid[central_row_index + 1, c] = 4
    
    # Fill Right Below (Green)
    flood_fill(output_grid, central_row_index + 1, central_col_index + 1, 3, 8)

    # Fill Bottom (Blue) - only on the last row
    if central_row_index+1<rows:
        for c in range(cols):
            if output_grid[rows-1,c] != 8:
                output_grid[rows - 1, c] = 1

    return output_grid

# Example Inputs and Outputs (replace with your actual data)
example_inputs = [
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
              [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

]
example_outputs = [
    np.array([[0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
              [0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
              [0, 4, 4, 4, 6, 3, 3, 3, 3, 0],
              [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
              [0, 0, 0, 0, 4, 4, 4, 4, 6, 3, 3, 3, 3, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
              [0, 0, 0, 0, 4, 4, 6, 3, 3, 3, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]])
]

for i, (input_grid, expected_output) in enumerate(zip(example_inputs, example_outputs)):
    predicted_output = transform(input_grid.copy())  # Work on a copy
    comparison = (predicted_output == expected_output)
    differences = np.where(comparison == False)
    print(f"--- Example {i+1} ---")
    print(f"  Mismatched pixels: {len(differences[0])}")
    if len(differences[0]) > 0:
        print("  Locations (row, col) and values (predicted, expected):")
        for j in range(len(differences[0])):
            row, col = differences[0][j], differences[1][j]
            print(f"    ({row}, {col}): ({predicted_output[row, col]}, {expected_output[row, col]})")
    print(f"  Input:\n{input_grid}")
    print(f"  Expected Output:\n{expected_output}")
    print(f"  Predicted Output:\n{predicted_output}")