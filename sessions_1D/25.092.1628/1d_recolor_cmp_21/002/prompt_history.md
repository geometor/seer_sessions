
## train_1

**input:**
```
0 8 8 8 8 8 0 0 0 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8
```


**output:**
```
0 8 8 8 8 8 0 0 0 5 5 5 5 5 5 5 0 0 8 8 8 8 8 8
```


## train_2

**input:**
```
0 8 8 8 8 8 0 0 8 8 8 8 0 8 0 0 0 8 8 8 8 8 0 0
```


**output:**
```
0 5 5 5 5 5 0 0 8 8 8 8 0 8 0 0 0 5 5 5 5 5 0 0
```


## train_3

**input:**
```
0 0 0 8 8 8 8 0 8 8 0 0 0 8 8 8 0 0 8 0 0 0 0 0
```


**output:**
```
0 0 0 5 5 5 5 0 8 8 0 0 0 8 8 8 0 0 8 0 0 0 0 0
```

## Perception
The input and output are both single rows of pixels. The input contains blocks of azure (8) pixels separated by white (0) pixels. The output is largely the same as the input, except for one specific block of azure pixels. This block, which originally consisted of seven consecutive azure pixels, has been changed to gray (5) pixels in the output. Other blocks of azure pixels, with lengths of five and six respectively, remain unchanged. The white pixels also remain unchanged. This suggests the transformation rule targets contiguous horizontal blocks of azure pixels based on their length. Specifically, blocks of azure pixels with a length of exactly seven are transformed into blocks of gray pixels of the same length.

## Facts


```yaml
elements:
  - type: pixel_grid
    description: A single row of pixels.
  - type: color
    values: [white (0), azure (8), gray (5)]
  - type: object
    identifier: contiguous_horizontal_block
    description: A sequence of one or more pixels of the same color along the row.
    properties:
      - color: azure (8) or gray (5)
      - length: count of pixels in the block

transformation:
  - action: identify
    target: contiguous_horizontal_blocks
    properties:
      - color: azure (8)
  - action: filter
    criteria: length == 7
    target: identified_azure_blocks
  - action: change_color
    target: filtered_azure_blocks
    from_color: azure (8)
    to_color: gray (5)
  - action: keep
    target: all other pixels (white pixels and azure blocks not matching the filter criteria)
    properties:
      - color: unchanged

relationships:
  - type: positional_invariance
    description: The positions of white pixels and unchanged azure blocks are preserved.
  - type: size_invariance
    description: The length of the transformed block remains the same, only the color changes.
```


## Natural Language Program

1.  Identify all contiguous horizontal blocks of azure (8) pixels in the input row.
2.  For each identified azure block, determine its length (number of pixels).
3.  If an azure block has a length exactly equal to 7, change the color of all pixels within that block to gray (5).
4.  Leave all other pixels (white pixels and azure blocks with lengths other than 7) unchanged.
5.  The output row is the result of these changes.
```python
import numpy as np

"""
Identifies contiguous horizontal blocks of azure (8) pixels in the input row.
If an azure block has a length exactly equal to 7, changes the color of all 
pixels within that block to gray (5). Leaves all other pixels unchanged.
Assumes the input grid has only one row.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the specified rule.

    Args:
        input_grid: A numpy ndarray representing the input grid. 
                      Expected to be a single row (1xN shape).

    Returns:
        A numpy ndarray representing the transformed grid.
    """
    
    # Ensure input is a numpy array
    input_grid_np = np.array(input_grid)
    
    # Basic validation for expected 2D shape with at least one row/column
    if input_grid_np.ndim != 2 or input_grid_np.shape[0] == 0 or input_grid_np.shape[1] == 0:
        # Return a copy if input is not as expected (e.g., empty)
        return input_grid_np.copy() 
        
    # The examples and description suggest the input is always a single row.
    # We will process the first row. If multiple rows were present, 
    # this current logic would only modify the first based on the rule.
    input_row = input_grid_np[0, :] # Get the first row
    output_row = input_row.copy() # Create a mutable copy to modify

    row_len = len(output_row)
    i = 0 # Current index scanning through the row
    
    # Iterate through the row to find blocks of azure pixels
    while i < row_len:
        current_color = output_row[i]
        
        # Check if the current pixel is azure (8)
        if current_color == 8:
            start_index = i # Mark the start of a potential azure block
            
            # Find the end of the contiguous block of azure pixels
            j = i
            while j < row_len and output_row[j] == 8:
                j += 1
            # j now points to the first pixel *after* the block or end of row
            
            block_length = j - start_index # Calculate the length of the block
            
            # Apply the transformation rule: change color if length is exactly 7
            if block_length == 7:
                # Change the color of pixels in this block to gray (5)
                output_row[start_index:j] = 5 # Numpy slice assignment
                
            # Move the main index past the processed block
            i = j 
        else:
            # If the current pixel is not azure, just move to the next pixel
            i += 1
                
    # Reshape the modified row back into a 2D grid format (1xN)
    # This assumes the output should maintain the 2D structure, even if it's just one row.
    output_grid = output_row.reshape(1, -1) 
    
    # If the original input had multiple rows, and the intent was to only modify 
    # the first row, this correctly returns the modified first row.
    # If the intent was different (e.g., apply to all rows), the logic would need extension.
    # Based on the provided NL program derived from train_1, this implementation is consistent.
    
    return output_grid
```
