"""
Transforms an input grid by modifying white objects based on interaction with 'trigger' pixels (green or gray). The type of trigger determines the modification rule.

1.  Initialize the output grid as a copy of the input grid.
2.  Find all green pixels and determine the set of unique rows containing them (`green_rows`).
3.  Find all distinct white objects (contiguous areas of white pixels using 8-way connectivity).
4.  **Check for Green Trigger:** If `green_rows` is not empty:
    a.  For each white object:
        i.  Determine the set of rows the object occupies (`white_rows`).
        ii. Find the rows where this object intersects with `green_rows` (`intersecting_rows`).
        iii. If `intersecting_rows` is not empty:
            1. Find the highest row index among the `intersecting_rows` (`highest_intersecting_row`).
            2. Find the rightmost column index occupied by any pixel in this object (`max_col`).
            3. Iterate through each pixel `(r, c)` of this white object:
                - If the pixel's row `r` is strictly less than `highest_intersecting_row`, change its color to orange (7) in the output grid.
                - Else if the pixel's column `c` is equal to `max_col`, change its color to magenta (6) in the output grid. (Orange takes precedence).
    b. Stop and return the modified output grid.
5.  **Check for Gray Trigger (only if no green trigger occurred):** If `green_rows` was empty:
    a.  Find all gray pixels and determine the set of unique rows containing them (`gray_rows`).
    b.  If `gray_rows` is not empty:
        i.  For each white object:
            1. Determine the set of rows the object occupies (`white_rows`).
            2. Find the rows where this object intersects with `gray_rows` (`intersecting_rows`).
            3. Calculate the object's width (difference between max and min column index + 1).
            4. If `intersecting_rows` is not empty AND the object's width is 2 or greater:
                - Find the leftmost column index occupied by any pixel in this object (`min_col`).
                - Iterate through each pixel `(r, c)` of this white object:
                    - If the pixel's column `c` is equal to `min_col`, change its color to magenta (6) in the output grid.
6.  **Final Output:** Return the output grid (which may be unchanged if no triggers applied, or modified by either the green or gray trigger logic).
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
                   representing the coordinates of pixels in a single object.
                   Returns an empty list if no objects are found.
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

            # i. Determine the set of rows the object occupies
            white_rows = {r for r, c in white_obj}
            
            # ii. Check if this white object's rows overlap with any green rows
            intersecting_rows = white_rows.intersection(green_rows)
            
            # iii. If there is an overlap (intersection is not empty)
            if intersecting_rows:
                # 1. Find the highest row index among the intersecting rows
                highest_intersecting_row = max(intersecting_rows)
                
                # 2. Find the maximum column index within this white object
                # Ensure the object is not empty before finding max col
                max_col = max(c for r, c in white_obj) 
                
                # 3. Iterate through each pixel belonging to this white object
                for r, c in white_obj:
                    # If the pixel's row is strictly above the highest intersecting row
                    if r < highest_intersecting_row:
                        # Change its color to orange (7)
                        output_grid[r, c] = 7
                    # Else if the pixel's column is the rightmost column of the object
                    # (This applies to pixels at or below the highest_intersecting_row)
                    elif c == max_col:
                         # Change its color to magenta (6)
                         # The 'elif' ensures orange takes precedence
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

            # 1. Find the set of rows occupied by this specific white object
            white_rows = {r for r, c in white_obj}
            
            # 2. Find rows where object intersects gray rows
            intersecting_rows = white_rows.intersection(gray_rows)
            
            # 3. Find min/max col and width of the white object
            white_cols = {c for r, c in white_obj}
            min_col = min(white_cols)
            max_col = max(white_cols)
            width = max_col - min_col + 1 # Calculate width

            # 4. Check if the object intersects with gray rows AND has a width >= 2
            if intersecting_rows and width >= 2:
                # Iterate through each pixel belonging to this white object
                for r, c in white_obj:
                    # If the pixel's column is the leftmost column of the object
                    if c == min_col:
                        # Change its color to magenta (6)
                        output_grid[r, c] = 6
                        
    # 6. Return the final grid. 
    # This will be the original grid if no triggers applied, 
    # or the grid modified by the gray trigger if it applied.
    return output_grid