```python
import numpy as np
from typing import List, Union, TypeAlias

# Define type aliases for clarity
GridRow: TypeAlias = List[int]
ObjectBlock: TypeAlias = List[GridRow]
Unit: TypeAlias = Union[GridRow, ObjectBlock] # A Unit can be a single Separator Row or an Object Block

"""
Transforms the input grid based on its horizontal segments.

The transformation involves the following steps:
1.  **Segment the Grid**: Examine the input grid row by row from top to bottom. Identify distinct horizontal "units". A unit is either:
    *   A **Separator Row**: A single row consisting entirely of the background color (white, 0).
    *   An **Object Block**: A maximal contiguous group of one or more rows where none of the rows are Separator Rows.
    Record the sequence of these units as they appear vertically in the grid.
2.  **Reverse Unit Order**: Create a new sequence containing the identified units, but arrange them in the reverse order of their appearance in the original grid.
3.  **Process Reversed Units**: Iterate through the units in the reversed sequence:
    *   If the unit is an **Object Block** (i.e., it contains one or more rows, none of which are all white), reverse the top-to-bottom order of the rows *within* that block (perform an internal vertical flip).
    *   If the unit is a **Separator Row**, leave it unchanged.
4.  **Reconstruct Output Grid**: Combine the processed units vertically, in their current (reversed) sequence order, to form the final output grid. Separator Rows remain single rows, and Object Blocks contribute their (potentially internally flipped) rows.
"""

def is_separator_row(row: GridRow) -> bool:
    """Checks if a row consists entirely of the background color 0."""
    # Handle empty rows safely - consider them separators.
    if not row:
        return True
    return all(pixel == 0 for pixel in row)

def identify_units(grid: List[GridRow]) -> List[Unit]:
    """
    Identifies separator rows (all background color 0) and object blocks
    (contiguous sequences of non-separator rows) in the input grid.

    Args:
        grid: The input grid as a list of lists of integers.

    Returns:
        A list of units, where each unit is either a single separator row (GridRow)
        or a list of rows representing an object block (ObjectBlock).
    """
    units: List[Unit] = []
    if not grid: # Handle empty input grid
        return units

    num_rows = len(grid)
    row_index = 0
    while row_index < num_rows:
        current_row = grid[row_index]

        # Check if the current row is a separator
        if is_separator_row(current_row):
            # If it's a separator, add the single row as a unit
            units.append(current_row) # Appends a List[int]
            row_index += 1
        else:
            # If it's not a separator, it's the start of an object block
            block_start_index = row_index

            # Find the end of this contiguous block of non-separator rows
            while row_index < num_rows and not is_separator_row(grid[row_index]):
                row_index += 1
            block_end_index = row_index # The end index is exclusive

            # Extract the rows belonging to this object block
            object_block: ObjectBlock = grid[block_start_index:block_end_index]
            units.append(object_block) # Appends a List[List[int]]
            # row_index is now correctly positioned at the start of the next unit

    return units

def transform(input_grid_np: np.ndarray) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid_np: A numpy ndarray representing the input grid.

    Returns:
        A list of lists of integers representing the transformed output grid.
    """
    # Convert input numpy array to list of lists to work with helper functions
    input_grid: List[List[int]] = input_grid_np.tolist()

    # 1. Segment the Grid: Identify units (separator rows and object blocks)
    units: List[Unit] = identify_units(input_grid)

    # 2. Reverse Unit Order: Reverse the overall order of the identified units
    reversed_units = units[::-1] # Creates a reversed copy

    # 3. Process Reversed Units and 4. Reconstruct Output Grid
    output_grid: List[GridRow] = []
    for unit in reversed_units:
        # Determine if the unit is an ObjectBlock (List[List[int]]) or SeparatorRow (List[int])
        # Check: if the unit is not empty and its first element is a list, it's a block.
        is_object_block = False
        if unit: # Check if unit is not empty
            # This check correctly distinguishes List[List[int]] from List[int].
            if isinstance(unit[0], list):
                is_object_block = True

        if is_object_block:
            # Process Object Block: Reverse the order of rows within this block
            object_block: ObjectBlock = unit
            flipped_block_rows = object_block[::-1] # Internal vertical flip
            # Add the rows of the flipped block to the output grid
            output_grid.extend(flipped_block_rows)
        else:
            # Process Separator Row: Add the separator row directly (unchanged)
            separator_row: GridRow = unit
            output_grid.append(separator_row)

    # Return the reconstructed grid as a list of lists
    # If the environment requires a NumPy array, convert here:
    # return np.array(output_grid, dtype=int)
    return output_grid

```