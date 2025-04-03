```python
import numpy as np

def transform(input_grid):
    """
    Transforms a 1D grid by replacing contiguous horizontal blocks of magenta (6) pixels 
    with a new color based on the block's length:
    - Blocks of length 1 become red (2).
    - Blocks of length 2 become gray (5).
    - Blocks of length 3 become azure (8).
    White (0) pixels remain unchanged in their original positions.
    """
    
    # Convert input list-of-lists to a 1D numpy array for easier processing.
    # ARC grids are list of lists, even if 1D (e.g., [[...]]). We take the first row.
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input case
        
    input_array = np.array(input_grid[0], dtype=int)
    
    # Initialize the output array as a copy of the input array.
    # Transformations will be applied directly to this array.
    output_array = input_array.copy()
    
    # Get the width (length) of the 1D grid.
    width = len(input_array)
    
    # Initialize the scanning index.
    i = 0
    
    # Iterate through the grid to find and process magenta blocks.
    while i < width:
        # Check if the current pixel is magenta (6).
        if input_array[i] == 6:
            # Found the start of a potential magenta block.
            block_start = i
            block_length = 0
            
            # Scan to the right to find the end of the contiguous magenta block.
            j = i
            while j < width and input_array[j] == 6:
                block_length += 1
                j += 1
                
            # Determine the replacement color based on the measured block length.
            replacement_color = -1 # Use -1 as an indicator for unhandled lengths
            if block_length == 1:
                replacement_color = 2 # Red
            elif block_length == 2:
                replacement_color = 5 # Gray
            elif block_length == 3:
                replacement_color = 8 # Azure
            # Note: If blocks of other lengths exist, they won't be replaced under this logic.
            # The task examples only show lengths 1, 2, and 3.
                
            # If a valid replacement color was determined (length was 1, 2, or 3),
            # update the corresponding segment in the output array.
            if replacement_color != -1:
                output_array[block_start : block_start + block_length] = replacement_color
                
            # Advance the main scanning index past the processed block.
            i = block_start + block_length
            
        else:
            # If the current pixel is not magenta, simply move to the next pixel.
            # White pixels (0) are implicitly kept as they are copied initially.
            i += 1
            
    # Convert the final 1D numpy array back into the required list-of-lists format for ARC.
    output_grid = [output_array.tolist()]
    
    return output_grid

```