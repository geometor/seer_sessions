```python
import numpy as np
from typing import List

"""
Transforms a 1D sequence of colored pixels (integers 0-9). 
Identifies contiguous blocks of non-white (non-zero) pixels ("objects").
If an object consists of a single pixel, it is expanded into three pixels of the same color in the output.
If an object consists of more than one pixel, it is copied unchanged to the output.
White (zero) pixels are copied unchanged.
The relative order of objects and white spaces is preserved.
"""

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid: A list of integers representing the 1D input sequence.

    Returns:
        A list of integers representing the transformed 1D output sequence.
    """
    output_grid = []
    i = 0
    n = len(input_grid)

    # Iterate through the input sequence
    while i < n:
        # Get the current pixel's color
        current_pixel = input_grid[i]

        # If the pixel is white (0), copy it directly
        if current_pixel == 0:
            output_grid.append(0)
            i += 1
        else:
            # If the pixel is non-white, identify the object
            object_color = current_pixel
            object_length = 0
            start_index = i
            
            # Find the length of the contiguous non-white object
            while i < n and input_grid[i] == object_color:
                object_length += 1
                i += 1 # Advance index past the object pixels
            
            # Apply transformation based on object length
            if object_length == 1:
                # Expand single-pixel object to three pixels
                output_grid.extend([object_color] * 3)
            else:
                # Copy multi-pixel object as is
                output_grid.extend([object_color] * object_length)
                
            # Note: Index 'i' is already advanced past the object in the inner while loop

    return output_grid

```