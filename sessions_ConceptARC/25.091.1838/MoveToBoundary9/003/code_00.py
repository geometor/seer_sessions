import numpy as np

"""
Transforms the input grid by moving groups of pixels based on their color. 
Each non-background color group (all pixels of that color, regardless of contiguity) 
is treated as a single unit. 
The horizontal center of the group's bounding box determines the movement direction:
left if the center is left of the grid's vertical midpoint, right otherwise.
The group is then shifted horizontally until its corresponding edge (leftmost column 
for leftward movement, rightmost column for rightward movement) aligns with the grid's edge. 
The relative positions of pixels within the group are preserved.
"""

def transform(input_grid):
    """
    Moves color groups horizontally to the grid edges.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)
    
    # Define background color
    background_color = 0
    
    # Calculate grid horizontal midpoint
    # Use floating point for accurate comparison, even for odd widths
    grid_mid_col = (width - 1) / 2.0 
    
    # Find all unique non-background colors
    unique_colors = np.unique(input_np)
    non_bg_colors = unique_colors[unique_colors != background_color]
    
    # Process each color group
    for color in non_bg_colors:
        # Find all coordinates (pixels) of the current color
        coords = np.argwhere(input_np == color)
        
        # Skip if this color isn't actually present (shouldn't happen with unique, but safe)
        if coords.size == 0:
            continue
            
        # Determine the horizontal extent (bounding box) of the color group
        cols = coords[:, 1]
        min_col = np.min(cols)
        max_col = np.max(cols)
        
        # Calculate the group's horizontal center
        group_center_col = (min_col + max_col) / 2.0
        
        # Determine movement direction and calculate horizontal shift (delta_col)
        delta_col = 0
        if group_center_col < grid_mid_col:
            # Move left: shift needed to bring min_col to 0
            delta_col = 0 - min_col
        else:
            # Move right: shift needed to bring max_col to width - 1
            delta_col = (width - 1) - max_col
            
        # Apply the shift to each pixel of the color group
        for r, c in coords:
            new_c = c + delta_col
            # Place the pixel in the output grid, checking bounds just in case
            if 0 <= new_c < width:
                output_np[r, new_c] = color

    # Convert output numpy array back to list of lists
    output_grid = output_np.tolist()
    
    return output_grid