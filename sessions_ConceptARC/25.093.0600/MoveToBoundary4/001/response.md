```python
import math
import copy

"""
For each row in the input grid independently:
1. Identify all contiguous horizontal blocks of the value 6.
2. Create a new output row initialized with the background value 0.
3. Place the identified blocks into the new output row, starting from the leftmost column (column 0).
4. Preserve the relative order of the blocks as they appeared in the input row.
5. Pack the blocks consecutively without any gaps between them in the output row.
6. The final output grid is composed of these newly generated rows.
"""

def find_blocks_in_row(row, target_value=6):
    """
    Identifies contiguous blocks of a target value in a row.

    Args:
        row (list): A list representing a row of the grid.
        target_value (int): The value to search for blocks of.

    Returns:
        list: A list containing the lengths of the identified contiguous blocks,
              in the order they appear from left to right.
    """
    blocks = []
    in_block = False
    block_start = -1
    for i, cell in enumerate(row):
        # Entering a block
        if cell == target_value and not in_block:
            in_block = True
            block_start = i
        # Exiting a block
        elif cell != target_value and in_block:
            in_block = False
            block_length = i - block_start
            blocks.append(block_length)
            block_start = -1 # Reset start index
    # Handle case where a block extends to the end of the row
    if in_block:
        block_length = len(row) - block_start
        blocks.append(block_length)
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by shifting all contiguous blocks of '6'
    in each row to the left, preserving their relative order and lengths.

    Args:
        input_grid (list of list of int): The input 2D grid.

    Returns:
        list of list of int: The transformed 2D grid.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid with background value (0)
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Process each row independently
    for r in range(height):
        input_row = input_grid[r]
        
        # Find all contiguous blocks of '6' in the current row
        block_lengths = find_blocks_in_row(input_row, target_value=6)

        # Place the blocks into the output row, shifted left
        current_output_col = 0
        for length in block_lengths:
            # Fill the block with '6's in the output row
            for c in range(length):
                # Check bounds just in case, though logic should prevent overflow
                if current_output_col + c < width: 
                    output_grid[r][current_output_col + c] = 6
            # Update the starting column for the next block
            current_output_col += length

    return output_grid
```