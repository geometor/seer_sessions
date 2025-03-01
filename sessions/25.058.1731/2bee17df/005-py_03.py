import numpy as np

# Provided transform function and helper (copied from above)
def get_neighbors(grid, row, col):
    """Returns a list of neighbors (up, down, left, right) for a given cell."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find inner azure pixels (adjacent to white)
    inner_azure_pixels = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 8:
                for nr, nc in get_neighbors(output_grid, r, c):
                    if output_grid[nr, nc] == 0:
                        inner_azure_pixels.append((r,c))
                        break

    # Define Green region
    for r in range(3, 9):
      for c in range(3, 9):
        # skip replacement when adjcent to red pixels
        neighbor_red = False
        for neighbor_row, neighbor_col in get_neighbors(output_grid,r, c):
          if output_grid[neighbor_row, neighbor_col] == 2:
            neighbor_red = True
            break
        if not neighbor_red and output_grid[r,c] == 0:
          output_grid[r,c] = 3

    return output_grid

# Example Inputs and Outputs (replace with actual data)
example_data = [
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]), np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 2, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 0, 0, 2, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]), np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 3, 3, 2, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 0, 8, 8],
       [8, 8, 8, 0, 0, 0, 2, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8]]), np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 3, 8, 8],
       [8, 8, 8, 3, 3, 3, 2, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8, 8]]))
]

for i, (input_grid, expected_output) in enumerate(example_data):
    transformed_grid = transform(input_grid)
    if not np.array_equal(transformed_grid, expected_output):
        print(f"Mismatch in example {i+1}:")
        print("Input:")
        print(input_grid)
        print("Expected Output:")
        print(expected_output)
        print("Actual Output:")
        print(transformed_grid)
    else:
        print(f"Example {i+1} is correct")