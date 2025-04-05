import numpy as np # Use numpy for potential array input/output and easier initialization

"""
Identifies a contiguous block of identical non-zero integers within a 12-element input sequence (list or numpy array).
Shifts this block 4 positions to the left.
Returns a new 12-element sequence (as a numpy array) with the shifted block, padding the remaining positions with zeros.
"""

def _find_non_zero_block(data: list[int] | np.ndarray) -> tuple[int | None, int, int]:
    """
    Finds the first contiguous block of identical non-zero integers.

    Args:
        data: The input sequence (list or numpy array).

    Returns:
        A tuple containing:
        - The non-zero integer composing the block (or None if no block found).
        - The length (count) of the block.
        - The starting index of the block.
        Returns (None, 0, -1) if no non-zero block is found.
    """
    start_index = -1
    block_digit = None
    block_length = 0

    for i, digit in enumerate(data):
        # Convert numpy int types to standard python int if needed for comparison
        current_digit = int(digit)

        if current_digit != 0:
            if block_digit is None: # Start of a potential block
                block_digit = current_digit
                start_index = i
                block_length = 1
            elif current_digit == block_digit: # Continuing the block
                block_length += 1
            else:
                # Found a different non-zero digit. Since examples only show one block,
                # assume the current block ended just before this different digit.
                break # Found the end of the block we were tracking
        elif block_digit is not None: # Found a zero after a block started
            break # End of the block

    if block_digit is None:
        return None, 0, -1 # No non-zero block found

    return block_digit, block_length, start_index


def transform(input_grid: list[int] | np.ndarray) -> np.ndarray:
    """
    Applies the block shifting transformation to the input sequence.

    Args:
        input_grid: The input sequence (list or numpy array of 12 integers).

    Returns:
        A numpy array representing the transformed sequence.
    """
    # Ensure input is treated consistently, get length
    input_sequence = np.array(input_grid) # Convert list to numpy array if necessary
    n = len(input_sequence)
    if n != 12:
        # Handle unexpected input length if necessary, though examples are fixed at 12
        # For now, assume length is always 12 based on provided examples.
        pass

    # 1. Identify the contiguous block of identical non-zero integers.
    block_digit, block_length, start_index = _find_non_zero_block(input_sequence)

    # 2. Initialize the output grid with zeros. Using numpy makes this easy.
    output_grid = np.zeros(n, dtype=int)

    # 3. Check if a block was actually found. If not, return the zero grid.
    if block_digit is None:
        return output_grid # Or maybe return input_grid? Examples imply transformation always happens. Let's stick to zeros.

    # 4. Calculate the target starting index for the non-zero block.
    # Subtract 4 from its starting index in the original input sequence.
    # Ensure the index doesn't go below 0.
    target_start_index = max(0, start_index - 4)

    # 5. Place the identified non-zero block into the output grid.
    # Use array slicing for efficiency if possible.
    # Ensure the block doesn't exceed the output grid bounds.
    end_index = min(target_start_index + block_length, n)
    for i in range(target_start_index, end_index):
         output_grid[i] = block_digit # Assign the block digit

    # 6. Return the newly created output grid (numpy array).
    return output_grid