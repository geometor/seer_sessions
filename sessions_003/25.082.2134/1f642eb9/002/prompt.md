
Previous Code:
```python
"""
Transforms the input grid by moving single pixels (1x1 color blocks) near azure (color 8) rectangles, 
based on their relative positions (above or to the left).
"""

import numpy as np

def find_azure_rectangles(grid):
    """Finds the top-left corner coordinates of all azure rectangles (3x2 or 2x3)."""
    rectangles = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 8:
                if (grid[r:r+2, c:c+3] == 8).all() and grid[r:r+2, c:c+3].size == 6:  # Check for 2x3
                  rectangles.append((r, c, 2, 3))
                elif (grid[r:r+3, c:c+2] == 8).all() and grid[r:r+3, c:c+2].size == 6:  # Check for 3x2
                    rectangles.append((r, c, 3, 2))
    return rectangles

def find_single_pixels(grid):
    """Finds the coordinates of all single pixels (excluding color 8)."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r,c] != 8:
                # Check if it's a single pixel (not part of a larger object)
                is_single = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == grid[r, c]:
                            is_single = False
                            break
                    if not is_single:
                        break
                if is_single:
                    pixels.append((r, c))
    return pixels

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find azure rectangles
    rectangles = find_azure_rectangles(input_grid)

    # Find single pixels
    single_pixels = find_single_pixels(input_grid)
    
    # dictionary to store value of single pixel to be moved
    moved_pixels = {}

    # Process Top Row Singularities
    for c in range(cols):
        if input_grid[0,c] != 0 and input_grid[0,c] != 8: # non-zero and not azure
             for r, c_rec, h_rec, w_rec in rectangles:
                 if c_rec <= c < c_rec + w_rec:
                     # Check if the rectangle is below the non-zero
                     if (r,c_rec) not in moved_pixels:  # prevent overwrite if other pixel moved already
                        output_grid[r, c_rec] = input_grid[0, c]
                        moved_pixels[(r,c_rec)] = input_grid[0,c] # store location and original value
                        break # only do this for the first rectangle

    # Process Left Column Singularities
    for r in range(rows):
      if input_grid[r,0] != 0 and input_grid[r,0] != 8: # non-zero and not azure
        for r_rec, c_rec, h_rec, w_rec in rectangles:
          if r_rec <= r < r_rec + h_rec:
            # check if the rectangle is to the right
            if (r_rec, c_rec) not in moved_pixels: # prevent overwrite if other pixel moved already
              output_grid[r_rec,c_rec] = input_grid[r,0]
              moved_pixels[(r_rec, c_rec)] = input_grid[r,0] # store location and original value
              break  # only do this for the first rectangle


    # Process rectangles based on moved_pixels
    for r, c, height, width in rectangles:
        # skip if a value was already moved there
        if (r,c) not in moved_pixels:

            # check top-left
            if r > 0 and (r - 1, c) in single_pixels:
                output_grid[r, c] = input_grid[r-1, c] # copy single pixel to top-left
                moved_pixels[(r,c)] = input_grid[r-1, c]

            # check left
            elif c > 0 and (r, c-1) in single_pixels:
                output_grid[r,c] = input_grid[r, c-1]
                moved_pixels[(r,c)] = input_grid[r, c-1]
        elif (r,c) in moved_pixels: # Value was moved here - do nothing
            pass # prevents replacing a value moved from top row or left column


    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
6 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
```
Expected Output:
```
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
6 0 0 0 6 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
```
Transformed Output:
```
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 8 0 0 0 0
0 0 0 0 6 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
6 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
```
![Transformed Image](1f642eb9-1.png)
match: False
pixels_off: 3
size_correct: True
color_palette_correct: True
correct_pixel_counts: None

## Example 2:
Input:
```
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 2
0 0 0 8 8 8 0 0 0 0
3 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
```
Expected Output:
```
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 6 7 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 2 0 0 0 2
0 0 0 8 8 8 0 0 0 0
3 0 0 3 8 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
```
Transformed Output:
```
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 7 6 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 3 8 0 0 0 2
0 0 0 8 8 8 0 0 0 0
3 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
```
![Transformed Image](1f642eb9-2.png)
match: False
pixels_off: 6
size_correct: True
color_palette_correct: True
correct_pixel_counts: None

## Example 3:
Input:
```
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 6
3 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
2 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 8 6 0 0 0 6
3 0 0 3 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
2 0 0 2 8 8 0 0 0 0
0 0 0 7 8 2 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 3 8 0 0 0 6
3 0 0 8 2 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
2 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
```
![Transformed Image](1f642eb9-3.png)
match: False
pixels_off: 7
size_correct: True
color_palette_correct: True
correct_pixel_counts: None
