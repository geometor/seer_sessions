import math
import re

"""
Processes a string containing two numerical grids separated by a blank line.
Discards the first grid.
If the second grid (InputGrid2) has an odd number of rows (H2), 
the output is InputGrid2 stacked vertically on top of itself.
If InputGrid2 has an even number of rows (H2), it's split into a top half 
(first H2/2 rows) and a bottom half (last H2/2 rows). The output is constructed 
by vertically stacking these halves in the sequence: BottomHalf, TopHalf, 
BottomHalf, TopHalf, BottomHalf.
"""

def parse_input_string(input_str: str) -> tuple[list[list[int]], list[list[int]]]:
    """
    Parses the input string into two grids.
    Handles potential leading/trailing whitespace and converts numbers.
    """
    # Split into blocks based on double newline or more
    blocks = re.split(r'\n\s*\n', input_str.strip())
    if len(blocks) != 2:
        # Handle cases with potentially only one grid if needed,
        # but based on examples, expect two.
        # For now, assume the second block might be empty if parsing fails
        # or raise an error. Let's assume valid input structure for now.
        pass # Or raise ValueError("Input does not contain two grids separated by a blank line.")

    grid1_str, grid2_str = blocks

    def parse_grid_block(block_str: str) -> list[list[int]]:
        grid = []
        lines = block_str.strip().split('\n')
        for line in lines:
            if line.strip(): # Ensure line is not empty
                 grid.append([int(num) for num in line.split()])
        return grid

    grid1 = parse_grid_block(grid1_str)
    grid2 = parse_grid_block(grid2_str)
    return grid1, grid2


def transform(input_str: str) -> list[list[int]]:
    """
    Applies the transformation rule based on the height parity of the second grid.

    Args:
        input_str: A string containing two grids separated by a blank line.

    Returns:
        A list of lists of integers representing the transformed output grid.
    """

    # Parse the input string to get the two grids
    # We only need the second grid for the transformation
    _, grid2 = parse_input_string(input_str)

    # Initialize output_grid
    output_grid = []

    # Get the height (number of rows) of the second grid
    h2 = len(grid2)

    # Check if the height is zero (empty grid2) - handle edge case
    if h2 == 0:
        return [] # Return empty grid if grid2 is empty

    # Check if the height H2 is odd or even
    if h2 % 2 != 0:
        # If H2 is odd: Stack InputGrid2 with itself
        # The '+' operator for lists performs concatenation
        output_grid = grid2 + grid2
    else:
        # If H2 is even: Split into top and bottom halves
        midpoint = h2 // 2
        top_half = grid2[:midpoint]
        bottom_half = grid2[midpoint:]

        # Construct the output by stacking in the sequence:
        # BottomHalf, TopHalf, BottomHalf, TopHalf, BottomHalf
        output_grid = bottom_half + top_half + bottom_half + top_half + bottom_half

    # Return the constructed output grid
    return output_grid
