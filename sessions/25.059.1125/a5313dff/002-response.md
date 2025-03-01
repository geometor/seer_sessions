# a5313dff • 002 • example_3 • investigate_coder

---
```python
"""
Identifies a closed shape defined by red (2) pixels and changes the color of all pixels within that shape to blue (1), keeping the shape outline.
"""

import numpy as np

def find_red_shape(grid):
    # Find all red pixels
    red_pixels = np.argwhere(grid == 2)
    
    # Assume shape pixels themselves are the outline, this will be validated by flood fill
    return set(map(tuple, red_pixels))


def flood_fill(grid, start_pixel, fill_color):
    """
    Performs a flood fill operation on the grid, starting from a given pixel.
    Only fills pixels within the outline and does NOT fill diagonally, only
    pixels connected orthagonally.
    
    Returns both changed grid and pixels that were impacted.

    Args:
    grid: 2d numpy array
    start_pixel: starting position tuple, should not be part of the perimeter.
    fill_color: new value to fill with
    """
    rows, cols = grid.shape
    visited = set()
    q = [start_pixel]

    # Use copy so that the passed array is not changed
    new_grid = grid.copy()
    changes = []

    while q:
        r, c = q.pop(0)
        if (r, c) in visited:
            continue
        visited.add((r, c))

        # only replace points inside, so do not run on red/outline color
        if grid[r, c] != 2:
            changes.append(((r,c), grid[r, c], fill_color))
            new_grid[r, c] = fill_color  # Change the color of the current pixel
        

            # Check neighbors (up, down, left, right), but not diagonals
            neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for nr, nc in neighbors:
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    q.append((nr, nc))
    return new_grid, changes

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation
    grid = np.array(input_grid)

    # Find the red shape (contiguous region of red pixels)
    red_shape_pixels = find_red_shape(grid)

    # find seed fill pixel by getting the bounding rect of the red pixels
    min_r = min(p[0] for p in red_shape_pixels)
    max_r = max(p[0] for p in red_shape_pixels)
    min_c = min(p[1] for p in red_shape_pixels)
    max_c = max(p[1] for p in red_shape_pixels)

    # seed must be inside so add 1
    start_pixel = (min_r + 1, min_c + 1)

    # Perform flood fill to change the color of enclosed pixels to blue (1)
    # if outside/zero get's filled - it's a bad outline, do nothing?
    
    output_grid, changes = flood_fill(grid, start_pixel, 1)
    
    return output_grid.tolist()
```
