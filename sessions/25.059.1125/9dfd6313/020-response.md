# 9dfd6313 • 020 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all pixels that are not white (0).

2.  **Azure (8) Shift:** Every azure (8) pixel moves two columns to the right.

3.  **Red (2) Shift:** Every red (2) pixel moves two columns to the right.

4.  **Blue(1) and Gray(5) interaction**: The blue (1) pixel moves to the position of gray(5) pixel. The gray (5) pixel is also copied to where the blue(1) pixel started.

5.  **Gray (5) Diagonal (Except when interacting with Blue):** Gray (5) pixels that *aren't* involved in the blue interaction, will remain in their original positions.

6. **Background:** Pixels that are not occupied after these movements will be white (0).
"""

import numpy as np

def find_object(grid, color):
    positions = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                positions.append((i, j))
    return positions

def transform(input_grid):
    output_grid = np.zeros_like(input_grid)

    # Azure (8) Shift
    azure_positions = find_object(input_grid, 8)
    for pos in azure_positions:
        new_col = pos[1] + 2
        if new_col < output_grid.shape[1]:  # Ensure within bounds
          output_grid[pos[0], new_col] = 8

    # Red (2) Shift
    red_positions = find_object(input_grid, 2)
    for pos in red_positions:
        new_col = pos[1] + 2
        if new_col < output_grid.shape[1]:  # Ensure within bounds
          output_grid[pos[0], new_col] = 2
    
    # Blue(1) and Gray(5) interaction
    blue_positions = find_object(input_grid, 1)
    gray_positions = find_object(input_grid, 5)
    
    if blue_positions and gray_positions:
        blue_pos = blue_positions[0]
        gray_pos = gray_positions[0]

        # Move blue to gray's position
        output_grid[gray_pos[0], gray_pos[1]] = 1
        # Copy gray to blue's original position
        output_grid[blue_pos[0], blue_pos[1]] = 5

    # Gray (5) Diagonal (Except when interacting with Blue)
    # Find *all* gray positions, not just the first
    gray_positions = find_object(input_grid, 5)
    for gray_pos in gray_positions:
         # Only keep if it's not the one that interacted with blue
        if not (blue_positions and gray_positions and gray_pos == gray_positions[0]):
             output_grid[gray_pos[0], gray_pos[1]] = 5


    return output_grid
```
