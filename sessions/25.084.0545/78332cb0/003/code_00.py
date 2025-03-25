"""
The input grid is divided into segments based on horizontal lines of '6's. If no divider lines are present, the entire grid is treated as one segment.
Within each segment, contiguous regions (objects) of colors other than 7 (white) are identified. The order of segments is reversed.
The output grid is constructed by stacking these segments vertically. Each object's position within a segment is preserved relative to the segment's origin.
The output grid's width is the maximum width of all input segments, and any empty spaces are filled with 7 (white).
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous blocks of the same color (excluding 7) in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 7:
                color = grid[row, col]
                obj = []
                dfs(row, col, color, obj)
                objects.append((color, obj))
    return objects

def split_grid(grid):
    """Splits the grid into segments based on rows of 6s."""
    segments = []
    start_row = 0
    for row in range(grid.shape[0]):
        if all(grid[row, :] == 6):
            if row > start_row:
                segments.append(grid[start_row:row, :])
            start_row = row + 1
    if start_row < grid.shape[0]:
        segments.append(grid[start_row:, :])
    return segments

def transform(input_grid):
    input_grid = np.array(input_grid)

    # 1. Split the grid into segments
    segments = split_grid(input_grid)

    # Handle the case where there are no divider lines
    if not segments:
        segments = [input_grid]

    # 2. Extract objects from each segment - Not strictly needed here but kept for consistency
    all_objects = []
    for segment in segments:
      all_objects.append(find_objects(segment))

    # 3. Reverse the segment order
    reversed_segments = segments[::-1]

    # 4. Determine output grid dimensions
    max_width = max(segment.shape[1] for segment in segments)
    total_height = sum(segment.shape[0] for segment in reversed_segments)
    output_grid = np.full((total_height, max_width), 7, dtype=int)  # Initialize with 7s

    # 5. Reconstruct the output grid
    current_height = 0
    for segment in reversed_segments:
        segment_height, segment_width = segment.shape
        #pad each segment.
        padded_segment = np.pad(segment,
                                ((0,0), (0, max_width-segment_width)),
                                mode='constant',
                                constant_values=7)
        output_grid[current_height:current_height + segment_height, 0:max_width] = padded_segment
        current_height += segment_height

    return output_grid.tolist()