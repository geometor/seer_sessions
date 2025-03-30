
Previous Code:
```python
import numpy as np
from collections import deque

"""
Horizontally shift the single colored object to the left based on its position relative to its bounding box.

1. Find the single connected group of non-white pixels (the "object") in the input grid. Record its color. If no object exists, return an empty grid of the same size.
2. Determine the bounding box of the object, specifically identifying the minimum row index (`min_row`) and minimum column index (`min_col`).
3. Find the actual top-leftmost pixel of the object. This is the pixel within the object that has the row index `min_row` and the smallest column index among pixels in that row. Let this column index be `top_pixel_col`.
4. Calculate the horizontal shift amount, `delta_c`, based on the following condition:
   a. If the object occupies the top-left corner of its bounding box (i.e., if `min_col` is equal to `top_pixel_col`), then the shift amount `delta_c` is equal to `min_col`.
   b. Otherwise (if `min_col` is less than `top_pixel_col`), the shift amount `delta_c` is calculated as `min_row + (top_pixel_col - min_col)`.
5. Create a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
6. Copy the object onto the output grid by taking each pixel `(r, c)` of the object from the input grid and placing its color at the coordinates `(r, c - delta_c)` in the output grid. Ensure that the destination column `c - delta_c` is not less than 0.
"""

def find_colored_object(grid):
    """
    Finds the first connected non-background object in the grid using BFS.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple containing:
        - set of (row, col) tuples for the object's pixels.
        - the color of the object (int).
        Returns (None, None) if no object is found.
    """
    rows, cols = grid.shape
    visited = set()
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and (r, c) not in visited:
                object_color = grid[r, c]
                object_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    object_pixels.add((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == object_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                # Found the first (and assumed only) object
                return object_pixels, object_color

    return None, None # No object found


def get_object_properties(pixels):
    """
    Calculates bounding box and top-left pixel properties.

    Args:
        pixels: A set of (row, col) tuples representing the object pixels.

    Returns:
        A tuple (min_row, min_col, top_pixel_row, top_pixel_col).
        Returns (None, None, None, None) if pixels is empty.
    """
    if not pixels:
        return None, None, None, None

    # Find bounding box top-left corner
    min_row = min(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    
    # top_pixel_row is the same as min_row by definition of top-leftmost
    top_pixel_row = min_row 
    
    # Find the minimum column among pixels *only in the top row*
    top_pixel_col = min(c for r, c in pixels if r == top_pixel_row)

    return min_row, min_col, top_pixel_row, top_pixel_col


def transform(input_grid):
    """
    Transforms the input grid by shifting the single colored object left.
    The shift amount depends on the object's position relative to its bounding box
    and potentially the top row index of the bounding box.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output_grid with background color (0)
    output_grid = np.zeros_like(input_np)

    # Step 1: Identify the single connected non-white object
    object_pixels, object_color = find_colored_object(input_np)

    # Handle case where no object is found
    if object_pixels is None:
        return output_grid.tolist() # Return background grid

    # Step 2 & 3: Determine bounding box and top-leftmost pixel properties
    min_row, min_col, top_pixel_row, top_pixel_col = get_object_properties(object_pixels)

    # Step 4: Calculate the horizontal shift amount delta_c
    if min_col == top_pixel_col:
        # Case a: Object occupies top-left corner of bounding box
        delta_c = min_col
    else:
        # Case b: Top-left corner of bounding box is empty
        delta_c = min_row + (top_pixel_col - min_col)
        
    # Step 5: Output grid initialized previously.

    # Step 6: Place the shifted object onto the output grid
    for r, c in object_pixels:
        # Calculate new position (vertical position unchanged)
        new_r = r
        new_c = c - delta_c
        
        # Ensure the new column coordinate is within the grid bounds
        if 0 <= new_c < cols:
            output_grid[new_r, new_c] = object_color

    # Convert numpy array back to list of lists for the required output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 0 2 2 0 0 2 0 0 0 0
0 0 0 0 0 2 0 0 2 2 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 2 0 0 0 0 0 0 0
0 0 0 2 0 0 2 2 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0
2 2 0 0 2 0 0 0 0 0 0 0 0
0 2 0 0 2 2 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 23
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 32.16783216783216

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 14.545454545454547

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 3 3 0 3 3 0 0
0 0 0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0 0 0 0 0
0 0 0 0 3 3 0 3 3 0 0 0 0
0 0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0 0 0 0
0 0 3 3 0 3 3 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 22
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 16.92307692307692

## Example 4:
Input:
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0
8 8 8 0 0 0 0
0 8 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0
8 8 8 0 0 0 0
8 8 8 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 4.081632653061234

## Example 5:
Input:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0
0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 8 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 23.636363636363626
