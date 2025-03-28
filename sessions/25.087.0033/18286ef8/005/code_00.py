import numpy as np

"""
Transforms the input grid based on the following rule:
1. Initialize: Create a copy of the input grid to serve as the output grid.
2. Locate Source: Find the unique 3x3 pattern consisting of a maroon (9) center pixel surrounded by eight gray (5) pixels. Record the coordinates of the center pixel as (r_s, c_s). If not found, return the grid unchanged.
3. Locate Target 1: Find the unique magenta (6) pixel in the grid. Record its coordinates as (r_t1, c_t1). If not found, return the grid unchanged.
4. Calculate Vector: Compute the vector V = (dr, dc) pointing from the source center to Target 1: dr = r_t1 - r_s, dc = c_t1 - c_s.
5. Determine Neighbor Offset: Calculate the offset (dr_n, dc_n) to find the neighbor pixel relative to the source center (r_s, c_s) based on the vector V:
    - If dr is 0 and dc is 0, the offset is (0, 0).
    - If dr is 0 (and dc is not 0), the offset is (0, sign(dc)).
    - If dc is 0 (and dr is not 0), the offset is (sign(dr), 0).
    - If neither dr nor dc is 0:
        - Calculate the ratio R = min(abs(dr), abs(dc)) / max(abs(dr), abs(dc)).
        - Define a threshold T = 0.3.
        - If R < T (vector is strongly cardinal):
            - If abs(dr) > abs(dc), the offset is (sign(dr), 0).
            - Otherwise (i.e., abs(dc) >= abs(dr)), the offset is (0, sign(dc)).
        - If R >= T (vector is substantially diagonal or components are equal):
            - The offset is (sign(dr), sign(dc)).
6. Calculate Neighbor Coordinates: Determine the coordinates of the neighbor pixel (Target 2) by adding the offset to the source center coordinates: (r_n, c_n) = (r_s + dr_n, c_s + dc_n).
7. Modify Source: Change the color of the pixel at the source center coordinates (r_s, c_s) in the output grid from maroon (9) to gray (5).
8. Modify Target 1: Change the color of the pixel at the Target 1 coordinates (r_t1, c_t1) in the output grid from magenta (6) to maroon (9).
9. Modify Neighbor (Target 2): Check if the calculated neighbor coordinates (r_n, c_n) are valid (within the grid boundaries) and different from the source coordinates (r_s, c_s). If valid and different, change the color of the pixel at (r_n, c_n) in the output grid from gray (5) to maroon (9).
10. Return: Return the modified output grid.
"""

def find_pattern_center(grid):
    """
    Finds the center coordinates (r, c) of the 3x3 pattern with a gray (5) border 
    and a maroon (9) center.
    Returns None if the pattern is not found.
    """
    height, width = grid.shape
    # Iterate only over possible center coordinates (avoiding edges)
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check if the center is maroon (9)
            if grid[r, c] == 9:
                # Check the 3x3 neighborhood for gray (5) border
                is_pattern = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Skip the center pixel itself
                        if dr == 0 and dc == 0:
                            continue
                        # Check if border pixel is gray (5)
                        nr, nc = r + dr, c + dc
                        # Ensure neighbor is within bounds AND is gray
                        if not (0 <= nr < height and 0 <= nc < width and grid[nr, nc] == 5):
                            is_pattern = False
                            break
                    if not is_pattern:
                        break
                
                # If the 3x3 pattern matches, return the center coordinates
                if is_pattern:
                    return r, c
    # Return None if the pattern was not found in the grid
    return None 

def find_unique_pixel(grid, color):
    """
    Finds the coordinates (r, c) of the unique pixel with the specified color.
    Returns None if the pixel is not found or if more than one is found.
    """
    # Find all locations of the specified color
    locations = np.argwhere(grid == color)
    # Check if exactly one location was found
    if len(locations) == 1:
        # Return the coordinates of the unique pixel
        return tuple(locations[0])
    # Return None if zero or more than one pixel of that color exists
    return None 

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    
    # 1. Initialize: Create a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape
    
    # 2. Locate Source (maroon center of gray pattern)
    source_coords = find_pattern_center(output_grid)
    if source_coords is None:
        # print("Warning: Source pattern (gray border, maroon center) not found.")
        return output_grid # Return unchanged if pattern not found

    # 3. Locate Target 1 (unique magenta pixel)
    target1_coords = find_unique_pixel(output_grid, 6) # 6 is magenta
    if target1_coords is None:
        # print("Warning: Unique magenta (6) pixel not found.")
        return output_grid # Return unchanged if unique magenta not found
        
    r_s, c_s = source_coords
    r_t1, c_t1 = target1_coords

    # 4. Calculate the relative vector V = (dr, dc)
    dr = r_t1 - r_s
    dc = c_t1 - c_s

    # 5. Determine the neighbor offset (dr_n, dc_n)
    dr_n, dc_n = 0, 0
    threshold = 0.3 
    
    if dr == 0 and dc == 0:
        dr_n, dc_n = 0, 0 # Source and Target1 are the same, no neighbor change
    elif dr == 0: # Purely horizontal move
        dc_n = np.sign(dc)
    elif dc == 0: # Purely vertical move
        dr_n = np.sign(dr)
    else: # Both dr and dc are non-zero
        # Use float division for ratio
        ratio = min(abs(float(dr)), abs(float(dc))) / max(abs(float(dr)), abs(float(dc)))
        
        if ratio < threshold:
            # Cardinal direction based on dominance
            if abs(dr) > abs(dc):
                 dr_n = np.sign(dr) # More vertical than horizontal
            else: # abs(dc) >= abs(dr) # More horizontal or equal (tie-break to horizontal if ratio < threshold, though this case implies inequality)
                 dc_n = np.sign(dc)
        else: # ratio >= threshold
            # Diagonal direction
            dr_n = np.sign(dr)
            dc_n = np.sign(dc)
            
    # 6. Calculate Neighbor Coordinates (Target 2)
    r_n = r_s + dr_n
    c_n = c_s + dc_n
        
    # 7. Modify Source: Change the source pixel's color (center of pattern) to gray (5)
    output_grid[r_s, c_s] = 5 

    # 8. Modify Target 1: Change the target1 pixel's color (original magenta) to maroon (9)
    output_grid[r_t1, c_t1] = 9
    
    # 9. Modify Neighbor (Target 2): Change the neighbor pixel's color to maroon (9)
    # Ensure coordinates are valid (within bounds) and not the same as the source center
    if (dr_n != 0 or dc_n != 0) and (0 <= r_n < height and 0 <= c_n < width):
        # We assume based on examples that this neighbor is initially gray(5)
        output_grid[r_n, c_n] = 9
    # else:
        # Handle edge cases or unexpected conditions if needed
        # if not (0 <= r_n < height and 0 <= c_n < width):
        #     print(f"Warning: Calculated neighbor ({r_n}, {c_n}) is out of bounds.")
        # if dr_n == 0 and dc_n == 0:
        #     print("Warning: Source and Target1 are the same, no neighbor change.")
        # pass # Do nothing if neighbor is out of bounds or same as source

    # 10. Return the modified grid
    return output_grid