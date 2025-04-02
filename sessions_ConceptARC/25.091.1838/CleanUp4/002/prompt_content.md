
Previous Code:
```python
import numpy as np
from collections import deque

"""
This function transforms an input grid based on one of three conditional rules or returns the grid unchanged if no rule applies.

Rule 1: If the grid contains both azure (8) and green (3) pixels, and at least one azure pixel is adjacent (orthogonally or diagonally) to a green pixel, then change all azure pixels to white (0) and change all green pixels that were adjacent to an azure pixel to white (0).

Rule 2: If Rule 1 does not apply, find all contiguous non-white objects. If there are 4 or more distinct objects with a size (pixel count) of 10 or more, keep only the 4 largest objects (including ties for the 4th position) and set all other pixels to white (0).

Rule 3: If neither Rule 1 nor Rule 2 applies, and the grid contains yellow (4) pixels, change all yellow pixels to green (3).

Default: If none of the above conditions are met, return the input grid unchanged.
"""

def get_neighbors(r, c, height, width, connectivity=8):
    """ Gets valid neighbor coordinates for a given cell (r, c). """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if connectivity == 4 and abs(dr) + abs(dc) != 1: # Skip diagonals for 4-connectivity
                 continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_objects(grid, ignore_color=0):
    """ Finds all contiguous objects of colors other than ignore_color. """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = [] # List to store (color, size, pixel_coords_set)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != ignore_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_pixels.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    # Use 4-connectivity for object definition as per ARC standard
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=4):
                        if grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            obj_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_pixels:
                    objects.append({'color': color, 'size': len(obj_pixels), 'pixels': obj_pixels})
    return objects


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    output_grid = grid.copy() # Start with a copy

    # --- Check Rule 1 Condition ---
    has_azure = np.any(grid == 8)
    has_green = np.any(grid == 3)
    adjacency_found = False
    green_to_remove = set()

    if has_azure and has_green:
        azure_pixels = np.argwhere(grid == 8)
        for r_az, c_az in azure_pixels:
            # Check 8-connectivity neighbors
            for nr, nc in get_neighbors(r_az, c_az, height, width, connectivity=8):
                if grid[nr, nc] == 3:
                    adjacency_found = True
                    green_to_remove.add((nr, nc))
            if adjacency_found: # Optimization: can stop checking neighbors for this azure pixel
                 # but need to continue checking *all* azure pixels to find *all* adjacent greens
                 pass

    # --- Apply Rule 1 if condition met ---
    if adjacency_found:
        # Find all azure pixels again (or use azure_pixels list if kept)
        azure_coords = np.where(grid == 8)
        output_grid[azure_coords] = 0 # Set all azure to white

        # Set adjacent green pixels to white
        for r, c in green_to_remove:
             output_grid[r, c] = 0
        return output_grid.tolist() # Rule 1 applied

    # --- Check Rule 2 Condition ---
    all_objects = find_objects(grid, ignore_color=0)
    large_objects = [obj for obj in all_objects if obj['size'] >= 10]

    if len(large_objects) >= 4:
        # --- Apply Rule 2 ---
        # Sort all non-white objects by size descending
        all_objects.sort(key=lambda x: x['size'], reverse=True)

        # Determine the size threshold (size of the 4th largest object)
        if len(all_objects) >= 4:
             size_threshold = all_objects[3]['size']
        else:
             # Should not happen based on len(large_objects)>=4 check, but handle defensively
             size_threshold = 0 

        # Select objects >= threshold size
        objects_to_keep = [obj for obj in all_objects if obj['size'] >= size_threshold]

        # Create new grid and draw kept objects
        output_grid = np.full_like(grid, 0) # Fill with white
        for obj in objects_to_keep:
            color = obj['color']
            for r, c in obj['pixels']:
                output_grid[r, c] = color
        return output_grid.tolist() # Rule 2 applied

    # --- Check Rule 3 Condition ---
    has_yellow = np.any(grid == 4)

    # --- Apply Rule 3 if condition met ---
    if has_yellow:
        yellow_coords = np.where(grid == 4)
        output_grid[yellow_coords] = 3 # Change yellow to green
        return output_grid.tolist() # Rule 3 applied

    # --- Default Case ---
    # If none of the rules applied, return the original grid (or the initial copy)
    return output_grid.tolist()

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0
8 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 3 3 3 3 0 0 0 3 0 0 0 8 3 0
0 0 3 0 0 3 0 0 0 3 0 8 0 0 3 0
0 0 3 0 8 3 0 0 0 3 0 0 0 0 3 0
0 0 3 3 3 3 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 8 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 3 8 0 0 0
3 8 3 8 0 3 0 0 0 0 0 3 8 0 0 0
8 0 3 8 0 3 0 8 0 8 0 3 0 0 0 0
3 3 3 0 0 3 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 8 0 0
0 0 8 0 0 0 0 0 0 0 0 8 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 3 3 3 3 0 0 0 3 0 0 0 0 3 0
0 0 3 0 0 3 0 0 0 3 0 0 0 0 3 0
0 0 3 0 0 3 0 0 0 3 0 0 0 0 3 0
0 0 3 3 3 3 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 3 0 0 0 0
3 3 3 0 0 3 0 0 0 0 0 3 0 0 0 0
3 0 3 0 0 3 0 0 0 0 0 3 0 0 0 0
3 3 3 0 0 3 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 3 0 0 0 0 0 0 3 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.75

## Example 2:
Input:
```
0 0 7 0 1 0 0 0 0 0 0
6 0 0 0 0 0 8 8 8 8 8
0 2 2 2 2 0 8 6 0 0 8
0 2 0 0 2 0 8 0 0 0 8
0 2 0 4 2 0 8 0 0 4 8
0 2 0 0 2 0 8 8 8 8 8
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 1 4 4 4 4
0 0 0 1 1 0 4 0 0 0 4
0 1 6 6 6 6 4 0 7 0 4
7 0 6 0 0 6 4 0 6 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 0 4 6 4 0 0 0 4
4 0 6 6 6 6 4 0 0 0 4
0 0 0 0 0 0 4 4 4 4 4
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8
0 2 2 2 2 0 8 0 0 0 8
0 2 0 0 2 0 8 0 0 0 8
0 2 0 0 2 0 8 0 0 0 8
0 2 0 0 2 0 8 8 8 8 8
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4
0 0 0 0 0 0 4 0 0 0 4
0 0 6 6 6 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 6 6 6 4 0 0 0 4
0 0 0 0 0 0 4 4 4 4 4
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8
0 2 2 2 2 0 8 0 0 0 8
0 2 0 0 2 0 8 0 0 0 8
0 2 0 0 2 0 8 0 0 0 8
0 2 0 0 2 0 8 8 8 8 8
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 4 0 0 0 4
0 0 6 6 6 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 0 0 6 4 0 0 0 4
0 0 6 6 6 6 4 0 0 0 4
0 0 0 0 0 0 4 4 4 4 4
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.2121212121212182

## Example 3:
Input:
```
3 4 3 3 3 3
3 3 2 2 2 2
3 3 2 3 4 2
3 4 2 3 3 2
3 3 2 2 2 2
4 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3
3 3 2 2 2 2
3 3 2 3 3 2
3 3 2 3 3 2
3 3 2 2 2 2
3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3
3 3 2 2 2 2
3 3 2 3 3 2
3 3 2 3 3 2
3 3 2 2 2 2
3 3 3 3 3 3
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
