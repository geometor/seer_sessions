import numpy as np
import copy

"""
Identifies contiguous blocks of non-white pixels (value > 0) in a 1D input row.
Extracts white pixels (value 0) located between the first and last non-white blocks.
Extracts the non-white pixels, preserving their relative order.
Reconstructs the output row by placing the extracted 'middle' white pixels immediately before the sequence of non-white blocks, while keeping the initial and final white pixels in their original places.
Specifically:
1. Find the start index of the first non-white pixel and the end index of the last non-white pixel.
2. Identify three groups of white pixels: those before the first non-white pixel ('prefix'), those between the first and last non-white pixels ('middle'), and those after the last non-white pixel ('suffix').
3. Identify all non-white pixels between the first and last non-white pixel (inclusive), preserving their relative order ('blocks').
4. Assemble the output row by concatenating: prefix_white + middle_white + blocks + suffix_white.
"""

def find_non_white_indices(row):
    """Finds the start index of the first non-white pixel and the end index of the last non-white pixel."""
    non_white_indices = [i for i, pixel in enumerate(row) if pixel != 0]
    if not non_white_indices:
        return -1, -1  # No non-white pixels found
    return non_white_indices[0], non_white_indices[-1]

def transform(input_grid):
    """
    Applies the described transformation rule to a 1xN input grid.
    """
    # Ensure input is treated as a 1D array/list
    # ARC grids are lists of lists, even if 1D
    if isinstance(input_grid, np.ndarray):
        if input_grid.ndim > 1 and input_grid.shape[0] != 1:
             raise ValueError("Input grid must be 1xN")
        row = input_grid[0].tolist() if input_grid.ndim > 1 else input_grid.tolist()
    elif isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
        row = input_grid[0]
    else:
        # Handle cases where input might be just a flat list (less common in ARC context but good practice)
        if isinstance(input_grid, list) and all(isinstance(item, int) for item in input_grid):
             row = input_grid
        else:
             raise ValueError("Input format not recognized or not 1xN")


    # Find the span of non-white pixels
    first_non_white_idx, last_non_white_idx = find_non_white_indices(row)

    # If no non-white pixels or only isolated non-white pixels with no whites in between, return original
    if first_non_white_idx == -1 or first_non_white_idx == last_non_white_idx:
        # Return in the original format (list of lists)
        return [row] if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list) else np.array([row])

    # Extract prefix white pixels (before the first non-white)
    prefix_white = row[:first_non_white_idx]

    # Extract suffix white pixels (after the last non-white)
    suffix_white = row[last_non_white_idx + 1:]

    # Extract the core segment containing non-white blocks and middle white pixels
    core_segment = row[first_non_white_idx : last_non_white_idx + 1]

    # Separate middle white pixels and non-white blocks within the core segment
    middle_white = [pixel for pixel in core_segment if pixel == 0]
    ordered_blocks = [pixel for pixel in core_segment if pixel != 0]

    # Check if there are any middle white pixels to move
    if not middle_white:
        # No change needed if no white pixels were between blocks
        return [row] if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list) else np.array([row])


    # Reconstruct the output row
    output_row = prefix_white + middle_white + ordered_blocks + suffix_white

    # Return the transformed row in the required format (list of lists or numpy array)
    if isinstance(input_grid, np.ndarray):
        return np.array([output_row])
    else:
         # Assume original was list of lists format if not numpy
        return [output_row]
