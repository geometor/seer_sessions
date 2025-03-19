"""
1.  **Identify Regions:** Locate all contiguous regions of gray (5) pixels and white (0) pixels within the input grid.
2.  **Analyze Gray Pixel Context:** For each gray pixel, examine its surrounding pixels (up, down, left, right, and potentially diagonals). The transformation of a gray pixel to green depends on a more complex relationship with adjacent white pixels than simply counting them. It likely involves a concept of being "enclosed" or "influenced" by a specific configuration of white pixels. This configuration needs further investigation.
3. Analyze White Pixel Context: Determine if the context of a white pixel changes its color
4. **Transform other Pixels:** If a pixel is not a gray pixel or white pixel, it may change color based on its context.
5. Other colors remain unchanged, except in cases described in 3 and 4
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonal=False):
    """Gets the neighbors of a cell, optionally including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonal and (i != 0 and j != 0):  # Skip diagonals if not included
                continue
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col, grid[neighbor_row, neighbor_col]))
    return neighbors

def analyze_gray_pixel_context(grid, row, col):
    """Analyzes the context of a gray pixel to determine if it should turn green."""
    neighbors = get_neighbors(grid, row, col, include_diagonal=False)
    white_neighbors = [n for n in neighbors if n[2] == 0]
    num_white_neighbors = len(white_neighbors)
    
    # Initial rule (modified):  Check for "enclosure"
    if num_white_neighbors >= 2:  #At least two.  
      #More complex check can go here (like checking relative positions, not JUST count
      return True
      
    return False
    

def analyze_white_pixel_context(grid, row, col):
    """Analyzes context of white pixel to see if it changes"""
    # Placeholder - needs more logic based on observations from examples
    neighbors = get_neighbors(grid, row, col)
    
    for r, c, color in neighbors:
        if color == 1: # if a neighbor is blue, check for a swap
            return 1 # turn to blue
            
    return 0 # default to keep it as is

def analyze_other_pixel_context(grid, row, col):
    """Analyzes the context of non-gray, non-white pixel to see if color change"""
    neighbors = get_neighbors(grid, row, col)
    current_color = grid[row, col]

    for r, c, color in neighbors:
      if color == 0 and current_color == 1:
        return 0 # if current color is 1, and there is an adjacent white, turn to white

    return current_color

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Analyze and transform gray pixels
            if input_grid[row, col] == 5:
                if analyze_gray_pixel_context(input_grid, row, col):
                    output_grid[row, col] = 3
            # Analyze and transform white pixels
            elif input_grid[row, col] == 0:
                new_color = analyze_white_pixel_context(input_grid, row, col)
                output_grid[row,col] = new_color
            # Analyze and potentially transform other pixels
            else:
              new_color = analyze_other_pixel_context(input_grid, row, col)
              output_grid[row, col] = new_color

    return output_grid