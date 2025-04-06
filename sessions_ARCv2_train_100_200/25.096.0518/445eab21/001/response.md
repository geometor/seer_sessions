```python
"""
Identify the most frequent non-zero digit in the 10x10 input grid and create a 2x2 output grid filled entirely with that digit.
"""

import collections

def find_non_zero_digits_and_counts(grid: list[list[int]]) -> dict[int, int]:
    """
    Finds all non-zero digits in the grid and counts their frequencies.

    Args:
        grid: The input grid (list of lists of integers).

    Returns:
        A dictionary where keys are the non-zero digits and values are their counts.
    """
    counts = collections.Counter()
    for row in grid:
        for cell in row:
            if cell != 0:
                counts[cell] += 1
    return counts

def find_most_frequent_digit(counts: dict[int, int]) -> int:
    """
    Determines the digit with the highest frequency from the counts dictionary.

    Args:
        counts: A dictionary of digit frequencies.

    Returns:
        The digit with the maximum count. Returns -1 if counts is empty.
    """
    if not counts:
        # Handle empty case if necessary, though problem implies non-zero digits exist
        return -1 # Or raise an error
    
    # Find the digit (key) with the maximum count (value)
    most_frequent = max(counts, key=counts.get)
    return most_frequent

def create_filled_grid(size: tuple[int, int], fill_value: int) -> list[list[int]]:
    """
    Creates a grid of a specified size filled with a specific value.

    Args:
        size: A tuple (rows, cols) specifying the dimensions of the grid.
        fill_value: The integer value to fill the grid with.

    Returns:
        A new grid (list of lists of integers) filled with the fill_value.
    """
    rows, cols = size
    return [[fill_value for _ in range(cols)] for _ in range(rows)]


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the identified rule:
    1. Find the two distinct non-zero digits in the input.
    2. Count the occurrences of each non-zero digit.
    3. Identify the digit with the higher count.
    4. Create a 2x2 grid filled with that most frequent digit.

    Args:
        input_grid: A 10x10 list of lists representing the input grid.

    Returns:
        A 2x2 list of lists representing the output grid.
    """
    
    # 1 & 2: Identify non-zero digits and count their frequencies
    digit_counts = find_non_zero_digits_and_counts(input_grid)

    # 3: Find the most frequent digit
    output_digit = find_most_frequent_digit(digit_counts)

    # 4 & 5: Create and fill the 2x2 output grid
    output_grid = create_filled_grid(size=(2, 2), fill_value=output_digit)

    return output_grid
```