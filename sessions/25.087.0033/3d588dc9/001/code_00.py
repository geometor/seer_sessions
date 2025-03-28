"""
Transforms an input grid based on the following rules:

1. Identify all white (0) objects (contiguous groups of pixels).
2. Check if any green (3) pixels exist in the input grid.
3. **If green pixels exist:**
   a. Determine the set of row indices occupied by any green pixel.
   b. For each white object that shares at least one row index with the green pixels:
      i. Find the maximum column index within that white object.
      ii. Change all pixels in that white object located at the maximum column index to magenta (6).
4. **If no green pixels exist, check if any gray (5) objects exist:**
   a. Determine the set of row indices occupied by any gray pixel (from any gray object).
   b. For each white object that:
      i. Shares at least one row index with the gray pixels, AND
      ii. Has a width of 2 or more columns (max_col - min_col + 1 >= 2):
         1. Find the minimum column index within that white object.
         2. Calculate the target column index as minimum column index + 1.
         3. Change all pixels in that white object located at the target column index to magenta (6).
5. If neither green pixels nor applicable gray objects (triggering a change in a white object) are found, the grid remains unchanged.
The output grid is initialized as a copy of the input grid, and modifications are applied directly to it.
"""

import numpy as np
from collections import deque

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of pixels in a single object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and (r, c) not in visited:
                current_object = set()
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object.add((curr_r, curr_c))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc

                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == target_color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                
                if current_object: # Ensure we only add non-empty objects
                    objects.append(current_object)
                    
    return objects

def get_pixel_locations(grid, target_color):
    """Finds all locations of a specific color."""
    return set(zip(*np.where(grid == target_color)))

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify white objects
    white_objects = find_objects(input_grid, 0)

    # 2. Identify green pixel locations
    green_pixels = get_pixel_locations(input_grid, 3)

    # 3. Check for Green Trigger
    if green_pixels:
        green_rows = {r for r, c in green_pixels}
        
        # 3.b. Iterate through white objects
        for white_obj in white_objects:
            white_rows = {r for r, c in white_obj}
            
            # 3.b.ii. Check row intersection
            if white_rows.intersection(green_rows):
                # 3.b.iii.1 Find max column index
                if not white_obj: continue # Skip empty object sets if any occurred
                max_col = -1
                for r, c in white_obj:
                    if c > max_col:
                        max_col = c
                
                # 3.b.iii.2 Change pixels at max_col to magenta
                for r, c in white_obj:
                    if c == max_col:
                        output_grid[r, c] = 6
        return output_grid # Return after processing green trigger

    # 4. Check for Gray Trigger (if no green found)
    gray_objects = find_objects(input_grid, 5)
    if gray_objects:
        all_gray_pixels = set().union(*gray_objects) # Combine pixels from all gray objects
        gray_rows = {r for r, c in all_gray_pixels}

        # 4.b. Iterate through white objects
        for white_obj in white_objects:
            if not white_obj: continue # Skip empty object sets

            white_rows = {r for r, c in white_obj}
            white_cols = {c for r, c in white_obj}
            min_col = min(white_cols)
            max_col = max(white_cols)
            width = max_col - min_col + 1

            # 4.b.i & 4.b.ii Check row intersection and width
            if white_rows.intersection(gray_rows) and width >= 2:
                # 4.b.ii.1 & 4.b.ii.2 Calculate target column
                target_col = min_col + 1

                # 4.b.ii.3 Change pixels at target_col to magenta
                for r, c in white_obj:
                    if c == target_col:
                        output_grid[r, c] = 6
                        
    # 5. Return the final grid
    return output_grid