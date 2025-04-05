import math
import collections

"""
Transforms a sequence of 12 digits by interpreting it as a 3x4 grid (3 rows, 4 columns),
performing a vertical circular shift upwards on the rows (Row 1 -> Row 3, Row 2 -> Row 1,
Row 3 -> Row 2), and then flattening the transformed grid back into a sequence.
The final output is formatted as a space-separated string.
"""

def reshape_to_grid(sequence, rows, cols):
    """
    Reshapes a flat sequence into a grid (list of lists).

    Args:
        sequence: A list of elements.
        rows: The desired number of rows.
        cols: The desired number of columns.

    Returns:
        A list of lists representing the grid.
    """
    if len(sequence) != rows * cols:
        raise ValueError("Sequence length does not match grid dimensions")
    grid = []
    for r in range(rows):
        # Calculate start and end indices for the current row
        start_index = r * cols
        end_index = start_index + cols
        # Extract the row from the sequence
        row = sequence[start_index:end_index]
        grid.append(row)
    return grid

def flatten_grid(grid):
    """
    Flattens a grid (list of lists) into a single sequence (list).

    Args:
        grid: A list of lists representing the grid.

    Returns:
        A flat list containing all elements from the grid.
    """
    sequence = []
    # Iterate through each row in the grid
    for row in grid:
        # Extend the sequence list with the elements of the current row
        sequence.extend(row)
    return sequence

def transform(input_str):
    """
    Applies the 3x4 grid vertical circular shift transformation.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing 12 space-separated digits representing the transformed sequence.
    """
    # Define grid dimensions based on the task description
    rows = 3
    cols = 4
    expected_length = rows * cols

    # --- Input Processing ---
    # Parse the input string into a list of integers
    try:
        input_sequence = [int(d) for d in input_str.split()]
    except ValueError:
        raise ValueError("Input string must contain only space-separated integers.")

    # Validate input length
    if len(input_sequence) != expected_length:
        raise ValueError(f"Input sequence length must be {expected_length}, got {len(input_sequence)}")

    # --- Core Transformation ---
    # 1. Reshape the input sequence into a 3x4 grid
    input_grid = reshape_to_grid(input_sequence, rows, cols)

    # 2. Apply the specific vertical circular shift
    # Rule: New Row 1 = Old Row 2
    #       New Row 2 = Old Row 3
    #       New Row 3 = Old Row 1
    # Initialize the output grid structure
    output_grid = [None] * rows

    # Apply the row shift logic based on 0-based indexing
    output_grid[0] = input_grid[1]  # New Row 0 (Row 1 in 1-based index) gets Old Row 1 (Row 2)
    output_grid[1] = input_grid[2]  # New Row 1 (Row 2) gets Old Row 2 (Row 3)
    output_grid[2] = input_grid[0]  # New Row 2 (Row 3) gets Old Row 0 (Row 1)

    # 3. Flatten the transformed grid back into a sequence
    output_sequence = flatten_grid(output_grid)

    # --- Output Formatting ---
    # Convert the list of integers back to a space-separated string
    output_str = " ".join(map(str, output_sequence))

    return output_str
