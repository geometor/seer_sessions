"""
The program splits the input grid into segments using solid rows of 6s as delimiters.
It extracts colored blocks (objects) that are not 7 (white) from each segment.
Then, it combines these extracted objects in reverse order of the segments in the original input.
The x,y positions within each object are preserved during recombination.
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
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array

    # 1. Split the grid into segments
    segments = split_grid(input_grid)

    # 2. Extract objects from each segment
    all_objects = []
    for segment in segments:
        all_objects.append(find_objects(segment))


    # 3. prepare output grid and Reverse the segment order to fill it up.
    output_grid = np.full((0, 0), 7)
    new_segments = []
    
    #reverse order the segment object list.
    for obj_list in reversed(all_objects):

        #build a segment grid for each reversed object
        max_x = 0
        max_y = 0
        for _, obj_pixels in obj_list:
            for x,y in obj_pixels:
                max_x = max(x, max_x)
                max_y = max(y, max_y)

        segment_grid = np.full((max_x + 1, max_y + 1), 7)
        for color, obj_pixels in obj_list:
            for x, y in obj_pixels:
                segment_grid[x,y] = color
        new_segments.append(segment_grid)


    #combine the segments in the reversed order.
    max_width = 0
    for segment in new_segments:
        max_width = max(max_width, segment.shape[1])
    
    output_list = []
    for segment in new_segments:
        pad_width = max_width - segment.shape[1]
        new_segment = np.pad(segment,
                             ((0,0), (0, pad_width)),
                             mode='constant',
                             constant_values=7)
        output_list.append(new_segment)

    output_grid = np.concatenate(output_list)
    
    return output_grid.tolist()