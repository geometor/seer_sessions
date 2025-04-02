import numpy as np
from typing import List, Dict

"""
Make a copy of the input grid; this copy will become the output grid.
Go through each row of the input grid one by one.
For the current row:
  a. Find all the pixels that are not white (color 0). Keep track of which 
     column each non-white pixel is in and what its color is.
  b. Look at the non-white pixels found in this row, grouping them by their 
     color.
  c. For each color group, check if it contains exactly two pixels.
  d. If a color appears exactly twice (at columns col1 and col2):
      i.  Note the color (fill_color).
      ii. Find the smaller column index (left_col = min(col1, col2)).
      iii.Find the larger column index (right_col = max(col1, col2)).
      iv. In the output grid, change the color of all pixels in the current 
          row that are located *between* left_col and right_col (i.e., from 
          column left_col + 1 to right_col - 1) to fill_color.
After checking and potentially modifying all rows in this way, return the 
final output grid.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Identifies pairs of same-colored non-white pixels in each row and fills 
    the horizontal space between them with that color.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Iterate through each row
    for r in range(height):
        # Dictionary to store column indices for each non-white color found 
        # in the row Format: {color: [col1, col2, ...]}
        color_locations: Dict[int, List[int]] = {}

        # a. Find non-white pixels and their locations in the current row
        for c in range(width):
            pixel_color = input_array[r, c]
            if pixel_color != 0:  # non-white pixel
                # b. Group by color
                if pixel_color not in color_locations:
                    color_locations[pixel_color] = []
                color_locations[pixel_color].append(c)

        # Process each color found in the row
        for color, locations in color_locations.items():
            # c. Check if there is exactly one pair of this color in the row
            if len(locations) == 2:
                # d. If a pair exists:
                # i. Note the color (variable 'color' already holds this)
                # ii. Get the column indices of the pair
                col1, col2 = locations[0], locations[1]
                # iii. Determine the start (left) and end (right) columns for filling
                start_col = min(col1, col2)
                end_col = max(col1, col2)
                
                # iv. Fill the gap between the pair in the output grid
                # Iterate from the column after the first pixel up to (but not 
                # including) the second pixel
                for c_fill in range(start_col + 1, end_col):
                    output_array[r, c_fill] = color

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    return output_grid