import numpy as np
import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the following logic:
    1. Identify the two distinct non-background (non-zero) colors present (C1, C2). If not exactly two, return the input grid unchanged.
    2. Create a copy of the input grid to serve as the output grid.
    3. Iterate through each row of the grid.
    4. For rows containing pixels of both C1 and C2:
        a. Find the minimum and maximum column indices occupied by C1 (min1, max1) and C2 (min2, max2) within that row.
        b. Determine the overall minimum (min_col) and maximum (max_col) column index occupied by either C1 or C2 in that row.
        c. Identify the 'fill_color':
            - If C1's horizontal span in the row includes or equals C2's span (min1 <= min2 and max1 >= max2), then fill_color is C1.
            - Else if C2's horizontal span includes or equals C1's span (min2 <= min1 and max2 >= max1), then fill_color is C2.
            - If neither condition is met (which shouldn't happen based on observed examples), no fill color is determined for this row.
        d. If a fill_color was determined, modify the output grid by setting all cells in the current row from min_col to max_col (inclusive) to the fill_color.
    5. Rows containing only one type of non-background color, or only background color, remain unchanged in the output grid.
    6. Return the modified output grid.
    """
    
    # Convert input to numpy array for easier manipulation and analysis
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring unchanged rows/pixels are preserved
    output_grid = np.copy(grid) 
    height, width = grid.shape

    # --- Step 1: Identify non-background colors ---
    unique_colors = np.unique(grid)
    non_background_colors = [c for c in unique_colors if c != 0]

    # --- Expecting exactly two non-background colors based on examples ---
    if len(non_background_colors) != 2:
        # If condition not met, return the original grid as per instructions/observations
        # print("Warning: Did not find exactly two non-background colors.")
        return input_grid 
        
    c1, c2 = non_background_colors

    # --- Step 3 & 4: Process each row ---
    for r in range(height):
        row = grid[r, :]
        
        # Find column indices for each color in the current row
        cols_c1 = np.where(row == c1)[0]
        cols_c2 = np.where(row == c2)[0]

        # --- Step 4: Proceed only if both colors are present in the row ---
        if len(cols_c1) > 0 and len(cols_c2) > 0:
            # --- Step 4a: Find min/max columns for each color ---
            min_col_c1, max_col_c1 = cols_c1.min(), cols_c1.max()
            min_col_c2, max_col_c2 = cols_c2.min(), cols_c2.max()

            # --- Step 4b: Find overall min/max columns for non-background colors ---
            min_col = min(min_col_c1, min_col_c2)
            max_col = max(max_col_c1, max_col_c2)

            # --- Step 4c: Determine the fill color based on horizontal span inclusion ---
            fill_color = -1 # Initialize with an invalid value
            if min_col_c1 <= min_col_c2 and max_col_c1 >= max_col_c2:
                 # C1 encloses or equals C2 horizontally, or spans the full range if C2 is single point
                 fill_color = c1 
            elif min_col_c2 <= min_col_c1 and max_col_c2 >= max_col_c1:
                 # C2 encloses or equals C1 horizontally, or spans the full range if C1 is single point
                 fill_color = c2 
            # else: 
                 # This case implies neither color fully encloses the other horizontally.
                 # Examples suggest one color's span will always define the bounds for filling.
                 # If this case were encountered, specific rules would be needed. We assume it won't happen.
                 # print(f"Warning: Ambiguous fill condition in row {r}.")
                 
            # --- Step 4d: Fill the row segment in the output grid ---
            if fill_color != -1:
                for c in range(min_col, max_col + 1):
                    # Modify the copied grid
                    output_grid[r, c] = fill_color
        # --- Step 5: Rows with 0 or 1 non-background color are implicitly unchanged ---
        # as we only modify rows where len(cols_c1)>0 and len(cols_c2)>0

    # --- Step 6: Convert back to list of lists for the final output ---
    return output_grid.tolist()