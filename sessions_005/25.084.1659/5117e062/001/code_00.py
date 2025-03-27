"""
Locate the single azure (8) pixel in the input grid.
Extract the 3x3 neighborhood centered on this azure pixel.
Identify the most frequent color within this 3x3 neighborhood, excluding white (0) and azure (8). This is the replacement color.
Create a 3x3 output grid by copying the extracted neighborhood, but replace the central pixel (which was originally azure) with the identified replacement color.
"""

import numpy as np
from collections import Counter

def find_pixel(grid, color):
  """Finds the first occurrence of a pixel with the given color."""
  coords = np.where(grid == color)
  if len(coords[0]) > 0:
    return coords[0][0], coords[1][0] # Return row, col of the first match
  return None

def extract_subgrid(grid, center_row, center_col, size):
  """Extracts a square subgrid of given size centered at (center_row, center_col)."""
  half_size = size // 2
  start_row = center_row - half_size
  end_row = center_row + half_size + 1
  start_col = center_col - half_size
  end_col = center_col + half_size + 1
  
  # Assuming center is always valid and subgrid fits within grid based on examples
  # Add boundary checks if necessary for more general cases
  return grid[start_row:end_row, start_col:end_col]

def find_dominant_color(subgrid, exclude_colors):
    """Finds the most frequent color in the subgrid, excluding specified colors."""
    pixels = []
    for r in range(subgrid.shape[0]):
        for c in range(subgrid.shape[1]):
            pixel = subgrid[r, c]
            if pixel not in exclude_colors:
                pixels.append(pixel)

    if not pixels:
        # Handle cases where only excluded colors are present (though not seen in examples)
        # Perhaps return a default or raise an error. For now, assume valid input.
        # Let's return white (0) as a fallback, although the task implies a non-excluded color will exist.
        return 0 
        
    count = Counter(pixels)
    # Find the color with the highest count
    dominant_color = count.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid based on the azure pixel neighborhood rule.
    """
    input_grid_np = np.array(input_grid)
    
    # 1. Scan the input grid to find the coordinates (r, c) of the single azure (8) pixel.
    azure_coords = find_pixel(input_grid_np, 8)
    if azure_coords is None:
        # Handle case where azure pixel is not found (error or default)
        # Based on task description, it should always exist.
        raise ValueError("Azure pixel (8) not found in the input grid.")
    center_row, center_col = azure_coords

    # 2. Define and extract the 3x3 area centered at (r, c).
    neighborhood_size = 3
    neighborhood = extract_subgrid(input_grid_np, center_row, center_col, neighborhood_size)

    # 3. Identify the dominant non-white, non-azure color in the neighborhood.
    exclude = {0, 8} # Colors to exclude: white and azure
    replacement_color = find_dominant_color(neighborhood, exclude)

    # 4. Create the 3x3 output grid.
    # 5. Copy the neighborhood, replacing the center with the replacement_color.
    output_grid = neighborhood.copy()
    center_of_output = neighborhood_size // 2
    output_grid[center_of_output, center_of_output] = replacement_color

    return output_grid.tolist() # Return as list of lists per ARC standard