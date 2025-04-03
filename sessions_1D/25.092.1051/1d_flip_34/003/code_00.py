import numpy as np
from collections import Counter

"""
Transformation rule:
1. Identify the contiguous block of non-white pixels in the input row.
2. Within this block, find the color that appears exactly once (singular_color) and the color that appears multiple times (repeated_color).
3. Reconstruct the block by placing all instances of the repeated_color first, followed by the single instance of the singular_color.
4. Replace the original block segment in the row with this reconstructed block.
5. Keep all white pixels outside the block unchanged.
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
    if len(non_white_indices) == (end_index - start_index + 1):
        return start_index, end_index
    else:
        # This case implies gaps or multiple blocks, which shouldn't occur based on examples.
        # For robustness, we only return the first contiguous block found if assumptions were wrong.
        # However, sticking to the observed pattern:
        # If the found non-white indices are not contiguous as a single block,
        # maybe treat it as an error or return None, None. Let's assume contiguity.
         return start_index, end_index # Assume contiguity based on examples

def analyze_block(block):
    """
    Identifies the singular and repeated colors and the count of the repeated color within a block.

    Args:
        block (np.array): The segment of the row representing the non-white block.

    Returns:
        tuple: (singular_color, repeated_color, repeated_count) if successful,
               otherwise (None, None, 0).
    """
    if len(block) == 0:
        return None, None, 0

    counts = Counter(block)
    singular_color = None
    repeated_color = None
    repeated_count = 0

    for color, count in counts.items():
        if count == 1:
            singular_color = color
        elif count > 1:
            repeated_color = color
            repeated_count = count
        # Assuming exactly one singular and one repeated based on examples

    # Check if the expected pattern was found
    if singular_color is not None and repeated_color is not None and len(counts) == 2:
         return singular_color, repeated_color, repeated_count
    elif len(counts) == 1 and len(block) > 1: # Case: block of only one color (repeated)
        # This doesn't fit the observed transformation pattern (needs a singular)
        # Return None to indicate the pattern wasn't matched for transformation
         return None, list(counts.keys())[0], list(counts.values())[0] # Allow repeated-only case? No, examples have singular.
    elif len(counts) == 1 and len(block) == 1: # Case: block of only one color (singular)
         return list(counts.keys())[0], None, 0 # Allow singular-only case? No, examples have repeated.
    
    # Default if pattern isn't exactly one singular and one repeated
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
    if not input_grid or not input_grid[0]:
        return [] # Return empty for empty input
        
    input_row = np.array(input_grid[0], dtype=int)
    output_row = input_row.copy() # Initialize output as a copy of input

    # Step 1: Identify the boundaries of the non-white block
    start_index, end_index = find_non_white_block(input_row)

    # If no block is found, return the original row
    if start_index is None:
        return [output_row.tolist()] # Return copy in list of lists format

    # Extract the block
    block = input_row[start_index : end_index + 1]

    # Step 2: Analyze the block to find singular and repeated colors
    singular_color, repeated_color, repeated_count = analyze_block(block)

    # Step 3 & 4: If the expected pattern (one singular, one repeated) is found, reconstruct and replace
    # Check specifically for the pattern seen in examples (singular exists and repeated exists)
    if singular_color is not None and repeated_color is not None:
        # Construct the new block arrangement
        new_block = [repeated_color] * repeated_count + [singular_color]

        # Place the new block back into the output row
        output_row[start_index : end_index + 1] = new_block

    # If the block didn't match the pattern (e.g., all same color, or >2 colors),
    # the output_row remains unchanged (as initialized from input_row).

    # Step 5: (Implicit) White pixels outside the block were preserved by copying initially.

    # Return the result in the expected format (list of lists)
    return [output_row.tolist()]