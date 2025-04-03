import copy

"""
Transformation Rule:
Identify single, isolated non-white pixels in the input grid's row. 
A pixel is considered isolated if its immediate left and right neighbors are white (0), or if it's at an edge and the neighbor on the other side is white.
For each identified isolated pixel, expand it into a horizontal block of three pixels of the same color in the output grid. 
This involves changing the white pixels immediately to the left and right (if they exist and are within bounds) of the original single pixel to match its color. 
Pixels that are not part of such an expansion (either original white pixels not adjacent to an expanding pixel, or pixels already part of a 3-block or other non-isolated structure in the input) remain unchanged, unless overwritten by an adjacent expansion. 
The analysis of isolated pixels is based entirely on the original input grid state. The modifications are applied to a copy of the grid.
"""

def is_isolated(grid_row, index, width):
    """
    Checks if a non-white pixel at a given index in a list (row) is isolated.
    
    Args:
        grid_row (list): The list representing the row of pixels.
        index (int): The index of the pixel to check.
        width (int): The total width (length) of the row.
        
    Returns:
        bool: True if the pixel is non-white and isolated, False otherwise.
    """
    # Check if pixel itself is non-white
    if grid_row[index] == 0:
        return False

    # Check left neighbor (or boundary)
    # True if it's the first pixel OR the pixel to the left is white (0)
    left_is_white_or_boundary = (index == 0) or (grid_row[index - 1] == 0)

    # Check right neighbor (or boundary)
    # True if it's the last pixel OR the pixel to the right is white (0)
    right_is_white_or_boundary = (index == width - 1) or (grid_row[index + 1] == 0)

    # It's isolated if both conditions are met
    return left_is_white_or_boundary and right_is_white_or_boundary

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Expands isolated non-white pixels into 3-pixel horizontal blocks.

    Args:
        input_grid (list): A list of lists representing the input grid. 
                           Expected to have only one row based on examples.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Handle empty or invalid input format
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        return [] 

    # Extract the single row from the input grid
    input_row = input_grid[0]
    width = len(input_row)
    
    # If the row is empty, return the input structure
    if width == 0:
        return [[]]

    # Create a deep copy of the input grid to modify for the output
    # This ensures changes don't affect the original input during iteration
    output_grid = copy.deepcopy(input_grid)
    output_row = output_grid[0] # Get the row reference from the copied grid

    # Iterate through each pixel index of the *original* input row
    for i in range(width):
        # Get the color of the current pixel in the original input
        pixel_color = input_row[i]

        # Check if the current pixel in the *original* input is isolated
        if is_isolated(input_row, i, width):
            # If isolated, expand it in the *output* row
            
            # Change the left neighbor in the output row if it exists (i > 0)
            if i > 0:
                output_row[i - 1] = pixel_color
            
            # The pixel itself retains its color (already set by the deep copy)
            # output_row[i] = pixel_color 

            # Change the right neighbor in the output row if it exists (i < width - 1)
            if i < width - 1:
                output_row[i + 1] = pixel_color

    # Return the modified grid (still as a list of lists)
    return output_grid