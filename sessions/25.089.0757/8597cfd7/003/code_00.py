import numpy as np

"""
Transformation Rule:
1. Find the horizontal line composed entirely of gray pixels (color 5) in the input grid.
2. Isolate the portion of the grid located below this gray line.
3. Within this lower portion, count the total number of red pixels (color 2) and the total number of yellow pixels (color 4).
4. Compare these two counts.
   - If the count of red pixels is greater than or equal to the count of yellow pixels, choose red (color 2).
   - Otherwise (if the count of yellow pixels is strictly greater than the count of red pixels), choose yellow (color 4).
5. Construct a new 2x2 grid. Fill every cell of this 2x2 grid with the color chosen in the previous step. This 2x2 grid is the output.
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
    Applies the transformation rule to the input grid.
    Identifies a horizontal gray line, counts red and yellow pixels below it,
    compares the counts (red wins ties), and returns a 2x2 grid filled
    with the winning color.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 1. Find the horizontal line composed entirely of gray pixels (color 5)
    gray_line_row = find_horizontal_gray_line(input_np)
    
    if gray_line_row == -1:
        # Handle cases where the gray line is missing (though not expected based on examples)
        # Returning an empty grid might be appropriate, or raise an error.
        # Based on ARC structure, an unexpected input structure might warrant returning the input unchanged or a minimal grid.
        # Let's return a 1x1 black grid as a sign of failure if no gray line is found.
        # print("Warning: Gray line not found!") 
        return [[0]] # Return 1x1 black grid for error/unexpected input
        
    # 2. Isolate the portion of the grid located below this gray line.
    lower_region = None
    if gray_line_row + 1 < height:
        lower_region = input_np[gray_line_row + 1:, :]
    # If gray_line_row is the last row, lower_region remains None

    # 3. Within this lower portion, count red (2) and yellow (4) pixels.
    red_color = 2
    yellow_color = 4
    
    red_count = count_color_in_region(lower_region, red_color)
    yellow_count = count_color_in_region(lower_region, yellow_color)

    # 4. Compare these two counts. Red wins or ties.
    # If red_count >= yellow_count, choose red. Otherwise, choose yellow.
    winning_color = red_color if red_count >= yellow_count else yellow_color
    
    # 5. Construct a new 2x2 grid filled with the winning color.
    output_grid_np = np.full((2, 2), winning_color, dtype=int)
    
    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid