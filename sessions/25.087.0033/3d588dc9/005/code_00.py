"""
Transforms an input grid based on identifying 'trigger' pixels (green or gray) and modifying specific white objects that interact with these triggers.

The transformation follows these rules:

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
                *   Else if the pixel's column `c` equals `max_col`, change its color to magenta (6) in the output grid. (Orange takes precedence if conditions overlap).
    b.  Return the output grid immediately after processing all white objects under the green trigger.

5.  **Gray Trigger Check:** If `green_rows` is empty (meaning the green trigger did not activate):
    a.  Identify the locations of all gray pixels (color 5) and create a set of unique row indices containing gray pixels (`gray_rows`).
    b.  If `gray_rows` is not empty:
        i.  For each white object found in step 3:
            1.  Find the set of row indices occupied by the object (`white_rows`).
            2.  Find the minimum column index (`min_col`) and maximum column index (`max_col`) within this white object. Calculate its `width = max_col - min_col + 1`.
            3.  Check if `white_rows` intersects with `gray_rows` AND the object's `width` is 2 or greater.
            4.  If both conditions are true:
                *   Iterate through all pixels `(r, c)` belonging to this white object:
                    *   If the pixel's column `c` equals `min_col`, change its color to magenta (6) in the output grid.

6.  **No Trigger:** If neither the green trigger nor the gray trigger applied (either no green/gray pixels, or no white objects met the trigger conditions), the output grid remains identical to the input grid.
7.  Return the final output grid.
"""

import numpy as np
from collections import deque

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in the grid using 8-way connectivity.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of pixels in a single object. Returns an empty list if no objects are found.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If the pixel is the target color and hasn't been visited yet
            if grid[r, c] == target_color and (r, c) not in visited:
                current_object = set()
                # Use a queue for Breadth-First Search (BFS)
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object.add((curr_r, curr_c))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            # Skip the center pixel itself
                            if dr == 0 and dc == 0:
                                continue
                            
                            nr, nc = curr_r + dr, curr_c + dc

                            # Check if the neighbor is within grid bounds
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # Check if the neighbor is the target color and not visited
                                if grid[nr, nc] == target_color and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    q.append((nr, nc))
                
                # Add the found object to the list if it's not empty
                if current_object: 
                    objects.append(current_object)
                    
    return objects

def get_pixel_locations(grid, target_color):
    """Finds all locations (set of (row, col) tuples) of a specific color."""
    # np.where returns a tuple of arrays (one for rows, one for columns)
    # zip pairs them up into (row, col) tuples
    # set creates a set of these unique tuples
    return set(zip(*np.where(grid == target_color)))

def transform(input_grid):
    """
    Applies the transformation logic based on green or gray triggers affecting white objects.
    """
    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Identify green pixel locations and the rows they occupy
    green_pixels = get_pixel_locations(input_grid, 3) # color 3 = green
    green_rows = {r for r, c in green_pixels} # Extract unique row indices

    # 3. Identify all distinct white objects (color 0)
    white_objects = find_objects(input_grid, 0) # color 0 = white

    # 4. Green Trigger Check: Does the grid contain any green pixels?
    if green_rows:
        # a. Iterate through each identified white object
        for white_obj in white_objects:
            # Ensure the object set is not empty (precautionary)
            if not white_obj: 
                continue 

            # Convert set to list for easier indexing if needed, though set ops are efficient
            white_coords = list(white_obj) 
            # Find the set of rows occupied by this specific white object
            white_rows = {r for r, c in white_coords}
            
            # ii. Check if this white object's rows overlap with any green rows
            intersecting_rows = white_rows.intersection(green_rows)
            
            # iii. If there is an overlap (intersection is not empty)
            if intersecting_rows:
                # 1. Find the maximum column index within this white object
                max_col = -1 
                # This could be done more efficiently: max_col = max(c for r, c in white_obj)
                for r, c in white_coords:
                    if c > max_col:
                        max_col = c
                
                # 2. Find the highest row index among the intersecting rows
                highest_intersecting_row = max(intersecting_rows)
                
                # 3. Iterate through each pixel belonging to this white object
                for r, c in white_coords:
                    # If the pixel's row is strictly above the highest intersecting row
                    if r < highest_intersecting_row:
                        # Change its color to orange (7)
                        output_grid[r, c] = 7
                    # Else if the pixel's column is the rightmost column of the object
                    # (This applies to pixels at or below the highest_intersecting_row)
                    elif c == max_col:
                         # Change its color to magenta (6)
                         # The 'elif' ensures orange takes precedence if a pixel met both conditions
                        output_grid[r, c] = 6
                        
        # b. Return the modified grid immediately after green trigger processing
        return output_grid 

    # 5. Gray Trigger Check: This part only runs if 'green_rows' was empty
    # a. Identify gray pixel locations and the rows they occupy
    gray_pixels = get_pixel_locations(input_grid, 5) # color 5 = gray
    gray_rows = {r for r, c in gray_pixels} # Extract unique row indices

    # b. If the grid contains any gray pixels
    if gray_rows:
        # i. Iterate through each identified white object
        for white_obj in white_objects:
            # Ensure the object set is not empty
            if not white_obj: 
                continue 

            white_coords = list(white_obj)
            # Find the set of rows occupied by this specific white object
            white_rows = {r for r, c in white_coords}
            
            # 2. Find min/max col and width of the white object
            if not white_coords: # Should not happen if find_objects is correct, but safe check
                 continue
            white_cols = {c for r, c in white_coords}
            min_col = min(white_cols)
            max_col = max(white_cols)
            width = max_col - min_col + 1 # Calculate width based on min/max columns

            # 3. Check if the object intersects with gray rows AND has a width >= 2
            if white_rows.intersection(gray_rows) and width >= 2:
                # 4. If both conditions are met
                # Iterate through each pixel belonging to this white object
                for r, c in white_coords:
                    # If the pixel's column is the leftmost column of the object
                    if c == min_col:
                        # Change its color to magenta (6)
                        output_grid[r, c] = 6
                        
    # 6 & 7. Return the final grid. 
    # This will be the original grid if no triggers applied, 
    # or the grid modified by the gray trigger if it applied.
    return output_grid