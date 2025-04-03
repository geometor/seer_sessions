import copy

"""
Transforms a 1D array based on a local expansion rule.

The transformation rule identifies isolated non-white pixels (pixels with a value 
other than 0) that are surrounded by white pixels (value 0) on both their left 
and right sides. When such a pattern (0, X, 0, where X != 0) is found, 
the isolated pixel X expands to its left and right, replacing the adjacent white 
pixels with its own color. The resulting pattern becomes (X, X, X).

Pixels that are part of existing sequences of three identical non-white pixels, 
or pixels that do not meet the isolated pixel criteria, remain unchanged.
White background pixels also remain unchanged unless they are adjacent to an 
isolated non-white pixel that expands.
"""

def transform(input_grid):
    """
    Applies the expansion transformation to a 1D input grid (list of integers).

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A new list of integers representing the transformed 1D output grid.
    """
    # Ensure input is a list (it might be passed as a tuple or other sequence)
    input_list = list(input_grid)
    
    # Initialize output_grid as a copy of the input_grid.
    # This ensures that pixels not affected by the rule are preserved.
    output_grid = copy.deepcopy(input_list)
    
    # Get the length of the grid
    grid_length = len(input_list)
    
    # Iterate through the input grid, checking for the pattern 0, X, 0
    # We iterate from index 1 to length-2 because we need to access i-1 and i+1.
    # If the grid has fewer than 3 elements, this loop will not run.
    for i in range(1, grid_length - 1):
        # Check if the current pixel is non-white (X != 0)
        # and its left neighbor (i-1) is white (0)
        # and its right neighbor (i+1) is white (0)
        if input_list[i-1] == 0 and input_list[i] != 0 and input_list[i+1] == 0:
            # If the pattern is found, get the color of the isolated pixel
            color_to_expand = input_list[i]
            
            # Update the output grid at positions i-1, i, and i+1 with the expansion color
            output_grid[i-1] = color_to_expand
            output_grid[i] = color_to_expand
            output_grid[i+1] = color_to_expand
            
    # Return the modified output grid
    return output_grid
