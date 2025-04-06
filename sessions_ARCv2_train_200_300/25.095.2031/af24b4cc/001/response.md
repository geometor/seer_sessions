```python
"""
Summarize a 9x10 input grid into a 4x5 output grid. The input grid contains six 3x2 blocks of non-zero digits separated by rows and columns of zeros. For each input block, find the non-zero digit that appears most frequently within that block. Place this most frequent digit into the corresponding cell in the 2x3 core of the 4x5 output grid. The output grid has a border of zeros.
"""

from collections import Counter
import numpy as np # Using numpy for easier slicing, though list comprehensions work too

def find_most_frequent_non_zero(numbers: list[int]) -> int | None:
    """
    Finds the most frequent non-zero integer in a list.
    Returns None if the list contains no non-zero numbers or is empty.
    Handles ties by returning the number that appears first in Counter's most_common.
    """
    non_zeros = [num for num in numbers if num != 0]
    if not non_zeros:
        return None  # Return 0 or handle as appropriate if block is all zeros

    count = Counter(non_zeros)
    # most_common(1) returns a list of tuples [(element, count)], get the element
    most_frequent = count.most_common(1)[0][0]
    return most_frequent

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the most frequent non-zero digit in defined blocks.
    """
    # Convert input to numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # initialize output_grid (4x5) with zeros
    output_grid = [[0 for _ in range(5)] for _ in range(4)]

    # Define input block boundaries (row_start, row_end_exclusive, col_start, col_end_exclusive)
    # These correspond to numpy slicing conventions
    block_definitions = [
        (1, 4, 1, 3),  # TopLeft
        (1, 4, 4, 6),  # TopMid
        (1, 4, 7, 9),  # TopRight
        (5, 8, 1, 3),  # BottomLeft
        (5, 8, 4, 6),  # BottomMid
        (5, 8, 7, 9),  # BottomRight
    ]

    # Define mapping from block index to output grid coordinates (row, col)
    output_coords = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3)
    ]

    # perform transformations for each block
    for i, (r_start, r_end, c_start, c_end) in enumerate(block_definitions):
        # Extract the block using numpy slicing
        block = input_array[r_start:r_end, c_start:c_end]

        # Flatten the block into a list of numbers
        block_values = block.flatten().tolist()

        # Find the most frequent non-zero number in the block
        most_frequent_num = find_most_frequent_non_zero(block_values)

        # Place the result in the corresponding output cell if a number was found
        if most_frequent_num is not None:
            out_r, out_c = output_coords[i]
            output_grid[out_r][out_c] = most_frequent_num

    return output_grid
```