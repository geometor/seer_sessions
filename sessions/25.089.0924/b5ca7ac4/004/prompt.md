
Previous Code:
```python
import numpy as np

"""
Transforms the input grid by conceptually dividing it into a 3x3 grid of nine 
rectangular regions. The regions might not have exactly the same dimensions due 
to integer division. The content (pixels) of each input region is copied to a 
different region in the output grid according to a fixed permutation map. 
The output grid has the same dimensions as the input grid.

The permutation map (input region index (row, col) -> output region index (row, col)), 
using 0-based indexing, is:
(0,0) -> (0,0)
(0,1) -> (0,2)
(0,2) -> (1,0)
(1,0) -> (1,1)
(1,1) -> (1,2)
(1,2) -> (2,1)
(2,0) -> (2,2)
(2,1) -> (2,0)
(2,2) -> (0,1)
"""

def transform(input_grid):
    """
    Permutes the content of a 3x3 division of the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed grid.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Get dimensions of the input grid
    H, W = input_np.shape

    # Initialize the output grid with the same dimensions, filled with zeros initially
    # The permutation will overwrite these values. Using the background color might
    # be slightly more robust if the background isn't always 0, but the permutation
    # covers the whole grid, so zeros are fine.
    output_np = np.zeros_like(input_np)

    # Calculate the row and column division points for the 3x3 grid
    # These points define the start of the second and third row/column of regions
    r1 = H // 3
    r2 = 2 * H // 3
    c1 = W // 3
    c2 = 2 * W // 3

    # Define the row start and end points for the 3 region rows
    row_boundaries = [0, r1, r2, H]
    
    # Define the column start and end points for the 3 region columns
    col_boundaries = [0, c1, c2, W]

    # Define the permutation map: input region (row, col) -> output region (row, col)
    # Using 0-based indices for rows and columns (0, 1, 2)
    permutation_map = {
        (0, 0): (0, 0),
        (0, 1): (0, 2),
        (0, 2): (1, 0),
        (1, 0): (1, 1),
        (1, 1): (1, 2),
        (1, 2): (2, 1),
        (2, 0): (2, 2),
        (2, 1): (2, 0),
        (2, 2): (0, 1)
    }

    # Iterate through the 3x3 grid regions of the input
    for r_in in range(3):
        for c_in in range(3):
            # Determine the pixel boundaries for the current input region
            start_row_in = row_boundaries[r_in]
            end_row_in = row_boundaries[r_in + 1]
            start_col_in = col_boundaries[c_in]
            end_col_in = col_boundaries[c_in + 1]

            # Extract the subgrid data from the input region
            input_subgrid = input_np[start_row_in:end_row_in, start_col_in:end_col_in]

            # Get the corresponding output region indices from the map
            r_out, c_out = permutation_map[(r_in, c_in)]

            # Determine the pixel boundaries for the target output region
            # We only need the top-left corner to place the extracted subgrid
            start_row_out = row_boundaries[r_out]
            end_row_out = row_boundaries[r_out + 1] # Not strictly needed for pasting, but defines the region
            start_col_out = col_boundaries[c_out]
            end_col_out = col_boundaries[c_out + 1] # Not strictly needed for pasting, but defines the region
            
            # Check if the shape matches (debugging check, should match if logic is correct)
            # target_shape = (end_row_out - start_row_out, end_col_out - start_col_out)
            # if input_subgrid.shape != target_shape:
            #     print(f"Shape mismatch! Input ({r_in},{c_in}) shape {input_subgrid.shape} -> Output ({r_out},{c_out}) shape {target_shape}")

            # Paste the extracted input subgrid into the output grid at the target location
            output_np[start_row_out:start_row_out + input_subgrid.shape[0], 
                      start_col_out:start_col_out + input_subgrid.shape[1]] = input_subgrid

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 8 8 8 8 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 8 8 8 8 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 8 3 3 3 8 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
2 6 6 6 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 6 6 6 2 0 0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0
2 6 6 6 2 2 2 2 2 2 0 0 8 4 4 4 8 0 0 0 0 0
2 2 2 2 2 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 5 5 5 8 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
8 5 5 5 8 8 8 8 8 8 0 0 0 0 0 0 0 2 1 1 1 2
8 5 5 5 8 8 3 3 3 8 0 0 0 0 0 0 0 2 1 1 1 2
8 8 8 8 8 8 3 3 3 8 0 0 0 0 0 0 0 2 1 1 1 2
0 0 0 0 0 8 3 3 3 8 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 8 8 8 8 8 0 0 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0 0
8 4 4 4 8 0 0 0 0 0 0 0 2 6 6 6 2 2 2 2 2 2
8 4 4 4 8 0 0 0 0 0 0 0 2 2 2 2 2 2 4 4 4 2
8 4 4 4 8 0 0 0 0 0 0 0 0 0 0 0 0 2 4 4 4 2
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 2 4 4 4 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 4 4 8 0 0 0 0 0 0 2 2 2 2 2 0
0 8 5 5 5 8 0 4 4 8 0 0 0 0 0 0 2 1 1 1 2 0
0 8 5 5 5 8 0 4 4 8 0 0 0 0 0 0 2 1 1 1 2 0
0 8 8 8 8 8 0 8 8 8 0 0 0 0 0 0 2 1 1 1 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 2 0
0 8 8 8 8 8 0 0 0 0 0 2 3 3 3 2 0 0 0 0 2 0
0 8 3 3 3 8 0 0 0 0 0 2 2 2 2 2 0 0 0 0 2 0
0 8 3 3 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0
0 8 3 3 3 8 0 2 2 2 2 2 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0 2 6 6 6 2 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0
2 2 2 0 0 8 4 2 2 2 2 0 0 0 2 6 6 6 2 2 2 0
4 4 2 0 0 8 4 9 9 9 2 0 0 0 2 2 2 2 2 2 4 0
4 4 2 0 0 8 4 9 9 9 2 0 0 0 0 0 0 0 0 2 4 0
4 4 2 0 0 8 8 9 9 9 2 0 0 0 0 0 0 0 0 2 4 0
2 2 2 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 219
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 90.49586776859503

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4 4 4 4 4 4
4 4 8 8 8 8 8 4 2 5 5 5 2 4 2 2 2 2 2 4 4 4
4 4 8 9 9 9 8 4 2 5 5 5 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 2 2 2 2 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 4 4 4 4 4 4 2 3 3 3 2 4 4 4
4 4 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 4 8 1 1 1 8 4 4 4 4 4 4 4 2 1 1 1 2 4 4 4
4 4 8 1 1 1 8 4 8 8 8 8 8 4 2 1 1 1 2 4 4 4
4 4 8 1 1 1 8 4 8 6 6 6 8 4 2 1 1 1 2 4 4 4
4 4 8 8 8 8 8 4 8 6 6 6 8 4 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 2 5 5 5 2 2 2 2 2 2
8 9 9 9 8 4 4 4 4 4 4 4 2 5 5 5 2 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 2 2 2 2 2 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 2 3 3 3 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 1 1 1 8 4 4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 2
8 1 1 1 8 8 8 8 8 8 4 4 4 4 4 4 4 2 1 1 1 2
8 1 1 1 8 8 6 6 6 8 4 4 4 4 4 4 4 2 1 1 1 2
8 8 8 8 8 8 6 6 6 8 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 2 2 2 2 2 4 0
4 4 4 4 4 4 4 2 1 1 1 2 4 4 4 2 5 5 5 2 4 0
4 4 8 8 8 8 8 2 1 1 1 2 4 4 4 2 5 5 5 2 4 0
4 4 8 9 9 9 8 2 1 1 1 2 4 4 4 2 5 5 5 2 4 0
4 4 8 9 9 9 8 2 2 2 2 2 4 4 4 2 2 2 2 2 4 0
4 4 8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 0
2 2 2 2 2 4 4 8 3 3 3 8 4 4 4 4 4 4 4 4 4 0
2 3 3 3 2 4 4 8 3 3 3 8 4 4 4 4 4 4 4 4 4 0
2 3 3 3 2 4 4 8 3 3 3 8 4 4 4 4 4 4 4 4 4 0
2 3 3 3 2 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 0
2 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8 8 8 8 8 0
4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 8 1 1 1 8 0
4 8 8 8 8 8 4 4 4 2 6 6 6 2 4 4 8 1 1 1 8 0
4 8 6 6 6 8 4 4 4 2 6 6 6 2 4 4 8 1 1 1 8 0
4 8 6 6 6 8 4 4 4 2 6 6 6 2 4 4 8 8 8 8 8 0
4 8 6 6 6 8 4 4 4 2 2 2 2 2 4 4 4 4 4 4 4 0
4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0
```
Match: False
Pixels Off: 285
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 235.53719008264463

## Example 3:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 2 2 2 2 2 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 2 2 2 2 1 1 1 1 1 1 1 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 1 1 8 8 8 8 8 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 2 4 4 4 2 1 1 1 1 1 1 1 2 2 0
1 1 1 8 8 8 8 2 4 4 4 2 1 1 1 1 1 1 1 2 3 0
1 1 1 8 2 2 2 2 2 2 2 2 1 1 1 1 1 1 1 2 3 0
1 1 1 8 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 2 3 0
1 1 1 8 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 2 2 0
1 1 1 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 8 8 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 6 0
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 6 0
3 3 2 1 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1 8 6 0
3 3 2 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1 8 8 0
3 3 2 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1 1 1 0
2 2 2 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1 1 1 0
8 8 8 1 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1 1 1 0
6 6 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
8 8 8 8 8 1 1 6 6 8 1 1 1 1 1 1 1 1 1 1 1 0
8 3 3 3 8 1 1 6 6 8 1 1 1 1 1 1 1 1 1 1 1 0
8 3 3 3 8 1 1 8 8 8 1 1 1 1 1 1 1 1 1 1 1 0
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
1 1 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1 1 1 1 1 0
1 1 1 1 1 1 1 2 4 4 4 2 1 1 1 1 1 1 1 1 1 0
1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0
```
Match: False
Pixels Off: 213
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 176.03305785123968
