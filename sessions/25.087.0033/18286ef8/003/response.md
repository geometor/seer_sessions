```python
import numpy as np

"""
Transforms the input grid based on the following rule:
1. Locate the unique 3x3 pattern with a gray (5) border and a maroon (9) center. Let the center be (r_s, c_s).
2. Locate the unique magenta (6) pixel. Let its coordinates be (r_t1, c_t1).
3. Calculate the relative vector V = (dr, dc) = (r_t1 - r_s, c_t1 - c_s).
4. Determine the primary direction based on the component of V with the larger absolute magnitude. If magnitudes are equal, prioritize the vertical (North/South) direction.
    - If |dr| >= |dc|, the primary direction is North (if dr < 0) or South (if dr >= 0).
    - If |dc| > |dr|, the primary direction is West (if dc < 0) or East (if dc > 0).
5. Determine the coordinates (r_n, c_n) of the gray (5) neighbor adjacent to the center (r_s, c_s) in the primary direction.
6. Create the output grid by copying the input grid.
7. Change the pixel at (r_s, c_s) from maroon (9) to gray (5).
8. Change the pixel at (r_t1, c_t1) from magenta (6) to maroon (9).
9. Change the pixel at the neighbor coordinates (r_n, c_n) from gray (5) to maroon (9).
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
                        if grid[r + dr, c + dc] != 5:
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
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # 1. Find the source pixel (center of the gray/maroon pattern)
    source_coords = find_pattern_center(output_grid)
    if source_coords is None:
        # If the pattern is not found, return the grid unchanged (as per examples)
        # print("Warning: Source pattern (gray border, maroon center) not found.")
        return output_grid 

    # 2. Find the target pixel (the unique magenta pixel)
    target1_coords = find_unique_pixel(output_grid, 6) # 6 is magenta
    if target1_coords is None:
        # If the unique magenta pixel is not found, return the grid unchanged
        # print("Warning: Unique magenta (6) pixel not found.")
        return output_grid 
        
    r_s, c_s = source_coords
    r_t1, c_t1 = target1_coords

    # 3. Calculate the relative vector V = (dr, dc)
    dr = r_t1 - r_s
    dc = c_t1 - c_s

    # 4. Determine the primary direction and neighbor offset (dr_n, dc_n)
    dr_n, dc_n = 0, 0
    if abs(dr) >= abs(dc):
        # Vertical direction is primary or equal
        if dr > 0: 
            dr_n = 1 # South
        elif dr < 0:
             dr_n = -1 # North
        # If dr == 0 (and dc == 0), offset remains (0,0), neighbor is center itself.
        # This case implies source == target, which shouldn't happen based on examples.
        # If dr == 0 and dc != 0 but abs(dr) >= abs(dc) is technically true, 
        # it means dc must be 0. We default dr_n to 0. The target neighbor logic needs care.
        # Let's refine: if dr==0 and dc==0, no neighbor change. If dr==0 and dc!=0, horizontal is dominant.
        # The condition abs(dr) >= abs(dc) handles the tie-break correctly if dr!=0 or dc!=0.
        # If dr > 0, dr_n=1. If dr < 0, dr_n = -1. If dr=0 (and abs(dc)<=abs(dr)), then dc must be 0, so dr_n=0, dc_n=0.
        
    else: # abs(dc) > abs(dr)
        # Horizontal direction is primary
        if dc > 0:
            dc_n = 1 # East
        elif dc < 0:
            dc_n = -1 # West
            
    # 5. Determine the coordinates (r_n, c_n) of the target neighbor
    # Ensure source and target are distinct to avoid neighbor being the source itself
    if dr_n != 0 or dc_n != 0: 
        r_n = r_s + dr_n
        c_n = c_s + dc_n
        
        # Check bounds for neighbor coordinates
        height, width = output_grid.shape
        if 0 <= r_n < height and 0 <= c_n < width:
            # 9. Change the pixel at the neighbor coordinates (r_n, c_n) to maroon (9)
            # We assume based on examples that this neighbor is always gray(5)
            output_grid[r_n, c_n] = 9
        else:
             # Handle edge case: neighbor is outside grid (shouldn't happen with pattern search)
             # print(f"Warning: Calculated neighbor ({r_n}, {c_n}) is out of bounds.")
             pass # Do nothing if neighbor is out of bounds

    # 7. Change the source pixel's color (center of pattern) to gray (5)
    output_grid[r_s, c_s] = 5 

    # 8. Change the target1 pixel's color (original magenta) to maroon (9)
    output_grid[r_t1, c_t1] = 9
    
    return output_grid
```