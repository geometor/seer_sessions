import numpy as np
from collections import Counter

"""
Determine the dimensions (Height H, Width W) of the input grid.
Identify the color of the top-left pixel (input[0,0]) as the Top-Left Color (TL_Color).
Identify the color of the bottom-right pixel (input[H-1, W-1]) as the Bottom-Right Color (BR_Color).
Count the frequency of each color in the input grid. Determine the Background Color (BG_Color) as the color with the highest frequency, excluding TL_Color and BR_Color.
Create a new output grid of the same dimensions (H x W) and fill it entirely with the BG_Color.
Fill the rectangular region from row 0 to row 2 and from column 0 to column 3 in the output grid with TL_Color.
Fill the rectangular region from row H-4 to row H-1 and from column W-3 to W-1 in the output grid with BR_Color.
Return the modified output grid.
"""

def find_background_color(grid, tl_color, br_color):
    """
    Finds the most frequent color in the grid, excluding the specified
    top-left and bottom-right corner colors.
    """
    # Flatten the grid to a 1D list of colors
    flat_grid = grid.flatten()
    
    # Count the frequency of each color
    color_counts = Counter(flat_grid)
    
    # Sort colors by frequency in descending order
    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)
    
    # Find the most frequent color that is not tl_color or br_color
    for color, count in sorted_colors:
        if color != tl_color and color != br_color:
            return color
            
    # Fallback (should not be needed based on examples, but good practice)
    # If all colors are tl_color or br_color, pick the most frequent overall
    if sorted_colors:
        return sorted_colors[0][0] 
    return 0 # Default to white if grid is empty or has only tl/br colors

def transform(input_grid):
    """
    Transforms the input grid by identifying corner colors, determining the
    background color, initializing the output grid with the background color,
    and then drawing expanded corner blocks.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the dimensions (Height H, Width W) of the input grid.
    H, W = input_np.shape
    
    # Identify the color of the top-left pixel as the Top-Left Color (TL_Color).
    tl_color = input_np[0, 0]
    
    # Identify the color of the bottom-right pixel as the Bottom-Right Color (BR_Color).
    br_color = input_np[H-1, W-1]
    
    # Determine the Background Color (BG_Color).
    bg_color = find_background_color(input_np, tl_color, br_color)
    
    # Create a new output grid of the same dimensions (H x W) and fill it entirely with the BG_Color.
    output_grid = np.full((H, W), bg_color, dtype=int)
    
    # Fill the rectangular region for the expanded top-left block with TL_Color.
    # Rows 0 to 2 (inclusive, total 3 rows)
    # Columns 0 to 3 (inclusive, total 4 columns)
    output_grid[0:3, 0:4] = tl_color
    
    # Fill the rectangular region for the expanded bottom-right block with BR_Color.
    # Rows H-4 to H-1 (inclusive, total 4 rows)
    # Columns W-3 to W-1 (inclusive, total 3 columns)
    output_grid[H-4:H, W-3:W] = br_color
    
    # Return the modified output grid as a list of lists
    return output_grid.tolist()
