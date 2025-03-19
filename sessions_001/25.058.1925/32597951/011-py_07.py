import numpy as np

def compare_grids(predicted, actual):
    """
    Compares two grids and returns a grid highlighting the differences.
    0: correct
    1: incorrect
    """
    comparison_result = (predicted != actual).astype(int)
    return comparison_result

def find_azure_region(grid):
    # Find coordinates of all azure pixels
    azure_coords = np.argwhere(grid == 8)
    if azure_coords.size == 0:
        return None, None, None, None
    # Determine the bounding box
    min_row = np.min(azure_coords[:, 0])
    max_row = np.max(azure_coords[:, 0])
    min_col = np.min(azure_coords[:, 1])
    max_col = np.max(azure_coords[:, 1])
    return min_row, max_row, min_col, max_col

def is_connected(grid, row, col, original_color):
    """
    Checks if a pixel at (row, col) is connected to other pixels of the same color
    using an 8-neighbor connectivity (including diagonals).
    """    
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == original_color:
                return True
    return False

def check_connectivity(grid, row, col, min_row, max_row, min_col, max_col):
    """
    Checks if removing a pixel at (row, col) would disconnect the region.
    """
    original_color = grid[row, col]
    grid[row, col] = 0  # Temporarily remove the pixel

    # Check if any of the neighbors are still connected to the region
    neighbors_connected = False
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if min_row <= nr <= max_row and min_col <= nc <= max_col:
                if grid[nr, nc] == original_color:
                    if is_connected(grid,nr, nc, original_color):
                      neighbors_connected = True
                      break
        if neighbors_connected:
          break

    grid[row, col] = original_color  # Restore the pixel
    return not neighbors_connected
  

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the region of interest (where azure pixels are)
    min_row, max_row, min_col, max_col = find_azure_region(input_grid)
    
    if min_row is None:  # No azure pixels found, return the original grid
        return output_grid

    # Iterate through the region of interest
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            # Check if the current pixel is azure
            if output_grid[row, col] == 8:
                # Check if removing this pixel disconnects the region
                if check_connectivity(output_grid, row, col, min_row, max_row, min_col, max_col):
                  output_grid[row,col] = 3

    return output_grid

# Example data (replace with actual data from the task)
train_ex = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 3, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 8, 3, 3, 3, 8, 0, 0, 0], [0, 0, 8, 3, 3, 3, 8, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 8, 3, 8, 0, 0, 0], [0, 0, 8, 3, 8, 0, 0, 0], [0, 0, 8, 3, 8, 0, 0, 0], [0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
       "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 3, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 3, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 3, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    }
]

results = []
for i, ex in enumerate(train_ex):
  input_grid = np.array(ex["input"])
  output_grid = np.array(ex["output"])
  predicted_grid = transform(input_grid)
  comparison = compare_grids(predicted_grid, output_grid)
  results.append({
      "example": i + 1,
      "input": input_grid.tolist(),
      "expected_output": output_grid.tolist(),
      "actual_output": predicted_grid.tolist(),
      "comparison": comparison.tolist(),
      "errors": int(np.sum(comparison))
  })

for result in results:
  print(result)