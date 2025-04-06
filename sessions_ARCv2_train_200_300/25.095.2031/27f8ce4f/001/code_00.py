import collections

"""
Transformation Rule Natural Language Description:

1.  Analyze the input 3x3 grid to find the frequency of each non-zero digit (1-9).
2.  Identify the digit (`target_digit`) that appears most frequently. If there is a tie in frequency, select the largest digit among those tied.
3.  Initialize a 9x9 output grid filled with zeros.
4.  Conceptually divide the 9x9 output grid into a 3x3 grid of smaller 3x3 blocks.
5.  Iterate through each cell `(r, c)` of the input 3x3 grid (where `r` is the row index and `c` is the column index, both 0-indexed).
6.  If the digit at `input_grid[r][c]` is equal to the `target_digit`, then copy the entire original 3x3 input grid into the corresponding 3x3 block of the output grid. The top-left corner of this block in the output grid is at `(r * 3, c * 3)`.
7.  If the digit at `input_grid[r][c]` is *not* equal to the `target_digit`, the corresponding 3x3 block in the output grid remains filled with zeros.
8.  Return the final 9x9 output grid.
"""

def get_most_frequent_digit(grid: list[list[int]]) -> int:
    """
    Finds the most frequent non-zero digit in the grid.
    If there's a tie, returns the largest digit among the tied ones.
    Returns 0 if the grid contains only zeros or is empty.
    """
    counts = collections.defaultdict(int)
    max_freq = 0
    most_frequent_digits = []

    # Count frequency of each non-zero digit
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            digit = grid[r][c]
            if digit != 0:
                counts[digit] += 1

    if not counts:
      return 0 # Handle case with only zeros or empty grid

    # Find the maximum frequency
    for digit in counts:
        if counts[digit] > max_freq:
            max_freq = counts[digit]

    # Find all digits with the maximum frequency
    for digit in counts:
        if counts[digit] == max_freq:
            most_frequent_digits.append(digit)

    # Return the largest digit among those with the maximum frequency
    return max(most_frequent_digits) if most_frequent_digits else 0

def copy_block(output_grid: list[list[int]], block: list[list[int]], start_row: int, start_col: int):
    """Copies a smaller block into the output grid at the specified location."""
    block_rows = len(block)
    block_cols = len(block[0])
    for r in range(block_rows):
        for c in range(block_cols):
            output_grid[start_row + r][start_col + c] = block[r][c]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 3x3 input grid into a 9x9 output grid based on the frequency
    of digits in the input. The input grid is copied into 3x3 blocks of the
    output grid corresponding to the locations of the most frequent digit
    in the input grid.
    """
    # Define grid dimensions
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])
    output_rows = input_rows * 3
    output_cols = input_cols * 3

    # Initialize the 9x9 output grid with zeros
    output_grid = [[0 for _ in range(output_cols)] for _ in range(output_rows)]

    # Find the target digit (most frequent, largest in case of tie)
    target_digit = get_most_frequent_digit(input_grid)

    # If no non-zero digits found, return the zero grid
    if target_digit == 0:
        return output_grid

    # Iterate through the input grid cells (r, c)
    for r in range(input_rows):
        for c in range(input_cols):
            # Check if the digit at the current cell matches the target digit
            if input_grid[r][c] == target_digit:
                # Calculate the top-left corner of the corresponding block in the output grid
                block_start_row = r * input_rows
                block_start_col = c * input_cols
                # Copy the entire input grid into that block
                copy_block(output_grid, input_grid, block_start_row, block_start_col)
            # Else: the block remains zeros (already initialized)

    return output_grid