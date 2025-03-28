
Previous Code:
```python
import numpy as np

"""
Identifies a central horizontal block of gray (5) pixels by finding the minimum and maximum row indices containing gray.
For each colored pixel (green 3, red 2, blue 1) found outside the row range of this block:
- If the pixel is above the block (row < min_gray_row), it casts a gray (5) imprint onto the cell in the row immediately above the block (min_gray_row - 1) in the same column.
- If the pixel is below the block (row > max_gray_row), it casts a gray (5) imprint onto the cell in the row immediately below the block (max_gray_row + 1) in the same column.
After processing all imprints, all original colored pixels (1, 2, and 3) are removed (changed to white 0) in the output.

Note: This logic assumes a clear main horizontal block exists and does not touch the top/bottom grid edges simultaneously, as seen in examples 2 and 3. Example 1 might follow a different rule or require a more nuanced definition of the "block" boundaries if the simple min/max row approach covers the entire grid height. This implementation prioritizes the pattern observed in examples 2 and 3.
"""

def find_gray_block_boundaries(grid):
    """
    Finds the top-most and bottom-most row indices containing gray (5) pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (min_row, max_row) or (None, None) if no gray pixels are found.
    """
    gray_rows = np.where(grid == 5)[0]
    if len(gray_rows) == 0:
        return None, None
    # Convert numpy integers to standard Python integers
    return int(np.min(gray_rows)), int(np.max(gray_rows))

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Find the boundaries of the gray block based on row indices
    min_gray_row, max_gray_row = find_gray_block_boundaries(input_np)

    # If no gray block exists, return the original grid copy
    if min_gray_row is None:
        return output_np.tolist()

    # --- Step 1: Create Gray Imprints ---
    # Iterate through each cell of the input grid to find source pixels
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]

            # Check if the pixel is one of the source colors (1, 2, 3)
            if color in [1, 2, 3]:
                # Check if the pixel is above the gray block's row range
                if r < min_gray_row:
                    # Calculate the target row for the imprint (just above the block)
                    target_r = min_gray_row - 1
                    # Ensure the target row is within grid bounds
                    if 0 <= target_r < height:
                        # Place the gray imprint in the output grid
                        output_np[target_r, c] = 5
                # Check if the pixel is below the gray block's row range
                elif r > max_gray_row:
                    # Calculate the target row for the imprint (just below the block)
                    target_r = max_gray_row + 1
                    # Ensure the target row is within grid bounds
                    if 0 <= target_r < height:
                        # Place the gray imprint in the output grid
                        output_np[target_r, c] = 5

    # --- Step 2: Remove Original Colored Pixels ---
    # Iterate through the grid again to remove original 1, 2, 3 pixels
    # This is done in a separate pass to ensure imprints are not accidentally removed
    # if they landed on a location that originally held a colored pixel (although unlikely with this rule).
    for r in range(height):
        for c in range(width):
            # Check the color in the *original* input grid
            if input_np[r, c] in [1, 2, 3]:
                # Change the pixel location to white in the output grid
                output_np[r, c] = 0

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 5 5 5 5 5 0 0 0 3 0
0 0 0 0 5 5 5 5 5 3 0 0 0 0
0 0 0 3 5 5 5 5 5 0 0 3 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
3 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 3 0 3 0
0 3 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 3 0 5 5 5 5 5 0 0 0 3 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 3 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.224489795918373

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 5 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 5 0 0 5 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 5 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 5 0 0 5 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.0204081632653015

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 1 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 5 5 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 5 0 5 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 5 5 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 2.040816326530603
