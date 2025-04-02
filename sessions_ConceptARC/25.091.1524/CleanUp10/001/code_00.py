import numpy as np

"""
Identify complete horizontal and vertical lines of red (2) pixels in the input grid. 
Create an output grid of the same dimensions, initialized to white (0). 
Transfer the identified complete horizontal and vertical red lines to their corresponding positions in the output grid. 
All other pixels in the output grid remain white (0).
"""

def transform(input_grid):
    """
    Transforms the input grid by preserving only complete horizontal and vertical red lines.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing and comparison
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Define the target color (red) and background color (white)
    target_color = 2
    background_color = 0
    
    # Initialize output_grid with the background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # Check for complete horizontal lines
    for r in range(height):
        # Check if all pixels in the current row are the target color
        if np.all(input_np[r, :] == target_color):
            # If yes, set the corresponding row in the output grid to the target color
            output_grid[r, :] = target_color

    # Check for complete vertical lines
    for c in range(width):
        # Check if all pixels in the current column are the target color
        if np.all(input_np[:, c] == target_color):
            # If yes, set the corresponding column in the output grid to the target color
            output_grid[:, c] = target_color

    return output_grid.tolist() # Return as list of lists if required by ARC interface, or keep as np.array
