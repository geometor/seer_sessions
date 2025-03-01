import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the valid neighbors (up, down, left, right) of a cell in a grid.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def flood_fill(grid, row, col, target_color, replacement_color):
    """
    Performs a flood fill operation on the grid.
    Replaces target_color with replacement_color starting from (row, col).
    """
    rows, cols = grid.shape
    if row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != target_color:
        return
    
    grid[row, col] = replacement_color
    
    for neighbor_row, neighbor_col in get_neighbors(grid, row, col):
      flood_fill(grid, neighbor_row, neighbor_col, target_color, replacement_color)


def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    Fills regions of color 0 with color 3, connecting regions of other colors, bounded by color 8.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find a color 0 to fill
    
    for r in range(rows):
        for c in range(cols):
          if output_grid[r,c] == 0:
              # start filling
              flood_fill(output_grid,r,c,0,3)
                

    # Fill between non-background and non-zero colors with 3

    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] != 8 and output_grid[r,c] != 3 and output_grid[r,c] != 0:
          # found a non-background, non-fill, and non-zero cell - now what are the
          # neighbors?
          for neighbor_row, neighbor_col in get_neighbors(input_grid,r,c):
              if input_grid[neighbor_row, neighbor_col] != 8 and \
                input_grid[neighbor_row,neighbor_col] != input_grid[r,c]:
                
                # this neighbor is also not background, is a different color than
                # current, now look between and start filling
                
                # midpoint - only checking cardinal directions (not diag)
                mid_r = (r + neighbor_row) // 2
                mid_c = (c + neighbor_col) // 2
                if output_grid[mid_r, mid_c] == 0:
                  flood_fill(output_grid, mid_r, mid_c, 0, 3)



    return output_grid

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid highlighting differences."""
    if grid1.shape != grid2.shape:
        print("Grids have different shapes!")
        return None

    diff_grid = np.zeros_like(grid1)
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                diff_grid[i, j] = 1  # Mark differences with 1
    return diff_grid

# Example Task Data (replace with actual data)
train = [
  (np.array([[8,8,8,8,8,8,8,8,8,8],[8,0,0,0,0,0,0,0,0,8],[8,0,0,0,2,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,8],[8,8,8,8,8,8,8,8,8,8]]), np.array([[8,8,8,8,8,8,8,8,8,8],[8,3,3,3,3,3,3,3,3,8],[8,3,3,3,2,3,3,3,3,8],[8,3,3,3,3,3,3,3,3,8],[8,8,8,8,8,8,8,8,8,8]])),
  (np.array([[8,8,8,8,8,8,8],[8,0,0,4,0,0,8],[8,0,4,4,4,0,8],[8,0,0,4,0,0,8],[8,8,8,8,8,8,8]]), np.array([[8,8,8,8,8,8,8],[8,3,3,4,3,3,8],[8,3,4,4,4,3,8],[8,3,3,4,3,3,8],[8,8,8,8,8,8,8]])),
  (np.array([[8,8,8,8,8,8,8,8],[8,0,0,0,0,0,0,8],[8,0,1,0,0,0,0,8],[8,0,0,0,0,5,0,8],[8,0,0,0,0,0,0,8],[8,8,8,8,8,8,8,8]]), np.array([[8,8,8,8,8,8,8,8],[8,3,3,3,3,3,3,8],[8,3,1,3,3,3,3,8],[8,3,3,3,3,5,3,8],[8,3,3,3,3,3,3,8],[8,8,8,8,8,8,8,8]])),
]

for i, (input_grid, expected_output) in enumerate(train):
    predicted_output = transform(np.copy(input_grid))
    diff_grid = compare_grids(predicted_output, expected_output)

    print(f"Example {i+1}:")
    print("Input:\n", input_grid)
    print("Expected Output:\n", expected_output)
    print("Predicted Output:\n", predicted_output)
    if diff_grid is not None:
        print("Differences (1 indicates a difference):\n", diff_grid)
        print(f"Number of differing pixels: {np.sum(diff_grid)}")
    print("-" * 20)