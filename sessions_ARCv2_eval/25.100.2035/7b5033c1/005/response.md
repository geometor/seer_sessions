```python
"""
Identifies the most frequent digit (background) in the input grid.
Scans the grid row by row, top-to-bottom, and left-to-right within rows.
Collects all digits that are *not* the background digit, preserving their scan order.
Formats the collected digits into a grid with a single column, where each row contains one collected digit.
Returns this single-column grid. If no non-background digits are found, returns an empty grid ([]).
"""

from collections import Counter
import itertools

def find_background_digit(grid: list[list[int]]) -> int | None:
  """
  Finds the most frequent digit in the grid.

  Args:
    grid: The input 2D list of integers.

  Returns:
    The integer digit that appears most frequently in the grid,
    or None if the grid is empty or contains no digits.
  """
  # Flatten the grid into a single list of digits
  all_digits = list(itertools.chain.from_iterable(grid))

  # Handle empty grid case
  if not all_digits:
      return None # No digits to find a background from

  # Count the occurrences of each digit
  counts = Counter(all_digits)

  # Find the digit with the maximum count
  # If there's a tie, most_common(1) returns one of the most frequent
  background_digit = counts.most_common(1)[0][0]
  return background_digit

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by extracting foreground digits and formatting
    them into a single-column output grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list representing a grid with one column, where each row
        contains one foreground digit from the input grid, ordered by
        row-major scan position. Returns an empty list ([]) if no
        foreground digits are found or the input grid is empty.
    """

    # 1. Identify the background digit
    background_digit = find_background_digit(input_grid)

    # Handle case where input grid was effectively empty
    if background_digit is None:
        return []

    # 2. Initialize an empty list to store foreground digits
    foreground_digits = []

    # 3. Scan the grid (top-to-bottom, left-to-right)
    for row in input_grid:
        for cell_value in row:
            # 4. Check if the cell value is a foreground digit
            if cell_value != background_digit:
                # 5. Extract (append) the foreground digit
                foreground_digits.append(cell_value)

    # 6. Format the output into a single-column grid
    # If no foreground digits were found, return an empty list
    if not foreground_digits:
        return []

    # Create the output grid: each foreground digit becomes a single-element row
    output_grid = [[digit] for digit in foreground_digits]

    # 7. Return the formatted single-column grid
    return output_grid
```