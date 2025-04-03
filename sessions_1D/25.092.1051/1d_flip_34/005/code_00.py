import numpy as np
from collections import Counter

"""
Transformation rule:
1. Identify the single contiguous block of non-white (non-zero) pixels in the input row.
2. Within this block, identify the color that appears exactly once ('singular_color') and the color that appears multiple times ('repeated_color').
3. Reconstruct the block by placing all instances of the 'repeated_color' first, followed by the single instance of the 'singular_color' at the end.
4. Replace the original block segment in the row with this reconstructed block.
5. Keep all white (zero) pixels outside the block unchanged.
"""

def find_non_white_block(row):
    """
    Finds the start and end indices of the first contiguous non-white block.

    Args:
        row (np.array): The input row (1D numpy array).

    Returns:
        tuple: (start_index, end_index) if a block is found, otherwise (None, None).
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None  # No non-white pixels

    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]

    # Verify contiguity: check if the number of non-white indices matches the span
    # Based on examples, we assume a single contiguous block if non-white pixels exist.
    if len(non_white_indices) == (end_index - start_index + 1):
        return start_index, end_index
    else:
        # Handle unexpected cases like gaps or multiple blocks if necessary.
        # For this task, assume contiguity as per examples.
        # If strict adherence to finding only *contiguous* blocks is needed,
        # more complex logic would check for breaks in non_white_indices.
        # Let's stick to the assumption based on examples.
        return start_index, end_index # Assume the span defines the block

def analyze_block(block):
    """
    Identifies the singular and repeated colors and the count of the repeated color within a block.
    Assumes the block fits the pattern of exactly one singular and one repeated color.

    Args:
        block (np.array): The segment of the row representing the non-white block.

    Returns:
        tuple: (singular_color, repeated_color, repeated_count) if the expected pattern is found,
               otherwise (None, None, 0).
    """
    if block.size == 0: # Use .size for numpy arrays
        return None, None, 0

    counts = Counter(block)
    singular_color = None
    repeated_color = None
    repeated_count = 0

    # Check if the block conforms to the pattern (exactly 2 distinct colors)
    if len(counts) != 2:
        return None, None, 0 # Pattern not met

    for color, count in counts.items():
        if count == 1:
            singular_color = color
        elif count > 1:
            repeated_color = color
            repeated_count = count
        # No need for further checks as we already confirmed len(counts) == 2

    # Final check if both were assigned correctly (should always be true if len(counts)==2)
    if singular_color is not None and repeated_color is not None:
        return singular_color, repeated_color, repeated_count
    else:
        # This case should theoretically not be reached if len(counts) == 2
        return None, None, 0


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A list containing one list (the row).

    Returns:
        list of lists: The transformed grid.
    """
    # Ensure input is valid and extract the row
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        # Handle invalid input format gracefully, maybe return empty or raise error
        return [] # Return empty for invalid/empty input

    input_row_list = input_grid[0]
    # Handle case where input row might be empty
    if not input_row_list:
      return [[]]

    input_row = np.array(input_row_list, dtype=int)
    # Initialize output_grid as a copy of the input
    output_row = input_row.copy()

    # Step 1: Identify the boundaries of the non-white block
    start_index, end_index = find_non_white_block(input_row)

    # If no non-white block is found, return the original grid
    if start_index is None:
        return [output_row.tolist()] # Return copy in list of lists format

    # Extract the block from the input row for analysis
    block = input_row[start_index : end_index + 1]

    # Step 2: Analyze the block to find singular and repeated colors
    singular_color, repeated_color, repeated_count = analyze_block(block)

    # Step 3 & 4: If the expected pattern (one singular, one repeated) is found, reconstruct and replace
    if singular_color is not None and repeated_color is not None:
        # Construct the new block arrangement as a list
        new_block_list = [repeated_color] * repeated_count + [singular_color]

        # Place the new block back into the output row
        # Ensure the lengths match (should always match if analysis was correct)
        if len(new_block_list) == (end_index - start_index + 1):
             output_row[start_index : end_index + 1] = new_block_list
        # else: # Optional: Handle mismatch case if robustness is needed
             # pass # Keep output_row unchanged or raise an error

    # Step 5: (Implicit) White pixels outside the block were preserved by copying initially.

    # Return the result in the expected format (list of lists)
    return [output_row.tolist()]