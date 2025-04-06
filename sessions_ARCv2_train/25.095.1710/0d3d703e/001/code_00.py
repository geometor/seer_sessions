import numpy as np # Although not strictly necessary for this specific logic, it's often useful for grid operations

"""
Transforms an input grid of digits by applying a fixed, element-wise mapping to each digit.
The mapping rules are:
1 -> 5
2 -> 6
3 -> 4
4 -> 3
5 -> 1
6 -> 2
8 -> 9
9 -> 8
Digits 0 and 7 map to themselves (based on assumption as they weren't in examples).
The transformation is applied independently to each cell, resulting in an output grid
of the same dimensions where each digit is the mapped version of the corresponding input digit.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a fixed digit mapping to each element of the input grid.

    Args:
        input_grid: A list of lists representing the input grid of digits.

    Returns:
        A list of lists representing the output grid with mapped digits.
    """

    # Define the fixed mapping for digits
    digit_map = {
        1: 5,
        2: 6,
        3: 4,
        4: 3,
        5: 1,
        6: 2,
        8: 9,
        9: 8,
        0: 0,  # Assumed mapping
        7: 7   # Assumed mapping
    }

    # Initialize the output grid as an empty list
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Create a new row for the output grid
        new_row = []
        # Iterate through each digit (cell) in the current input row
        for digit in row:
            # Find the mapped digit using the dictionary.
            # Use .get() with the digit itself as default to handle unmapped digits (0, 7)
            mapped_digit = digit_map.get(digit, digit)
            # Append the mapped digit to the new row
            new_row.append(mapped_digit)
        # Append the completed new row to the output grid
        output_grid.append(new_row)

    # Return the fully transformed grid
    return output_grid