"""
Transforms the input grid by identifying horizontal segments of non-white pixels in each row, consolidating segments of the same color within a row (conditionally), and shifting the segments by a fixed amount, potentially determined by their initial position.
"""

import numpy as np

def find_segments(grid):
    """Finds all horizontal segments of non-white pixels in the grid."""
    segments = []
    for row_index, row in enumerate(grid):
        col_index = 0
        while col_index < len(row):
            if row[col_index] != 0:
                color = row[col_index]
                start_col = col_index
                length = 0
                while col_index < len(row) and row[col_index] == color:
                    length += 1
                    col_index += 1
                segments.append({'color': color, 'length': length, 'row': row_index, 'start_col': start_col})
            else:
                col_index += 1
    return segments

def consolidate_segments(segments):
    """Consolidates segments of the same color within each row."""
    consolidated = {}
    for segment in segments:
        row = segment['row']
        color = segment['color']
        if (row, color) not in consolidated:
            consolidated[(row, color)] = 0
        consolidated[(row, color)] += segment['length']
    return consolidated

def calculate_shift(segment, grid_width):
    """Calculates the shift amount for a segment."""
    # This is a placeholder.  The actual shift calculation may need to be more complex
    # and could depend on more than just the start_col. It might need task-specific logic.
    # For now, we are trying right-alignment (example 1) and +2 shift (examples 2 & 3)

    # Trying a +2 shift.
    return 2
    #return grid_width - (segment['start_col'] + segment['length']) # Right align


def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros_like(input_grid)
    grid_height, grid_width = input_grid.shape

    # Find all horizontal segments
    segments = find_segments(input_grid)

    # Consolidate segments by row and color
    #consolidated_segments = consolidate_segments(segments) # Used for right-align (example 1)
    consolidated_segments = {} # Try without consolidating
    for segment in segments:
        consolidated_segments[(segment['row'], segment['color'], segment['start_col'])] = segment['length']


    # Place consolidated segments in the output grid
    for (row, color, start_col), length in consolidated_segments.items():
        # Calculate the shift
        #shift = calculate_shift({'start_col': start_col, 'length': length}, grid_width) # Pass segment info
        shift = 2 # Hardcode shift for now
        new_start_col = min(grid_width - length, max(0, start_col + shift)) # Apply and constrain shift

        output_grid[row, new_start_col:new_start_col + length] = color

    return output_grid