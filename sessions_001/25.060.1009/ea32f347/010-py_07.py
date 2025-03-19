"""
Transforms an input grid by changing the color of grey (5) pixels based on their arrangement into connected components, specifically vertical and horizontal segments. Grey pixels in a vertical segment are changed to blue (1).  Horizontal segments connected to the left of the vertical segment are changed to yellow (4), and those to the right are changed to red (2).
"""

import numpy as np

def get_connected_components(grid, color):
    """
    Finds connected components of a specific color in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(row, col, current_component):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_component.append((row, col))
        dfs(row + 1, col, current_component)
        dfs(row - 1, col, current_component)
        dfs(row, col + 1, current_component)
        dfs(row, col - 1, current_component)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_component = []
                dfs(row, col, current_component)
                components.append(current_component)
    return components

def classify_segments(component):
    """
    Classifies segments within a connected component as vertical or horizontal.
    """
    rows, cols = zip(*component)
    min_col, max_col = min(cols), max(cols)
    min_row, max_row = min(rows), max(rows)

    vertical_segment = []
    horizontal_segments = []
    
    is_vertical = (max_row - min_row +1 ) == len(component) and (max_col == min_col)

    if is_vertical:
      vertical_segment = component
    else:
      # extract vertical segment - look for the longest connected line in a
      # single column
      col_counts = {}
      for r,c in component:
        if c not in col_counts:
          col_counts[c] = []
        col_counts[c].append(r)
    
      longest_col = -1
      longest_col_len = -1

      for col, row_list in col_counts.items():
        row_list.sort()
        
        local_max_len = 0
        max_len = 0
        for i in range(len(row_list)):
          if i == 0:
            local_max_len = 1
          elif row_list[i] == row_list[i-1] + 1:
            local_max_len += 1
          else:
            local_max_len = 1
          max_len = max(max_len, local_max_len)

        if max_len > longest_col_len:
          longest_col_len = max_len
          longest_col = col
      
      # build vertical segment
      for r,c in component:
        if c == longest_col:
          vertical_segment.append( (r,c))
      vertical_segment.sort() # top to bottom

      # horizontal components are the other parts
      for r,c in component:
        if (r,c) not in vertical_segment:
          horizontal_segments.append( (r,c))

    return vertical_segment, horizontal_segments

def transform(input_grid):
    # Initialize output grid with the same values as the input grid
    output_grid = np.copy(input_grid)

    # Find connected components of grey pixels
    grey_components = get_connected_components(input_grid, 5)

    # Process each grey component
    for component in grey_components:
        # Classify segments
        vertical_segment, horizontal_segments = classify_segments(component)

        # Change color of vertical segment to blue
        for row, col in vertical_segment:
            output_grid[row, col] = 1

        # Change color of horizontal segments based on their position relative to the vertical segment
        for row, col in horizontal_segments:
          if len(vertical_segment) > 0:
            vertical_col = vertical_segment[0][1]  # Column of the vertical segment
            if col < vertical_col:
                output_grid[row, col] = 4  # Yellow for left segments
            elif col > vertical_col:
                output_grid[row, col] = 2  # Red for right segments

    return output_grid