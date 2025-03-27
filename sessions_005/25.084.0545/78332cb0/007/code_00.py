"""
1.  **Identify Divider Columns:** Examine the input grid to locate columns that *would be* entirely color '6' (magenta) *if* filled. This implicitly divides the grid, both vertically and horizontally, into segments. The locations of these divider *columns* determines the segment boundaries, even if the columns aren't explicitly filled with '6'.
2.  **Horizontal Segmentation:** Within each vertically-divided section, locate horizontal rows consisting entirely of color '6' (magenta). These rows further subdivide the grid into smaller segments.
3.  **Reverse Segment Order:** Reverse the order of the major segments defined by the *implicit* vertical '6' columns.
4.  **Stack Segments:**  Within each major segment, stack the sub-segments (created by horizontal '6' rows) vertically.
5. **Implicit Padding** Empty columns between objects are considered implicit '6' dividers.
6.  **Output Construction:** Construct the output grid by stacking the segments according to the reversed order from step 3 and the vertical stacking from step 4. Maintain the relative positions of objects within each segment during the re-arrangement, but transpose the entire result.
"""

import numpy as np

def find_divider_columns(grid):
    """Finds columns that are or could be dividers (all 6s)."""
    divider_cols = []
    for col in range(grid.shape[1]):
        if all(grid[:, col] == 6) or all(grid[:,col] == 7): #all magenta or could be
             divider_cols.append(col)

    return divider_cols

def split_grid_horizontal(grid):
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
    
    # 1. Identify Divider Columns
    divider_cols = find_divider_columns(input_grid)

    # If no explicit divider columns, treat the entire grid as one segment
    if not divider_cols:
        segments = {0: [input_grid]}  # Wrap in a list for consistency
        major_segment_widths = [input_grid.shape[1]]
    else:
        segments = {}
        major_segment_widths = []
        start_col = 0

        for i, col in enumerate(divider_cols):
          
            segment = input_grid[:, start_col:col]
            major_segment_widths.append(col - start_col)

            # 2. Horizontal Segmentation
            horizontal_segments = split_grid_horizontal(segment)
            segments[i] = horizontal_segments
            start_col = col + 1  # Move past the divider column

        #add last segment
        segment = input_grid[:, start_col:]
        major_segment_widths.append(input_grid.shape[1] - start_col)
        horizontal_segments = split_grid_horizontal(segment)
        segments[len(divider_cols)] = horizontal_segments


    # 3. Reverse Segment Order (of major segments)
    reversed_segment_keys = sorted(segments.keys(), reverse=True)

    # 4. & 5. Stack and Pad Segments + 6. Output
    # Calculate output dimensions based on reversed segments

    max_segment_height = 0
    for key in reversed_segment_keys:
       for sub_segment in segments[key]:
           max_segment_height = max(max_segment_height, sub_segment.shape[0])


    total_width = sum(major_segment_widths)

    output_grid = np.full((max_segment_height * len(segments), input_grid.shape[1]), 7, dtype=int) # Pad with 7s

    current_x = 0

    for key in reversed_segment_keys:
      current_y = 0
      for h_seg in segments[key]:
            h, w = h_seg.shape
            output_grid[current_y:current_y + h, current_x:current_x+w] = h_seg
            current_y += max_segment_height

      current_x += major_segment_widths[key] # use width of this segment



    return output_grid.tolist()