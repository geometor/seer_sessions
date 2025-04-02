import copy

"""
Expand single non-white pixels into horizontal blocks of three, keeping existing blocks of three unchanged.

Iterate through the input row. If a non-white pixel is found that is surrounded by white pixels (or grid boundaries), 
expand it into a block of three pixels of the same color in the output grid, centered at the original pixel's position.
Pixels that are already part of a block of three or more in the input, or white pixels not overwritten by expansion, 
are copied directly to the output.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the rule.

    Args:
        input_grid (list): A list containing a single list representing the input row.

    Returns:
        list: A list containing a single list representing the transformed output row.
    """
    # As the grid is described as 1D, extract the single row
    # Handle potential empty input gracefully
    if not input_grid or not input_grid[0]:
        return []
        
    input_row = input_grid[0]
    width = len(input_row)
    
    # Initialize output_row as a copy of the input_row
    output_row = list(input_row) 

    # Iterate through each pixel in the input row
    for i in range(width):
        color = input_row[i]

        # Check if the pixel is non-white (color > 0)
        if color > 0:
            # Check if the pixel to the left is white (0) or out of bounds
            is_left_white_or_boundary = (i == 0) or (input_row[i-1] == 0)
            
            # Check if the pixel to the right is white (0) or out of bounds
            is_right_white_or_boundary = (i == width - 1) or (input_row[i+1] == 0)

            # If both neighbors are white or boundaries, it's a single pixel to be expanded
            if is_left_white_or_boundary and is_right_white_or_boundary:
                # Expand the single pixel into a block of three in the output_row
                # Center pixel (already copied, but set explicitly for clarity)
                output_row[i] = color
                # Left pixel (if within bounds)
                if i > 0:
                    output_row[i-1] = color
                # Right pixel (if within bounds)
                if i < width - 1:
                    output_row[i+1] = color
            # Else: The pixel is part of an existing block or adjacent to another non-white pixel.
            # In this case, the initial copy from input_row to output_row handles it correctly,
            # as we only modify the output_row when expanding a single pixel.

    # Return the modified row wrapped in a list to match the expected grid format
    return [output_row]
