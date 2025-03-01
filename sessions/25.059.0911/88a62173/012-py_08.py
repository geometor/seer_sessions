"""
The input grid is divided into four quadrants. Each quadrant maps to a cell in the 2x2 output grid. The output cell's color is determined by a summary of the colors in the corresponding input quadrant. The exact color mapping rule is still being determined, but it's not solely based on blue pixel presence.
"""

import numpy as np

def get_quadrant(input_grid, row_start, row_end, col_start, col_end):
    """Extracts a quadrant from the input grid."""
    return input_grid[row_start:row_end, col_start:col_end]

def summarize_quadrant(quadrant):
    """
    Analyzes a quadrant and returns a summarized color. 
    This is a placeholder for the actual color mapping rule,
    which needs to be determined through further analysis.
    """
    colors = set(quadrant.flatten())
    colors.discard(0)  # Remove white, as it seems to be the default

    if not colors:  # If only white remains
        return 0  # Return white

    # Placeholder logic:  Return *a* color from the set.
    # This is where the core logic needs to be developed,
    # perhaps a mapping, a conditional rule, etc.
    return list(colors)[0]
    

def transform(input_grid):
    """Transforms the input grid to the output grid based on quadrant analysis."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Calculate midpoints for quadrant division
    row_mid = rows // 2
    col_mid = cols // 2

    # Initialize the output grid as 2x2 with all white pixels (0)
    output_grid = np.zeros((2, 2), dtype=int)

    # Define the four quadrants, handling edge cases for odd dimensions
    quadrants = [
        (0, row_mid + (rows%2), 0, col_mid + (cols%2)),  # Top-left
        (0, row_mid + (rows%2), col_mid, cols),         # Top-right
        (row_mid, rows, 0, col_mid + (cols%2)),         # Bottom-left
        (row_mid, rows, col_mid, cols)                # Bottom-right
    ]

    # Iterate through quadrants and determine output colors
    for i, (row_start, row_end, col_start, col_end) in enumerate(quadrants):
        quadrant = get_quadrant(input_grid, row_start, row_end, col_start, col_end)
        output_color = summarize_quadrant(quadrant)  # Use the summary function
       
        output_row = i // 2
        output_col = i % 2
        output_grid[output_row, output_col] = output_color

    return output_grid.tolist()