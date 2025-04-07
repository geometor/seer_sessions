
Previous Code:
```python
import numpy as np
import copy

"""
Transformation Rule:
1. Create a copy of the input grid to serve as the output grid.
2. Find all solid 3x3 squares of a single color (not white/0) in the *original input* grid. Record their top-left coordinates (r, c) and color.
3. If no solid 3x3 squares are found, return the unchanged output grid copy.
4. Determine the location rule based on the positions of all found solid squares:
    a. Check if *all* identified solid squares share the same top row index r=1.
5. For each solid 3x3 square found in the original input:
    a. Determine a 'partner' color based on a swap rule: Red (2) <-> Green (3), Blue (1) <-> Yellow (4), Magenta (6) <-> Magenta (6).
    b. Determine the top-left coordinates (new_r, new_c) for a *new* hollow frame based on the original square's top-left position (r, c) and the overall location rule:
        i. If the 'all in row 1' rule (4a) is true: new_r = 14, new_c = c.
        ii. Otherwise, if the original square's column c is 2: new_r = r, new_c = 15.
        iii. Otherwise, if the original square's column c is 15: new_r = r, new_c = 2.
        iv. (Assume these rules cover all required cases based on examples).
    c. Draw a *new* 3x3 hollow frame (perimeter = partner color, center = white/0) onto the *output grid* at the calculated new location (new_r, new_c). This new frame may overwrite existing pixels in the output grid.
6. The original solid 3x3 squares are *not* explicitly modified unless they happen to be overwritten by a newly drawn frame.
7. Return the modified output grid.
"""

def find_solid_3x3_squares(grid):
    """Finds the top-left coordinates and color of all solid 3x3 squares."""
    squares = []
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            color = grid[r, c]
            # Check if the top-left is a potential start (not background)
            if color == 0:
                continue
                
            # Assume it's solid until proven otherwise
            is_solid = True
            for i in range(3):
                for j in range(3):
                    # Check bounds just in case, though outer loop handles most
                    if r + i >= height or c + j >= width or grid[r + i, c + j] != color:
                        is_solid = False
                        break
                if not is_solid:
                    break
                    
            if is_solid:
                squares.append({'r': r, 'c': c, 'color': color})
    return squares

def draw_hollow_frame(grid, r, c, color):
    """Draws a 3x3 hollow frame onto the grid at (r, c) with the given color."""
    height, width = grid.shape
    # Check if the frame is entirely within bounds
    if r < 0 or r + 2 >= height or c < 0 or c + 2 >= width:
        # Invalid location, do nothing
        # print(f"Warning: Attempted to draw frame outside bounds at ({r},{c})") # Optional debug
        return 
        
    # Draw perimeter pixels
    for i in range(3):
        # Top and bottom rows
        if r >= 0 and r < height and c + i >= 0 and c + i < width:
             grid[r, c + i] = color
        if r + 2 >= 0 and r + 2 < height and c + i >= 0 and c + i < width:
             grid[r + 2, c + i] = color
        # Left and right columns (avoiding corners already drawn)
        if i > 0 and i < 2:
            if r + i >= 0 and r + i < height and c >= 0 and c < width:
                 grid[r + i, c] = color
            if r + i >= 0 and r + i < height and c + 2 >= 0 and c + 2 < width:
                 grid[r + i, c + 2] = color
                 
    # Set center pixel to white (0)
    if r + 1 >= 0 and r + 1 < height and c + 1 >= 0 and c + 1 < width:
        grid[r + 1, c + 1] = 0

def transform(input_grid):
    """
    Applies the transformation rule: finds solid 3x3 squares in the input,
    and draws new, color-swapped, position-shifted hollow frames onto a copy.
    """
    # 1. Create a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 2. Find all solid 3x3 squares in the original input grid
    solid_squares = find_solid_3x3_squares(input_grid)

    # 3. If no squares found, return the copy
    if not solid_squares:
        return output_grid

    # 4. Determine the location rule: check if all are in row 1
    all_in_row_1 = all(sq['r'] == 1 for sq in solid_squares)

    # Define the color swap map
    color_swap_map = {
        2: 3, 3: 2,  # Red <-> Green
        1: 4, 4: 1,  # Blue <-> Yellow
        6: 6        # Magenta <-> Magenta
    }

    # 5. Process each found solid square
    for square in solid_squares:
        r, c, color = square['r'], square['c'], square['color']

        # 5a. Determine the partner color
        # If the color isn't in the swap map, it shouldn't have been found by find_solid_3x3_squares
        # based on the examples, but handle defensively just in case.
        swapped_color = color_swap_map.get(color) 
        if swapped_color is None:
            # print(f"Warning: Found solid square with unexpected color {color} at ({r},{c})") # Optional debug
            continue # Skip if color is not one we expect to transform

        # 5b. Determine the new location
        new_r, new_c = -1, -1 # Initialize invalid coordinates

        if all_in_row_1:
            # Rule i: All originals in row 1 -> new frame in row 14
            new_r, new_c = 14, c
        elif c == 2:
            # Rule ii: Original in col 2 -> new frame in col 15
             new_r, new_c = r, 15
        elif c == 15:
             # Rule iii: Original in col 15 -> new frame in col 2
             new_r, new_c = r, 2
        # If none of the location rules match, new_r/new_c remain -1
        # and the frame won't be drawn (handled by draw_hollow_frame check).

        # 5c. Create the new hollow frame at the new location on the output grid
        if new_r != -1 and new_c != -1: # Ensure a valid location rule was applied
             draw_hollow_frame(output_grid, new_r, new_c, swapped_color)
             
    # 6 & 7. Return the modified output grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 8 8 8 8 8 8 0 0 8 8 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 9 9 9 9 8 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 8 0 9 9 9 9 0 0 4 0 4 0 0 0 0
0 0 4 0 4 8 5 8 5 9 9 9 9 8 8 0 4 0 0 0 0 0
0 0 0 4 0 0 0 8 0 9 9 9 9 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 8 0 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 8 8 8 0 0 8 8 8 8 8 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 0 3 0 3 8 8 8 8 8 8 0 0 8 8 0 2 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 8 0 0 8 0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 8 8 9 9 9 9 8 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 8 0 9 9 9 9 0 0 4 0 4 0 0 0 0
0 0 4 0 4 8 5 8 5 9 9 9 9 8 8 0 4 0 0 0 0 0
0 0 0 4 0 0 0 8 0 9 9 9 9 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 8 0 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 8 0 0 8 0 0 0 0 3 0 3 0 0 0 0
0 0 2 0 2 8 8 8 0 0 8 8 8 8 8 0 3 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0
0 0 6 0 6 8 8 8 8 8 8 8 8 8 8 0 6 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0
0 0 3 3 3 8 8 8 8 8 8 0 0 8 8 2 0 2 0 0 0 0
0 0 3 3 3 0 0 0 0 0 8 0 0 8 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 8 8 9 9 9 9 8 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 8 0 9 9 9 9 0 0 4 0 4 0 0 0 0
0 0 4 0 4 8 5 8 5 9 9 9 9 8 8 0 4 0 0 0 0 0
0 0 0 4 0 0 0 8 0 9 9 9 9 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 8 0 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 8 0 0 8 0 0 0 0 3 3 3 0 0 0 0
0 0 2 2 2 8 8 8 0 0 8 8 8 8 8 3 0 3 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 9.917355371900811

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 2 2 2 0 3 3 3 0 4 4 4 0 0 0 0
0 0 0 1 1 1 0 2 2 2 0 3 3 3 0 4 4 4 0 0 0 0
0 0 0 1 1 1 0 2 2 2 0 3 3 3 0 4 4 4 0 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 8 8 5 8 5 8 0 0 0
0 0 0 0 8 0 0 0 5 0 0 0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0 8 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 8 5 8 5 8 5 8 5 8 8 8 0 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 8 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 2 0 0 0 3 0 0 0 4 0 0 0 0 0
0 0 0 1 0 1 0 2 0 2 0 3 0 3 0 4 0 4 0 0 0 0
0 0 0 0 1 0 0 0 2 0 0 0 3 0 0 0 4 0 0 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 8 8 5 8 5 8 0 0 0
0 0 0 0 8 0 0 0 5 0 0 0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0 8 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 8 5 8 5 8 5 8 5 8 8 8 0 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 8 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 4 0 4 0 2 0 2 0 1 0 1 0 3 0 3 0 0 0 0
0 0 0 0 4 0 0 0 2 0 0 0 1 0 0 0 3 0 0 0 0 0
0 0 0 4 0 4 0 2 0 2 0 1 0 1 0 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 2 2 2 0 3 3 3 0 4 4 4 0 0 0 0
0 0 0 1 1 1 0 2 2 2 0 3 3 3 0 4 4 4 0 0 0 0
0 0 0 1 1 1 0 2 2 2 0 3 3 3 0 4 4 4 0 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 8 8 5 8 5 8 0 0 0
0 0 0 0 8 0 0 0 5 0 0 0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0 8 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 8 5 8 5 8 5 8 5 8 8 8 0 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 8 8 0 0 0
0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 4 4 4 0 3 3 3 0 2 2 2 0 1 1 1 0 0 0 0
0 0 0 4 0 4 0 3 0 3 0 2 0 2 0 1 0 1 0 0 0 0
0 0 0 4 4 4 0 3 3 3 0 2 2 2 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 52
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.880382775119614

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 4 4 4 0 6 6 6 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 4 4 4 0 6 6 6 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 4 4 4 0 6 6 6 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 9 9 9 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 9 9 9 0 0 8 8 8 5 8 5 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 8 0 8 9 9 9 9 0 0 0 0
0 0 0 8 8 8 8 8 0 0 9 9 0 8 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 8 0 0 9 9 0 8 9 9 9 9 0 0 0 0
0 0 0 8 8 8 5 8 5 8 8 8 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 8 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 1 0 0 0 4 0 0 0 6 0 0 0 0 0 0
0 0 2 0 2 0 1 0 1 0 4 0 4 0 6 0 6 0 0 0 0 0
0 0 0 2 0 0 0 1 0 0 0 4 0 0 0 6 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 9 9 9 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 9 9 9 0 0 8 8 8 5 8 5 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 8 0 8 9 9 9 9 0 0 0 0
0 0 0 8 8 8 8 8 0 0 9 9 0 8 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 8 0 0 9 9 0 8 9 9 9 9 0 0 0 0
0 0 0 8 8 8 5 8 5 8 8 8 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 8 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 4 0 4 0 2 0 2 0 1 0 1 0 6 0 6 0 0 0 0 0
0 0 0 4 0 0 0 2 0 0 0 1 0 0 0 6 0 0 0 0 0 0
0 0 4 0 4 0 2 0 2 0 1 0 1 0 6 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 4 4 4 0 6 3 3 3 0 0 0 0
0 0 2 2 2 0 0 0 0 0 4 4 4 0 6 3 0 3 0 0 0 0
0 0 2 2 2 0 0 0 0 0 4 4 4 0 6 3 3 3 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 9 9 9 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 9 9 9 0 0 8 8 8 5 8 5 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 8 0 8 9 9 9 9 0 0 0 0
0 0 0 8 8 8 8 8 0 0 9 9 0 8 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 8 0 0 9 9 0 8 9 9 9 9 0 0 0 0
0 0 0 8 8 8 5 8 5 8 8 8 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 8 8 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 40
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 33.05785123966939
