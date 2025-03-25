"""
1.  **Identify Regions:** Divide the input grid into distinct regions. A region is a group of connected pixels of the same color. Pixels are considered connected if they are adjacent horizontally, vertically, or diagonally.
2.  **Identify Boundary Pixels:** A boundary pixel is a pixel that belongs to a region and is directly adjacent (horizontally, vertically, or diagonally) to a pixel of a *different* color. White pixels act act as boundary _except_ when the white pixels make a straight line between regions.
3. **Line Completion Rule**: Examine the boundaries between colored regions (excluding white, except where a white line separates). If a pixel at the boundary, when changed to azure (8), would *complete a continuous, straight line of azure* of length greater than one, then make the transformation based on these additional constraints:
   * If the changed pixel has only one adjacent non-white neighbor in the target region, it changes to azure (8).
   * If the changed pixel has 3 or more adjacent non-white neighbors in the adjacent region, _and_ is part of the other color region, it changes to azure (8).

4. Never change the color of a white (0) pixel.
"""

import numpy as np

def get_neighbors(grid, r, c, include_white=False):
    """Gets the valid neighbors of a pixel, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the pixel itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if include_white or grid[nr, nc] != 0:
                  neighbors.append((nr, nc))
    return neighbors

def would_complete_line(grid, r, c, color=8):
    """
    Checks if changing the pixel at (r, c) to 'color' would complete a line.
    """
    rows, cols = grid.shape
    
    # Check horizontal line
    if c > 0 and c < cols - 1 and grid[r, c-1] == color and grid[r, c+1] == color:
        return True
    # Check vertical line
    if r > 0 and r < rows - 1 and grid[r-1, c] == color and grid[r+1, c] == color:
        return True
      
    #check diagonal line
    if r > 0 and r < rows -1 and c > 0 and c < cols - 1:

        if grid[r-1,c-1] == color and grid[r+1,c+1] == color:
            return True

        if grid[r-1,c+1] == color and grid[r+1, c-1] == color:
            return True

    return False

def transform(input_grid):
    """
    Transforms the input grid by changing the color of boundary pixels.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through each pixel to find boundary pixels
    for r in range(rows):
        for c in range(cols):
            current_color = input_grid[r, c]

            # Skip white pixels
            if current_color == 0:
                continue

            neighbors = get_neighbors(input_grid, r, c)
            for nr, nc in neighbors:
                neighbor_color = input_grid[nr, nc]

                # Check for boundary and color difference
                if neighbor_color != current_color and neighbor_color != 0:
                    # Check Line Completion Rule
                    if would_complete_line(output_grid, r, c):
                        
                        non_white_neighbors_target = 0
                        for nnr, nnc in get_neighbors(input_grid,r,c, include_white = False):
                            if input_grid[nnr,nnc] == current_color:
                                non_white_neighbors_target += 1

                        non_white_neighbors_adjacent = 0
                        for nnr, nnc in get_neighbors(input_grid, r,c, include_white=False):
                            if input_grid[nnr,nnc] == neighbor_color:
                                non_white_neighbors_adjacent+=1
                            
                        if non_white_neighbors_target == 1:
                            output_grid[r,c] = 8

                        elif non_white_neighbors_adjacent >=3 and input_grid[r,c] != current_color:
                           output_grid[r,c] = 8


    return output_grid