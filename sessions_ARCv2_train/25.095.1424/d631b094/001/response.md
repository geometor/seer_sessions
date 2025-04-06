```python
import math
import collections
import numpy as np
from typing import List, Tuple, Dict, Any, Optional

"""
Extracts all non-zero numbers from an input 2D grid and returns them as a single space-separated string, preserving the order encountered when scanning the grid row by row, left to right.

1.  Initialize an empty list to store the non-zero numbers.
2.  Iterate through each row of the input grid, from the top row to the bottom row.
3.  Within each row, iterate through each element (number) from left to right.
4.  If the current element is not zero, append it to the list of non-zero numbers.
5.  After iterating through all elements in the grid, convert the numbers in the collected list to strings.
6.  Join the string representations of the numbers with a single space delimiter to form the final output string.
"""


def transform(input_grid: list[list[int]]) -> str:
    """
    Extracts non-zero elements from a grid and returns them as a space-separated string.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A string containing the non-zero elements from the grid, separated by spaces,
        in the order they appear (row-major).
    """

    # Initialize an empty list to store the non-zero numbers.
    non_zero_elements = []

    # Iterate through each row of the input grid.
    for row in input_grid:
        # Within each row, iterate through each element.
        for element in row:
            # If the current element is not zero, append it to the list.
            if element != 0:
                non_zero_elements.append(element)

    # Convert the collected numbers to strings.
    string_elements = [str(num) for num in non_zero_elements]

    # Join the string representations with a single space delimiter.
    output_string = " ".join(string_elements)

    # Return the final output string.
    return output_string

```