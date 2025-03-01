"""
1.  **Iterate Rows:** Process each row of the input grid independently.
2.  **Identify Azure Pixels:** Within each row, locate all pixels colored azure (value 8).
3.  **Identify White Pixels:** Within each row, locate all pixels colored white (value 0).
4. **Shift Azure:**
      * If any white is left of any azure, move all azure pixels to the leftmost white pixel location within the row. All azure pixels in the row are combined.
      * If there are no white pixels in the row, and if there are any non-white, non-azure to the left of the first azure, then combine all azure pixels in the row and place to the right of the rightmost non-white, non-azure pixel
      *If there are no white pixels in the row, and no non-white, non-azure to the left, then move all azure pixels to the leftmost cell.
5.  **Preserve Other Colors:** Pixels that are neither azure nor white remain in their original positions.
"""

import numpy as np

def get_object_locations(grid, color):
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for row in range(rows):
        # find all white pixels
        row_white_pixels = np.where(input_grid[row] == 0)[0]

        # find all azure pixels
        row_azure_pixels = get_object_locations(input_grid, 8)
        row_azure_pixels = row_azure_pixels[row_azure_pixels[:, 0] == row]

        # combine and shift
        if len(row_azure_pixels) > 0:  # only process if azure exists
             #find leftmost white
            if len(row_white_pixels) > 0:
              first_azure = np.min(row_azure_pixels[:,1])
              white_left_of_azure = row_white_pixels[row_white_pixels < first_azure]
              if len(white_left_of_azure) > 0:
                leftmost_white = np.min(white_left_of_azure)
                # clear current azure
                for pixel in row_azure_pixels:
                  output_grid[row, pixel[1]] = 0

                # fill the leftmost
                output_grid[row, leftmost_white] = 8
              else:
                #check for non white pixels to the left of first azure
                first_azure = np.min(row_azure_pixels[:,1])
                non_white_left = np.where(input_grid[row, :first_azure] != 0)[0]
                if(len(non_white_left) > 0):
                    #check if any are azure
                    non_white_left_non_azure = non_white_left[np.where(input_grid[row,non_white_left] != 8)[0]]
                    if len(non_white_left_non_azure) > 0:
                        leftmost_non_white = np.max(non_white_left_non_azure)
                        # clear current azure
                        for pixel in row_azure_pixels:
                          output_grid[row, pixel[1]] = 0
                        output_grid[row, leftmost_non_white+1] = 8
                    else:
                        # clear current azure
                        for pixel in row_azure_pixels:
                          output_grid[row, pixel[1]] = 0

                        # fill the leftmost
                        output_grid[row, 0] = 8
                else:
                  # clear current azure
                  for pixel in row_azure_pixels:
                    output_grid[row, pixel[1]] = 0

                  # fill the leftmost
                  output_grid[row, 0] = 8

            else:
                #check for non white pixels to the left of first azure
                first_azure = np.min(row_azure_pixels[:,1])
                non_white_left = np.where(input_grid[row, :first_azure] != 0)[0]
                if(len(non_white_left) > 0):
                  #check if any are azure
                    non_white_left_non_azure = non_white_left[np.where(input_grid[row,non_white_left] != 8)[0]]
                    if len(non_white_left_non_azure) > 0:

                        leftmost_non_white = np.max(non_white_left_non_azure)
                        # clear current azure
                        for pixel in row_azure_pixels:
                          output_grid[row, pixel[1]] = 0
                        output_grid[row, leftmost_non_white+1] = 8
                    else:
                        # clear current azure
                        for pixel in row_azure_pixels:
                            output_grid[row, pixel[1]] = 0

                        # fill the leftmost
                        output_grid[row, 0] = 8
                else:
                  # clear current azure
                    for pixel in row_azure_pixels:
                      output_grid[row, pixel[1]] = 0

                    # fill the leftmost
                    output_grid[row, 0] = 8


    return output_grid