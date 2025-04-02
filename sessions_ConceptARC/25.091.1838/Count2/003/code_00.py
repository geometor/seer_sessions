import numpy as np

"""
Transformation Rule:

1. Identify all blue pixels (color 1) in the input grid.
2. For each blue pixel, count its eight neighbors (adjacent and diagonal). Neighbors outside the grid boundaries are counted as non-blue.
3. A blue pixel is considered a "vertex" if it has 6 or more non-blue neighbors.
4. Count the total number of such vertices (N).
5. Create a new output grid with dimensions 1 row and N columns.
6. Fill all cells of this output grid with the orange color (7).
"""

def count_non_blue_neighbors(grid, r, c):
    """
    Counts the number of non-blue (not color 1) neighbors for a pixel at (r, c).
    Neighbors include 8 directions (adjacent and diagonal).
    Cells outside the grid boundary are considered non-blue.
    """
    height, width = grid.shape
    non_blue_count = 0
    # Iterate through the 8 neighbors defined by offsets dr and dc
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue
                
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is outside the grid boundaries
            if not (0 <= nr < height and 0 <= nc < width):
                non_blue_count += 1
            # Check if neighbor is inside the grid and not blue (color 1)
            elif grid[nr, nc] != 1:
                non_blue_count += 1
                
    return non_blue_count

def transform(input_grid):
    """
    Transforms the input grid by finding blue pixels, counting those that are 
    "vertices" (defined as having >= 6 non-blue neighbors), and creating an 
    orange output row of length equal to the vertex count.
    
    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The output grid (a single row) as a list of lists.
                       Returns [[7]] * N where N is the vertex count.
                       Returns an empty list of lists [[]] if no vertices are found (N=0).
    """
    # Convert input list of lists to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Initialize vertex counter
    vertex_count = 0
    
    # Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is blue (color 1)
            if grid[r, c] == 1:
                # Count its non-blue neighbors
                neighbors_count = count_non_blue_neighbors(grid, r, c)
                # Check if the count meets the vertex threshold (>= 6)
                if neighbors_count >= 6:
                    # If it's a vertex, increment the counter
                    vertex_count += 1
            
    # Create the output grid based on the vertex count
    if vertex_count > 0:
      # Create a 1xN numpy array filled with orange (7)
      output_grid_np = np.full((1, vertex_count), 7, dtype=int)
      # Convert numpy array back to list of lists
      output_grid = output_grid_np.tolist()
    else:
      # Handle the case of 0 vertices: return a 1x0 grid representation [[ ]]
      output_grid = [[]] 

    return output_grid