import numpy as np
from typing import List, Union, TypeAlias

# Define type aliases for clarity
GridRow: TypeAlias = List[int]
ObjectBlock: TypeAlias = List[GridRow]
Unit: TypeAlias = Union[GridRow, ObjectBlock] # A Unit can be a single Separator Row or an Object Block

"""
Transforms the input grid based on its horizontal segments.

The transformation involves the following steps:
1.  **Parse the Grid:** Scan the input grid row by row from top to bottom. Identify distinct horizontal "units":
    *   A "Separator Row" unit is any single row consisting entirely of the background color (white, 0).
    *   An "Object Block" unit is a maximal contiguous sequence of one or more rows where none of the rows are Separator Rows.
    *   Record the sequence of these units in the order they appear.
2.  **Reverse Units Order:** Create a new sequence containing the identified units, but in reverse order compared to their original appearance in the grid.
3.  **Process Reversed Units:** Iterate through the units in the reversed sequence:
    *   If a unit is an Object Block: Reverse the order of the rows within that block (internal vertical flip).
    *   If a unit is a Separator Row: Leave it unchanged.
4.  **Reconstruct Grid:** Concatenate the processed units vertically in their current (reversed) order to form the final output grid. Ensure that Separator Rows remain single rows and Object Blocks contribute their (potentially internally-flipped) rows.
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
    Uses standard Python iteration to avoid potential NumPy boolean ambiguity errors.

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
            # Slicing a list of lists results in a list of lists
            object_block: ObjectBlock = grid[block_start_index:block_end_index] 
            units.append(object_block) # Appends a List[List[int]]
            # row_index is now correctly positioned at the start of the next unit 
            # (or at the end of the grid)

    return units

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by reversing the vertical order of distinct horizontal segments
    (object blocks and background separators), and also reversing the rows within each
    multi-row object block.
    """

    # 1. Identify all units (separator rows and object blocks) in order
    #    This version uses pure Python checks to potentially avoid NumPy errors.
    units: List[Unit] = identify_units(input_grid)

    # 2. Reverse the overall order of the identified units
    reversed_units = units[::-1] # Creates a reversed copy

    # 3. Process reversed units: Flip rows within object blocks
    # 4. Reconstruct the final grid
    output_grid: List[GridRow] = []
    for unit in reversed_units:
        # Determine if the unit is an ObjectBlock (List[List[int]]) or SeparatorRow (List[int]).
        # We rely on the structure returned by identify_units.
        # A simple check: if the unit is not empty and its first element is a list, it's a block.
        # This assumes valid ARC grids (no blocks like [[]] or empty units from identify_units).
        is_object_block = False
        if unit: # Check if unit is not empty
            # Check if the first element exists and is itself a list.
            # This correctly identifies List[List[int]] vs List[int].
            if isinstance(unit[0], list):
                is_object_block = True
                
        if is_object_block:
            # This unit is an object block (List[GridRow])
            object_block: ObjectBlock = unit 
            # Reverse the order of rows within this block
            flipped_block_rows = object_block[::-1]
            # Add the rows of the flipped block to the output grid
            output_grid.extend(flipped_block_rows)
        else:
            # This unit is a separator row (GridRow)
            # Includes the case where unit might be an empty list [] if identify_units produced it.
            separator_row: GridRow = unit 
            # Add the separator row directly to the output grid
            output_grid.append(separator_row)

    return output_grid