# a79310a0 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** a 2x2 square of azure (8) pixels in the input grid.
2.  **Locate** the position of this 2x2 square.
3.  **Create** an output grid identical to the input grid.
4. **Move** one row down from square from the original position.
5.  **Change** the color of the 2x2 square in the new position in the output grid to red (2).
6.  **Keep** all other pixels in the output grid the same as the input grid (white/0).
"""

import numpy as np

def find_square(grid, size, color):
    """Finds the top-left coordinates of a square of given size and color."""
    rows, cols = grid.shape
    for i in range(rows - size + 1):
        for j in range(cols - size + 1):
            if np.all(grid[i:i+size, j:j+size] == color):
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Define the size and color of the square to search for
    size = 2
    color = 8
    
    # Find the top-left corner of the square
    square_pos = find_square(input_grid, size, color)
    
    if square_pos:
        # Calculate new position (move one row down)
        new_row = square_pos[0] + 1
        new_col = square_pos[1]

        # Change original square to white
        output_grid[square_pos[0]:square_pos[0]+size, square_pos[1]:square_pos[1]+size] = 0


        # Check boundaries before moving
        if new_row + size <= output_grid.shape[0]:
           # Change the color of the square at the new position to red (2)
            output_grid[new_row:new_row+size, new_col:new_col+size] = 2
    
    return output_grid
```
