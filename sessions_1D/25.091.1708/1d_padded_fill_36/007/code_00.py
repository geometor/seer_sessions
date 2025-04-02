"""
Transforms an input grid by filling horizontal segments between specific pairs of identical non-white pixels within each row.

1. Create a copy of the input grid to serve as the output grid.
2. Iterate through each row of the input grid using its row index.
3. For the current row:
    a. Find all non-white pixels (color > 0) and record their color and column index.
    b. Check Condition 1: Proceed only if exactly two non-white pixels are found.
    c. Check Condition 2: Proceed only if the colors of these two pixels are identical.
    d. Execute Fill: If both conditions are met:
        i. Get the fill_color (the color of the pair).
        ii. Get the start_col (minimum column index) and end_col (maximum column index).
        iii. In the output grid, modify the current row by setting all pixels from start_col to end_col (inclusive) to fill_color.
4. After iterating through all rows, return the modified output grid as a list of lists.
"""

import numpy as np

def find_non_white_pixels_in_row(row):
    """
    Identifies non-white pixels (value != 0) and their column indices in a row.

    Args:
        row (np.array): A 1D numpy array representing a single row of the grid.

    Returns:
        list: A list of tuples, where each tuple is (color, column_index).
              Returns an empty list if no non-white pixels are found.
    """
    non_white_pixels = []
    # Iterate through each pixel in the row with its index
    for col_index, pixel_color in enumerate(row):
        # Check if the pixel color is not white (0)
        if pixel_color != 0:
            non_white_pixels.append((pixel_color, col_index))
    return non_white_pixels

def transform(input_grid):
    """
    Transforms the input grid by filling horizontal segments between pairs of 
    same-colored markers in each row. Assumes input_grid is a 2D list of lists.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Step 1: Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_np)
    
    # Get the number of rows in the grid
    num_rows = input_np.shape[0]

    # Step 2: Iterate through each row of the grid using its index
    for r_idx in range(num_rows):
        # Get the current row from the input grid (can use output_grid as well initially)
        current_row = input_np[r_idx, :] 
        
        # Step 3a: Find all non-white pixels in the current row
        non_white_pixels = find_non_white_pixels_in_row(current_row)
        
        # Step 3b: Check Condition 1 - exactly two non-white pixels
        if len(non_white_pixels) == 2:
            # Extract color and column index for both pixels
            pixel1_color, pixel1_col = non_white_pixels[0]
            pixel2_color, pixel2_col = non_white_pixels[1]
            
            # Step 3c: Check Condition 2 - the two pixels have the same color
            if pixel1_color == pixel2_color:
                
                # Step 3d: Execute Fill - conditions met
                
                # Step 3d.i: Determine the fill color
                fill_color = pixel1_color
                
                # Step 3d.ii: Determine the start column (leftmost) and end column (rightmost)
                start_col = min(pixel1_col, pixel2_col)
                end_col = max(pixel1_col, pixel2_col)
                
                # Step 3d.iii: Fill the segment in the output grid for the current row.
                # Use slicing: [start:end+1] includes the end column index.
                output_grid[r_idx, start_col : end_col + 1] = fill_color
                
    # Step 4: Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()