
## train_1

**input:**
```
2 2 0 0 0 0 0 0 0 0
6 2 0 0 3 0 0 1 0 0
0 0 1 6 0 0 0 0 0 0
0 0 1 1 0 0 6 0 0 6
0 0 0 0 3 3 0 0 0 0
0 3 0 0 3 3 0 1 0 0
0 0 0 0 0 3 4 4 0 0
0 1 0 0 7 0 4 6 0 0
7 0 0 0 0 0 0 0 5 5
0 0 0 0 3 0 0 0 7 5
```


**output:**
```
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 5 5
```


## train_2

**input:**
```
0 0 0 4 0 0 0 4 4 3
0 6 0 0 0 0 0 0 3 3
0 0 0 0 0 0 7 7 0 0
0 0 0 4 0 0 6 7 0 0
4 0 0 0 6 6 0 0 0 0
0 1 0 0 6 8 0 0 0 0
0 0 5 5 0 0 0 0 6 0
0 0 1 5 0 0 6 0 0 0
9 9 0 0 0 0 0 0 0 1
8 9 0 0 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0
```

**Perception:**

1.  **Input/Output Structure:** Both input and output grids are 10x10.
2.  **Color Palette:** Various colors (red, magenta, blue, green, yellow, gray, orange, azure, maroon) are present on a white background in the input. The output retains some of these colors but removes others, replacing them with white.
3.  **Key Feature:** The transformation focuses on identifying and preserving `2x2` blocks of uniform non-white color.
4.  **Transformation:** Pixels that are part of a solid `2x2` block of a single color in the input are kept in the output. All other pixels, including those non-white pixels not part of such a `2x2` block, are turned white (0) in the output.
5.  **Object Identification:** The relevant objects are contiguous `2x2` squares where all four pixels share the same non-white color.
6.  **Rule Consistency:** Both examples demonstrate the same rule: find all `2x2` blocks of a single color and keep only those pixels in the output, setting everything else to white.

**Facts:**


```yaml
Task: Preserve 2x2 blocks
Input_Grid:
  Type: 2D array of integers (0-9)
  Properties:
    - Contains scattered pixels of various colors (1-9) on a white (0) background.
    - Dimensions observed: 10x10 (in examples)
Output_Grid:
  Type: 2D array of integers (0-9)
  Properties:
    - Same dimensions as the input grid.
    - Contains only the pixels that were part of a 2x2 block in the input.
    - All other pixels are white (0).
Objects:
  - Name: Pixel
    Properties:
      - Color (integer 0-9)
      - Position (row, column)
  - Name: 2x2_Block
    Definition: A set of four pixels at positions (r, c), (r+1, c), (r, c+1), (r+1, c+1)
    Properties:
      - All four pixels must have the same non-white color (1-9).
      - Identified by its top-left corner position (r, c).
Transformation:
  Action: Filter pixels based on 2x2 block membership.
  Rule:
    1. Identify all unique 2x2_Blocks in the input grid.
    2. Create an output grid of the same dimensions as the input, initialized with white (0).
    3. For each identified 2x2_Block in the input, copy its four pixels (color and position) to the corresponding positions in the output grid.
Relationship:
  - A pixel in the output grid retains its original color from the input grid if and only if it was part of at least one 2x2_Block in the input grid.
  - Otherwise, the output pixel is set to white (0).
```


**Natural Language Program:**

1.  Create a new grid (the "output grid") with the same dimensions as the input grid, and fill it entirely with the background color (white, 0).
2.  Iterate through each possible top-left corner position `(row, col)` in the input grid, excluding the last row and last column (i.e., `row` from 0 to height-2, `col` from 0 to width-2).
3.  For each `(row, col)`, examine the 2x2 square of pixels starting at this position: `(row, col)`, `(row+1, col)`, `(row, col+1)`, and `(row+1, col+1)`.
4.  Check if all four pixels in this 2x2 square have the *same* color and if this color is *not* the background color (white, 0).
5.  If the condition in step 4 is true (it's a solid, non-white 2x2 block), then copy the color of these four pixels from the input grid to the corresponding positions `(row, col)`, `(row+1, col)`, `(row, col+1)`, and `(row+1, col+1)` in the output grid.
6.  After checking all possible top-left corners, the output grid contains the final result.
```python
"""
Identifies all 2x2 blocks of a single, non-white color within the input grid. 
Creates an output grid of the same dimensions, initially all white. 
Copies the pixels belonging to any identified 2x2 block from the input to the corresponding positions in the output grid. All other positions remain white.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by preserving only the pixels that are part of a 2x2 block 
    of the same non-white color.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier slicing and comparison
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid with the same dimensions as input_grid, filled with white (0)
    output_array = np.zeros_like(input_array)

    # Iterate through each possible top-left corner (r, c) of a 2x2 block
    # We only need to iterate up to height-2 and width-2
    for r in range(height - 1):
        for c in range(width - 1):
            # Get the color of the top-left pixel of the potential 2x2 block
            top_left_color = input_array[r, c]

            # Check if the color is non-white (not 0)
            if top_left_color != 0:
                # Check if all four pixels in the 2x2 block have the same color
                if (input_array[r + 1, c] == top_left_color and
                    input_array[r, c + 1] == top_left_color and
                    input_array[r + 1, c + 1] == top_left_color):
                    
                    # If it's a solid non-white 2x2 block, copy these four pixels to the output grid
                    output_array[r, c] = top_left_color
                    output_array[r + 1, c] = top_left_color
                    output_array[r, c + 1] = top_left_color
                    output_array[r + 1, c + 1] = top_left_color

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid

```
