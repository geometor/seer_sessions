"""
Change to green all white pixels in a region formed by the left, the top, and a line that would connect the azure pixels.
"""

import numpy as np

def find_red_rectangle(grid):
    # Find the coordinates of the red (2) rectangle.
    rows, cols = np.where(grid == 2)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def find_azure_pixels(grid):
    # Find the coordinates of the azure (8) pixels.
    rows, cols = np.where(grid == 8)
    return list(zip(rows, cols))

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find azure pixels.
    azure_pixels = find_azure_pixels(input_grid)
    if not azure_pixels:
        return output_grid # Return original if no azure pixels
        
    # Find top right coordinate
    height, width = input_grid.shape
    top_right = (0, width-1)

    # Determine bounding line parameters
    if len(azure_pixels) >= 2:
      azure_pixels.sort()
      top_azure = azure_pixels[0]
      bottom_azure = azure_pixels[-1]

    else:
        top_azure = azure_pixels[0]
        bottom_azure = azure_pixels[0]

    
    # define filling function
    def fill_region(grid, start_row, start_col):
        # start filling from top right using flood fill approach
        rows, cols = grid.shape
        visited = np.zeros_like(grid, dtype=bool)
        stack = [(start_row, start_col)]

        while stack:
            row, col = stack.pop()

            if row < 0 or row >= rows or col < 0 or col >= cols or visited[row, col] or grid[row,col] != 0:
                continue

            visited[row, col] = True
            grid[row,col] = 3


            # Calculate the normalized position relative to the line between the azure pixels

            if bottom_azure[0] - top_azure[0] == 0:
              # Handle cases where there is no row change between azures, preventing zero division
              if col > bottom_azure[1]:
                stack.append((row, col -1))

              stack.append((row - 1, col)) #up
              stack.append((row , col+1)) #right


            else:
                line_parameter = (col - top_azure[1]) / (bottom_azure[1] - top_azure[1])  if bottom_azure[1] != top_azure[1] else 0
                if (row - top_azure[0])/(bottom_azure[0] - top_azure[0]) > line_parameter:
                #stop when below the diagonal line defined by the azure pixels
                    stack.append((row + 1, col))  # Down
                if  (row - top_azure[0])/(bottom_azure[0] - top_azure[0]) >= line_parameter:
                    stack.append((row, col - 1))  # Left

            stack.append((row - 1, col)) #up
            stack.append((row , col+1)) #right
                
    
    # fill
    fill_region(output_grid, 0, width -1)

    return output_grid