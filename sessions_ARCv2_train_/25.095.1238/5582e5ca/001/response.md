```python
"""
Transforms a 3x3 grid of digits by identifying the most frequent digit (mode)
in the input grid and creating a new 3x3 grid filled entirely with that mode digit.
"""

from collections import Counter
import itertools

def find_mode(numbers: list[int]) -> int:
    """
    Finds the mode (most frequent number) in a list of numbers.
    If there are ties for the mode, returns the smallest number among the modes.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty")

    counts = Counter(numbers)
    max_count = 0
    modes = []

    # Find the maximum frequency
    for number, count in counts.items():
        if count > max_count:
            max_count = count

    # Find all numbers with the maximum frequency
    for number, count in counts.items():
        if count == max_count:
            modes.append(number)

    # Return the smallest number among the modes in case of a tie
    return min(modes)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the mode digit.

    Args:
        input_grid: A 3x3 list of lists containing single-digit integers.

    Returns:
        A 3x3 list of lists where all cells are filled with the mode
        digit from the input_grid.
    """
    # 1. Flatten the input grid into a single list of digits.
    #    Use itertools.chain.from_iterable for efficient flattening.
    all_digits = list(itertools.chain.from_iterable(input_grid))

    # 2. Count occurrences and find the mode digit using the helper function.
    #    The helper handles ties by choosing the smallest digit.
    mode_digit = find_mode(all_digits)

    # 3. Determine the dimensions of the input grid (assuming square grid or using first row).
    #    For this specific task, we know it's 3x3.
    rows = len(input_grid)
    # Assuming it's not an empty grid, get cols from the first row
    cols = len(input_grid[0]) if rows > 0 else 0

    # 4. Construct a new grid with the same dimensions.
    # 5. Fill every cell of the new grid with the mode digit.
    output_grid = [[mode_digit for _ in range(cols)] for _ in range(rows)]

    # 6. Return the resulting grid.
    return output_grid

```