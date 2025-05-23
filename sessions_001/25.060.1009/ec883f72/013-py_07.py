import numpy as np

def find_azure_shape(grid):
    """Finds the coordinates of all azure (8) pixels."""
    azure_coords = np.argwhere(grid == 8)
    print(f"azure_coords: {azure_coords}")
    return azure_coords

def translate_shape(coords, rows_to_move):
    """Translates a set of coordinates down by a specified number of rows."""
    translated_coords = []
    for r, c in coords:
        translated_coords.append((r + rows_to_move, c))
    print(f"translated_coords: {translated_coords}")
    return np.array(translated_coords)

def find_magenta_endpoints(grid):
    """ find endpoints for the columns to fill, by iterating original columns"""
    endpoints = []
    
    azure_coords = find_azure_shape(grid)
    
    if len(azure_coords) > 0: # check to prevent errors
      min_azure_row = np.min(azure_coords[:, 0])
      max_azure_row = np.max(azure_coords[:, 0])

      # iterate each column that contains any azure
      azure_cols = np.unique(azure_coords[:, 1])

      for col in azure_cols:
          # bottom of translated azure shape, in this column
          endpoints.append( (max_azure_row + 1, col) )

    magenta_coords = np.argwhere(grid == 6)      
    for r, c in magenta_coords:
        endpoints.append( (r,c))
    print(f"magenta_endpoints: {endpoints}")
    return endpoints

def find_lowest_non_white_row(grid):
    """Finds the lowest row index that contains a non-white pixel."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols):
            if grid[r, c] != 0:
                print(f"lowest_non_white_row: {r}")
                return r
    return 0
    

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the Azure Shape
    azure_coords = find_azure_shape(input_grid)

    # 2. Translate the Azure Shape (one row down)
    translated_azure_coords = translate_shape(azure_coords, 1)
    for r, c in translated_azure_coords:
        if 0 <= r < rows and 0 <= c < cols: # check bounds
           output_grid[r, c] = 8

    # 3. find fill endpoints
    magenta_endpoints = find_magenta_endpoints(input_grid)

    # 4. fill endpoints down to lowest non-white cell
    lowest_non_white = find_lowest_non_white_row(input_grid)

    for r,c in magenta_endpoints:
      for row_index in range(r, lowest_non_white + 1):
          output_grid[row_index,c] = 6


    return output_grid

# Example grids (replace with actual data from the task)
example_grids = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 8, 8, 0, 0],
              [0, 0, 8, 8, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 8, 8, 8, 0],
              [0, 0, 8, 8, 8, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 2, 2, 2, 0]]),
    np.array([[0, 0, 0, 0, 0, 6],
              [0, 0, 0, 0, 8, 0],
              [0, 0, 0, 8, 0, 0],
              [0, 0, 8, 0, 0, 0],
              [0, 8, 0, 0, 0, 0]])

]

for i, grid in enumerate(example_grids):
    print(f"--- Example {i + 1} ---")
    transform(grid)