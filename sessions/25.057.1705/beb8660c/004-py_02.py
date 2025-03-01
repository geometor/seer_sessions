"""
Transforms the input grid by identifying horizontal segments of non-white pixels in each row, consolidating segments of the same color within a row, and right-aligning the resulting segments in the output grid, maintaining the original row order.
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

def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros_like(input_grid)
    grid_height, grid_width = input_grid.shape

    # Find all horizontal segments
    segments = find_segments(input_grid)

    # Consolidate segments by row and color
    consolidated_segments = consolidate_segments(segments)

    # Place consolidated segments in the output grid
    for (row, color), length in consolidated_segments.items():
        start_col = grid_width - length
        output_grid[row, start_col:start_col + length] = color

    return output_grid