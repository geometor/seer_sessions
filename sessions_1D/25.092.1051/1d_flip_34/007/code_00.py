import numpy as np
from collections import Counter

"""
Transformation rule:
1. Identify the single contiguous block of non-white (non-zero) pixels in the input row.
2. Within this block, identify the color that appears exactly once ('singular_color') and the color that appears multiple times ('repeated_color').
3. If this specific pattern (one singular, one repeated) is found, reconstruct the block by placing all instances of the 'repeated_color' first, followed by the single instance of the 'singular_color' at the end.
4. Replace the original block segment in the row with this reconstructed block.
5. Keep all white (zero) pixels outside the block unchanged. If the pattern is not found in the block, return the original row.
"""

def find_non_white_block(row):
    """
    Finds the start and end indices of the first contiguous non-white block.

    Args:
        row (np.array): The input row (1D numpy array).

    Returns:
        tuple: (start_index, end_index + 1) representing the slice indices
               if a block is found, otherwise (None, None).
               Returns end_index + 1 for easy slicing.
    """
    non_white_indices = np.where(row != 0)[0]
    if non_white_indices.size == 0:
        return None, None  # No non-white pixels

    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]

    # Verify contiguity assumption based on examples
    if non_white_indices.size == (end_index - start_index + 1):
        return start_index, end_index + 1 # Return slice indices
    else:
        # Handles cases not seen in examples (e.g. gaps).
        # Based on examples, assume single contiguous block.
        # If non-contiguous, this might return the span covering the first and last non-white pixel.
        # For robustness according to the explicit rule of *contiguous* block:
        # One could iterate through non_white_indices to find the first contiguous sequence.
        # However, sticking to example patterns, we'll assume the span is the block.
        # If the rule strictly requires handling non-contiguity by returning None,
        # add a check here:
        # is_contiguous = np.all(np.diff(non_white_indices) == 1)
        # if not is_contiguous: return None, None # Or handle differently
        return start_index, end_index + 1 # Assume span is the target block based on examples


def analyze_block(block):
    """
    Identifies the singular and repeated colors and the count of the repeated color within a block.
    Checks if the block fits the pattern of exactly one singular and one repeated color.

    Args:
        block (np.array): The segment of the row representing the non-white block.

    Returns:
        tuple: (singular_color, repeated_color, repeated_count) if the expected pattern is found,
               otherwise (None, None, 0).
    """
    if block.size <= 1: # A block needs at least 2 elements for a singular and repeated
        return None, None, 0

    counts = Counter(block)
    singular_color = None
    repeated_color = None
    repeated_count = 0

    # Check if the block conforms to the pattern (exactly 2 distinct colors)
    if len(counts) != 2:
        return None, None, 0 # Pattern not met: requires exactly two colors

    # Identify singular (count=1) and repeated (count>1)
    found_singular = False
    found_repeated = False
    for color, count in counts.items():
        if count == 1:
            singular_color = color
            found_singular = True
        elif count > 1:
            repeated_color = color
            repeated_count = count
            found_repeated = True

    # Ensure both types were found (handles cases like two colors each appearing >1 times)
    if found_singular and found_repeated:
        return singular_color, repeated_color, repeated_count
    else:
        # Pattern not met (e.g., both colors appear multiple times)
        return None, None, 0


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A list containing one list representing the row.

    Returns:
        list of lists: The transformed grid.
    """
    # Input validation
    if not input_grid or not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle invalid input format - return as is or empty based on convention
        return input_grid # Or potentially raise an error or return []

    input_row_list = input_grid[0]
    if not input_row_list: # Handle empty row case
      return [[]]

    # Convert to numpy array for easier processing
    input_row = np.array(input_row_list, dtype=int)
    # Initialize output_row as a copy of the input
    output_row = input_row.copy()

    # Step 1: Identify the boundaries of the non-white block
    start_index, end_index_slice = find_non_white_block(input_row)

    # If no non-white block is found, return the original grid
    if start_index is None:
        return [output_row.tolist()] # Return copy in list of lists format

    # Step 2: Extract the block from the input row for analysis
    block = input_row[start_index : end_index_slice]

    # Step 3: Analyze the block to find singular and repeated colors
    singular_color, repeated_color, repeated_count = analyze_block(block)

    # Step 4: If the expected pattern (one singular, one repeated) is found, reconstruct and replace
    if singular_color is not None and repeated_color is not None:
        # Construct the new block arrangement as a list
        # Ensure the count is correct (it's derived from the block analysis)
        new_block_list = [repeated_color] * repeated_count + [singular_color]

        # Double-check length consistency before replacement
        if len(new_block_list) == block.size:
             # Replace the segment in the output row
             output_row[start_index : end_index_slice] = new_block_list
        # else: optional handling for unexpected length mismatch

    # Step 5: (Implicit) White pixels outside the block were preserved.
    # If the pattern wasn't found in analyze_block, output_row remains unchanged.

    # Return the result in the expected format (list of lists)
    return [output_row.tolist()]