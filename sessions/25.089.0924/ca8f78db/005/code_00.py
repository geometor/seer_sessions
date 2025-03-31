import numpy as np

"""
The transformation restores a background pattern that has been partially obscured by white (0) pixels.
The background pattern consists of two alternating row types:
1. Even-numbered rows (0, 2, 4, ...) are entirely filled with blue (1).
2. Odd-numbered rows (1, 3, 5, ...) consist of a horizontally repeating sequence of colors.

The process is:
1.  Determine the repeating background color sequence (S) and its length (L) for the odd-numbered rows by:
    a.  Finding the first odd-numbered row in the input grid that does not contain any white (0) pixels.
    b.  Identifying the pattern in this row by finding the first index 'L' (L > 0) where the color matches the color at index 0. The sequence S is the sub-array from index 0 to L-1.
2.  Create an output grid by copying the input grid.
3.  Iterate through each cell (row, col) of the input grid.
4.  If a cell contains white (0):
    a.  If the cell is in an even row (row % 2 == 0), replace the white pixel in the output grid with blue (1).
    b.  If the cell is in an odd row (row % 2 != 0), replace the white pixel in the output grid with the color from the sequence S at index (col % L).
5. Return the modified output grid.
"""

def find_odd_row_pattern_simple(grid_np):
    """
    Finds the repeating color sequence and its length from the first odd row
    that doesn't contain any white (0) pixels. Assumes the pattern starts
    at column 0 and repeats.

    Args:
        grid_np (np.ndarray): The input grid as a numpy array.

    Returns:
        tuple: A tuple containing the sequence (list) and its length (int).

    Raises:
        ValueError: If no suitable odd row (without 0s) is found or if no repeat
                    is found within a suitable row.
    """
    height, width = grid_np.shape
    # Iterate through odd rows (1, 3, 5...)
    for r in range(1, height, 2):
        row_data = grid_np[r, :]
        # Check if the row contains any white pixels (0)
        if 0 not in row_data:
            # Found a suitable row. Find the pattern length.
            start_color = row_data[0]
            sequence = None
            seq_len = 0
            # Find the first repeat of the starting color
            for l in range(1, width):
                if row_data[l] == start_color:
                    sequence = list(row_data[0:l])
                    seq_len = l
                    return sequence, seq_len
            # If no repeat found, maybe the whole row is the unit (less likely)
            # Or perhaps the pattern doesn't start repeating within the grid width?
            # Let's assume for now a repeat must exist if the row is non-zero.
            # If we reach here without returning, something is wrong or assumption failed.
            raise ValueError(f"Could not find repeat of start color in suitable odd row {r}.")


    # Raise an error if no suitable row found
    raise ValueError("Could not determine the repeating pattern: No odd row without '0' found.")


def transform(input_grid):
    """
    Restores the background pattern obscured by white pixels.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid with the pattern restored.
    """
    # Convert input_grid to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize output_grid as a copy of the input
    output_grid_np = input_grid_np.copy()

    # Find the repeating sequence and its length for odd rows
    try:
        odd_row_sequence, seq_len = find_odd_row_pattern_simple(input_grid_np)
        if seq_len == 0: # Safety check
             raise ValueError("Identified sequence length is zero.")
    except ValueError as e:
        # If pattern finding fails, return the original grid copy
        # This might occur if there are no odd rows without 0s,
        # or if the pattern assumption fails.
        print(f"Warning: Error finding pattern: {e}. Returning input copy.")
        return output_grid_np.tolist()

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the input is white (0)
            if input_grid_np[r, c] == 0:
                # Determine the correct background color based on row type
                if r % 2 == 0:
                    # Even row: background is blue (1)
                    output_grid_np[r, c] = 1
                else:
                    # Odd row: background follows the repeating sequence
                    # Calculate the index in the sequence based on column
                    pattern_index = c % seq_len
                    output_grid_np[r, c] = odd_row_sequence[pattern_index]
            # Else: Non-white pixels are already correct due to the initial copy

    # Convert the result back to a list of lists before returning
    return output_grid_np.tolist()