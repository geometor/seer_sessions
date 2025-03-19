"""
1.  **Identify Gray Pixels:** Locate all pixels with the value 5 (gray) in the input grid.
2.  **Focus on Central Gray:** If more than one exists, determine the one is at the "center"
    in the following way: find the gray(5) in the input grid on the middle row
3.  **Horizontal Neighbors:** If horizontal neighbors of the 'center' are non-gray,
    and have the *same* value, extend those horizontally until you reach the edges of the grid or another color.
4. **Propagate Change:** Propagate this process to other object(5) on the center row.
5. **Diagonal:** From the *other* objects(5) on the original center row, if the diagonal neighbors have the same value, extend it until you reach the edges of the grid.
6.  **Replace:** Replace all the object(5) with 0.
7.  **Output:** Return the resulting modified grid.
"""

import numpy as np

def find_gray_pixels(grid):
    # find all gray pixels (value 5)
    return np.argwhere(grid == 5)

def get_center_gray_pixels(grid, gray_pixels):
     # find center gray on middle row

    mid_row = grid.shape[0] // 2
    center_gray_pixels = [p for p in gray_pixels if p[0] == mid_row ]
    return center_gray_pixels

def extend_horizontally(grid, start_row, start_col, color):
    """Extend the color horizontally from the start position."""

    rows, cols = grid.shape
    extended_pixels = []

    # Extend to the right
    for c in range(start_col, cols):
        if grid[start_row, c] == color:
            extended_pixels.append((start_row, c))
        else:
            break  # Stop when a different color is encountered

    # Extend to the left
    for c in range(start_col -1 , -1, -1):
      if grid[start_row,c] == color:
        extended_pixels.append((start_row,c))
      else:
        break

    return extended_pixels

def extend_diagonally(grid, start_row, start_col, color):
    """Extend a color diagonally, taking row and col of a gray(5)"""
    rows, cols = grid.shape
    extended_pixels = []

    # Extend diagonally up and right
    r, c = start_row - 1, start_col + 1
    while 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
        extended_pixels.append((r, c))
        r -= 1
        c += 1
        
    # Extend diagonally down and right
    r, c = start_row + 1, start_col + 1
    while 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
        extended_pixels.append((r, c))
        r += 1
        c += 1

    # Extend diagonally up and left
    r, c = start_row - 1, start_col - 1
    while 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
        extended_pixels.append((r, c))
        r -= 1
        c -= 1

    # Extend diagonally down and left
    r, c = start_row + 1, start_col - 1
    while 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
        extended_pixels.append((r, c))
        r += 1
        c -= 1

    return extended_pixels
    

def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # find all gray pixels (5)
    gray_pixels = find_gray_pixels(grid)
    if len(gray_pixels) == 0:
        return output_grid.tolist()
    
    # find center gray on middle row
    center_gray_pixels = get_center_gray_pixels(grid, gray_pixels)

    # create a list to iterate all the gray pixels
    all_gray_to_process = []
    for gray_pixel in center_gray_pixels:
        all_gray_to_process.append(gray_pixel)
        
    # check horizontal neighbors
    for gray_pixel in center_gray_pixels:
        row, col = gray_pixel
        #print(f"gray: {gray_pixel}")

        # Check right neighbor
        if col + 1 < cols:
          right_neighbor_color = grid[row,col+1]
          if right_neighbor_color != 5:
              #print(f"  right color: {right_neighbor_color}")

              # check left neighbor
              if col - 1 >= 0:
                left_neighbor_color = grid[row,col-1]
                #print(f"  left color: {left_neighbor_color}")
                if left_neighbor_color == right_neighbor_color:

                  # extend the color horizontally
                  extended = extend_horizontally(grid,row,col-1,left_neighbor_color)
                  #print(f"extended: {extended}")
                  for r,c in extended:
                    output_grid[r,c] = left_neighbor_color

                  # now find other objects(5) on that horizontal line
                  for c in range(cols):
                    if grid[row,c] == 5 and c != col:
                      all_gray_to_process.append([row,c])

    # process diagonal neighbors
    for gray_pixel in all_gray_to_process:
        row, col = gray_pixel
        
        # Check top-right neighbor
        if row - 1 >= 0 and col + 1 < cols:
            top_right_color = grid[row - 1, col + 1]
            if top_right_color != 5:
              # Check bottom-left neighbor
              if row + 1 < rows and col -1 >= 0:
                bottom_left_color = grid[row+1,col-1]
                if top_right_color == bottom_left_color:
                  extended = extend_diagonally(grid,row,col,top_right_color)
                  for r,c in extended:
                    output_grid[r,c] = top_right_color

        # Check top-left neighbor
        if row - 1 >= 0 and col - 1 >= 0:
          top_left_color = grid[row - 1, col-1]
          if top_left_color != 5:
            if row + 1 < rows and col + 1 < cols:
              bottom_right_color = grid[row+1,col+1]
              if top_left_color == bottom_right_color:
                extended = extend_diagonally(grid,row,col,top_left_color)
                for r,c in extended:
                  output_grid[r,c] = top_left_color
    
    # Replace gray(5) with white(0)
    for r, c in gray_pixels:
      output_grid[r,c] = 0

    return output_grid.tolist()