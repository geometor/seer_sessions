```python
"""
Identify the background color (azure, 8). Find all pixels in the input grid 
that are not the background color. Determine their common color. Based on this 
color, apply a specific translation (movement) to each non-background pixel.
The translation rules are:
- Blue (1) moves 1 pixel right (0, 1).
- Red (2) moves 2 pixels left (0, -2).
- Orange (7) moves 2 pixels up (-2, 0).
- Maroon (9) moves 2 pixels down (2, 0).
The original positions of the moved pixels are replaced with the background color.
"""

import numpy as np

# Define the mapping from color to movement vector (delta_row, delta_col)
COLOR_TO_VECTOR = {
    1: (0, 1),   # Blue: Right 1
    2: (0, -2),  # Red: Left 2
    7: (-2, 0),  # Orange: Up 2
    9: (2, 0)    # Maroon: Down 2
}

# Define the assumed background color
BACKGROUND_COLOR = 8

def find_foreground_pixels(grid, background_color):
    """Finds all pixels that are not the background color."""
    foreground_pixels = []
    foreground_color = None
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != background_color:
                foreground_pixels.append(((r, c), grid[r, c]))
                if foreground_color is None:
                    foreground_color = grid[r, c]
                elif foreground_color != grid[r, c]:
                    # This case should ideally not happen based on examples, 
                    # but good to handle potential inconsistencies.
                    # For now, we assume all foreground pixels have the same color.
                    pass 
    return foreground_pixels, foreground_color

def transform(input_grid):
    """
    Applies a color-dependent translation to non-background pixels.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Find the foreground pixels and their color
    foreground_pixels, color = find_foreground_pixels(input_np, BACKGROUND_COLOR)
    
    # If no foreground pixels are found, or the color is not in our map, return the original grid
    if not foreground_pixels or color not in COLOR_TO_VECTOR:
        return output_grid.tolist() # Return as list of lists
        
    # Get the movement vector based on the color
    delta_r, delta_c = COLOR_TO_VECTOR[color]
    
    # First, clear the original positions of foreground pixels
    for (r, c), _ in foreground_pixels:
        # Check bounds just in case, although original positions are always valid
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            output_grid[r, c] = BACKGROUND_COLOR
            
    # Then, apply the transformation and set the new positions
    for (r, c), pixel_color in foreground_pixels:
        new_r, new_c = r + delta_r, c + delta_c
        
        # Check if the new position is within the grid boundaries
        if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
            output_grid[new_r, new_c] = pixel_color
            
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```