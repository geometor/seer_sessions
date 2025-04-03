```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D grid by identifying a contiguous block of a single non-white color. 
The output grid retains the color of the block only at its start and end indices, 
with all other pixels set to white (0).
"""

def find_contiguous_block(grid: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the start index, end index, and color of the first contiguous 
    block of non-white pixels in a 1D grid.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A tuple (start_index, end_index, color) if a block is found, 
        otherwise None.
    """
    start_index = -1
    end_index = -1
    block_color = 0
    
    # Find the start of the block
    for i, pixel in enumerate(grid):
        if pixel != 0:
            start_index = i
            block_color = pixel
            break
            
    # If no non-white pixel found, return None
    if start_index == -1:
        return None
        
    # Find the end of the block (last consecutive pixel of the same color)
    end_index = start_index
    for i in range(start_index + 1, len(grid)):
        if grid[i] == block_color:
            end_index = i
        else:
            # Stop as soon as the color changes or a white pixel is encountered
            break
            
    return start_index, end_index, block_color

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list of integers representing the 1D input grid.
        
    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    
    # Find the contiguous block of non-white color
    block_info = find_contiguous_block(input_grid)
    
    # Initialize the output grid with the same size as input, filled with white (0)
    output_grid = [0] * len(input_grid)
    
    # If a block was found, place its color at the start and end indices
    if block_info:
        start_index, end_index, block_color = block_info
        output_grid[start_index] = block_color
        # Ensure we don't write the same pixel twice if the block length is 1
        if start_index != end_index:
             output_grid[end_index] = block_color
             
    return output_grid

```