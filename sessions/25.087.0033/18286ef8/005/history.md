
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 0 7 7 7 0 7 7 4 7
7 7 2 0 7 7 7 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
4 7 7 0 5 5 5 0 7 7 7 7
7 7 7 0 5 9 5 0 7 7 7 8
7 7 7 0 5 5 5 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 0 7 7 7 0 7 7 7 7
7 7 8 0 7 7 7 0 7 7 6 7
7 7 7 0 7 7 7 0 7 7 7 7
```
Expected Output:
```
7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 0 7 7 7 0 7 7 4 7
7 7 2 0 7 7 7 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
4 7 7 0 5 5 5 0 7 7 7 7
7 7 7 0 5 5 5 0 7 7 7 8
7 7 7 0 5 5 9 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 0 7 7 7 0 7 7 7 7
7 7 8 0 7 7 7 0 7 7 9 7
7 7 7 0 7 7 7 0 7 7 7 7
```
Transformed Output:
```
7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 0 7 7 7 0 7 7 4 7
7 7 2 0 7 7 7 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
4 7 7 0 5 5 5 0 7 7 7 7
7 7 7 0 5 5 5 0 7 7 7 8
7 7 7 0 5 9 5 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 0 7 7 7 0 7 7 7 7
7 7 8 0 7 7 7 0 7 7 9 7
7 7 7 0 7 7 7 0 7 7 7 7
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 1.3888888888888857

## Example 2:
Input:
```
1 7 0 7 7 4 0 7
7 7 0 7 7 7 0 7
0 0 0 0 0 0 0 0
6 7 0 5 5 5 0 7
7 7 0 5 9 5 0 7
7 7 0 5 5 5 0 7
0 0 0 0 0 0 0 0
7 3 0 7 7 7 0 7
```
Expected Output:
```
1 7 0 7 7 4 0 7
7 7 0 7 7 7 0 7
0 0 0 0 0 0 0 0
9 7 0 5 5 5 0 7
7 7 0 9 5 5 0 7
7 7 0 5 5 5 0 7
0 0 0 0 0 0 0 0
7 3 0 7 7 7 0 7
```
Transformed Output:
```
1 7 0 7 7 4 0 7
7 7 0 7 7 7 0 7
0 0 0 0 0 0 0 0
9 7 0 5 5 5 0 7
7 7 0 9 5 5 0 7
7 7 0 5 5 5 0 7
0 0 0 0 0 0 0 0
7 3 0 7 7 7 0 7
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
7 7 7 7 7 8 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 1 7 0 7 7 2 7
7 6 7 7 7 7 0 7 7 7 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 0 5 5 5 0 7 7 7 7
7 7 7 7 7 7 0 5 9 5 0 8 7 7 7
7 7 7 7 7 7 0 5 5 5 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 4 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 7 7 0 7 7 7 1
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 2 7 0 7 1 7 0 7 7 7 1
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
```
Expected Output:
```
7 7 7 7 7 8 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 1 7 0 7 7 2 7
7 9 7 7 7 7 0 7 7 7 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 0 9 5 5 0 7 7 7 7
7 7 7 7 7 7 0 5 5 5 0 8 7 7 7
7 7 7 7 7 7 0 5 5 5 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 4 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 7 7 0 7 7 7 1
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 2 7 0 7 1 7 0 7 7 7 1
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
```
Transformed Output:
```
7 7 7 7 7 8 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 1 7 0 7 7 2 7
7 9 7 7 7 7 0 7 7 7 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 0 5 5 5 0 7 7 7 7
7 7 7 7 7 7 0 9 5 5 0 8 7 7 7
7 7 7 7 7 7 0 5 5 5 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 4 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 7 7 0 7 7 7 1
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 2 7 0 7 1 7 0 7 7 7 1
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 7 7 7 0 7 7 7 0 7 7 7 7
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.8888888888888857
Ah, the numpy integer types are not directly JSON serializable. I need to convert them to standard Python ints.



*code_execution:*
```python
import numpy as np
import json

# Helper function to convert numpy types to Python types for JSON serialization
def convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, tuple):
        return tuple(convert_numpy(item) for item in obj)
    elif isinstance(obj, list):
        return [convert_numpy(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    return obj

def find_pattern_center(grid):
    height, width = grid.shape
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if grid[r, c] == 9:
                is_pattern = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        # Check bounds before accessing grid element
                        nr, nc = r + dr, c + dc
                        if not (0 <= nr < height and 0 <= nc < width and grid[nr, nc] == 5):
                            is_pattern = False
                            break
                    if not is_pattern: break
                if is_pattern:
                    return r, c
    return None

def find_unique_pixel(grid, color):
    locations = np.argwhere(grid == color)
    if len(locations) == 1:
        return tuple(locations[0])
    return None

# Example 1 Data
grid1_in = np.array([
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 4, 7],
    [7, 7, 2, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 5, 9, 5, 0, 7, 7, 7, 8],
    [7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 8, 0, 7, 7, 7, 0, 7, 7, 6, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7]
])
grid1_out = np.array([
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 4, 7],
    [7, 7, 2, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 8],
    [7, 7, 7, 0, 5, 5, 9, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 8, 0, 7, 7, 7, 0, 7, 7, 9, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7]
])

# Example 2 Data
grid2_in = np.array([
    [1, 7, 0, 7, 7, 4, 0, 7],
    [7, 7, 0, 7, 7, 7, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [6, 7, 0, 5, 5, 5, 0, 7],
    [7, 7, 0, 5, 9, 5, 0, 7],
    [7, 7, 0, 5, 5, 5, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [7, 3, 0, 7, 7, 7, 0, 7]
])
grid2_out = np.array([
    [1, 7, 0, 7, 7, 4, 0, 7],
    [7, 7, 0, 7, 7, 7, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [9, 7, 0, 5, 5, 5, 0, 7],
    [7, 7, 0, 9, 5, 5, 0, 7],
    [7, 7, 0, 5, 5, 5, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [7, 3, 0, 7, 7, 7, 0, 7]
])

# Example 3 Data
grid3_in = np.array([
    [7, 7, 7, 7, 7, 8, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 1, 7, 0, 7, 7, 2, 7],
    [7, 6, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 5, 9, 5, 0, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 4, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 1],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 2, 7, 0, 7, 1, 7, 0, 7, 7, 7, 1],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7]
])
grid3_out = np.array([
    [7, 7, 7, 7, 7, 8, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 1, 7, 0, 7, 7, 2, 7],
    [7, 9, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7, 7, 0, 9, 5, 5, 0, 7, 7, 7, 7], # NOTE: Correction here based on my analysis
    [7, 7, 7, 7, 7, 7, 0, 5, 5, 5, 0, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 4, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 1],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 2, 7, 0, 7, 1, 7, 0, 7, 7, 7, 1],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7]
])

results = {}
for i, (grid_in, grid_out) in enumerate([(grid1_in, grid1_out), (grid2_in, grid2_out), (grid3_in, grid3_out)]):
    center = find_pattern_center(grid_in)
    magenta = find_unique_pixel(grid_in, 6)
    
    example_data = {}
    if center:
        example_data["Center (Maroon 9)"] = center
    else:
        example_data["Center (Maroon 9)"] = None
    
    if magenta:
        example_data["Magenta (6)"] = magenta
    else:
        example_data["Magenta (6)"] = None

    if center and magenta:
        r_s, c_s = center
        r_t1, c_t1 = magenta
        dr = r_t1 - r_s
        dc = c_t1 - c_s
        example_data["Vector (dr, dc)"] = (dr, dc)
        
        # Check expected changes
        example_data["Center Change (9->5) Check"] = grid_out[r_s, c_s] == 5
        example_data["Magenta Change (6->9) Check"] = grid_out[r_t1, c_t1] == 9

        # Find the neighbor pixel coordinates in the output grid that changed from 5 to 9
        diff_mask = (grid_in == 5) & (grid_out == 9)
        potential_neighbors = np.argwhere(diff_mask)
        neighbor = None
        if len(potential_neighbors) == 1:
             neighbor = tuple(potential_neighbors[0])
        example_data["Expected Neighbor Change (5->9) at"] = neighbor
        
        # Calculate the neighbor offset based on the proposed logic
        dr_n, dc_n = 0, 0
        if dr == 0 and dc == 0:
            dr_n, dc_n = 0, 0
        elif dr == 0:
            dc_n = np.sign(dc)
        elif dc == 0:
            dr_n = np.sign(dr)
        else: # dr != 0 and dc != 0
            ratio = min(abs(dr), abs(dc)) / max(abs(dr), abs(dc))
            threshold = 0.3
            if ratio < threshold:
                if abs(dr) > abs(dc):
                     dr_n = np.sign(dr)
                else: # abs(dc) > abs(dr)
                     dc_n = np.sign(dc)
            else: # ratio >= threshold
                dr_n = np.sign(dr)
                dc_n = np.sign(dc)
        
        calculated_neighbor = (r_s + dr_n, c_s + dc_n)
        example_data["Calculated Neighbor Offset (dr_n, dc_n)"] = (dr_n, dc_n)
        example_data["Calculated Neighbor Coords"] = calculated_neighbor
        example_data["Neighbor Match Check"] = (calculated_neighbor == neighbor)

    results[f"Example {i+1}"] = example_data

# Convert numpy types before printing
results_serializable = convert_numpy(results)
print(json.dumps(results_serializable, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_FAILED
```
Traceback (most recent call last):
  File "<string>", line 197, in <module>
  File "__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type bool is not JSON serializable

```
My apologies, the `convert_numpy` helper needs to handle boolean types as well.



*code_execution:*
```python
import numpy as np
import json

# Helper function to convert numpy types to Python types for JSON serialization
def convert_numpy(obj):
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, tuple):
        return tuple(convert_numpy(item) for item in obj)
    elif isinstance(obj, list):
        return [convert_numpy(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    return obj

def find_pattern_center(grid):
    height, width = grid.shape
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if grid[r, c] == 9:
                is_pattern = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        # Check bounds before accessing grid element
                        nr, nc = r + dr, c + dc
                        if not (0 <= nr < height and 0 <= nc < width and grid[nr, nc] == 5):
                            is_pattern = False
                            break
                    if not is_pattern: break
                if is_pattern:
                    return r, c
    return None

def find_unique_pixel(grid, color):
    locations = np.argwhere(grid == color)
    if len(locations) == 1:
        return tuple(locations[0])
    return None

# Example 1 Data
grid1_in = np.array([
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 4, 7],
    [7, 7, 2, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 5, 9, 5, 0, 7, 7, 7, 8],
    [7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 8, 0, 7, 7, 7, 0, 7, 7, 6, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7]
])
grid1_out = np.array([
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 4, 7],
    [7, 7, 2, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 8],
    [7, 7, 7, 0, 5, 5, 9, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 8, 0, 7, 7, 7, 0, 7, 7, 9, 7],
    [7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7]
])

# Example 2 Data
grid2_in = np.array([
    [1, 7, 0, 7, 7, 4, 0, 7],
    [7, 7, 0, 7, 7, 7, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [6, 7, 0, 5, 5, 5, 0, 7],
    [7, 7, 0, 5, 9, 5, 0, 7],
    [7, 7, 0, 5, 5, 5, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [7, 3, 0, 7, 7, 7, 0, 7]
])
grid2_out = np.array([
    [1, 7, 0, 7, 7, 4, 0, 7],
    [7, 7, 0, 7, 7, 7, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [9, 7, 0, 5, 5, 5, 0, 7],
    [7, 7, 0, 9, 5, 5, 0, 7],
    [7, 7, 0, 5, 5, 5, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [7, 3, 0, 7, 7, 7, 0, 7]
])

# Example 3 Data
grid3_in = np.array([
    [7, 7, 7, 7, 7, 8, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 1, 7, 0, 7, 7, 2, 7],
    [7, 6, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 5, 9, 5, 0, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 4, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 1],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 2, 7, 0, 7, 1, 7, 0, 7, 7, 7, 1],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7]
])
grid3_out = np.array([
    [7, 7, 7, 7, 7, 8, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 1, 7, 0, 7, 7, 2, 7],
    [7, 9, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7, 7, 0, 9, 5, 5, 0, 7, 7, 7, 7], # NOTE: Made correction here based on my analysis
    [7, 7, 7, 7, 7, 7, 0, 5, 5, 5, 0, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 5, 5, 5, 0, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 4, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 1],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 2, 7, 0, 7, 1, 7, 0, 7, 7, 7, 1],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7]
])

results = {}
for i, (grid_in, grid_out) in enumerate([(grid1_in, grid1_out), (grid2_in, grid2_out), (grid3_in, grid3_out)]):
    center = find_pattern_center(grid_in)
    magenta = find_unique_pixel(grid_in, 6)
    
    example_data = {}
    if center:
        example_data["Center (Maroon 9)"] = center
    else:
        example_data["Center (Maroon 9)"] = None
    
    if magenta:
        example_data["Magenta (6)"] = magenta
    else:
        example_data["Magenta (6)"] = None

    if center and magenta:
        r_s, c_s = center
        r_t1, c_t1 = magenta
        dr = r_t1 - r_s
        dc = c_t1 - c_s
        example_data["Vector (dr, dc)"] = (dr, dc)
        
        # Check expected changes
        example_data["Center Change (9->5) Check"] = grid_out[r_s, c_s] == 5
        example_data["Magenta Change (6->9) Check"] = grid_out[r_t1, c_t1] == 9

        # Find the neighbor pixel coordinates in the output grid that changed from 5 to 9
        diff_mask = (grid_in == 5) & (grid_out == 9)
        potential_neighbors = np.argwhere(diff_mask)
        neighbor = None
        if len(potential_neighbors) == 1:
             neighbor = tuple(potential_neighbors[0])
        example_data["Expected Neighbor Change (5->9) at"] = neighbor
        
        # Calculate the neighbor offset based on the proposed logic
        dr_n, dc_n = 0, 0
        if dr == 0 and dc == 0:
            dr_n, dc_n = 0, 0
        elif dr == 0:
            dc_n = np.sign(dc)
        elif dc == 0:
            dr_n = np.sign(dr)
        else: # dr != 0 and dc != 0
            # Use float division for ratio
            ratio = min(abs(float(dr)), abs(float(dc))) / max(abs(float(dr)), abs(float(dc)))
            threshold = 0.3
            if ratio < threshold:
                # Cardinal direction based on dominance
                if abs(dr) > abs(dc):
                     dr_n = np.sign(dr)
                else: # abs(dc) >= abs(dr) # Include equality here for robustness, though ratio<threshold implies inequality
                     dc_n = np.sign(dc)
            else: # ratio >= threshold
                # Diagonal direction
                dr_n = np.sign(dr)
                dc_n = np.sign(dc)
        
        calculated_neighbor = (r_s + dr_n, c_s + dc_n)
        example_data["Calculated Neighbor Offset (dr_n, dc_n)"] = (dr_n, dc_n)
        example_data["Calculated Neighbor Coords"] = calculated_neighbor
        example_data["Neighbor Match Check"] = (calculated_neighbor == neighbor)

    results[f"Example {i+1}"] = example_data

# Convert numpy types before printing
results_serializable = convert_numpy(results)
print(json.dumps(results_serializable, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{
  "Example 1": {
    "Center (Maroon 9)": [
      5,
      5
    ],
    "Magenta (6)": [
      10,
      10
    ],
    "Vector (dr, dc)": [
      5,
      5
    ],
    "Center Change (9->5) Check": true,
    "Magenta Change (6->9) Check": true,
    "Expected Neighbor Change (5->9) at": [
      6,
      6
    ],
    "Calculated Neighbor Offset (dr_n, dc_n)": [
      1,
      1
    ],
    "Calculated Neighbor Coords": [
      6,
      6
    ],
    "Neighbor Match Check": true
  },
  "Example 2": {
    "Center (Maroon 9)": [
      4,
      4
    ],
    "Magenta (6)": [
      3,
      0
    ],
    "Vector (dr, dc)": [
      -1,
      -4
    ],
    "Center Change (9->5) Check": true,
    "Magenta Change (6->9) Check": true,
    "Expected Neighbor Change (5->9) at": [
      4,
      3
    ],
    "Calculated Neighbor Offset (dr_n, dc_n)": [
      0,
      -1
    ],
    "Calculated Neighbor Coords": [
      4,
      3
    ],
    "Neighbor Match Check": true
  },
  "Example 3": {
    "Center (Maroon 9)": [
      5,
      8
    ],
    "Magenta (6)": [
      2,
      1
    ],
    "Vector (dr, dc)": [
      -3,
      -7
    ],
    "Center Change (9->5) Check": true,
    "Magenta Change (6->9) Check": true,
    "Expected Neighbor Change (5->9) at": [
      4,
      7
    ],
    "Calculated Neighbor Offset (dr_n, dc_n)": [
      -1,
      -1
    ],
    "Calculated Neighbor Coords": [
      4,
      7
    ],
    "Neighbor Match Check": true
  }
}

```
## General Assessment

The initial code failed on examples 1 and 3 because the logic for determining the adjacent neighbor pixel to modify was incorrect. The original logic prioritized cardinal directions (North, South, East, West) based solely on the dominant component of the vector pointing from the pattern center to the magenta pixel. The analysis of all examples revealed a more nuanced rule: a diagonal neighbor is chosen unless the vector is strongly aligned with a cardinal axis (i.e., the ratio of the smaller vector component to the larger one is below a certain threshold). The refined logic, incorporating this ratio check, correctly identifies the neighbor pixel in all three examples.

## Metrics

The `tool_code` execution provides the following metrics, confirming the analysis:


```json
{
  "Example 1": {
    "Center (Maroon 9)": [5, 5],
    "Magenta (6)": [10, 10],
    "Vector (dr, dc)": [5, 5],
    "Center Change (9->5) Check": true,
    "Magenta Change (6->9) Check": true,
    "Expected Neighbor Change (5->9) at": [6, 6],
    "Calculated Neighbor Offset (dr_n, dc_n)": [1, 1], // Ratio 1.0 >= 0.3 -> Diagonal
    "Calculated Neighbor Coords": [6, 6],
    "Neighbor Match Check": true
  },
  "Example 2": {
    "Center (Maroon 9)": [4, 4],
    "Magenta (6)": [3, 0],
    "Vector (dr, dc)": [-1, -4],
    "Center Change (9->5) Check": true,
    "Magenta Change (6->9) Check": true,
    "Expected Neighbor Change (5->9) at": [4, 3],
    "Calculated Neighbor Offset (dr_n, dc_n)": [0, -1], // Ratio 0.25 < 0.3 -> Cardinal (dominant dc)
    "Calculated Neighbor Coords": [4, 3],
    "Neighbor Match Check": true
  },
  "Example 3": {
    "Center (Maroon 9)": [5, 8],
    "Magenta (6)": [2, 1],
    "Vector (dr, dc)": [-3, -7],
    "Center Change (9->5) Check": true,
    "Magenta Change (6->9) Check": true,
    "Expected Neighbor Change (5->9) at": [4, 7],
    "Calculated Neighbor Offset (dr_n, dc_n)": [-1, -1], // Ratio ~0.43 >= 0.3 -> Diagonal
    "Calculated Neighbor Coords": [4, 7],
    "Neighbor Match Check": true
  }
}
```


These metrics confirm:
1.  The identification of the pattern center (source) and the unique magenta pixel (target 1) is correct.
2.  The basic color changes (source 9->5, target1 6->9) are consistent across examples.
3.  The calculation of the neighbor pixel (target 2) based on the vector ratio logic matches the expected output for all three examples.

## Facts


```yaml
task_description: The transformation involves relocating a marker and indicating the direction of relocation.

grid_properties:
  - height and width vary between examples.
  - contain background colors (white 0, various shades of gray 7) and separators (black 0).
  - contain various other colored pixels/objects (blue 1, red 2, green 3, yellow 4, gray 5, magenta 6, orange 7, azure 8, maroon 9) that are mostly static, except for the key objects involved in the transformation.

key_objects:
  - object_1:
      description: A 3x3 pattern acting as the source or origin.
      pixels:
        - color: gray (5)
          role: border (8 pixels surrounding the center)
        - color: maroon (9)
          role: center (1 pixel)
      properties:
        - unique within the grid
        - location denoted as (r_s, c_s) for the center pixel.
  - object_2:
      description: A single pixel acting as the primary target or destination indicator.
      pixels:
        - color: magenta (6)
          role: target indicator
      properties:
        - unique within the grid
        - location denoted as (r_t1, c_t1).
  - object_3:
      description: A single pixel adjacent to the center of object_1, acting as the secondary target or direction indicator.
      pixels:
        - color: gray (5)
          role: initial state (before change)
      properties:
        - adjacent (including diagonals) to the center of object_1.
        - its specific location relative to object_1 depends on the vector between object_1 and object_2.
        - location denoted as (r_n, c_n).

actions:
  - action_1:
      description: Locate object_1 (source pattern).
      inputs: input_grid
      outputs: coordinates (r_s, c_s) of the maroon center.
  - action_2:
      description: Locate object_2 (unique magenta pixel).
      inputs: input_grid
      outputs: coordinates (r_t1, c_t1).
  - action_3:
      description: Calculate the relative vector V from source center to target 1.
      inputs: (r_s, c_s), (r_t1, c_t1)
      outputs: vector (dr, dc) = (r_t1 - r_s, c_t1 - c_s).
  - action_4:
      description: Determine the offset vector (dr_n, dc_n) for the neighbor pixel based on vector V.
      inputs: vector (dr, dc)
      outputs: offset vector (dr_n, dc_n)
      logic:
        - If dr=0 and dc=0, offset=(0, 0).
        - If dr=0, offset=(0, sign(dc)).
        - If dc=0, offset=(sign(dr), 0).
        - If dr!=0 and dc!=0:
            - ratio = min(abs(dr), abs(dc)) / max(abs(dr), abs(dc))
            - threshold = 0.3 (approximately)
            - If ratio < threshold: # Cardinal direction of dominant component
                - If abs(dr) > abs(dc), offset=(sign(dr), 0).
                - Else, offset=(0, sign(dc)).
            - Else (ratio >= threshold): # Diagonal direction
                - offset=(sign(dr), sign(dc)).
  - action_5:
      description: Calculate the coordinates of the neighbor pixel (object_3).
      inputs: (r_s, c_s), (dr_n, dc_n)
      outputs: coordinates (r_n, c_n) = (r_s + dr_n, c_s + dc_n).
  - action_6:
      description: Create the output grid by copying the input grid.
      inputs: input_grid
      outputs: output_grid
  - action_7:
      description: Modify the color of the source pattern center in the output grid.
      inputs: output_grid, (r_s, c_s)
      outputs: output_grid with pixel at (r_s, c_s) changed from maroon (9) to gray (5).
  - action_8:
      description: Modify the color of the primary target pixel in the output grid.
      inputs: output_grid, (r_t1, c_t1)
      outputs: output_grid with pixel at (r_t1, c_t1) changed from magenta (6) to maroon (9).
  - action_9:
      description: Modify the color of the neighbor pixel (secondary target) in the output grid.
      inputs: output_grid, (r_n, c_n)
      outputs: output_grid with pixel at (r_n, c_n) changed from gray (5) to maroon (9). (Ensure coordinates are within bounds).

```


## Natural Language Program

1.  **Initialize**: Create a copy of the input grid to serve as the output grid.
2.  **Locate Source**: Find the unique 3x3 pattern consisting of a maroon (9) center pixel surrounded by eight gray (5) pixels. Record the coordinates of the center pixel as (r_s, c_s). If not found, return the grid unchanged.
3.  **Locate Target 1**: Find the unique magenta (6) pixel in the grid. Record its coordinates as (r_t1, c_t1). If not found, return the grid unchanged.
4.  **Calculate Vector**: Compute the vector V = (dr, dc) pointing from the source center to Target 1: `dr = r_t1 - r_s`, `dc = c_t1 - c_s`.
5.  **Determine Neighbor Offset**: Calculate the offset `(dr_n, dc_n)` to find the neighbor pixel relative to the source center (r_s, c_s) based on the vector V:
    *   If `dr` is 0 and `dc` is 0, the offset is (0, 0).
    *   If `dr` is 0 (and `dc` is not 0), the offset is (0, sign(dc)).
    *   If `dc` is 0 (and `dr` is not 0), the offset is (sign(dr), 0).
    *   If neither `dr` nor `dc` is 0:
        *   Calculate the ratio `R = min(abs(dr), abs(dc)) / max(abs(dr), abs(dc))`.
        *   Define a threshold `T = 0.3`.
        *   If `R < T` (vector is strongly cardinal):
            *   If `abs(dr) > abs(dc)`, the offset is (sign(dr), 0).
            *   Otherwise (i.e., `abs(dc) >= abs(dr)`), the offset is (0, sign(dc)).
        *   If `R >= T` (vector is substantially diagonal or components are equal):
            *   The offset is (sign(dr), sign(dc)).
6.  **Calculate Neighbor Coordinates**: Determine the coordinates of the neighbor pixel (Target 2) by adding the offset to the source center coordinates: `(r_n, c_n) = (r_s + dr_n, c_s + dc_n)`.
7.  **Modify Source**: Change the color of the pixel at the source center coordinates (r_s, c_s) in the output grid from maroon (9) to gray (5).
8.  **Modify Target 1**: Change the color of the pixel at the Target 1 coordinates (r_t1, c_t1) in the output grid from magenta (6) to maroon (9).
9.  **Modify Neighbor (Target 2)**: Check if the calculated neighbor coordinates (r_n, c_n) are valid (within the grid boundaries) and different from the source coordinates (r_s, c_s). If valid and different, change the color of the pixel at (r_n, c_n) in the output grid from gray (5) to maroon (9). (Based on examples, this neighbor is always initially gray).
10. **Return**: Return the modified output grid.
