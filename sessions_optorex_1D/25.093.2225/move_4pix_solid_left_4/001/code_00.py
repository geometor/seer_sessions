"""
Identifies a contiguous block of non-zero integers in the input sequence
and shifts it 4 positions to the left to create the output sequence.
The sequence length is fixed at 12. Zeros act as padding.
If the shift would place elements outside the sequence boundaries (index < 0),
those elements are omitted.
"""

# No external libraries needed for this implementation

def find_block(sequence):
    """
    Finds the contiguous block of non-zero elements and its start index.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple containing:
        - list: The block of non-zero integers.
        - int: The starting index of the block in the sequence.
        Returns (None, -1) if no non-zero block is found.
    """
    start_index = -1
    block = []

    # Iterate to find the first non-zero element (start of the block)
    for i, val in enumerate(sequence):
        if val != 0:
            start_index = i
            break

    # If no non-zero element was found, return None for block and -1 for index
    if start_index == -1:
        return None, -1

    # Starting from the found start_index, collect all contiguous non-zero elements
    for i in range(start_index, len(sequence)):
        if sequence[i] != 0:
            block.append(sequence[i])
        else:
            # Stop collecting once a zero is encountered after the block started
            break

    return block, start_index

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence (grid).

    Args:
        input_grid: A list of 12 integers representing the input sequence.

    Returns:
        A list of 12 integers representing the transformed output sequence.
    """
    # Define constants for the transformation
    sequence_length = 12
    shift_amount = -4 # Negative value indicates a left shift

    # --- Step 1: Identify the non-zero block and its position ---
    block, start_index = find_block(input_grid)

    # Initialize the output grid with zeros
    output_grid = [0] * sequence_length

    # --- Step 2: Handle case where no block is found ---
    # If no block was found, the output is just the initialized grid of zeros
    # (or could return input_grid[:] if the requirement was to return input as is)
    if block is None:
        return output_grid

    # --- Step 3: Calculate the new starting position for the block ---
    new_start_index = start_index + shift_amount

    # --- Step 4: Construct the output grid ---
    # Place the identified block into the output grid at the new position.
    # Iterate through the elements of the block.
    for i in range(len(block)):
        # Calculate the target index in the output grid for the current block element
        target_index = new_start_index + i

        # Check if the target index is within the valid bounds (0 to sequence_length - 1)
        if 0 <= target_index < sequence_length:
            # Place the block element into the output grid at the target index
            output_grid[target_index] = block[i]
        # If the target_index is out of bounds (e.g., negative due to shift),
        # the element is effectively dropped, matching the observed behavior implicitly.

    # --- Step 5: Return the result ---
    return output_grid
