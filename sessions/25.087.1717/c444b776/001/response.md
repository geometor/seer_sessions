```python
import numpy as np

"""
Identifies horizontal and/or vertical lines composed entirely of yellow (4) pixels. 
These lines act as axes of reflection.
If only a horizontal line exists, the pattern above the line is reflected vertically downwards.
If only a vertical line exists, the pattern to the left of the line is reflected horizontally to the right.
If both lines exist, the pattern in the top-left quadrant is reflected horizontally, vertically, and diagonally (combination of both reflections) into the other quadrants.
The yellow lines themselves and the original source pattern(s) are preserved.
"""

def find_horizontal_line(grid):
    """Finds the row index of a horizontal line of yellow pixels."""
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r, :] == 4):
            # Ensure it's a full line, not just yellow pixels within a pattern
            # Although the examples suggest full lines, this is a safer check
            is_full_line = True
            if r > 0 and np.any(grid[r-1, :] != 0) and np.any(grid[r-1, :] != 4):
                 # Check if row above has non-background colors other than yellow
                 pass # Potentially part of a larger shape, but task seems to use background separation
            if r < height - 1 and np.any(grid[r+1, :] != 0) and np.any(grid[r+1, :] != 4):
                 # Check if row below has non-background colors other than yellow
                 pass # Potentially part of a larger shape

            # For this task, simply checking if the row is all yellow seems sufficient based on examples
            return r
    return None

def find_vertical_line(grid):
    """Finds the column index of a vertical line of yellow pixels."""
    height, width = grid.shape
    for c in range(width):
        if np.all(grid[:, c] == 4):
             # Similarly, check if it's a full line if needed, but examples suggest clear lines
            return c
    return None

def transform(input_grid):
    """
    Reflects patterns across horizontal and/or vertical yellow lines.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    # Initialize output grid as a copy of the input
    output_grid = np.copy(grid_np)

    # Find the yellow lines
    hr = find_horizontal_line(grid_np)
    vc = find_vertical_line(grid_np)

    # --- Apply reflection logic ---

    if hr is not None and vc is not None:
        # Case 1: Both horizontal and vertical lines exist
        # Source region is top-left quadrant
        for r in range(hr):
            for c in range(vc):
                pixel_color = grid_np[r, c]
                if pixel_color != 4: # Don't reflect the reflection lines themselves if part of pattern
                    # Reflect horizontally to top-right
                    reflected_c_right = vc + (vc - c)
                    if 0 <= reflected_c_right < width:
                        output_grid[r, reflected_c_right] = pixel_color

                    # Reflect vertically to bottom-left
                    reflected_r_bottom = hr + (hr - r)
                    if 0 <= reflected_r_bottom < height:
                        output_grid[reflected_r_bottom, c] = pixel_color

                    # Reflect diagonally to bottom-right
                    if 0 <= reflected_r_bottom < height and 0 <= reflected_c_right < width:
                        output_grid[reflected_r_bottom, reflected_c_right] = pixel_color

    elif hr is not None:
        # Case 2: Only horizontal line exists
        # Source region is above the line
        for r in range(hr):
            for c in range(width):
                 pixel_color = grid_np[r, c]
                 if pixel_color != 4: # Avoid reflecting the line itself
                    # Reflect vertically downwards
                    reflected_r = hr + (hr - r)
                    if 0 <= reflected_r < height:
                         output_grid[reflected_r, c] = pixel_color

    elif vc is not None:
        # Case 3: Only vertical line exists
        # Source region is left of the line
         for r in range(height):
            for c in range(vc):
                 pixel_color = grid_np[r, c]
                 if pixel_color != 4: # Avoid reflecting the line itself
                    # Reflect horizontally to the right
                    reflected_c = vc + (vc - c)
                    if 0 <= reflected_c < width:
                         output_grid[r, reflected_c] = pixel_color

    # Case 4: No yellow lines found - output_grid remains a copy of input_grid

    # Convert numpy array back to list of lists
    return output_grid.tolist()
```