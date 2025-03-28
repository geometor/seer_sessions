import numpy as np

"""
Identify the four 5x4 quadrants in the 11x9 input grid defined by the central 
yellow horizontal (row 5) and vertical (column 4) lines. These quadrants are:
- Top-Left (TL): Rows 0-4, Columns 0-3
- Top-Right (TR): Rows 0-4, Columns 5-8
- Bottom-Left (BL): Rows 6-10, Columns 0-3
- Bottom-Right (BR): Rows 6-10, Columns 5-8

Create a 5x4 output grid. For each cell (r, c) in the output grid, determine 
its color by checking the corresponding cells in the input quadrants in the 
following priority order: BR, TL, TR, BL. The output cell takes the color of 
the first non-white (non-zero) cell encountered in this sequence. If all 
corresponding cells in the quadrants are white, the output cell remains white.
"""

def transform(input_grid):
    """
    Transforms the input grid based on combining quadrant information with priority.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)

    # Define the dimensions for quadrants and output
    quad_height = 5
    quad_width = 4
    output_height = quad_height
    output_width = quad_width

    # Extract the four quadrants
    # Top-Left (TL): Rows 0-4, Columns 0-3
    tl_quad = input_np[0:quad_height, 0:quad_width]
    # Top-Right (TR): Rows 0-4, Columns 5-8 (input cols 5 to 5+width)
    tr_quad = input_np[0:quad_height, quad_width + 1 : quad_width + 1 + quad_width]
    # Bottom-Left (BL): Rows 6-10 (input rows 6 to 6+height), Columns 0-3
    bl_quad = input_np[quad_height + 1 : quad_height + 1 + quad_height, 0:quad_width]
    # Bottom-Right (BR): Rows 6-10, Columns 5-8
    br_quad = input_np[quad_height + 1 : quad_height + 1 + quad_height, quad_width + 1 : quad_width + 1 + quad_width]

    # Initialize the output grid with white (0)
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Apply priority order: BR -> TL -> TR -> BL
            # Check Bottom-Right quadrant
            if br_quad[r, c] != 0:
                output_grid_np[r, c] = br_quad[r, c]
            # Check Top-Left quadrant
            elif tl_quad[r, c] != 0:
                output_grid_np[r, c] = tl_quad[r, c]
            # Check Top-Right quadrant
            elif tr_quad[r, c] != 0:
                output_grid_np[r, c] = tr_quad[r, c]
            # Check Bottom-Left quadrant
            elif bl_quad[r, c] != 0:
                output_grid_np[r, c] = bl_quad[r, c]
            # If all are 0, the output cell remains 0 (already initialized)

    # Convert the result back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid