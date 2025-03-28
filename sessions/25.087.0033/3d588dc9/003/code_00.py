import numpy as np
from collections import deque

"""
Transforms an input grid based on the following rules:

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the locations of all green pixels (color 3) and create a set of unique row indices containing green pixels (`green_rows`).
3.  Identify all distinct white objects (contiguous areas of color 0, using 8-way connectivity).
4.  **Green Trigger Check:** If `green_rows` is not empty:
    a.  For each white object:
        i.  Find the set of row indices occupied by the object (`white_rows`).
        ii. Check if `white_rows` intersects with `green_rows`. Let the intersection be `intersecting_rows`.
        iii. If `intersecting_rows` is not empty:
            1.  Find the maximum column index (`max_col`) within this white object.
            2.  Identify the highest row index from `intersecting_rows` (`highest_intersecting_row = max(intersecting_rows)`).
            3.  Iterate through all pixels `(r, c)` belonging to this white object:
                *   If the pixel's row `r` is strictly less than `highest_intersecting_row`, change its color to orange (7) in the output grid.
                *   Else if the pixel's column `c` equals `max_col`, change its color to magenta (6) in the output grid.
    b.  Return the output grid (processing stops after the green trigger).
5.  **Gray Trigger Check:** If `green_rows` is empty:
    a.  Identify the locations of all gray pixels (color 5) and create a set of unique row indices containing gray pixels (`gray_rows`).
    b.  If `gray_rows` is not empty:
        i.  For each white object found in step 3:
            1.  Find the set of row indices occupied by the object (`white_rows`).
            2.  Find the minimum column index (`min_col`) and maximum column index (`max_col`) within this white object. Calculate its `width = max_col - min_col + 1`.
            3.  Check if `white_rows` intersects with `gray_rows` AND `width` is 2 or greater.
            4.  If both conditions are true:
                *   Iterate through all pixels `(r, c)` belonging to this white object:
                    *   If the pixel's column `c` equals `min_col`, change its color to magenta (6) in the output grid.
6.  **No Trigger:** If neither the green trigger nor the gray trigger applied, the output grid remains identical to the input grid.
7.  Return the modified output grid.
"""

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in the grid using 8-way connectivity.

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
    """Finds all locations (set of (row, col) tuples) of a specific color."""
    return set(zip(*np.where(grid == target_color)))

def transform(input_grid):
    # 1. Initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Identify green pixel locations and rows
    green_pixels = get_pixel_locations(input_grid, 3)
    green_rows = {r for r, c in green_pixels}

    # 3. Identify white objects
    white_objects = find_objects(input_grid, 0)

    # 4. Green Trigger Check
    if green_rows:
        # a. Iterate through white objects
        for white_obj in white_objects:
            if not white_obj: continue # Skip empty object sets if any occurred

            white_coords = list(white_obj)
            white_rows = {r for r, c in white_coords}
            
            # ii. Check for intersection with green rows
            intersecting_rows = white_rows.intersection(green_rows)
            
            # iii. If intersection exists
            if intersecting_rows:
                # 1. Find max column
                max_col = -1
                for r, c in white_coords:
                    if c > max_col:
                        max_col = c
                
                # 2. Find highest intersecting row
                highest_intersecting_row = max(intersecting_rows)
                
                # 3. Iterate through object pixels and apply changes
                for r, c in white_coords:
                    if r < highest_intersecting_row:
                        # Change pixels strictly above the highest intersection to orange
                        output_grid[r, c] = 7
                    elif c == max_col:
                         # Change pixels in the max column (at or below highest intersection) to magenta
                         # The 'elif' ensures orange takes precedence if a pixel met both conditions hypothetically
                         # (though geometrically unlikely for max_col to be above intersection row)
                        output_grid[r, c] = 6
                        
        # b. Return after processing green trigger
        return output_grid 

    # 5. Gray Trigger Check (only if no green found)
    # a. Identify gray pixel locations and rows
    gray_pixels = get_pixel_locations(input_grid, 5)
    gray_rows = {r for r, c in gray_pixels}

    # b. If gray rows exist
    if gray_rows:
        # i. Iterate through white objects
        for white_obj in white_objects:
            if not white_obj: continue # Skip empty object sets

            white_coords = list(white_obj)
            white_rows = {r for r, c in white_coords}
            
            # 2. Find min/max col and width
            if not white_coords: continue # Should not happen if find_objects is correct
            white_cols = {c for r, c in white_coords}
            min_col = min(white_cols)
            max_col = max(white_cols)
            width = max_col - min_col + 1

            # 3. Check intersection and width condition
            if white_rows.intersection(gray_rows) and width >= 2:
                # 4. If conditions met, change min_col pixels to magenta
                for r, c in white_coords:
                    if c == min_col:
                        output_grid[r, c] = 6
                        
    # 6 & 7. Return the final grid (either modified by gray trigger or unchanged)
    return output_grid