import copy

"""
Identify single non-white pixels (C) that are surrounded by white pixels (0) 
on their immediate left and right (0 C 0 pattern) within each row. 
Expand this pattern into a triplet of the non-white color (C C C), 
replacing the original 0 C 0 sequence in the output. 
Sequences that are already triplets (or longer) of non-white colors, 
or single non-white pixels not flanked by white on both sides, remain unchanged.
The transformation is applied independently to each row.
"""

def transform(input_grid):
    """
    Transforms the input grid by expanding flanked single non-white pixels into triplets.

    Args:
        input_grid (list of lists of int): The input grid representing colors.

    Returns:
        list of lists of int: The transformed grid.
    """
    # Initialize output_grid as a deep copy to preserve original elements not modified
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Iterate through each row
    for r in range(height):
        # Iterate through columns, checking for the 0 C 0 pattern
        # We need to check indices c-1, c, c+1, so iterate c from 1 to width-2
        for c in range(1, width - 1):
            # Check if the current pixel is non-white (C > 0)
            if input_grid[r][c] > 0:
                # Check if the left neighbor is white (0)
                is_left_white = input_grid[r][c-1] == 0
                # Check if the right neighbor is white (0)
                is_right_white = input_grid[r][c+1] == 0
                
                # If both neighbors are white (0 C 0 pattern found)
                if is_left_white and is_right_white:
                    # Get the color of the center pixel
                    color_to_expand = input_grid[r][c]
                    # Expand the color into a triplet in the output grid
                    output_grid[r][c-1] = color_to_expand
                    output_grid[r][c] = color_to_expand
                    output_grid[r][c+1] = color_to_expand

    return output_grid