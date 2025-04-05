import numpy as np # Import numpy as input might be an array

"""
Identifies two blocks of identical non-zero numbers in the input sequence (list or NumPy array).
Let the first found block be A and the second be B.
Reorders the blocks based on their lengths: if the second block found (B) is strictly longer 
than the first block found (A), the output order becomes (B, A). Otherwise, the order remains (A, B).
Let the final ordered blocks be X (first in pair) and Y (second in pair).
Constructs the output sequence by placing block Y at the far right, preceded by a single zero, 
preceded by block X. The remaining positions at the beginning are filled with zeros. 
The total length of the sequence remains unchanged.
"""

def find_blocks(data):
    """
    Finds the first two contiguous blocks of identical non-zero numbers in the input list or array.
    
    Args:
        data: A list or NumPy array of integers representing the input sequence.

    Returns:
        A tuple containing two lists: (first_block, second_block).
        If fewer than two blocks are found, the missing blocks are represented by empty lists.
    """
    # Convert numpy array to list if necessary, otherwise assume it's list-like
    if isinstance(data, np.ndarray):
        data = data.tolist()
    elif not isinstance(data, list):
        try:
            data = list(data) # Attempt conversion for other iterables
        except TypeError:
            # Handle cases where conversion isn't possible, return empty blocks
            print(f"Warning: Cannot convert input of type {type(data)} to list in find_blocks.")
            return [], []
            
    blocks = []
    i = 0
    n = len(data)
    while i < n:
        # Skip zeros
        if data[i] == 0:
            i += 1
            continue
            
        # Found the start of a potential non-zero block
        start_index = i
        block_val = data[i]
        
        # Find the end of this contiguous block of identical numbers
        while i < n and data[i] == block_val:
            i += 1
            
        # Add the found block (as a list of numbers)
        blocks.append(data[start_index:i])
        
        # Stop searching once two blocks are found
        if len(blocks) == 2:
            break
            
    # Ensure exactly two blocks are returned, padding with empty lists if necessary
    while len(blocks) < 2:
        blocks.append([])
        
    return blocks[0], blocks[1]

def transform(input_list):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_list: A list or NumPy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    
    # Get the length of the input sequence
    n = len(input_list)
    if n == 0:
        return [] # Handle empty input

    # 1. Identify the first (A) and second (B) contiguous blocks of non-zero numbers
    block_a, block_b = find_blocks(input_list)

    # Check if two non-empty blocks were found (as expected from examples)
    if not block_a or not block_b:
        # Behavior for invalid input (fewer than 2 blocks) is undefined by examples.
        # Returning the input unchanged or raising an error might be options.
        # For now, return an empty list or handle as error.
        print(f"Warning: Could not find two non-empty blocks in input: {input_list}. Returning empty list.")
        return [] 

    # 2. Compare lengths and determine output order (X, Y)
    len_a = len(block_a)
    len_b = len(block_b)
    
    # If len(B) > len(A), order is (B, A). Else, order is (A, B).
    if len_b > len_a:
        block_x = block_b # The block that will appear first (leftmost) in the output pair
        block_y = block_a # The block that will appear second (rightmost) in the output pair
    else:
        block_x = block_a
        block_y = block_b

    len_x = len(block_x)
    len_y = len(block_y)

    # 3. Construct the output sequence
    
    # Calculate the total length required for the non-zero part + separator
    required_len = len_x + len_y + 1 

    # Check if the combined blocks and separator fit within the sequence length
    if required_len > n:
        print(f"Error: Combined block length ({len_x} + {len_y}) plus separator (1) exceeds sequence length ({n}). Cannot construct output.")
        return [] # Cannot construct valid output

    # Calculate the number of leading zeros needed
    num_leading_zeros = n - required_len

    # Create the final output list by concatenating components
    output_list = [0] * num_leading_zeros + block_x + [0] + block_y
    
    # Ensure output list has the correct length (should be guaranteed by calculations)
    if len(output_list) != n:
         print(f"Error: Constructed output length {len(output_list)} does not match input length {n}.")
         # This case indicates a logic error in length calculation
         return [] # Or raise an error

    # Convert back to numpy array if that's the desired output format
    # return np.array(output_list) 
    # For now, returning a standard list as per template implication
    return output_list