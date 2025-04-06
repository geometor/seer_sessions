```python
import collections
import itertools
import numpy as np

"""
Transforms an input grid of integers into an output grid based on the frequency of non-zero numbers.

1.  Count the frequency of each unique non-zero integer in the input grid.
2.  Determine the maximum frequency count among all non-zero integers. This sets the number of rows for the output grid.
3.  Identify the unique non-zero integers and sort them primarily by their frequency (descending) and secondarily by their value (ascending) to break ties. This order determines the columns of the output grid.
4.  The number of columns in the output grid is the count of unique non-zero integers.
5.  Create an output grid with the determined dimensions (max_frequency rows, unique_non_zeros columns), initialized with zeros.
6.  For each unique non-zero integer in the sorted list (corresponding to an output column), fill that column from the top downwards with the integer, repeating it a number of times equal to its frequency count.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on non-zero integer frequencies.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    # 1. Count Frequencies
    # Flatten the grid to easily iterate through all elements
    all_elements = list(itertools.chain.from_iterable(input_grid))
    # Count occurrences of non-zero elements
    counts = collections.Counter(el for el in all_elements if el != 0)

    # Handle case where input grid contains only zeros
    if not counts:
        # Based on examples, if there are no non-zero numbers,
        # the output should be an empty grid (0 rows, 0 cols).
        return []

    # 2. Find Max Frequency
    max_count = max(counts.values())

    # 3. Sort Unique Numbers
    # Sort unique non-zero numbers: primary key = count (desc), secondary key = value (asc)
    sorted_unique_numbers = sorted(counts.keys(), key=lambda x: (-counts[x], x))

    # 4. Determine Output Dimensions
    num_output_rows = max_count
    num_output_cols = len(sorted_unique_numbers)

    # 5. Initialize Output Grid
    # Create the output grid filled with zeros
    output_grid = [[0] * num_output_cols for _ in range(num_output_rows)]

    # 6. Construct Output Grid
    # Iterate through the sorted numbers, using the index as the column number
    for col_index, number in enumerate(sorted_unique_numbers):
        # Get the frequency count for the current number
        count = counts[number]
        # Fill the corresponding column from the top down
        for row_index in range(count):
            # Ensure we don't write past the allocated rows (though this shouldn't happen
            # if max_count is calculated correctly)
            if row_index < num_output_rows:
                output_grid[row_index][col_index] = number

    return output_grid
```