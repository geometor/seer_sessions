
Previous Code:
```python
import numpy as np

"""
Transformation Rule:
1. Create a copy of the input grid to serve as the output grid.
2. Locate the unique Magenta (6) pixel (M) and the unique Maroon (9) pixel (R) in the input grid.
3. Change the color of the pixel at M's coordinates to Maroon (9) in the output grid.
4. Calculate the direction vector (dr, dc) towards M from R: dr = sign(M_row - R_row) and dc = sign(M_col - R_col).
5. Determine the coordinates of the target pixel (T), one step from R towards M: T = (R_row + dr, R_col + dc).
6. Check if the target coordinates T are within the grid boundaries and if the color of the pixel at T in the *input* grid is Gray (5).
7. If both conditions in step 6 are true (the move is valid):
    a. Change the color of the pixel at T's coordinates to Maroon (9) in the output grid.
    b. Change the color of the pixel at R's original coordinates to Gray (5) in the output grid.
8. If the conditions in step 6 are false (the move is invalid or blocked), the pixel at R's original coordinates remains Maroon (9) (as initially copied).
9. Return the modified output grid.
"""

def find_pixel(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the given color."""
    coords = np.argwhere(grid == color)
    if coords.shape[0] > 0:
        # Return as (row, col) tuple
        return tuple(coords[0])
    return None

def sign(x):
    """Returns the sign of a number: -1 for negative, 1 for positive, 0 for zero."""
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier manipulation and copying
    input_np = np.array(input_grid, dtype=int)
    # 1. Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # 2. Locate the unique Magenta (6) pixel (M) and the unique Maroon (9) pixel (R).
    magenta_coord = find_pixel(input_np, 6)
    maroon_coord = find_pixel(input_np, 9)

    # Basic validation: ensure M and R pixels were found
    if magenta_coord is None or maroon_coord is None:
        # This shouldn't happen based on task examples, but return copy if they are missing.
        return output_grid.tolist()

    m_row, m_col = magenta_coord
    r_row, r_col = maroon_coord

    # 3. Change the color of the pixel at M's coordinates to Maroon (9) in the output grid.
    output_grid[m_row, m_col] = 9

    # 4. Calculate the direction vector (dr, dc).
    dr = sign(m_row - r_row)
    dc = sign(m_col - r_col)

    # 5. Determine the coordinates of the target pixel (T).
    t_row = r_row + dr
    t_col = r_col + dc

    # 6. Check if T is within bounds and if the color at T in the *input* grid is Gray (5).
    is_valid_move = False
    if 0 <= t_row < height and 0 <= t_col < width:
        if input_np[t_row, t_col] == 5:
            is_valid_move = True

    # 7. If the move is valid:
    if is_valid_move:
        # 7.a. Change T's color to Maroon (9) in the output.
        output_grid[t_row, t_col] = 9
        # 7.b. Change R's original position to Gray (5) in the output.
        output_grid[r_row, r_col] = 5
    # 8. Else (move is invalid), R's original position remains Maroon (9)
    #    (already set via the initial copy). No action needed here.

    # 9. Return the modified output grid.
    return output_grid.tolist()
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
7 7 7 0 5 5 9 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 7 7 7 0 7 7 7 7
7 7 7 0 7 7 7 0 7 7 7 7
7 7 8 0 7 7 7 0 7 7 9 7
7 7 7 0 7 7 7 0 7 7 7 7
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

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
9 7 0 9 5 5 0 7
7 7 0 5 5 5 0 7
7 7 0 5 5 5 0 7
0 0 0 0 0 0 0 0
7 3 0 7 7 7 0 7
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 3.125

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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
