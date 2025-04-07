
Previous Code:
```python
import numpy as np

"""
Transformation Rule:
1. Identify the color of the pixel at the top-left corner (0, 0) - the anchor color.
2. Determine a vertical shift amount based on the anchor color using a predefined mapping:
   - Maroon (9) -> shift 0
   - Yellow (4) -> shift 3
   - Magenta (6) -> shift 2
   - Orange (7) -> shift 5
   - Default: shift 0 for any other color.
3. Initialize an output grid of the same dimensions as the input, filled with the background color (white, 0).
4. Copy the anchor pixel from input (0, 0) to output (0, 0).
5. Iterate through all pixels in the input grid, excluding the anchor pixel at (0, 0).
6. For each non-background pixel found at (row, col):
   a. Calculate its new row position: new_row = row + shift.
   b. If the new_row is within the grid's height boundaries:
      i. Copy the pixel's color to the output grid at (new_row, col).
7. Return the resulting output grid.
"""

def transform(input_grid):
    """
    Applies a vertical shift to non-anchor, non-background pixels based on the
    color of the anchor pixel at (0, 0).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize the output grid with the background color (0)
    output_array = np.zeros_like(input_array)

    # 1. Identify the anchor color
    anchor_color = input_array[0, 0]

    # 2. Determine the vertical shift amount based on the anchor color
    shift_map = {
        9: 0,  # Maroon
        4: 3,  # Yellow
        6: 2,  # Magenta
        7: 5   # Orange
    }
    shift = shift_map.get(anchor_color, 0) # Default shift is 0

    # 3. Copy the anchor pixel to the output grid
    output_array[0, 0] = anchor_color

    # 4. Iterate through all pixels in the input grid, excluding the anchor
    for r in range(height):
        for c in range(width):
            # Skip the anchor pixel itself
            if r == 0 and c == 0:
                continue

            # Get the color of the current pixel
            pixel_color = input_array[r, c]

            # 5. Process non-background pixels
            if pixel_color != 0:
                # a. Calculate the new row position
                new_r = r + shift

                # b. Check if the new row is within grid bounds
                if 0 <= new_r < height:
                    # c. Copy the pixel to the new location in the output grid
                    # Check if the target pixel is currently background (0).
                    # This handles potential overlaps where later pixels might overwrite earlier ones
                    # if they shift to the same spot. Based on examples, direct overwrite seems intended.
                    output_array[new_r, c] = pixel_color

    # Convert the NumPy array back to a list of lists for the standard ARC format
    return output_array.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
```
Expected Output:
```
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
```
Transformed Output:
```
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
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
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 9 4 4 4 7 0 2 3 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 6 5 5 0 1 7 7 7 7 4 0
0 6 0 5 0 1 0 0 0 0 4 0
0 6 0 5 0 1 0 0 0 0 4 0
```
Expected Output:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 9 0 0 2 0 0 0 8 0 0
0 0 9 0 0 2 0 0 0 8 0 0
0 0 9 0 0 2 7 0 2 8 0 0
0 6 5 5 0 1 7 0 2 3 3 0
0 6 0 5 0 1 7 0 2 0 3 0
0 6 0 5 0 1 7 7 7 7 3 0
```
Transformed Output:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 9 4 4 4 7 0 2 3 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 0 9 0 0 0 7 0 2 0 3 0
```
Match: False
Pixels Off: 22
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 30.55555555555557

## Example 3:
Input:
```
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 9 4 4 4 7 0 2 3 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 6 5 5 0 1 7 7 7 7 4 0
0 6 0 5 0 1 0 0 0 0 4 0
0 6 0 5 0 1 0 0 0 0 4 0
```
Expected Output:
```
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 7 0 2 3 3 0
0 0 0 0 0 2 7 0 2 0 3 0
0 0 9 4 4 4 7 0 2 0 3 0
0 0 9 5 0 1 7 7 7 7 4 0
0 0 9 5 0 1 0 0 0 0 4 0
0 0 5 5 0 1 0 0 0 0 4 0
```
Transformed Output:
```
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 9 4 4 4 7 0 2 3 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 6 5 5 0 1 7 7 7 7 4 0
```
Match: False
Pixels Off: 27
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 37.5

## Example 4:
Input:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
```
Expected Output:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 7 0
0 0 6 0 0 3 0 5 0 7 7 0
0 0 6 0 0 3 0 5 0 7 7 0
0 0 2 2 2 2 2 2 2 2 7 0
```
Transformed Output:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.555555555555571

## Example 5:
Input:
```
7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
```
Expected Output:
```
7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 4 6 3 3 3 0 5 1 0 0 0
0 4 6 0 0 3 0 5 1 0 0 0
0 4 6 0 0 3 0 5 5 0 0 0
0 4 2 2 2 2 2 2 2 2 0 0
```
Transformed Output:
```
7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
```
Match: False
Pixels Off: 26
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 36.111111111111114
