
Previous Code:
```python
import numpy as np

"""
Processes a grid based on a central horizontal axis defined by non-white pixels. 
1. Initialize an output grid of the same size as the input grid, filled entirely with white (0).
2. Identify all non-white pixels in the input grid. If none, return the white grid.
3. Find the unique row indices containing non-white pixels ('active_rows') and sort them.
4. Determine the 'middle_row' as the median row index from 'active_rows'.
5. Find all non-white pixels from the input grid located on this 'middle_row'.
6. Identify the 'fill_color' as the color of the leftmost non-white pixel on the 'middle_row'.
7. Fill the entire 'middle_row' in the output grid with the 'fill_color'.
8. Overlay the original non-white pixels from the input's 'middle_row' onto the output's 'middle_row'.
9. For each non-white pixel in the input grid:
    - If its row is above the 'middle_row', project its color diagonally up and to the left onto the output grid until a boundary is hit.
    - If its row is below the 'middle_row', project its color diagonally down and to the left onto the output grid until a boundary is hit.
    - Pixels on the 'middle_row' are not projected.
10. Return the final output grid.
"""

def find_non_white_pixels(grid):
    """Finds all non-white pixels and returns their coordinates and colors."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                pixels.append(((r, c), color))
    return pixels

def project_up_left(grid, r_start, c_start, color):
    """Projects a color diagonally up-left from (r_start, c_start) onto the grid."""
    rows, cols = grid.shape
    r, c = r_start, c_start
    while r >= 0 and c >= 0:
        grid[r, c] = color
        r -= 1
        c -= 1

def project_down_left(grid, r_start, c_start, color):
    """Projects a color diagonally down-left from (r_start, c_start) onto the grid."""
    rows, cols = grid.shape
    r, c = r_start, c_start
    while r < rows and c >= 0:
        grid[r, c] = color
        r += 1
        c -= 1

def transform(input_grid):
    """
    Applies transformations based on a median 'middle row'.
    Pixels above the middle row project up-left.
    Pixels below the middle row project down-left.
    The middle row is filled based on its *leftmost* pixel, then overlaid with original middle row pixels.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    # 1. Initialize output grid
    output_grid = np.zeros_like(input_grid_np) # Initialize with white (0)

    # 2. Identify all non-white pixels
    non_white_pixels = find_non_white_pixels(input_grid_np)

    # Handle empty input
    if not non_white_pixels:
        return output_grid.tolist() # Return empty white grid

    # 3. Collect and sort active rows
    active_rows = sorted(list(set(r for (r, c), color in non_white_pixels)))

    # Should not happen if non_white_pixels is not empty, but safeguard
    if not active_rows:
         return output_grid.tolist() 

    # 4. Determine the middle row (median row index)
    middle_row_list_index = len(active_rows) // 2
    middle_row = active_rows[middle_row_list_index]

    # 5. Find pixels located on the middle row in the input
    middle_row_pixels = [((r, c), color) for (r, c), color in non_white_pixels if r == middle_row]

    # 6. Determine the fill color from the *leftmost* pixel on the middle row
    fill_color = 0 # Default to white if middle row has no pixels (unlikely)
    if middle_row_pixels:
        leftmost_col = cols # Start higher than any possible column index
        # Find the pixel with the minimum column index
        for (r, c), color in middle_row_pixels:
            if c < leftmost_col:
                leftmost_col = c
                fill_color = color
        
        # 7. Fill the entire middle row with the fill color
        output_grid[middle_row, :] = fill_color

        # 8. Overlay original pixels from the middle row onto the filled row
        for (r, c), color in middle_row_pixels:
             # This overwrites the fill color at these specific columns
            output_grid[r, c] = color
            
    # 9. Process all non-white pixels for projection
    for (r, c), color in non_white_pixels:
        if r < middle_row:
            # Project pixels above the middle row up-left
            project_up_left(output_grid, r, c, color)
        elif r > middle_row:
            # Project pixels below the middle row down-left
            project_down_left(output_grid, r, c, color)
        # else: r == middle_row -> Do nothing, handled by fill/overlay

    # 10. Return the final grid
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 5 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 2 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 2 2 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 5 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 6 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 2 2 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 5 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 51
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.5

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 1 2 0 0 0 0
0 0 0 2 6 2 0 0 0 0
0 0 0 2 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 3 0 0 1 0 0 2 0 0
0 0 3 0 1 0 2 0 0 0
0 0 0 3 1 2 0 0 0 0
2 2 2 2 6 2 2 2 2 2
0 0 0 2 7 7 0 0 0 0
0 0 2 0 7 0 7 0 0 0
0 2 0 0 7 0 0 7 0 0
2 0 0 0 7 0 0 0 7 0
0 0 0 0 7 0 0 0 0 7
0 0 0 0 7 0 0 0 0 0
```
Transformed Output:
```
0 3 1 2 0 0 0 0 0 0
0 0 3 1 2 0 0 0 0 0
0 0 0 3 1 2 0 0 0 0
2 2 2 2 6 2 2 2 2 2
0 0 0 2 7 7 0 0 0 0
0 0 2 7 7 0 0 0 0 0
0 2 7 7 0 0 0 0 0 0
2 7 7 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 23
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 23.0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 5 7 0 0 0 0 0 0 0 0 0 0
0 0 2 8 7 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 2 0 5 0 7 0 0 0 0 0 0 0 0 0
0 0 2 5 7 0 0 0 0 0 0 0 0 0 0
2 2 2 8 7 7 7 7 7 7 7 7 7 7 7
0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 3 0 0 0 0 0 0 0 0 0
3 0 0 3 0 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 3 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 3 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 3 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 3
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 2 5 7 0 0 0 0 0 0 0 0 0 0 0
0 0 2 5 7 0 0 0 0 0 0 0 0 0 0
2 2 2 8 7 2 2 2 2 2 2 2 2 2 2
0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 39
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 34.66666666666666
