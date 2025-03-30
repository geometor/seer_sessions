import numpy as np

"""
Identify all unique pixels in the input grid whose colors are not white (0), red (2), or yellow (4). Record these colors in a list ('fill_colors') in the order they are first encountered when scanning the grid top-to-bottom, left-to-right.
Identify all distinct, contiguous, vertical segments composed only of red (2) pixels. Store each segment's column index, start row, and end row.
Sort these red line segments first by their start row index (ascending) and then by their column index (ascending).
Iterate through the sorted red line segments and the 'fill_colors' list simultaneously. For the i-th segment, use the i-th fill color.
For each red segment, change the color of the pixels immediately to its right (in the column col+1) for all rows spanned by the segment, using the corresponding fill color. All other pixels remain unchanged.
"""

def find_fill_colors(grid):
    """
    Finds unique fill colors (not 0, 2, or 4) in scan order.
    """
    fill_colors = []
    seen_colors = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color not in {0, 2, 4} and color not in seen_colors:
                fill_colors.append(color)
                seen_colors.add(color)
    return fill_colors

def find_red_segments(grid):
    """
    Finds all vertical red (2) segments and returns them as a list of tuples:
    (column, start_row, end_row).
    """
    rows, cols = grid.shape
    segments = []
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is red and not yet part of a found segment
            if grid[r, c] == 2 and not visited[r, c]:
                # Found the potential start of a vertical segment
                start_row = r
                end_row = r
                # Explore downwards to find the end of the segment
                while end_row + 1 < rows and grid[end_row + 1, c] == 2:
                    end_row += 1
                
                # Mark the cells of this segment as visited
                for row_idx in range(start_row, end_row + 1):
                    visited[row_idx, c] = True
                
                # Store the segment information
                segments.append({'col': c, 'start_row': start_row, 'end_row': end_row})
                
    # Sort segments primarily by start_row, secondarily by col
    segments.sort(key=lambda s: (s['start_row'], s['col']))
    return segments


def transform(input_grid):
    """
    Applies the transformation rule based on red lines and fill colors.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find fill colors in scan order
    fill_colors = find_fill_colors(input_grid)

    # 2. Find vertical red segments
    red_segments = find_red_segments(input_grid)

    # 3. Associate segments with fill colors and modify the output grid
    num_segments = len(red_segments)
    num_colors = len(fill_colors)

    for i in range(min(num_segments, num_colors)): # Process only pairs we have colors for
        segment = red_segments[i]
        fill_color = fill_colors[i]

        col = segment['col']
        start_row = segment['start_row']
        end_row = segment['end_row']

        # Check if the column to the right is within grid bounds
        target_col = col + 1
        if target_col < cols:
            # Modify the pixels to the right of the segment
            for r in range(start_row, end_row + 1):
                 # Only modify if the target cell exists (redundant check with target_col < cols but safe)
                 if r < rows:
                    # Apply the fill color to the pixel immediately right of the red segment
                    output_grid[r, target_col] = fill_color

    return output_grid