import numpy as np

"""
Restores a background pattern in a grid where parts of the pattern are obscured by white pixels (0).

The grid is assumed to contain two types of rows:
1. Rows composed entirely of blue pixels (1).
2. Rows containing a repeating horizontal color sequence, potentially obscured by white pixels (0).

The transformation identifies the repeating color sequence from the first non-blue row that does *not* contain any white pixels. This sequence is then used to fill in any white pixels found in other non-blue rows based on their column position relative to the sequence length. Pixels that are not white are left unchanged.
"""

def find_reference_sequence(grid):
    """
    Finds the first non-solid-blue row without white pixels to use as the reference sequence.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list representing the color sequence, or None if no suitable row is found.
    """
    height, _ = grid.shape
    for r in range(height):
        row = grid[r, :]
        # Check if the row is not entirely blue (1)
        if not np.all(row == 1):
            # Check if the row does not contain any white (0) pixels
            if 0 not in row:
                # Found the first suitable reference row
                return row.tolist() 
    # No suitable reference row was found
    return None

def transform(input_grid):
    """
    Applies the pattern restoration transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid with the pattern restored.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Create a copy of the input grid to modify and return as output
    output_grid = np.copy(input_array)

    # 1. Identify the reference sequence for non-solid-blue rows
    reference_sequence = find_reference_sequence(input_array)

    # 2. Check if a reference sequence was found
    if reference_sequence is None:
        # If no reference sequence is found (e.g., all blue grid, or no 'clean' sequence rows),
        # we cannot perform the transformation based on the current logic.
        # Return the original grid or handle as an error case if needed.
        # Based on the problem description, we assume a reference sequence should exist.
        # If this assumption fails on real data, this part needs refinement.
        print("Warning: No reference sequence found. Returning input grid unchanged.")
        return input_grid # Return original list of lists

    sequence_length = len(reference_sequence)
    
    # Ensure sequence length is valid
    if sequence_length == 0:
         print("Warning: Found an empty reference sequence. Returning input grid unchanged.")
         return input_grid # Return original list of lists

    # 3. Iterate through the grid and restore the pattern where pixels are white (0)
    for r in range(height):
        # Check if the current row is potentially a sequence row (i.e., contains non-blue or white pixels)
        # We only need to check pixels that are white (0)
        for c in range(width):
            if input_array[r, c] == 0:
                # This pixel needs to be replaced.
                # Calculate the replacement color using the reference sequence.
                # The color depends on the column index modulo the sequence length.
                try:
                    replacement_color = reference_sequence[c % sequence_length]
                    # Update the output grid
                    output_grid[r, c] = replacement_color
                except IndexError:
                     # This should not happen if sequence_length > 0, but added defensively.
                     print(f"Error: Index out of bounds during replacement at ({r},{c}). Sequence length: {sequence_length}")
                     # Optionally, handle this error more gracefully (e.g., leave pixel as 0)

    # 4. Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()