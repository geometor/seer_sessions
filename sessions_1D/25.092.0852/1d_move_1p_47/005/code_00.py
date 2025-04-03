import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
1. Examine the input sequence of pixels, treated as a one-dimensional list.
2. Find the first contiguous block of pixels where all pixels have the same non-white color (color is not 0). Record the start index and end index of this block.
3. If no such non-white block is found, return the original sequence unchanged.
4. Check the pixel immediately following the block (at index `end_index + 1`).
5. If this index is outside the bounds of the sequence, or if the pixel at this index is not white (0), return the original sequence unchanged.
6. Otherwise (a non-white block was found, and it's immediately followed by a white pixel):
   a. Identify the source index: `source_index = end_index + 1`.
   b. Identify the destination index: `destination_index = start_index`.
   c. Create a new sequence by removing the white pixel from `source_index` and inserting a white pixel (0) at `destination_index`.
7. Return the modified sequence.
"""

def find_first_non_white_block(sequence: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end indices of the first contiguous block of identical non-white pixels.
    
    Args:
        sequence: The input list of integers (pixels).
        
    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise None.
    """
    start_index = -1
    end_index = -1
    block_color = -1
    in_block = False
    
    if not sequence: # Handle empty sequence
        return None
        
    for i, pixel in enumerate(sequence):
        # Found the start of a potential block (must be non-white)
        if pixel != 0 and not in_block:
            start_index = i
            block_color = pixel # Record the color of this block
            in_block = True
        # Found the end of the block (either a white pixel or a different non-white pixel)
        elif in_block and (pixel == 0 or pixel != block_color):
            end_index = i - 1
            break # Found the first block, no need to continue
            
    # Handle case where the block extends to the very end of the sequence
    if in_block and end_index == -1:
        end_index = len(sequence) - 1
        
    # If we never entered a block, start_index remains -1
    if start_index == -1:
        return None
        
    return start_index, end_index


def transform(input_grid: np.ndarray) -> List[int]:
    """
    Applies the transformation rule to the input grid/sequence.
    
    Args:
        input_grid: A NumPy array representing the input pixel data. 
                    It's assumed to represent a 1D sequence or will be flattened.
        
    Returns:
        A new list with the transformation applied, or a copy of the input 
        flattened into a list if the conditions for transformation are not met.
    """
    
    # Ensure input is treated as a 1D sequence (list)
    # Flatten the numpy array and convert to a list
    input_sequence = list(input_grid.flatten())

    # Find the first contiguous block of non-white pixels
    block_indices = find_first_non_white_block(input_sequence)
    
    # If no non-white block was found, return the original sequence as a list
    if block_indices is None:
        return input_sequence # Return the flattened list

    start_index, end_index = block_indices
        
    # Calculate the index of the potential source pixel (the one to move)
    source_index = end_index + 1
    
    # Check if the source index is valid (within bounds) 
    # and if the pixel there is white (0)
    if source_index >= len(input_sequence) or input_sequence[source_index] != 0:
        # Conditions not met (no pixel after block, or pixel is not white)
        # Return the original sequence as a list
        return input_sequence
        
    # Conditions are met, proceed with the move
    
    # Calculate the destination index for the move (start of the non-white block)
    destination_index = start_index
    
    # Create a mutable copy of the input sequence to modify
    output_sequence = list(input_sequence) # Explicitly work with a list copy
    
    # Remove the source white pixel (value 0) from its original position
    # We don't need to store the popped value, as we know it's 0
    output_sequence.pop(source_index)
    
    # Insert a white pixel (value 0) at the destination index
    output_sequence.insert(destination_index, 0)
    
    # Return the modified sequence as a list
    return output_sequence