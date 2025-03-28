
Previous Code:
```python
import numpy as np

"""
Transformation Rule:
1. Identify the two unique non-white pixel values (colors) present in the input grid. Let these be color1 and color2.
2. Create an output grid of the same dimensions as the input grid.
3. Iterate through each pixel of the input grid.
4. If the input pixel's color is color1, set the corresponding output pixel to color2.
5. If the input pixel's color is color2, set the corresponding output pixel to color1.
6. If the input pixel's color is white (0), keep the corresponding output pixel as white (0).
7. Return the completed output grid.
"""

def find_non_white_colors(grid_np):
    """
    Finds the unique non-white (non-zero) colors in a numpy grid.

    Args:
        grid_np: A numpy array representing the grid.

    Returns:
        A list of unique non-white colors found in the grid.
        Returns an empty list if no non-white colors are found.
    """
    unique_values = np.unique(grid_np)
    non_white_colors = unique_values[unique_values != 0]
    return non_white_colors.tolist()

def transform(input_grid):
    """
    Swaps the two non-white colors found in the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid with the two non-white
        colors swapped. White pixels remain unchanged. If fewer than two 
        non-white colors are present, the original grid is returned.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)

    # Find the unique non-white colors in the input grid
    non_white_colors = find_non_white_colors(input_np)

    # Check if exactly two non-white colors were found
    if len(non_white_colors) != 2:
        # If not exactly two, return the original grid as a list of lists
        # (This covers cases with 0 or 1 non-white color, where no swap occurs,
        # and potentially unexpected cases with >2 colors based on the examples provided)
        return input_np.tolist() 
        
    color1, color2 = non_white_colors[0], non_white_colors[1]

    # Create a copy of the input grid to modify for the output
    # Using np.copy ensures we don't alter the original input array inadvertently
    output_np = np.copy(input_np)

    # Create boolean masks to identify the locations of color1 and color2
    mask_color1 = (input_np == color1)
    mask_color2 = (input_np == color2)

    # Apply the swap:
    # Where the input was color1, set the output to color2
    output_np[mask_color1] = color2
    # Where the input was color2, set the output to color1
    output_np[mask_color2] = color1
    # White pixels (0) remain unchanged as they are not selected by either mask

    # Convert the resulting numpy array back to a list of lists for the final output
    return output_np.tolist()

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 3 0 3 0 0
0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 8 0 0 0
0 8 8 8 0 8 8 8 0 0
0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 8 0 8 0 8 0 8 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 15
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 33.333333333333314

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 2 2 0 2 2 0 0 0
0 2 0 0 2 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 3 0 0 0
0 0 0 0 2 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 3 0 0 0
0 3 3 0 3 3 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 2 2 0 0 0
0 0 0 0 3 3 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 3 3 0 3 3 0 0 0
0 3 0 0 3 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 2 0 0 0
0 0 0 0 3 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 9.259259259259252

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 1 0 0 0 7 0
0 0 1 0 0 1 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 1 0 0
0 7 0 0 7 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 7 0 0 7 0 0 0 1 0
0 0 7 0 0 7 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 18.181818181818173

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 8 8 8 0 0 0 0
0 0 8 0 0 0 0 1 1 1 0 0 0 0 8 0 0
0 8 8 8 0 0 0 0 1 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0
0 1 1 1 0 0 0 0 8 0 0 0 0 1 1 1 0
0 0 1 0 0 0 0 8 8 8 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 0
0 0 1 0 0 0 0 8 8 8 0 0 0 0 1 0 0
0 1 1 1 0 0 0 0 8 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 15.686274509803923
