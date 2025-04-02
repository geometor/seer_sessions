
## train_1

**input:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
```


## train_2

**input:**
```
0 0 0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0
```

## Perception

The input and output are both single rows (1D grids) composed of pixels.
Each input row contains a single contiguous block of non-white pixels (e.g., red '2' or magenta '6') surrounded by white pixels ('0').
The output row contains the exact same block of non-white pixels (same color, same length) as the input, but its position is shifted horizontally to the right.
The surrounding pixels remain white.
By comparing the starting positions of the non-white block in the input and output across all examples, the shift amount is consistently 3 positions to the right.

## Facts


```yaml
task_type: grid_transformation
grid_dimensionality: 1D (single row)

components:
  - type: background
    color: white (0)
    role: static_canvas
  - type: object
    description: A single contiguous block of non-white pixels.
    properties:
      color: variable (e.g., red, magenta)
      length: variable
      position: defined by start and end indices

transformation:
  action: horizontal_shift
  target: the non-white object block
  direction: right
  magnitude: 3 positions
  effect: The start and end indices of the block increase by 3. The color and length remain unchanged. The background remains white.

examples_summary:
  - example: train_1
    object_color: red (2)
    input_start_index: 4
    output_start_index: 7
    shift: 3
  - example: train_2
    object_color: magenta (6)
    input_start_index: 3
    output_start_index: 6
    shift: 3
  - example: train_3
    object_color: magenta (6)
    input_start_index: 7
    output_start_index: 10
    shift: 3
```


## Natural Language Program

1.  Identify the single contiguous block of non-white pixels in the input row. Note its color, length, and starting position.
2.  Create an output row of the same length as the input row, initially filled with white pixels (0).
3.  Place the identified block of non-white pixels into the output row, starting 3 positions to the right of its original starting position in the input row. Ensure the color and length of the block are preserved.
```python
import numpy as np

"""
Identifies a single contiguous block of non-white pixels in a 1D input grid (row) 
and shifts this block 3 positions to the right in the output grid, preserving 
the block's color and length and keeping the background white.
"""

def find_non_white_block(grid_row):
    """
    Finds the start index, end index (exclusive), and color of the first 
    contiguous block of non-white pixels in a 1D array.

    Args:
        grid_row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (start_index, end_index, color) or (None, None, None) if no block found.
    """
    start_index = -1
    end_index = -1
    color = -1
    
    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1: # Start of a potential block
                start_index = i
                color = pixel
            # Check if the color is consistent with the start of the block
            elif pixel != color: 
                # This handles cases where there might be multiple blocks or colors,
                # but based on examples, we expect only one. We stop at the first block.
                end_index = i 
                break 
        elif start_index != -1: # Found a white pixel after the block started
            end_index = i
            break
            
    # If the block extends to the end of the row
    if start_index != -1 and end_index == -1:
        end_index = len(grid_row)
        
    if start_index != -1:
        return start_index, end_index, color
    else:
        return None, None, None


def transform(input_grid):
    """
    Transforms the input grid by shifting the single non-white block 3 positions 
    to the right.

    Args:
        input_grid (list or np.array): A 1D list or array representing the input row.

    Returns:
        np.array: A 1D numpy array representing the transformed output row.
    """
    # Ensure input is a numpy array for easier manipulation
    input_row = np.array(input_grid, dtype=int)
    
    # Initialize output grid with the same shape and background color (white=0)
    output_grid = np.zeros_like(input_row)
    
    # Find the non-white block in the input row
    start_index, end_index, color = find_non_white_block(input_row)
    
    # If a block was found
    if start_index is not None:
        # Calculate the new start and end positions
        new_start_index = start_index + 3
        new_end_index = end_index + 3
        
        # Get the length of the block
        block_length = end_index - start_index
        
        # Determine the actual start and end indices within the output grid bounds
        # This handles cases where the shifted block might partially go out of bounds
        actual_start = max(0, new_start_index)
        actual_end = min(len(output_grid), new_end_index)
        
        # Determine the length of the block segment to actually place
        actual_length = actual_end - actual_start

        # Place the block (or the visible part of it) into the output grid
        if actual_length > 0:
             output_grid[actual_start:actual_end] = color

    # Return the modified output grid
    return output_grid.tolist() # Return as list as per standard ARC format expectation
```
