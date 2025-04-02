```python
import numpy as np
from skimage import measure

"""
Transforms the input grid based on blue objects (color 1) against a yellow background (color 4).
For each distinct blue object:
1. Identifies yellow pixels adjacent (orthogonally or diagonally) to the blue object.
2. Partitions these adjacent yellow pixels into two groups:
    a. 'Frame': Those adjacent yellow pixels that are also adjacent (orthogonally or diagonally) to at least one yellow pixel *not* adjacent to the current blue object. These frame pixels are colored red (2).
    b. 'Fill': Those adjacent yellow pixels that are *not* 'Frame' pixels.
3. Colors the 'Fill' pixels based on their adjacency to the 'Frame':
    a. If a 'Fill' pixel is adjacent (orthogonally or diagonally) to any 'Frame' pixel (now colored red), it's colored azure (8).
    b. Otherwise, it's colored magenta (6).
4. The original blue object pixels and the rest of the yellow background pixels remain unchanged.
"""

def _get_neighbors(r, c, height, width, include_diagonal=True):
    """ Gets valid neighbor coordinates for a given cell. """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if not include_diagonal and abs(dr) + abs(dc) > 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def _find_objects(grid, color):
    """ Finds connected components of a specific color. """
    binary_grid = (grid == color).astype(int)
    labeled_grid, num_labels = measure.label(binary_grid, connectivity=2, background=0, return_num=True) # connectivity=2 means diagonal connections are included
    
    objects = []
    for i in range(1, num_labels + 1):
        coords = set(map(tuple, np.argwhere(labeled_grid == i)))
        objects.append(coords)
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Define colors
    background_color = 4
    object_color = 1
    frame_color = 2
    outer_fill_color = 8
    inner_fill_color = 6

    # Find all blue objects
    blue_objects = _find_objects(input_grid, object_color)
    
    # Get coordinates of all yellow pixels
    all_yellow_coords = set(map(tuple, np.argwhere(input_grid == background_color)))

    for blue_object_coords in blue_objects:
        # 1. Find yellow pixels adjacent to the current blue object
        adjacent_to_blue_coords = set()
        for r, c in blue_object_coords:
            neighbors = _get_neighbors(r, c, height, width, include_diagonal=True)
            for nr, nc in neighbors:
                 adjacent_to_blue_coords.add((nr, nc))

        adjacent_yellow_coords = {
            (r, c) for r, c in adjacent_to_blue_coords 
            if input_grid[r, c] == background_color
        }

        # 2. Find yellow pixels NOT adjacent to the current blue object
        non_adjacent_to_current_blue_yellow_coords = all_yellow_coords - adjacent_yellow_coords

        # 3. Determine Frame pixels
        actual_frame_coords = set()
        for yr, yc in adjacent_yellow_coords:
            is_frame = False
            neighbors = _get_neighbors(yr, yc, height, width, include_diagonal=True)
            for nr, nc in neighbors:
                if (nr, nc) in non_adjacent_to_current_blue_yellow_coords:
                    is_frame = True
                    break
            if is_frame:
                actual_frame_coords.add((yr, yc))

        # 4. Determine Fill pixels
        fill_coords = adjacent_yellow_coords - actual_frame_coords

        # 5. Color Frame pixels in the output grid
        for r, c in actual_frame_coords:
            output_grid[r, c] = frame_color

        # 6. Color Fill pixels in the output grid
        for r, c in fill_coords:
            is_adjacent_to_frame = False
            neighbors = _get_neighbors(r, c, height, width, include_diagonal=True)
            # Check adjacency against the *final* frame coordinates
            for nr, nc in neighbors:
                 # We check against actual_frame_coords, not the output_grid's current state
                 # because multiple objects might interact otherwise.
                 if (nr, nc) in actual_frame_coords: 
                    is_adjacent_to_frame = True
                    break
            
            if is_adjacent_to_frame:
                output_grid[r, c] = outer_fill_color # Azure
            else:
                output_grid[r, c] = inner_fill_color # Magenta

    return output_grid
```