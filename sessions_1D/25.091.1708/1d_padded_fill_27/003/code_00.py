"""
Fill the horizontal gap between pairs of identical colored pixels in each row.

Iterate through each row of the input grid. For each row, identify all non-white pixels. 
If exactly two non-white pixels are found in a row, and they both have the same color, 
then fill the segment of that row between these two pixels (inclusive) with their color. 
Otherwise, leave the row unchanged.
"""

import numpy as np

def find_non_white_pixels(row):
    """
    Finds the indices and colors of non-white (non-zero) pixels in a given row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        list: A list of dictionaries, where each dictionary contains the 
              'index' and 'color' of a non-white pixel. Returns an empty
              list if no non-white pixels are found.
    """
    non_white_pixels = []
    # Iterate through each pixel in the row along with its column index
    for col_idx, pixel_color in enumerate(row):
        # Check if the pixel color is not white (0)
        if pixel_color != 0: 
            non_white_pixels.append({'index': col_idx, 'color': pixel_color})
    return non_white_pixels

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Fills the horizontal segment between exactly two identical non-white pixels in each row.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_array to modify
    output_grid = np.copy(input_array)
    
    # Get the number of rows in the grid
    num_rows = input_array.shape[0]

    # Iterate through each row of the grid
    for r in range(num_rows):
        # Get the current row from the input array
        current_row = input_array[r, :]

        # Find all non-white pixels in the current row
        non_white_info = find_non_white_pixels(current_row)

        # Check if exactly two non-white pixels were found in this row
        if len(non_white_info) == 2:
            pixel1 = non_white_info[0]
            pixel2 = non_white_info[1]

            # Check if the two non-white pixels have the same color
            if pixel1['color'] == pixel2['color']:
                # Determine the color to fill with
                fill_color = pixel1['color']
                
                # Find the minimum and maximum column indices of the two pixels
                start_col = min(pixel1['index'], pixel2['index'])
                end_col = max(pixel1['index'], pixel2['index'])

                # Fill the segment in the output grid's corresponding row
                # The slice `start_col:end_col + 1` includes the end_col index
                output_grid[r, start_col : end_col + 1] = fill_color
        
        # If conditions (exactly 2 non-white pixels of the same color) are not met, 
        # the row in output_grid remains unchanged (as it started as a copy).

    # Convert the final NumPy array back to a list of lists before returning
    return output_grid.tolist()