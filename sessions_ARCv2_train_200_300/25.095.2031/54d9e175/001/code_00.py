import math
import json

# Helper function import (simulated)
# Assume functions like find_objects, get_color, etc. are available if needed.
# For this task, direct list manipulation seems sufficient.

def parse_grid_string(grid_string: str) -> list[list[int]]:
    """Parses a string representation of the grid into a list of lists of integers."""
    lines = grid_string.strip().split('\n')
    grid = [[int(x) for x in line.split()] for line in lines]
    return grid

def grid_to_string(grid: list[list[int]]) -> str:
    """Converts a list of lists of integers back to the string representation."""
    return '\n'.join(' '.join(map(str, row)) for row in grid)

"""
Transforms the input grid based on identified sections and key rows.

1. Identifies separator rows composed entirely of the digit 5.
2. Divides the grid into sections based on these separator rows (or grid boundaries).
3. For each non-separator section:
    a. Locates a 'key row' (assumed to be the second row of the section based on examples) 
       which contains signal digits in columns 1, 5, and 9.
    b. Extracts these signal digits (d1, d5, d9).
    c. Calculates target output values by adding 5 to each signal digit (o1=d1+5, o5=d5+5, o9=d9+5).
    d. Fills all rows within that section in the output grid according to a pattern:
       - Columns 0-2 get value o1.
       - Column 3 gets value 5.
       - Columns 4-6 get value o5.
       - Column 7 gets value 5.
       - Columns 8-10 get value o9.
4. Separator rows from the input are copied directly to the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    num_rows = len(input_grid)
    if num_rows == 0:
        return []
    
    # Assume consistent number of columns based on examples (11)
    num_cols = len(input_grid[0]) 
    if num_cols != 11:
        # Handle unexpected column count if necessary, for now assume 11
        print(f"Warning: Expected 11 columns, found {num_cols}")
        # Or raise an error: raise ValueError("Input grid must have 11 columns")

    # Initialize output grid - creating a new one to fill
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # 1. Identify separator rows (all 5s)
    separator_indices = {r for r, row in enumerate(input_grid) if all(cell == 5 for cell in row)}

    # 2. Define sections based on separators
    section_starts = [0] + [i + 1 for i in sorted(list(separator_indices))]
    section_ends = [i for i in sorted(list(separator_indices))] + [num_rows]
    sections = list(zip(section_starts, section_ends))

    # 3. Process each section
    for start_row, end_row in sections:
        # Skip empty sections or sections that would only contain the separator itself
        if start_row >= end_row: 
            continue
            
        # Check if this 'section' is just a separator row that wasn't captured because it's at the start/end
        is_only_separator = True
        for r in range(start_row, end_row):
             if r not in separator_indices:
                 is_only_separator = False
                 break
        if is_only_separator:
            # This block only contains separator rows, handle them later
            continue

        # Find the 'key row' - assume it's the second row in the section (index start_row + 1)
        # Check if the section is large enough to contain a potential key row (at least 2 rows)
        if end_row > start_row + 1:
            key_row_index = start_row + 1
            
            # Sanity check: Make sure the assumed key row is not a separator row
            if key_row_index in separator_indices:
                 # This case shouldn't happen based on examples, but good to consider.
                 # Maybe search for the first non-zero, non-separator row?
                 # For now, stick to the observed pattern.
                 print(f"Warning: Assumed key row {key_row_index} is a separator row. Skipping section {start_row}-{end_row}.")
                 # Need to decide how to handle this - copy input? Raise error?
                 # Let's copy input for this section rows as a fallback
                 for r in range(start_row, end_row):
                     if r not in separator_indices: # Avoid overwriting separators that might be handled later
                        output_grid[r] = input_grid[r][:]
                 continue # Move to next section


            key_row = input_grid[key_row_index]

            # Extract signal digits from columns 1, 5, 9
            d1 = key_row[1]
            d5 = key_row[5]
            d9 = key_row[9]

            # Calculate output values by adding 5
            o1 = d1 + 5
            o5 = d5 + 5
            o9 = d9 + 5

            # Fill the output rows for this section (excluding separator rows)
            for r in range(start_row, end_row):
                if r in separator_indices:
                    # Skip separator rows within the section definition (should be handled later)
                    continue 
                
                output_grid[r][0:3] = [o1] * 3
                output_grid[r][3] = 5
                output_grid[r][4:7] = [o5] * 3
                output_grid[r][7] = 5
                output_grid[r][8:11] = [o9] * 3
        
        # Handle sections too small to have the assumed key row structure (e.g., only 1 row)
        elif end_row == start_row + 1:
             # If a section has only one row, and it's not a separator row
             # The examples don't cover this. What should happen?
             # Let's assume for now such sections maintain their input values if they aren't separators.
             if start_row not in separator_indices:
                 output_grid[start_row] = input_grid[start_row][:]
             # Separator rows will be handled in the next step anyway

    # 4. Copy separator rows directly from input to output
    for r in separator_indices:
        if r < num_rows: # Ensure index is valid
             output_grid[r] = input_grid[r][:]

    return output_grid
