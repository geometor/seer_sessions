```python
"""
Processes a grid of single-digit integers.
Determines the scan direction (horizontal or vertical) based on the grid's aspect ratio (rows vs. columns).
If rows >= columns, scan horizontally (row-by-row).
If columns > rows, scan vertically (column-by-column).
For each line (row or column) in the scan direction, find the most frequent number (dominant number). Ties are resolved arbitrarily by Counter.
Collect the sequence of these dominant numbers.
Collapse this sequence by removing consecutive identical numbers, preserving the order of the first occurrence of each band.
Construct the output grid:
- If scanned horizontally, the output is a single column grid (Nx1) containing the collapsed sequence.
- If scanned vertically, the output is a single row grid (1xN) containing the collapsed sequence.
"""

import collections
import numpy as np
from typing import List, Tuple

def _find_dominant_number(line: List[int]) -> int:
    """Finds the most frequent number in a list. Handles ties by picking one."""
    if not line:
        # This case should ideally not happen based on ARC task constraints,
        # but if it did, we might need a default or raise an error.
        # Let's assume non-empty lines as per examples.
        # If an empty line resulted in, say, 0 counts, most_common might fail.
         raise ValueError("Encountered an empty line/column for dominant number calculation.")

    # Count occurrences of each number
    counts = collections.Counter(line)
    # Find the number with the maximum count
    # most_common(1) returns a list of the single most common item: [ (element, count) ]
    dominant_num, _ = counts.most_common(1)[0]
    return dominant_num

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on dominant numbers in rows or columns,
    returning the collapsed sequence formatted as a single row or column grid.

    Args:
        input_grid: A list of lists representing the grid of integers.

    Returns:
        A list of lists representing the output grid (either Nx1 or 1xN).
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return [[]] # Or return [] depending on expected format for empty input

    # 1. Determine grid dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # 2. Determine scan direction
    scan_direction = 'horizontal' if num_rows >= num_cols else 'vertical'

    # 3. Initialize dominant numbers list
    dominant_numbers = []

    # 4./5. Calculate dominant numbers for each row or column
    if scan_direction == 'horizontal':
        # Iterate through each row
        for row_idx in range(num_rows):
            row = input_grid[row_idx]
            dominant_num = _find_dominant_number(row)
            dominant_numbers.append(dominant_num)
    else: # scan_direction == 'vertical'
        # Use numpy for easy column access
        np_grid = np.array(input_grid, dtype=int)
        # Iterate through each column
        for col_idx in range(num_cols):
            column = np_grid[:, col_idx].tolist()
            dominant_num = _find_dominant_number(column)
            dominant_numbers.append(dominant_num)

    # 6. Initialize collapsed sequence list
    collapsed_sequence = []

    # 7. Identify unique consecutive dominant numbers (collapse bands)
    if dominant_numbers:
        # Add the first dominant number
        collapsed_sequence.append(dominant_numbers[0])
        # Iterate through the rest, adding only when the number changes
        for i in range(1, len(dominant_numbers)):
            if dominant_numbers[i] != dominant_numbers[i-1]:
                collapsed_sequence.append(dominant_numbers[i])

    # 8. Construct the output_grid based on scan_direction
    output_grid = []
    if scan_direction == 'horizontal':
        # Create a column vector (Nx1 grid)
        output_grid = [[num] for num in collapsed_sequence]
    else: # scan_direction == 'vertical'
        # Create a row vector (1xN grid)
        # Need to check if collapsed_sequence is empty first
        if collapsed_sequence:
             output_grid = [collapsed_sequence]
        else:
             output_grid = [] # Handle empty sequence case

    # 9. Return the output_grid
    return output_grid
```