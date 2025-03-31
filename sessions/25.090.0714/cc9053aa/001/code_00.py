import numpy as np

"""
Identifies the column span of azure (8) pixels.
Categorizes maroon (9) pixels based on their column position relative to this span:
- 'left': columns to the left of the azure span.
- 'right': columns to the right of the azure span.
- 'middle': columns overlapping with the azure span.

Transformation Rules (applied in order of precedence):
1. If 'right' maroons exist, change all azure pixels in the *leftmost* column of the azure span to maroon.
2. If 'left' maroons exist, change all azure pixels in the *rightmost* column of the azure span to maroon. 
   (Rules 1 and 2 can apply simultaneously).
3. If NEITHER 'left' NOR 'right' maroons exist, BUT 'middle' maroons do exist:
   Find the minimum column index ('min_middle_col') among the 'middle' maroons.
   Change all azure pixels in columns from 'min_middle_col' up to and including the *rightmost* column of the azure span to maroon.
4. If none of the above conditions are met (e.g., no maroons, or no relevant maroons), no changes are made.
"""

def transform(input_grid):
    """
    Applies transformations to an input grid based on the relative positions 
    of azure (8) and maroon (9) pixels.
    """
    # Convert input list of lists to a numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    azure = 8
    maroon = 9

    # Find coordinates of all azure pixels
    azure_coords = np.argwhere(grid == azure)
    
    # If there are no azure pixels, return the original grid unchanged
    if azure_coords.size == 0:
        return output_grid.tolist() 

    # Determine the minimum and maximum column indices occupied by azure pixels
    azure_cols = azure_coords[:, 1]
    min_col = np.min(azure_cols)
    max_col = np.max(azure_cols)

    # Find coordinates of all maroon pixels
    maroon_coords = np.argwhere(grid == maroon)
    
    # If there are no maroon pixels, return the original grid unchanged
    if maroon_coords.size == 0:
        return output_grid.tolist() 

    # Get the column indices of maroon pixels
    maroon_cols = maroon_coords[:, 1]

    # Categorize maroon pixels based on their column relative to the azure span
    left_maroon_exists = np.any(maroon_cols < min_col)
    right_maroon_exists = np.any(maroon_cols > max_col)
    
    # Identify maroon pixels within the azure column span
    middle_maroon_mask = (maroon_cols >= min_col) & (maroon_cols <= max_col)
    middle_maroon_cols = maroon_cols[middle_maroon_mask]
    middle_maroon_exists = middle_maroon_cols.size > 0

    # Apply transformation rules based on maroon locations
    
    # Flag to track if left/right rules were applied, giving them precedence
    left_right_transformed = False 

    # Rule 1: If maroons exist to the right of the azure span
    if right_maroon_exists:
        # Find rows in the leftmost azure column containing azure pixels
        rows_to_change_min = np.where(grid[:, min_col] == azure)[0]
        # Change those azure pixels to maroon in the output grid
        if rows_to_change_min.size > 0:
             output_grid[rows_to_change_min, min_col] = maroon
             left_right_transformed = True # Mark that a transformation occurred

    # Rule 2: If maroons exist to the left of the azure span
    if left_maroon_exists:
        # Find rows in the rightmost azure column containing azure pixels
        rows_to_change_max = np.where(grid[:, max_col] == azure)[0]
         # Change those azure pixels to maroon in the output grid
        if rows_to_change_max.size > 0:
            output_grid[rows_to_change_max, max_col] = maroon
            left_right_transformed = True # Mark that a transformation occurred

    # Rule 3: If no left/right maroons, but middle maroons exist
    # This rule only applies if the left/right rules did NOT trigger
    if not left_right_transformed and middle_maroon_exists:
        # Find the minimum column index among the middle maroons
        min_middle_col = np.min(middle_maroon_cols)
        # Iterate through columns from the min_middle_col to the max_col of the azure span
        for c in range(min_middle_col, max_col + 1):
            # Find rows in the current column 'c' containing azure pixels
            rows_to_change_middle = np.where(grid[:, c] == azure)[0]
            # Change those azure pixels to maroon in the output grid
            if rows_to_change_middle.size > 0:
                 output_grid[rows_to_change_middle, c] = maroon

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()