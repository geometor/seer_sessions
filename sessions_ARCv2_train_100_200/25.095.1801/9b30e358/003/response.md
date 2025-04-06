```python
import re
import math # Included for completeness, though not strictly needed for this logic

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

def parse_grid_block(block_str: str) -> list[list[int]]:
    """
    Parses a block of text representing a grid into a 2D list of integers.
    """
    grid = []
    lines = block_str.strip().split('\n')
    for line in lines:
        if line.strip(): # Ensure line is not empty or just whitespace
             # Split line by whitespace and convert each part to int
             row = [int(num) for num in line.split()]
             grid.append(row)
    return grid

def parse_input_string(input_str: str) -> tuple[list[list[int]], list[list[int]]]:
    """
    Parses the raw input string into two separate grids (list of lists of ints).
    Assumes the input string contains two grids separated by one or more blank lines.
    """
    # Split into blocks based on one or more blank lines (uses regex for flexibility)
    blocks = re.split(r'\n\s*\n', input_str.strip())
    
    # Handle cases where splitting might not yield exactly two blocks
    if len(blocks) < 2:
        # Or raise ValueError("Input does not contain two grids separated by a blank line.")
        # Based on problem description, we expect two grids.
        # If only one block is found, maybe treat it as grid2? Or error?
        # Let's assume valid input means two blocks. If block[1] is empty, parse_grid_block handles it.
         grid1_str = blocks[0] if len(blocks) > 0 else ""
         grid2_str = "" # No second grid found
    elif len(blocks) > 2:
        # If more than two blocks, maybe combine blocks after the first?
        # For now, strictly adhere to the two-block structure.
        grid1_str = blocks[0]
        # Let's assume the second logical grid is the second block found
        grid2_str = blocks[1] 
    else:
        grid1_str, grid2_str = blocks

    # Parse each block string into a grid
    grid1 = parse_grid_block(grid1_str)
    grid2 = parse_grid_block(grid2_str)
    
    return grid1, grid2


def transform(input_str: str) -> list[list[int]]:
    """
    Applies the transformation rule based on the height parity of the second grid
    parsed from the input string.
    """
    # Parse the input string to get the two grids
    # The first grid (grid1) is discarded as per the transformation rule
    _, grid2 = parse_input_string(input_str)

    # Initialize the output grid (list of lists)
    output_grid = []

    # Get the height (number of rows) of the second grid
    h2 = len(grid2)

    # Check if the second grid is empty
    if h2 == 0:
        return [] # Return an empty grid if grid2 is empty

    # Determine the transformation based on whether h2 is odd or even
    if h2 % 2 != 0:
        # --- Odd height case ---
        # Vertically stack grid2 on top of itself
        output_grid = grid2 + grid2
    else:
        # --- Even height case ---
        # Calculate the midpoint row index
        midpoint = h2 // 2
        
        # Split grid2 into top and bottom halves
        top_half = grid2[:midpoint]
        bottom_half = grid2[midpoint:]

        # Construct the output grid by stacking halves in the required sequence:
        # Bottom, Top, Bottom, Top, Bottom
        output_grid = bottom_half + top_half + bottom_half + top_half + bottom_half

    # Return the constructed output grid
    return output_grid
```