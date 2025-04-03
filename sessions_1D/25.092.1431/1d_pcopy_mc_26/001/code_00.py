import copy

"""
Transforms a 1D grid (represented as a 1xN 2D grid) by identifying isolated non-white pixels 
and changing their immediate left and right white neighbors to match the isolated pixel's color.

An isolated non-white pixel is defined as a pixel C (where C != 0) at index i such that the 
pixel at i-1 is white (0) and the pixel at i+1 is white (0).

The transformation iterates through the grid, and for each identified isolated pixel, 
it updates the colors of its white neighbors in the output grid. Pixels not meeting 
this specific condition remain unchanged. Only grids with a single row are processed.
"""

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to have only one row based on examples.

    Returns:
        list of lists: The transformed grid. Returns the original grid if input 
                       does not have exactly one row.
    """
    # Check if the input grid has exactly one row, as seen in examples
    if len(input_grid) != 1:
        # If not a single row grid, return input unchanged as the rule is unclear
        return input_grid

    input_row = input_grid[0]
    height = 1
    width = len(input_row)
    
    # Initialize output_grid as a deep copy of the input_grid
    # Operate on the first row copy
    output_row = copy.deepcopy(input_row)

    # Iterate through the pixels of the row, excluding the first and last elements
    # as they cannot be surrounded by neighbors
    for i in range(1, width - 1):
        # Get the colors of the current pixel and its immediate neighbors
        center_color = input_row[i]
        left_color = input_row[i-1]
        right_color = input_row[i+1]

        # Check if the center pixel is non-white (not 0)
        # and both its left and right neighbors are white (0)
        if center_color != 0 and left_color == 0 and right_color == 0:
            # If the condition is met, change the white neighbors in the output row
            # to the color of the center pixel
            output_row[i-1] = center_color
            output_row[i+1] = center_color

    # Return the transformed row wrapped in a list to maintain the grid structure
    return [output_row]