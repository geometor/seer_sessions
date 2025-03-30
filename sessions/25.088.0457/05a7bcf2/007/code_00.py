import numpy as np

"""
Transformation Rule:
1.  **Identify the Divider**: Locate the single, complete row or column composed entirely of azure (8) pixels. Determine its orientation (horizontal or vertical) and index (row or column number).
2.  **Define Regions**: Based on the divider, identify the two distinct regions of the grid (e.g., Region 1: above/left, Region 2: below/right).
3.  **Initialize Output Grid**: Create an output grid initially identical to the input grid.
4.  **Process Each Region Independently**: Apply the following steps sequentially within each region, using the *input* grid to determine conditions and locations, and modifying the *output* grid:
    a.  **Color Change**: Check the *input* pixels within the current region. If any yellow (4) pixels are present anywhere in this input region, change *all* corresponding yellow (4) pixels in the *output* grid for this region to green (3). Red (2) pixels from the input remain red (2) in the output (this is handled by the initial copy unless overwritten by subsequent fills).
    b.  **Fill Towards Divider**: For each line perpendicular to the divider (i.e., each column for a horizontal divider, each row for a vertical divider) that intersects the current region:
        i.  **Yellow Fill**: Check if the *input* grid region originally contained *any* yellow (4) pixels. If yes:
            - Find the yellow (4) pixel in the *input* grid on the current line that is closest to the divider.
            - If such a pixel exists, identify all the cells on this line strictly *between* that closest yellow pixel's original position and the divider.
            - For each identified cell, if its corresponding cell in the *input* grid was white (0), change its color in the *output* grid to yellow (4).
        ii. **Azure Fill**: Check if the *input* grid region originally contained *any* red (2) pixels. If yes:
            - Find the red (2) pixel in the *input* grid on the current line that is closest to the divider.
            - If such a pixel exists, identify all the cells on this line strictly *between* that closest red pixel's original position and the divider.
            - For each identified cell, if its corresponding cell in the *input* grid was white (0), change its color in the *output* grid to azure (8). (Note: This check against the original input grid prevents azure fill from overwriting a yellow fill that targeted the same original white cell).
5.  **Final Output**: The modified output grid after processing both regions is the result.
"""

import numpy as np

def find_divider(grid):
    """
    Finds the divider line (full row or column of azure) in the grid.

    Args:
        grid: numpy array representing the input grid.

    Returns:
        A tuple (orientation, index) where orientation is 'horizontal' or 'vertical',
        and index is the row or column index of the divider.
        Returns (None, None) if no divider is found.
    """
    height, width = grid.shape

    # Check for horizontal divider
    for r in range(height):
        if np.all(grid[r, :] == 8):
            return 'horizontal', r

    # Check for vertical divider
    for c in range(width):
        if np.all(grid[:, c] == 8):
            return 'vertical', c

    return None, None

def process_region(input_np, output_grid, orientation, divider_index, region_rows, region_cols):
    """
    Processes a single region defined by row/column slices.
    Applies color changes and filling based on input colors in the region.
    Modifies the output_grid directly.

    Args:
        input_np: The original input numpy array.
        output_grid: The numpy array representing the output grid (modified in-place).
        orientation: 'horizontal' or 'vertical' orientation of the divider.
        divider_index: Row or column index of the divider.
        region_rows: Slice object for the rows of this region.
        region_cols: Slice object for the columns of this region.
    """
    height, width = input_np.shape
    # Extract the view of the input grid for this region
    region_slice_input = input_np[region_rows, region_cols]

    # Check for presence of key colors in the input region
    has_yellow_in_region = np.any(region_slice_input == 4)
    has_red_in_region = np.any(region_slice_input == 2)

    # 4a. Color Change (Yellow -> Green)
    if has_yellow_in_region:
        # Iterate through the defined region coordinates
        for r in range(region_rows.start, region_rows.stop):
             for c in range(region_cols.start, region_cols.stop):
                 if input_np[r, c] == 4:
                     output_grid[r, c] = 3 # Change yellow to green in output

    # 4b. Fill Towards Divider
    if orientation == 'horizontal':
        # Iterate through each column within the region's column bounds
        for c in range(region_cols.start, region_cols.stop):
            # Get the slice of the *input* column within the region's row bounds
            col_slice_input = input_np[region_rows, c]

            # i. Yellow Fill (if applicable for this region)
            if has_yellow_in_region:
                yellow_indices_relative = np.where(col_slice_input == 4)[0]
                if len(yellow_indices_relative) > 0:
                    # Adjust indices to be absolute row indices in the full grid
                    absolute_yellow_indices = yellow_indices_relative + region_rows.start
                    
                    # Determine the row index of the yellow pixel closest to the divider
                    if region_rows.start < divider_index: # Region is above divider
                        closest_yellow_row = np.max(absolute_yellow_indices)
                        # Define the range of rows to potentially fill (exclusive of pixel, inclusive of divider edge)
                        fill_start_row = closest_yellow_row + 1
                        fill_end_row = divider_index # Fill up to (not including) the divider row
                    else: # Region is below divider
                        closest_yellow_row = np.min(absolute_yellow_indices)
                        # Define the range of rows to potentially fill
                        fill_start_row = divider_index + 1 # Fill starts below divider
                        fill_end_row = closest_yellow_row # Fill up to (not including) the yellow pixel row
                    
                    # Fill the white cells in the output grid
                    for fill_r in range(fill_start_row, fill_end_row):
                        if input_np[fill_r, c] == 0: # Check original input cell
                            output_grid[fill_r, c] = 4

            # ii. Azure Fill (if applicable for this region)
            if has_red_in_region:
                red_indices_relative = np.where(col_slice_input == 2)[0]
                if len(red_indices_relative) > 0:
                    # Adjust indices to be absolute row indices
                    absolute_red_indices = red_indices_relative + region_rows.start

                    # Determine the row index of the red pixel closest to the divider
                    if region_rows.start < divider_index: # Region is above divider
                        closest_red_row = np.max(absolute_red_indices)
                        fill_start_row = closest_red_row + 1
                        fill_end_row = divider_index
                    else: # Region is below divider
                        closest_red_row = np.min(absolute_red_indices)
                        fill_start_row = divider_index + 1
                        fill_end_row = closest_red_row

                    # Fill the white cells in the output grid
                    for fill_r in range(fill_start_row, fill_end_row):
                         if input_np[fill_r, c] == 0: # Check original input cell
                            output_grid[fill_r, c] = 8


    elif orientation == 'vertical':
         # Iterate through each row within the region's row bounds
        for r in range(region_rows.start, region_rows.stop):
            # Get the slice of the *input* row within the region's column bounds
            row_slice_input = input_np[r, region_cols]

            # i. Yellow Fill (if applicable for this region)
            if has_yellow_in_region:
                yellow_indices_relative = np.where(row_slice_input == 4)[0]
                if len(yellow_indices_relative) > 0:
                    # Adjust indices to be absolute column indices
                    absolute_yellow_indices = yellow_indices_relative + region_cols.start

                    # Determine the column index of the yellow pixel closest to the divider
                    if region_cols.start < divider_index: # Region is left of divider
                        closest_yellow_col = np.max(absolute_yellow_indices)
                        fill_start_col = closest_yellow_col + 1
                        fill_end_col = divider_index
                    else: # Region is right of divider
                        closest_yellow_col = np.min(absolute_yellow_indices)
                        fill_start_col = divider_index + 1
                        fill_end_col = closest_yellow_col
                        
                    # Fill the white cells in the output grid
                    for fill_c in range(fill_start_col, fill_end_col):
                        if input_np[r, fill_c] == 0: # Check original input cell
                            output_grid[r, fill_c] = 4

            # ii. Azure Fill (if applicable for this region)
            if has_red_in_region:
                red_indices_relative = np.where(row_slice_input == 2)[0]
                if len(red_indices_relative) > 0:
                     # Adjust indices to be absolute column indices
                    absolute_red_indices = red_indices_relative + region_cols.start

                    # Determine the column index of the red pixel closest to the divider
                    if region_cols.start < divider_index: # Region is left of divider
                        closest_red_col = np.max(absolute_red_indices)
                        fill_start_col = closest_red_col + 1
                        fill_end_col = divider_index
                    else: # Region is right of divider
                        closest_red_col = np.min(absolute_red_indices)
                        fill_start_col = divider_index + 1
                        fill_end_col = closest_red_col

                    # Fill the white cells in the output grid
                    for fill_c in range(fill_start_col, fill_end_col):
                        if input_np[r, fill_c] == 0: # Check original input cell
                            output_grid[r, fill_c] = 8


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    Identifies an azure divider, splits the grid into regions,
    and processes each region based on the presence of yellow or red pixels.
    Yellow pixels turn green. Empty space (white) between yellow/red pixels
    and the divider is filled with yellow/azure respectively.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 3. Initialize Output Grid as a copy of the input
    output_grid = np.copy(input_np)

    # 1. Identify the divider
    orientation, divider_index = find_divider(input_np)

    # If no divider is found, return the original grid unchanged
    # (Based on problem description, a divider should always exist)
    if orientation is None:
        print("Warning: No divider found. Returning input grid.") # Or raise error
        return input_grid # Return original list of lists

    # 2. Define Regions and 4. Process Regions
    if orientation == 'horizontal':
        # Divider is a row, regions are above and below
        d_r = divider_index
        # Process Region 1 (Above), if it exists (divider is not the top row)
        if d_r > 0:
            region1_rows = slice(0, d_r)
            region1_cols = slice(0, width)
            process_region(input_np, output_grid, orientation, d_r, region1_rows, region1_cols)

        # Process Region 2 (Below), if it exists (divider is not the bottom row)
        if d_r < height - 1:
            region2_rows = slice(d_r + 1, height)
            region2_cols = slice(0, width)
            process_region(input_np, output_grid, orientation, d_r, region2_rows, region2_cols)

    elif orientation == 'vertical':
        # Divider is a column, regions are left and right
        d_c = divider_index
        # Process Region 1 (Left), if it exists (divider is not the leftmost column)
        if d_c > 0:
            region1_rows = slice(0, height)
            region1_cols = slice(0, d_c)
            process_region(input_np, output_grid, orientation, d_c, region1_rows, region1_cols)

        # Process Region 2 (Right), if it exists (divider is not the rightmost column)
        if d_c < width - 1:
            region2_rows = slice(0, height)
            region2_cols = slice(d_c + 1, width)
            process_region(input_np, output_grid, orientation, d_c, region2_rows, region2_cols)

    # 5. Final Output: Convert the modified numpy array back to list of lists
    return output_grid.tolist()