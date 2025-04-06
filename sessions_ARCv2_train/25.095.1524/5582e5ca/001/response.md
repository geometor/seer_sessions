```python
"""
Transforms a 3x3 input grid of digits by finding the most frequent digit 
within the input grid and creating a new 3x3 grid filled entirely with 
that most frequent digit.
"""

from collections import Counter
import itertools

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Finds the most frequent digit in the input 3x3 grid and returns a 
    new 3x3 grid filled with that digit.

    Args:
        input_grid: A 3x3 list of lists containing single-digit integers.

    Returns:
        A 3x3 list of lists where all elements are the most frequent 
        digit from the input_grid.
    """

    # Flatten the 2D input grid into a 1D list of digits
    all_digits = list(itertools.chain.from_iterable(input_grid))

    # Count the frequency of each digit
    digit_counts = Counter(all_digits)

    # Find the digit with the highest frequency
    # most_common(1) returns a list of tuples [(digit, count)], so we take the first element [0]
    # and then the digit itself [0] from the tuple.
    most_frequent_digit = digit_counts.most_common(1)[0][0]

    # Determine the dimensions of the input grid (assuming it's always 3x3 based on examples)
    rows = len(input_grid)
    # Assuming a square grid or at least consistent row lengths
    cols = len(input_grid[0]) if rows > 0 else 0 

    # Initialize the output grid with the same dimensions as the input
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Fill the output grid with the most frequent digit
    for r in range(rows):
        for c in range(cols):
            output_grid[r][c] = most_frequent_digit

    return output_grid

```