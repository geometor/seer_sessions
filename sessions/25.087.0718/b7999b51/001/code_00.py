import numpy as np

"""
Identifies all unique non-white colors in the input grid.
For each unique color, calculates its vertical extent (height) as the difference 
between the maximum and minimum row indices where it appears, plus one.
Determines the maximum height among all colors.
Sorts the unique colors in descending order based on their calculated heights.
Creates an output grid with height equal to the maximum height found and width 
equal to the number of unique non-white colors.
Fills the output grid column by column, corresponding to the sorted colors. 
Each column is filled from the top with its associated color for a number of rows 
equal to its calculated height. The remaining cells in the column are left as the 
background color (white, 0).
"""

def calculate_color_heights(input_grid):
    """
    Finds unique non-white colors and calculates their vertical span (height).

    Args:
        input_grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (color, height).
              Returns an empty list if no non-white colors are found.
    """
    unique_colors = np.unique(input_grid)
    non_white_colors = [color for color in unique_colors if color != 0]
    
    color_heights = []
    if not non_white_colors:
        return color_heights

    for color in non_white_colors:
        # Find row indices where the color appears
        rows, _ = np.where(input_grid == color)
        
        if rows.size > 0:
            min_row = np.min(rows)
            max_row = np.max(rows)
            height = max_row - min_row + 1
            color_heights.append((color, height))
            
    return color_heights

def transform(input_grid):
    """
    Transforms the input grid based on the vertical span of its colored objects.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid)

    # 1. Identify unique non-white colors and calculate their heights.
    color_data = calculate_color_heights(input_grid_np)

    # Handle edge case: No non-white colors found
    if not color_data:
        # Return an empty grid or a minimal white grid based on convention.
        # Returning a 1x1 white grid seems reasonable if output must have dimensions.
        # Let's return 0x0 based on typical ARC empty outputs.
        return np.zeros((0, 0), dtype=int) 

    # 2. Determine the maximum height (output grid height).
    max_height = 0
    if color_data:
      max_height = max(height for _, height in color_data)

    # 3. Determine the number of unique colors (output grid width).
    num_colors = len(color_data)

    # 4. Sort the colors by height in descending order.
    # No tie-breaking specified, default Python sort stability or sorting by color is fine.
    # Let's sort by height (desc) then color (asc) for determinism if needed.
    sorted_color_data = sorted(color_data, key=lambda item: (-item[1], item[0]))

    # 5. Create the output grid, initialized with background color 0.
    output_grid = np.zeros((max_height, num_colors), dtype=int)

    # 6. Fill the output grid column by column based on sorted colors and heights.
    for col_idx, (color, height) in enumerate(sorted_color_data):
        # Fill the column from top (row 0) down to row `height - 1`
        output_grid[0:height, col_idx] = color

    return output_grid.tolist() # Convert back to list of lists if required by ARC standard
