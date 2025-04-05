import sys 
import re # Import re although not used in the final version, kept from thought process

"""
Identifies two blocks of identical non-zero numbers in the input sequence.
Reorders the blocks based on their lengths: if the second block found (B) is strictly longer 
than the first block found (A), the output order becomes (B, A). Otherwise, the order remains (A, B).
Let the final ordered blocks be X (first in pair) and Y (second in pair).
Constructs the output sequence by placing block Y at the far right, preceded by a single zero, 
preceded by block X. The remaining positions at the beginning are filled with zeros. 
The total length of the sequence remains unchanged.
"""

def find_blocks(data):
    """
    Finds the first two contiguous blocks of identical non-zero numbers in the input list.
    
    Args:
        data: A list of integers representing the input sequence.

    Returns:
        A tuple containing two lists: (first_block, second_block).
        If fewer than two blocks are found, the missing blocks are represented by empty lists.
    """
    blocks = []
    i = 0
    n = len(data)
    while i < n:
        # Skip leading zeros
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
        
        # Stop searching once two blocks are found, as per problem constraints
        if len(blocks) == 2:
            break
            
    # Ensure exactly two blocks are returned, padding with empty lists if necessary
    # This handles cases where the input might not strictly contain two blocks,
    # although the examples suggest it always does.
    while len(blocks) < 2:
        blocks.append([])
        
    # Check if the found blocks are non-empty, as expected from examples
    # This is more of an assertion based on observed patterns.
    if not blocks[0] or not blocks[1]:
         # This might indicate an unexpected input format or flaw in assumptions.
         # For now, just print a warning. The calling function might handle errors.
         # print(f"Warning: Did not find two non-empty blocks in {data}. Found: {blocks}")
         pass # Proceeding even if a block is empty, though this shouldn't happen per examples.

    return blocks[0], blocks[1]

def transform(input_str):
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string of space-separated integers.

    Returns:
        A string of space-separated integers representing the transformed sequence.
        Returns an empty string or raises an error if input is invalid or blocks cannot be placed.
    """
    
    # 1. Parse the input string into a list of integers
    try:
        input_list = [int(x) for x in input_str.split()]
    except ValueError:
        print(f"Error: Input string contains non-integer values: {input_str}")
        return "" # Or raise error
        
    n = len(input_list)
    if n == 0:
        return "" # Handle empty input

    # 2. Identify the first (A) and second (B) contiguous blocks of non-zero numbers
    block_a, block_b = find_blocks(input_list)

    # Basic validation based on problem description (expect two non-empty blocks)
    if not block_a or not block_b:
        print(f"Error: Could not find two distinct non-zero blocks in input: {input_str}")
        # Depending on requirements, could return input, empty string, or raise error
        return "" 

    # 3. Compare lengths and determine output order (X, Y)
    # If len(B) > len(A), order is (B, A). Else, order is (A, B).
    if len(block_b) > len(block_a):
        block_x = block_b # The block that will appear first (leftmost) in the output pair
        block_y = block_a # The block that will appear second (rightmost) in the output pair
    else:
        block_x = block_a
        block_y = block_b

    # 4. Construct the output sequence
    # Initialize with zeros
    output_list = [0] * n

    # Calculate lengths and required space
    len_x = len(block_x)
    len_y = len(block_y)
    required_len = len_x + len_y + 1 # +1 for the separating zero

    # Check if the combined blocks and separator fit within the sequence length
    if required_len > n:
        print(f"Error: Combined block length ({len_x} + {len_y}) plus separator (1) exceeds sequence length ({n}) for input: {input_str}")
        return "" # Cannot construct valid output

    # 5. Place block Y at the rightmost end
    start_y = n - len_y
    if start_y < 0 : # Should be caught by required_len check, but added for safety
         print(f"Error: Cannot place block Y. Start index {start_y} is invalid.")
         return ""
    output_list[start_y:] = block_y

    # 6. Place the separating zero (implicitly placed by initialization, ensure index is valid)
    sep_index = start_y - 1
    if sep_index < 0 : 
         print(f"Error: Cannot place separator. Index {sep_index} is invalid.")
         return ""
    # output_list[sep_index] = 0 # This position should already be 0

    # 7. Place block X to the left of the separator
    start_x = sep_index - len_x
    if start_x < 0:
        print(f"Error: Cannot place block X. Start index {start_x} is invalid.")
        return ""
    output_list[start_x:sep_index] = block_x

    # 8. Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
