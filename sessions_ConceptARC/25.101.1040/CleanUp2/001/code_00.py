"""
Checks if the input grid has a uniform border (all perimeter pixels are the same color).
If a uniform border exists:
  - The border pixels in the output grid retain the border color.
  - All interior pixels (not on the border) in the output grid are filled with the most frequent color found within the interior region of the input grid.
If no uniform border exists:
  - The entire output grid is filled with the single most frequent color found across the entire input grid.
"""

import numpy as np
from collections import Counter

def find_dominant_color(pixels: np.ndarray) -> int:
    """
    Finds the most frequent color in a flattened array of pixels.
    Handles ties by returning the smallest color index.
    """
    if pixels.size == 0:
        # Handle empty region case if necessary, though unlikely based on examples
        return 0 # Default to white or raise error? Defaulting for now.
    
    counts = Counter(pixels.flatten())
    # Find the maximum count
    max_count = 0
    for color, count in counts.items():
        if count > max_count:
            max_count = count
            
    # Get all colors with the maximum count
    dominant_colors = [color for color, count in counts.items() if count == max_count]
    
    # Return the smallest color index in case of a tie
    return min(dominant_colors)

def has_uniform_border(grid: np.ndarray) -> tuple[bool, int | None]:
    """
    Checks if the grid has a uniform border.
    Returns (True, border_color) if uniform, otherwise (False, None).
    Handles 1xN and Nx1 grids.
    """
    height, width = grid.shape
    
    # Handle trivial cases (1x1 grid has a 'uniform' border)
    if height == 1 and width == 1:
        return True, grid[0, 0]
        
    border_color = grid[0, 0]
    
    # Check top and bottom rows
    if height > 0:
        for c in range(width):
            if grid[0, c] != border_color:
                return False, None
            if height > 1 and grid[height - 1, c] != border_color:
                 return False, None
                 
    # Check left and right columns (excluding corners already checked)
    if width > 0:
        for r in range(1, height - 1): # Exclude corners
            if grid[r, 0] != border_color:
                 return False, None
            if width > 1 and grid[r, width - 1] != border_color:
                return False, None

    return True, border_color

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on border detection and dominant color filling.
    """
    # Convert input list of lists to a NumPy array for easier slicing and operations
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    
    # Initialize output_grid as a NumPy array of the same shape
    output_grid_np = np.zeros_like(grid_np)

    # Check for a uniform border
    is_uniform, border_color = has_uniform_border(grid_np)

    if is_uniform and border_color is not None:
        # Case 1: Uniform border exists
        
        # Define the interior region (handle grids smaller than 3x3)
        if height > 2 and width > 2:
            interior_region = grid_np[1:-1, 1:-1]
        elif height <= 2 or width <= 2 : # No interior if height/width is 1 or 2
             interior_region = np.array([]) # empty interior
        # else: # This logic seems redundant given the check for <=2 above. Simplified.
        #     interior_region = np.array([]) # Should not happen if is_uniform is True unless 1xN or Nx1 with H,W > 2? No, handled above.

        # Find the dominant color in the interior
        # If interior is empty (e.g., 2xN grid), dominant color doesn't matter as it won't be used.
        # Default to border color if interior is empty to avoid errors, though fill logic handles this.
        dominant_interior_color = find_dominant_color(interior_region) if interior_region.size > 0 else border_color

        # Create the output grid: Fill interior first
        output_grid_np.fill(dominant_interior_color)
        
        # Apply the border color to the perimeter
        if height > 0:
            output_grid_np[0, :] = border_color  # Top row
            if height > 1:
                output_grid_np[height - 1, :] = border_color # Bottom row
        if width > 0:
             output_grid_np[:, 0] = border_color  # Left column
             if width > 1:
                output_grid_np[:, width - 1] = border_color # Right column
                
    else:
        # Case 2: No uniform border
        
        # Find the dominant color across the entire grid
        overall_dominant_color = find_dominant_color(grid_np)
        
        # Fill the entire output grid with the overall dominant color
        output_grid_np.fill(overall_dominant_color)

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()
    
    return output_grid
