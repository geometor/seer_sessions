```python
import math
import json

# helper functions
def find_first_non_zero_row(grid: list[list[int]]) -> int:
    """Finds the index of the first row containing any non-zero element."""
    for r_idx, row in enumerate(grid):
        if any(cell != 0 for cell in row):
            return r_idx
    return -1 # Indicate no non-zero row found, though problem constraints suggest one always exists

def extract_active_block(grid: list[list[int]], start_row_index: int) -> list[list[int]]:
    """Extracts rows from start_row_index to the end."""
    if start_row_index < 0 or start_row_index >= len(grid):
        return [] # Return empty list if index is invalid
    return grid[start_row_index:]

def reverse_rows(block: list[list[int]]) -> list[list[int]]:
    """Reverses the order of rows in a block."""
    return block[::-1]

"""
Identify the first row in the input grid containing a non-zero number. Extract all rows from this row to the end (the "active block"). Create the output grid by first appending the rows of the active block in reverse order, and then appending the rows of the active block in their original order.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying the active block (rows from the first non-zero row onwards),
    reversing it, and concatenating the reversed block with the original active block.
    """

    # 1. Find the index of the first row containing a non-zero number.
    first_non_zero_idx = find_first_non_zero_row(input_grid)

    # Handle edge case where grid might be all zeros (though unlikely based on examples)
    if first_non_zero_idx == -1:
        return [] # Or return input_grid, depending on desired behavior for all-zero input

    # 2. Extract the "active block" from the identified index to the end.
    active_block = extract_active_block(input_grid, first_non_zero_idx)

    # 3. Create a reversed version of the active block's rows.
    reversed_active_block = reverse_rows(active_block)

    # 4. Concatenate the reversed block and the original active block vertically.
    # The output grid is formed by placing the reversed block on top of the original block.
    output_grid = reversed_active_block + active_block

    # 5. Return the resulting grid.
    return output_grid

```