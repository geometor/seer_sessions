"""
Identify the most frequent digit (background) in the input grid.
Scan the grid row by row, from top to bottom, and left to right within each row.
Collect all digits that are *not* the background digit into a new list, preserving the scan order.
Return the resulting list of foreground digits.
"""

from collections import Counter
import itertools

def find_background_digit(grid: list[list[int]]) -> int:
  """Finds the most frequent digit in the grid."""
  # Flatten the grid into a single list of digits
  all_digits = list(itertools.chain.from_iterable(grid))
  # Count the occurrences of each digit
  counts = Counter(all_digits)
  # Find the digit with the maximum count
  # If there's a tie, most_common(1) returns one of the most frequent
  background_digit = counts.most_common(1)[0][0]
  return background_digit

def transform(input_grid: list[list[int]]) -> list[int]:
  """
    Extracts foreground digits from a grid based on frequency analysis.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 1D list containing the foreground digits in scan order.
    """

  # 1. Identify the background digit
  background_digit = find_background_digit(input_grid)

  # 2. Initialize an empty list for the output
  output_list = []

  # 3. Scan the grid (top-to-bottom, left-to-right)
  for row in input_grid:
    for cell_value in row:
      # 4. Check if the cell value is a foreground digit
      if cell_value != background_digit:
        # 5. Extract (append) the foreground digit
        output_list.append(cell_value)

  # 6. Return the list of extracted foreground digits
  return output_list