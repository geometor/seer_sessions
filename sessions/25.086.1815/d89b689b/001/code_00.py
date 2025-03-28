"""
Transforms an input grid based on the following rules:
1. Locates a 2x2 square of azure (8) pixels in the input grid. This square's top-left position determines the location of the output 2x2 square.
2. Identifies four 'source' pixels in the input grid, defined as any pixel that is not white (0) and not azure (8).
3. Determines the quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) of each source pixel within the input grid (assuming a 10x10 grid divided into 5x5 quadrants).
4. Creates an output grid of the same size as the input, initially filled with white (0).
5. Populates a 2x2 square in the output grid, starting at the location identified in step 1.
6. The color of the top-left cell of the output square is taken from the source pixel found in the input's Top-Left quadrant.
7. The color of the top-right cell of the output square is taken from the source pixel found in the input's Top-Right quadrant.
8. The color of the bottom-left cell of the output square is taken from the source pixel found in the input's Bottom-Left quadrant.
9. The color of the bottom-right cell of the output square is taken from the source pixel found in the input's Bottom-Right quadrant.
"""

import numpy as np

def _find_marker_top_left(grid):
    """Finds the top-left coordinate (row, col) of the 2x2 azure (8) marker."""
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            if (grid[r, c] == 8 and
                    grid[r + 1, c] == 8 and
                    grid[r, c + 1] == 8 and
                    grid[r + 1, c + 1] == 8):
                return r, c
    return None # Should not happen based on problem description

def _find_source_pixels(grid):
    """Finds all non-white (0) and non-azure (8) pixels."""
    source_pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0 and color != 8:
                source_pixels.append({'color': color, 'row': r, 'col': c})
    return source_pixels

def _get_quadrant(row, col, height, width):
    """Determines the quadrant for a given coordinate."""
    mid_row = height // 2
    mid_col = width // 2
    if row < mid_row and col < mid_col:
        return 'TL'
    elif row < mid_row and col >= mid_col:
        return 'TR'
    elif row >= mid_row and col < mid_col:
        return 'BL'
    else: # row >= mid_row and col >= mid_col
        return 'BR'

def transform(input_grid):
    """
    Applies the quadrant mapping transformation to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize output_grid with background color (white/0)
    output_array = np.zeros_like(input_array)

    # 1. Find the marker square's top-left position
    marker_pos = _find_marker_top_left(input_array)
    if marker_pos is None:
        # Handle error: Marker not found (though problem implies it always exists)
        print("Error: Azure marker not found.")
        return output_array.tolist() # Return empty grid
    target_row, target_col = marker_pos

    # 2. Identify the four source pixels
    source_pixels = _find_source_pixels(input_array)
    if len(source_pixels) != 4:
        # Handle error: Incorrect number of source pixels
        print(f"Error: Expected 4 source pixels, found {len(source_pixels)}.")
        return output_array.tolist()

    # 3. Determine the quadrant for each source pixel and store colors
    quadrant_colors = {}
    for pixel_info in source_pixels:
        quadrant = _get_quadrant(pixel_info['row'], pixel_info['col'], height, width)
        if quadrant in quadrant_colors:
             # Handle error: More than one source pixel in a quadrant
             print(f"Error: Multiple source pixels found in quadrant {quadrant}.")
             return output_array.tolist()
        quadrant_colors[quadrant] = pixel_info['color']

    # Check if all quadrants are represented
    if len(quadrant_colors) != 4:
        print(f"Error: Source pixels found in only {len(quadrant_colors)} quadrants.")
        return output_array.tolist()

    # 4. Populate the 2x2 output square based on quadrant mapping
    if 'TL' in quadrant_colors:
        output_array[target_row, target_col] = quadrant_colors['TL']
    if 'TR' in quadrant_colors:
        output_array[target_row, target_col + 1] = quadrant_colors['TR']
    if 'BL' in quadrant_colors:
        output_array[target_row + 1, target_col] = quadrant_colors['BL']
    if 'BR' in quadrant_colors:
        output_array[target_row + 1, target_col + 1] = quadrant_colors['BR']

    # Convert back to list of lists for the ARC standard format
    output_grid = output_array.tolist()

    return output_grid