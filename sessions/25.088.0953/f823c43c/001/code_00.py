import numpy as np
from collections import Counter

"""
Replace all pixels of the noise color (Magenta=6) with the most frequent 
'background' color found in the input grid (excluding the noise color itself).
"""

def find_background_color(grid, noise_color):
    """
    Finds the most frequent color in the grid, excluding the specified noise_color.
    
    Args:
        grid (np.array): The input grid.
        noise_color (int): The color value to exclude from frequency counting.

    Returns:
        int: The most frequent color value, excluding the noise_color. Returns -1 if
             only the noise color or no other colors are present.
    """
    # Flatten the grid to easily count all pixel values
    pixels = grid.flatten()
    
    # Count the frequency of each color
    color_counts = Counter(pixels)
    
    # Remove the noise color from the counts if it exists
    if noise_color in color_counts:
        del color_counts[noise_color]
        
    # Check if there are any other colors left
    if not color_counts:
        # Handle edge case where only the noise color was present or grid was empty
        # In the context of ARC, assuming a default background (like 0) might be an option,
        # but based *only* on the provided examples, returning an indicator like -1 is safer.
        # Or, we could default to the most frequent color *including* noise if no other exists.
        # Let's stick to the rule: exclude noise, find most frequent *other*. If none, problem.
        # Re-evaluating based on examples: It seems reasonable that if *only* noise exists,
        # replacing it with 0 (white/background) might be a default.
        # However, the problem description implies finding the *most frequent other* color.
        # Let's find the most frequent and return it. If the counter is empty, return 0 as a safe default.
         return 0 # Default to white if no other dominant color found

    # Find the color with the highest frequency
    background_color = color_counts.most_common(1)[0][0]
    
    return background_color

def transform(input_grid):
    """
    Replaces instances of a specific 'noise' color (6) with the most 
    frequent non-noise color in the grid.
    
    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    grid_np = np.array(input_grid, dtype=int)
    
    # Define the noise color to be replaced
    noise_color = 6
    
    # Find the most frequent color in the grid, excluding the noise color
    background_color = find_background_color(grid_np, noise_color)
    
    # Create a copy of the input grid to modify
    # This ensures the original input_grid is not changed
    output_grid_np = grid_np.copy()
    
    # Iterate through each pixel of the grid
    rows, cols = grid_np.shape
    for r in range(rows):
        for c in range(cols):
            # If the current pixel's color is the noise color
            if output_grid_np[r, c] == noise_color:
                # Replace it with the determined background color
                output_grid_np[r, c] = background_color
                
    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()
    
    return output_grid