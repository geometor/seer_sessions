import numpy as np

"""
The transformation restores a background pattern that has been partially obscured by white (0) pixels.
The background pattern consists of two alternating row types:
1. Even-numbered rows (0, 2, 4, ...) are entirely filled with blue (1).
2. Odd-numbered rows (1, 3, 5, ...) consist of a horizontally repeating sequence of colors.

The process is:
1.  Determine the repeating background color sequence for the odd-numbered rows by:
    a.  Finding the first odd-numbered row in the input grid that does not contain any white (0) pixels.
    b.  Analyzing this row to identify the shortest sequence of colors (S) that repeats horizontally to form the row content, and record its length (L).
2.  Create an output grid by copying the input grid.
3.  Iterate through each cell (row, col) of the input grid.
4.  If a cell contains white (0):
    a.  If the cell is in an even row (row % 2 == 0), replace the white pixel in the output grid with blue (1).
    b.  If the cell is in an odd row (row % 2 != 0), replace the white pixel in the output grid with the color from the sequence S at index (col % L).
5. Return the modified output grid.
"""

def find_shortest_repeating_sequence(row_array):
    """
    Finds the shortest repeating sequence in a 1D numpy array.

    Args:
        row_array (np.ndarray): A 1D numpy array representing a row.

    Returns:
        tuple: A tuple containing the sequence (list) and its length (int).
               Returns (list(row_array), len(row_array)) if no shorter repeat is found.
    """
    n = len(row_array)
    for length in range(1, n // 2 + 1):
        # Check if the length divides the array length or if the partial segment matches
        if n % length == 0: # Perfect fit
             is_repeating = True
             sequence = row_array[:length]
             for i in range(length, n, length):
                 if not np.array_equal(row_array[i:i+length], sequence):
                     is_repeating = False
                     break
             if is_repeating:
                 return list(sequence), length
        else: # Check if the row is composed of repeats plus a prefix of the sequence
            is_repeating = True
            sequence = row_array[:length]
            num_full_repeats = n // length
            for i in range(length, num_full_repeats * length, length):
                 if not np.array_equal(row_array[i:i+length], sequence):
                     is_repeating = False
                     break
            if is_repeating:
                 # Check the remaining partial segment
                 remaining_len = n % length
                 if np.array_equal(row_array[num_full_repeats * length:], sequence[:remaining_len]):
                     return list(sequence), length

    # If no shorter repeating sequence is found, the whole row is the sequence
    return list(row_array), n


def find_odd_row_pattern(grid_np):
    """
    Finds the repeating color sequence from the first odd row
    that doesn't contain any white (0) pixels.

    Args:
        grid_np (np.ndarray): The input grid as a numpy array.

    Returns:
        tuple: A tuple containing the sequence (list) and its length (int).

    Raises:
        ValueError: If no suitable odd row (without 0s) is found.
    """
    height, width = grid_np.shape
    # Iterate through odd rows (1, 3, 5...)
    for r in range(1, height, 2):
        row_data = grid_np[r, :]
        # Check if the row contains any white pixels (0)
        if 0 not in row_data:
            # Found a suitable row. Find the shortest repeating pattern in it.
            return find_shortest_repeating_sequence(row_data)

    # Raise an error if no suitable row found (shouldn't happen based on examples)
    raise ValueError("Could not determine the repeating pattern in odd rows: No odd row without '0' found.")


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
        odd_row_sequence, seq_len = find_odd_row_pattern(input_grid_np)
        if seq_len == 0: # Should not happen if find_odd_row_pattern works correctly
             raise ValueError("Identified sequence length is zero.")
    except ValueError as e:
        # Handle error case - perhaps return input or a default grid?
        # For now, re-raise or print, as the logic depends on finding this pattern.
        print(f"Error finding pattern: {e}")
        # Returning the input copy might be a safe fallback for some ARC tasks
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