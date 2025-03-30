import numpy as np

"""
Identify non-white pixels in the input grid. For each non-white pixel found, 
create a 3x3 square centered on it in the output grid. The center of the 
square retains the original pixel's color. The 8 surrounding pixels of the 
square are filled with a new color determined by a specific mapping: 
green (3) maps to magenta (6), red (2) maps to blue (1), and azure (8) maps 
to yellow (4). Pixels outside these generated squares retain their original 
color (typically white).
"""

def transform(input_grid):
    """
    Transforms the input grid by creating 3x3 colored squares around 
    non-white pixels based on a color mapping rule.
    
    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.
        
    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Define the mapping from center pixel color to border pixel color
    color_map = {
        3: 6,  # green -> magenta
        2: 1,  # red -> blue
        8: 4   # azure -> yellow
    }

    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize the output grid as a copy of the input grid.
    # This preserves the original pixels and background unless modified.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            center_color = input_grid[r, c]

            # Check if the pixel is non-white and has a mapping defined
            if center_color != 0 and center_color in color_map:
                border_color = color_map[center_color]

                # Iterate through the 3x3 neighborhood around the center pixel (r, c)
                for dr in range(-1, 2):  # delta row: -1, 0, 1
                    for dc in range(-1, 2):  # delta column: -1, 0, 1
                        
                        # Skip the center pixel itself (it's already correct)
                        if dr == 0 and dc == 0:
                            continue

                        # Calculate the coordinates of the neighbor pixel
                        nr, nc = r + dr, c + dc

                        # Check if the neighbor coordinates are within the grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Update the neighbor pixel in the output grid with the border color
                            output_grid[nr, nc] = border_color
                            
    return output_grid