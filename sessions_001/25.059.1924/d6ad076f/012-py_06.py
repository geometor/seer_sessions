"""
Identifies distinct colored rectangles in the input grid and creates a new azure (color 8) row connecting the existing rectangles.
"""

import numpy as np

def find_rectangles(grid):
    # Find distinct colored rectangles in the grid
    rectangles = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                color = grid[r, c]
                start_row, start_col = r, c
                end_row, end_col = r, c

                # Expand rectangle horizontally
                while end_col + 1 < cols and grid[r, end_col + 1] == color and not visited[r, end_col+1]:
                    end_col += 1

                # Expand rectangle vertically
                while end_row + 1 < rows and all(grid[end_row + 1, start_col:end_col + 1] == color) and not all(visited[end_row+1, start_col:end_col+1]):
                    end_row += 1

                #mark visisted
                for i in range(start_row, end_row + 1):
                  for j in range(start_col, end_col + 1):
                    visited[i,j] = True

                rectangles.append({
                    'color': color,
                    'start_row': start_row,
                    'start_col': start_col,
                    'end_row': end_row,
                    'end_col': end_col
                })
    return rectangles

def check_existing_bridge(grid, rect1, rect2):
    # Check if an azure bridge already exists between two rectangles.
    min_col = rect1['end_col'] + 1
    max_col = rect2['start_col'] -1
    
    # Check for a single row
    for row in range(grid.shape[0]):
      for col in range(min_col, max_col+1):
          if grid[row,col] == 8:
            return True
    return False
  
def get_bridge_position(rect1, rect2, grid):
  #try direct middle connection
  row_mid = (rect1['end_row'] + rect2['start_row']) //2

  #determine width and height

  height = 1 #fixed based on provided cases, must be a single row
  width = rect2['start_col'] - rect1['end_col'] -1

  start_row = row_mid
  start_col = rect1['end_col'] + 1


  return start_row, start_col, height, width

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find distinct colored rectangles in the input grid
    rectangles = find_rectangles(input_grid)

    # Create a new azure rectangle connecting the existing rectangles, if more than one found.
    if len(rectangles) >= 2:

      #sort by col to create consistent bridge
      rectangles.sort(key=lambda x: x['start_col'])

      #iterate all rectangle pairs
      for i in range(len(rectangles) - 1):
        #check existing bridge
        if not check_existing_bridge(input_grid, rectangles[i], rectangles[i+1]):

          #find bridging location
          bridge_start_row, bridge_start_col, height, width = get_bridge_position(rectangles[i], rectangles[i+1], input_grid)

          #draw onto output
          for r in range(bridge_start_row, bridge_start_row + height):
            for c in range(bridge_start_col, bridge_start_col + width):
              if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]: #check bounds
                if output_grid[r,c] == 0: #only overwrite 0's
                  output_grid[r, c] = 8

    return output_grid