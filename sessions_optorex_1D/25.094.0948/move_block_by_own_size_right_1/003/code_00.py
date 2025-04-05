import numpy as np

"""
Transforms an input 1D NumPy array of digits by identifying the single contiguous 
block of non-zero digits and shifting it to the right. The amount of the shift 
is equal to the length of the non-zero block itself. Zeros act as placeholders.

1.  Initialize an output array of the same size as the input, filled with zeros.
2.  Find the start index, length, and elements of the contiguous non-zero block 
    in the input array.
3.  If a block is found:
    a. Calculate the new starting position for the block by adding its original 
       start index and its length.
    b. Place the extracted block elements into the output array at the calculated 
       new start position, ensuring not to exceed array bounds.
4.  If no non-zero block is found, the output array remains all zeros.
5.  Return the output array.
"""

def find_non_zero_block(data_array):
    """
    Finds the start index, length, and elements of the first contiguous non-zero block.

    Args:
        data_array: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, length, block_elements) if a block is found.
        Returns (-1, 0, []) if no non-zero block is found.
    """
    start_index = -1
    length = 0
    block_elements = []
    n = len(data_array)

    # Find the start index of the first non-zero element
    for i in range(n):
        if data_array[i] != 0:
            start_index = i
            break

    # If no non-zero elements were found, return default values
    if start_index == -1:
        return start_index, length, block_elements

    # Find the end of the block (where it hits a zero or the end of the array)
    # and extract the block elements
    for i in range(start_index, n):
        if data_array[i] != 0:
            length += 1
            block_elements.append(data_array[i])
        else:
            # Found the end of the block (hit a zero)
            break
            
    # Convert block elements to numpy array for easier slicing later if needed,
    # though list works fine for assignment.
    # block_elements = np.array(block_elements) 
            
    return start_index, length, block_elements


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block-shifting transformation to the input 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array representing the sequence of digits.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array (it should be based on test framework)
    if not isinstance(input_grid, np.ndarray):
         # Handle potential list input if necessary, though unlikely based on error
         input_grid = np.array(input_grid)
         
    n = len(input_grid)
    
    # Initialize the output_grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero block in the input grid
    start_index, block_length, block_elements = find_non_zero_block(input_grid)

    # If a non-zero block was found
    if start_index != -1:
        # Calculate the new starting position for the block
        new_start_index = start_index + block_length
        
        # Calculate the theoretical end index for slicing in the output grid
        new_end_index = new_start_index + block_length

        # Check if the new starting position is within the bounds of the output grid
        if new_start_index < n:
             # Determine how many elements of the block can actually fit
             place_length = min(block_length, n - new_start_index)
             
             # Place the block elements (or the portion that fits) into the output grid
             output_grid[new_start_index : new_start_index + place_length] = block_elements[:place_length]

    # Return the transformed grid
    return output_grid