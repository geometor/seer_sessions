```python
import numpy as np
import copy

"""
Transforms an input grid based on a row-specific condition determined by the pixel color in column index 2 (the 'control column'). The transformation affects only the pixels to the right of column index 3 (the 'separator column').

1.  Identify the background color (orange, 7).
2.  Identify the control column index (2) and the separator column index (3).
3.  Create an output grid initialized as a copy of the input grid.
4.  Iterate through each row `r` of the grid.
5.  Get the color of the control pixel for the current row: `control_color = input[r, 2]`.
6.  Check the control color against the background color:
    a.  If `control_color` is NOT the background color (7), then modify the output grid: For all columns `c` greater than the separator index (c > 3), set `output[r, c]` to the background color (7).
    b.  If `control_color` IS the background color (7), then make no changes to the output grid for that row in columns `c > 3`. The pixels remain as they were copied from the input.
7.  Pixels in columns 0 through 3 (inclusive) are never modified and retain their original input values.
8.  Return the modified output grid.

Note: This rule represents the most consistent pattern observed across the training examples (primarily derived from Ex2 and Ex3), but it does not perfectly match all provided examples, especially Example 1 and specific rows in Example 2 and 3 where the control pixel is white (0).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the control pixel in column 2.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to a numpy array for easier slicing and modification
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid
    output_np = np.copy(input_np)
    
    # Define constants based on observations
    background_color = 7
    control_column_index = 2
    separator_column_index = 3
    
    # Get grid dimensions
    num_rows, num_cols = input_np.shape
    
    # Iterate through each row
    for r in range(num_rows):
        # Get the color of the control pixel for this row
        control_pixel_color = input_np[r, control_column_index]
        
        # Check the condition: if the control pixel is NOT the background color
        if control_pixel_color != background_color:
            # Modify the right region (columns > separator_column_index)
            # Set all pixels in this region to the background color
            # Ensure we don't try to write past the last column if separator_column_index is near the edge
            if separator_column_index + 1 < num_cols:
                 output_np[r, separator_column_index + 1:] = background_color
        # else: (control_pixel_color == background_color)
            # If the control pixel IS the background color, do nothing to the right region.
            # The output row already contains the copied values from the input.
            pass 
            
    # Convert the result back to a list of lists format
    output_grid = output_np.tolist()
    
    return output_grid

```