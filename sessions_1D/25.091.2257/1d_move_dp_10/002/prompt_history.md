
## train_1

**input:**
```
0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 1 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 1 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 0 0
```

*   **Perception:**
    The input and output are 1D arrays (representing rows of a grid) containing integer values representing colors. Each input contains exactly one contiguous block of a single color (magenta, yellow, or red in the examples, but generally non-white and non-blue) and exactly one 'blue' pixel (value 1). The rest of the pixels are 'white' (value 0). The 'blue' pixel always appears to the right of the colored block. The transformation involves shifting the colored block to the right so that it becomes adjacent to the 'blue' pixel, effectively closing the gap of 'white' pixels that existed between them in the input. The 'blue' pixel itself does not move.

*   **Facts:**
    
```yaml
    task_description: Shift a colored block rightwards to abut a stationary blue marker.

    elements:
      - object: colored_block
        description: A contiguous sequence of pixels with the same color, where the color is not white (0) and not blue (1). There is exactly one such block per input.
        properties:
          - color: The color value (e.g., 6, 4, 2).
          - start_index: The starting position (0-based index) of the block in the input array.
          - end_index: The ending position (0-based index) of the block in the input array.
          - length: The number of pixels in the block (end_index - start_index + 1).
      - object: blue_marker
        description: A single pixel with the color blue (1). There is exactly one such pixel per input.
        properties:
          - index: The position (0-based index) of the blue pixel in the input array.
      - object: white_space
        description: Pixels with the color white (0).
        properties:
          - location: Specifically refers to the white pixels located between the 'colored_block' and the 'blue_marker'.
          - gap_length: The count of white pixels between the end of the 'colored_block' and the 'blue_marker' (blue_marker.index - colored_block.end_index - 1).

    relationships:
      - The 'colored_block' always appears to the left of the 'blue_marker' in the input.
      - There is always at least one 'white_space' pixel between the 'colored_block' and the 'blue_marker' in the input.

    actions:
      - Identify the 'colored_block' (its color, start_index, end_index).
      - Identify the 'blue_marker' (its index).
      - Calculate the 'gap_length' of the 'white_space' between them.
      - Determine the shift amount: shift_amount = gap_length.
      - Create the output array (same size as input, initially all white).
      - Place the 'colored_block' into the output array, shifted right by 'shift_amount'. Its new start index will be (colored_block.start_index + shift_amount).
      - Place the 'blue_marker' into the output array at its original index.
    ```


*   **Natural Language Program:**
    1.  Initialize the output array as a copy of the input array, filled entirely with white (0) pixels.
    2.  Scan the input array to find the contiguous block of non-white, non-blue pixels (the "colored block"). Record its color, start index, and end index.
    3.  Scan the input array to find the index of the blue (1) pixel (the "blue marker").
    4.  Calculate the number of white (0) pixels strictly between the end index of the colored block and the index of the blue marker. This is the shift distance.
    5.  Determine the new start index for the colored block in the output array by adding the shift distance to its original start index.
    6.  Fill the corresponding segment in the output array with the color of the colored block, starting at the new start index and having the same length as the original block.
    7.  Place the blue marker (1) in the output array at its original index.
```python
"""
Shift a contiguous block of a non-white, non-blue color rightwards until it is 
adjacent to a stationary blue marker pixel. The blue marker and all other 
white pixels maintain their original positions, except for those overwritten 
by the shifted block.
"""

import numpy as np
from typing import List, Tuple, Optional

# Helper function to find the contiguous colored block (non-white, non-blue)
def find_colored_block(grid: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of non-white (0) and non-blue (1) pixels.

    Args:
        grid: The input 1D list representing the grid row.

    Returns:
        A tuple containing (color, start_index, end_index) of the block,
        or None if no such block is found.
    """
    start_index = -1
    color = -1
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 1:
            if start_index == -1:
                start_index = i
                color = pixel
            # Check if the color continues or if it's a different block color
            elif pixel != color: 
                 # This condition assumes only ONE block, consistent with examples
                 # If multiple blocks were possible, logic would need adjustment.
                 # For now, we assume the first block found is the target.
                 return (color, start_index, i - 1)
        elif start_index != -1:
            # Block ended
            return (color, start_index, i - 1)
            
    # Handle case where the block extends to the end of the grid
    if start_index != -1:
        return (color, start_index, len(grid) - 1)
        
    return None

# Helper function to find the blue marker
def find_blue_marker(grid: List[int]) -> Optional[int]:
    """
    Finds the index of the blue (1) marker pixel.

    Args:
        grid: The input 1D list representing the grid row.

    Returns:
        The index of the blue marker, or None if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == 1:
            return i
    return None

def transform(input_grid: List[int]) -> List[int]:
    """
    Shifts a colored block rightwards to abut a stationary blue marker.

    Args:
        input_grid: A 1D list of integers representing pixel colors.

    Returns:
        A 1D list of integers representing the transformed grid row.
    """
    
    # Find the colored block
    block_info = find_colored_block(input_grid)
    if block_info is None:
        # Should not happen based on examples, but handle defensively
        return input_grid[:] # Return a copy if no block found

    block_color, block_start, block_end = block_info
    block_length = block_end - block_start + 1

    # Find the blue marker
    marker_index = find_blue_marker(input_grid)
    if marker_index is None:
        # Should not happen based on examples, but handle defensively
        return input_grid[:] # Return a copy if no marker found
        
    # Calculate the gap and the required shift
    # The new end position of the block should be marker_index - 1
    new_block_end = marker_index - 1
    shift_amount = new_block_end - block_end
    
    # Calculate the new start position
    new_block_start = block_start + shift_amount

    # Initialize the output grid with white pixels
    output_grid = [0] * len(input_grid)

    # Place the shifted colored block into the output grid
    for i in range(block_length):
        if 0 <= new_block_start + i < len(output_grid): # Boundary check
             output_grid[new_block_start + i] = block_color

    # Place the blue marker at its original position
    if 0 <= marker_index < len(output_grid): # Boundary check
        output_grid[marker_index] = 1
        
    # Note: Other white pixels remain white by initialization.

    return output_grid

```
