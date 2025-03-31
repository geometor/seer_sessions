```python
import numpy as np
from collections import deque

"""
Identify the single contiguous block of non-white pixels in the input grid.
Determine its color and bounding box.
Create an output grid of the same dimensions, filled with the background color (white, 0).
Calculate the new top-left position for the object based on its color:
- If Azure (8), move horizontally to align with the right edge (new_col = grid_width - object_width), keeping the original row.
- If Yellow (4), move vertically to align with the bottom edge (new_row = grid_height - object_height), keeping the original column.
- If Magenta (6), move vertically to align with the top edge (new_row = 0), keeping the original column.
Copy the object's pixels from their original locations to the new calculated locations in the output grid.
"""

def find_object_properties(grid):
    """
    Finds the first contiguous non-background object in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (color, min_row, min_col, max_row, max_col, object_pixels)
               Returns None if no object is found.
               object_pixels is a list of (row, col) tuples.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    background_color = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    object_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                return color, min_r, min_c, max_r, max_c, object_pixels
    return None # No object found

def transform(input_grid):
    """
    Moves a single colored object within the grid based on its color.
    Azure (8) moves right, Yellow (4) moves down, Magenta (6) moves up.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Find the object and its properties
    object_info = find_object_properties(grid_np)

    # If no object is found, return the original grid (or an empty one)
    if object_info is None:
        # Per instructions, create a white grid of the same size
        return np.zeros_like(grid_np).tolist() 

    color, min_r, min_c, max_r, max_c, object_pixels = object_info
    obj_height = max_r - min_r + 1
    obj_width = max_c - min_c + 1

    # Initialize the output grid with the background color
    output_grid = np.zeros_like(grid_np)

    # Determine the new top-left position based on color
    new_min_r, new_min_c = min_r, min_c # Default to original position if color rule doesn't match
    if color == 8:  # Azure -> move right
        new_min_r = min_r
        new_min_c = width - obj_width
    elif color == 4: # Yellow -> move down
        new_min_r = height - obj_height
        new_min_c = min_c
    elif color == 6: # Magenta -> move up
        new_min_r = 0
        new_min_c = min_c
    # Add cases for other colors if needed, otherwise they stay put by default

    # Copy the object pixels to the new location in the output grid
    for r, c in object_pixels:
        # Calculate the pixel's position relative to the object's top-left corner
        rel_r = r - min_r
        rel_c = c - min_c
        # Calculate the new absolute position in the output grid
        new_r = new_min_r + rel_r
        new_c = new_min_c + rel_c
        # Ensure the new position is within bounds (should be if logic is correct)
        if 0 <= new_r < height and 0 <= new_c < width:
            output_grid[new_r, new_c] = color
        else:
            # This case should ideally not happen with the current rules
            print(f"Warning: Calculated pixel position ({new_r}, {new_c}) out of bounds.")


    # Convert the output grid back to a list of lists
    return output_grid.tolist()
```