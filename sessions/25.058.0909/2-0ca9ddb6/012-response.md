# 2-0ca9ddb6 • 012 • refine_coder

---
```python
"""
1.  **Identify Key Pixels:** Locate all blue (1), red (2), and azure (8) pixels within the input grid.

2.  **Conditional Orange Placement:**
    *   Examine *specific* neighboring cells of blue and red pixels. The exact neighbors to check (e.g., only to the right of red, only to the left of blue) *must* be determined by carefully observing *all* training examples.
    *   If the specific neighboring cell is white (0), change it to orange (7).

3.  **Conditional Yellow Placement:**
    *   For each pair of blue (1) and azure (8) pixels:
        *   Determine if they are aligned either vertically (same column) or horizontally (same row).
        *   If they are aligned, count the number of white (0) pixels between them.
        *   *Only* if the count of white pixels is *greater than 2*, fill the intervening cells with yellow (4).
        * If there are fewer than 3 white pixels, do nothing.

4. **Preservation of Input:** Any input colors not explicitly modified by the above rules should remain in their original locations and colors in the output.

5.  **No-op Cases:** If there are no pixels to transform, the output grid will be identical to the input grid.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the positions of pixels of a specific color."""
    return np.argwhere(grid == color)

def get_specific_neighbors(grid, row, col, color):
    """Gets specific neighbors based on the color of the pixel."""
    rows, cols = grid.shape
    neighbors = []
    
    if color == 1:  # Blue - Check right
        if col + 1 < cols:
            neighbors.append((row, col + 1))
    elif color == 2:  # Red - Check left
        if col - 1 >= 0:
            neighbors.append((row, col - 1))
    return neighbors
            

def count_empty_cells_between(grid, pos1, pos2):
    """Counts empty cells between two positions in the same row or column."""
    if pos1[0] == pos2[0]:  # Same row
        start = min(pos1[1], pos2[1]) + 1
        end = max(pos1[1], pos2[1])
        return np.sum(grid[pos1[0], start:end] == 0)
    elif pos1[1] == pos2[1]:  # Same column
        start = min(pos1[0], pos2[0]) + 1
        end = max(pos1[0], pos2[0])
        return np.sum(grid[start:end, pos1[1]] == 0)
    else:
        return -1  # Not in the same row or column

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find pixels of color 1, 2 and 8
    one_positions = find_pixels_by_color(input_grid, 1)
    two_positions = find_pixels_by_color(input_grid, 2)
    eight_positions = find_pixels_by_color(input_grid, 8)

    # Add orange (7) around 1s and 2s based on specific neighbors
    for pos in one_positions:
        for r, c in get_specific_neighbors(input_grid, pos[0], pos[1], 1):
            if output_grid[r, c] == 0:
                output_grid[r, c] = 7

    for pos in two_positions:
         for r, c in get_specific_neighbors(input_grid, pos[0], pos[1], 2):
            if output_grid[r, c] == 0:
                output_grid[r, c] = 7
    

    # Add yellow (4) between 1s and 8s
    for one_pos in one_positions:
        for eight_pos in eight_positions:
            empty_count = count_empty_cells_between(input_grid, one_pos, eight_pos)
            if empty_count >= 3:
                if one_pos[0] == eight_pos[0]:  # Same row
                    start = min(one_pos[1], eight_pos[1]) + 1
                    end = max(one_pos[1], eight_pos[1])
                    output_grid[one_pos[0], start:end] = 4
                elif one_pos[1] == eight_pos[1]:  # Same column
                    start = min(one_pos[0], eight_pos[0]) + 1
                    end = max(one_pos[0], eight_pos[0])
                    output_grid[start:end, one_pos[1]] = 4

    return output_grid
```

