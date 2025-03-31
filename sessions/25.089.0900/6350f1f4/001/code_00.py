import numpy as np

"""
Identify the dominant color from the top-left pixel (0,0) of the input grid.
Create an output grid initialized as a copy of the input grid.
Iterate through each pixel in the input grid.
If a pixel's color is neither white (0) nor the dominant color, check its non-diagonal neighbors (up, down, left, right) in the *input* grid.
If any of these neighbors has the dominant color, change the corresponding pixel's color in the *output* grid to the dominant color.
White pixels and pixels already having the dominant color remain unchanged.
Return the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the dominant color propagation rule.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Identify the dominant color from the top-left pixel
    dominant_color = input_np[0, 0]
    
    # Define white color constant
    color_white = 0
    
    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            current_color = input_np[r, c]
            
            # Skip processing if the pixel is white or already the dominant color
            if current_color == color_white or current_color == dominant_color:
                continue
                
            # Check non-diagonal neighbors
            found_dominant_neighbor = False
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # Up, Down, Left, Right
                nr, nc = r + dr, c + dc
                
                # Check if neighbor coordinates are within grid bounds
                if 0 <= nr < height and 0 <= nc < width:
                    # Check if the neighbor in the *input* grid has the dominant color
                    if input_np[nr, nc] == dominant_color:
                        found_dominant_neighbor = True
                        break # No need to check other neighbors
            
            # If a dominant neighbor was found, update the pixel in the output grid
            if found_dominant_neighbor:
                output_grid[r, c] = dominant_color
                
    # Convert the result back to a list of lists
    return output_grid.tolist()
