import numpy as np

"""
Transformation Rule:
1. Find the horizontal line composed entirely of gray pixels (color 5) in the input grid.
2. Define the 'upper region' as all rows above the gray line and the 'lower region' as all rows below it.
3. Count the number of red pixels (color 2) and yellow pixels (color 4) in both the upper region (R_above, Y_above) and the lower region (R_below, Y_below).
4. Determine the output color based on the counts:
   - The default output color is red (2).
   - The output color becomes yellow (4) *only if* all three of the following conditions are met:
     a) The yellow count is strictly greater than the red count in the upper region (Y_above > R_above).
     b) The yellow count is strictly greater than the red count in the lower region (Y_below > R_below).
     c) The difference (margin) between yellow and red counts in the lower region is greater than or equal to the difference in the upper region ((Y_below - R_below) >= (Y_above - R_above)).
5. Construct a new 2x2 grid filled entirely with the determined output color.
"""

def find_horizontal_gray_line(grid):
    """Finds the row index of the first horizontal line made entirely of gray pixels."""
    height, width = grid.shape
    gray_color = 5
    for r in range(height):
        if np.all(grid[r, :] == gray_color):
            return r
    return -1 # Indicate not found

def count_color_in_region(grid_region, color):
    """Counts the occurrences of a specific color in a given grid region."""
    # Check if the region is valid and not empty before counting
    if grid_region is not None and grid_region.size > 0:
        return np.count_nonzero(grid_region == color)
    return 0

def transform(input_grid):
    """
    Applies the refined transformation rule to the input grid.
    Finds a gray line, counts red/yellow pixels above and below,
    applies a specific set of conditions to determine the output color (red or yellow),
    and returns a 2x2 grid filled with that color.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 1. Find Separator: Locate the horizontal gray line.
    gray_line_row = find_horizontal_gray_line(input_np)
    
    if gray_line_row == -1:
        # Handle cases where the gray line is missing (unexpected based on examples).
        # Returning a default small grid (e.g., 1x1 black) might be appropriate.
        return [[0]] 
        
    # 2. Define Regions: Identify upper and lower regions.
    # Handle edge cases where the gray line is the first or last row.
    upper_region = None
    if gray_line_row > 0:
        upper_region = input_np[:gray_line_row, :]
        
    lower_region = None
    if gray_line_row + 1 < height:
        lower_region = input_np[gray_line_row + 1:, :]

    # Define colors
    red_color = 2
    yellow_color = 4
    
    # 3. Count Above: Count red and yellow pixels in the upper region.
    r_above = count_color_in_region(upper_region, red_color)
    y_above = count_color_in_region(upper_region, yellow_color)
    
    # 4. Count Below: Count red and yellow pixels in the lower region.
    r_below = count_color_in_region(lower_region, red_color)
    y_below = count_color_in_region(lower_region, yellow_color)

    # 5. Determine Winning Color: Apply the refined comparison logic.
    # Default to red
    winning_color = red_color 
    
    # Check conditions to switch to yellow
    condition_a = y_above > r_above
    condition_b = y_below > r_below
    
    # Calculate differences safely, handle potential division by zero or comparison with non-existent regions if necessary (though counts are 0 if regions don't exist)
    diff_above = y_above - r_above
    diff_below = y_below - r_below
    condition_c = diff_below >= diff_above # Equivalent to (y_below - r_below) >= (y_above - r_above)

    if condition_a and condition_b and condition_c:
        winning_color = yellow_color # Switch to yellow only if all conditions met

    # 6. Construct Output: Create a 2x2 grid filled with the winning color.
    output_grid_np = np.full((2, 2), winning_color, dtype=int)
    
    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid