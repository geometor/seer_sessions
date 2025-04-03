"""
Transforms a 1xN input grid by rearranging specific components.
The transformation identifies a contiguous block of a single color (not white 0 or maroon 9),
a single pivot pixel (maroon 9), and the sequence of pixels (the gap) between them.
It then reconstructs the row by placing the elements before the block (prefix), followed by the pivot,
the gap, the colored block, and finally the elements after the pivot (suffix).
Essentially, the pivot and the colored block swap positions relative to each other, preserving the gap and all other elements' relative order.
"""

import numpy as np
from typing import List, Tuple, Dict, Any, Union

def find_components_1d(row: List[int], background_color: int = 0, pivot_color: int = 9) -> Dict[str, Any]:
    """
    Identifies the pivot, colored block, gap, prefix, and suffix in a 1D row.

    Args:
        row: The input list of pixel values.
        background_color: The value representing the background.
        pivot_color: The value representing the pivot pixel.

    Returns:
        A dictionary containing:
        - 'pivot_index': Index of the pivot pixel.
        - 'pivot_value': Value of the pivot pixel (should be pivot_color).
        - 'block': List of pixels in the colored block.
        - 'block_start': Start index of the colored block.
        - 'block_end': End index of the colored block.
        - 'gap': List of pixels in the gap between block and pivot.
        - 'prefix': List of pixels before the colored block.
        - 'suffix': List of pixels after the pivot pixel.
    Raises:
        ValueError: If the pivot or colored block is not found, or if the input assumptions are violated (e.g., block not before pivot).
    """
    pivot_index = -1
    block = []
    block_start = -1
    block_end = -1
    in_block = False
    block_color = -1

    # First pass: Find pivot and the single colored block
    for i, pixel in enumerate(row):
        if pixel == pivot_color:
            if pivot_index != -1:
                raise ValueError("More than one pivot pixel found.")
            pivot_index = i
        elif pixel != background_color and pixel != pivot_color:
            current_pixel_color = pixel
            if not in_block: # Start of a potential block
                # Check if we already found a block and are starting another distinct one
                if block_start != -1:
                     raise ValueError("More than one colored block found or block is non-contiguous.")
                block_start = i
                block_color = current_pixel_color
                in_block = True
                block.append(pixel)
                block_end = i
            elif in_block and pixel == block_color: # Continue the block
                block.append(pixel)
                block_end = i
            elif in_block and pixel != block_color: # End of the block (different non-bg/pivot color)
                # This implies a second block or non-contiguous block, which violates assumptions
                raise ValueError("Found second colored block or non-contiguous block.")
        elif in_block: # End of the block (background or pivot detected after being in_block)
            in_block = False # Reset flag, the block definition is complete

    # Validate findings
    if pivot_index == -1:
        raise ValueError(f"Pivot color {pivot_color} not found.")
    if not block:
        raise ValueError("Colored block not found.")
    if block_end >= pivot_index:
         raise ValueError("Colored block must precede the pivot pixel in the input.")

    # Identify components based on indices
    prefix = row[:block_start]
    gap = row[block_end + 1 : pivot_index] # Gap is between block end and pivot start
    suffix = row[pivot_index + 1:]
    pivot_value = row[pivot_index] # Store the actual pivot value found

    return {
        'pivot_index': pivot_index,
        'pivot_value': pivot_value,
        'block': block,
        'block_start': block_start,
        'block_end': block_end,
        'gap': gap,
        'prefix': prefix,
        'suffix': suffix
    }


def transform(input_grid: Union[np.ndarray, List[List[int]]]) -> Union[np.ndarray, List[List[int]]]:
    """
    Applies the rearrangement transformation to the input grid.

    Args:
        input_grid: A 1xN grid, represented as a numpy array or list of lists.

    Returns:
        The transformed 1xN grid in the same format as the input.
    """
    # --- Input Handling ---
    is_numpy = isinstance(input_grid, np.ndarray)
    
    # Convert numpy array to list of lists for consistent processing
    if is_numpy:
        # Ensure it's 2D, even if 1xN
        if input_grid.ndim == 1:
             input_list = [input_grid.tolist()] # Treat 1D array as single row
        elif input_grid.ndim == 2:
             input_list = input_grid.tolist()
        else:
            raise ValueError("Input grid must be 1D or 2D.")
    elif isinstance(input_grid, list) and isinstance(input_grid[0], list):
         input_list = input_grid
    else:
         # Handle case where input might be just a flat list like [0, 0, 1, 1, 0, 9, 0]
         if isinstance(input_grid, list) and all(isinstance(x, int) for x in input_grid):
             input_list = [input_grid]
             is_numpy = False # Treat it as list of list conceptually
         else:
            raise TypeError("Input must be a numpy array or list of lists representing the grid.")

    # --- Validation ---
    if len(input_list) != 1:
        raise ValueError("Input grid must contain exactly one row.")
    
    input_row = input_list[0]
    if not input_row: # Handle empty row case
        # Decide behavior: return empty or raise error? Returning empty seems safer.
        return np.array([[]]) if is_numpy else [[]]

    # --- Core Logic ---
    try:
        # 1. Parse the input row to identify components
        components = find_components_1d(input_row)
    except ValueError as e:
        # Handle cases where the expected structure isn't found
        print(f"Warning: Could not find expected components in input row: {e}. Returning original grid.")
        # Depending on ARC rules, returning original might be necessary
        return input_grid

    # 2. Extract components for clarity
    prefix = components['prefix']
    pivot_value = components['pivot_value']
    gap = components['gap']
    colored_block = components['block']
    suffix = components['suffix']

    # 3. Construct the output row by concatenating in the new order
    # Order: prefix + pivot + gap + colored_block + suffix
    output_row = prefix + [pivot_value] + gap + colored_block + suffix

    # --- Output Formatting ---
    # 4. Format the resulting row back into the original grid structure
    if is_numpy:
        output_grid = np.array([output_row], dtype=input_grid.dtype) # Preserve dtype
    else:
        # Check if original input was list of list or just flat list
        if isinstance(input_grid, list) and isinstance(input_grid[0], list):
             output_grid = [output_row]
        else: # Original was likely a flat list
             output_grid = output_row # Return as flat list


    # --- Final Validation (Optional) ---
    # Ensure output has same length as input row if input wasn't empty
    if input_row and len(output_row) != len(input_row):
         print(f"Warning: Output length ({len(output_row)}) differs from input length ({len(input_row)}). This might indicate an error.")
         # Could raise error here, or return original, depending on desired strictness

    return output_grid