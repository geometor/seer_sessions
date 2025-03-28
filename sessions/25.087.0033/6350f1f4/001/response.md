```python
import numpy as np
from collections import Counter

def find_most_frequent_color(grid_np):
    """
    Finds the most frequent non-white color in the grid.
    If there's a tie in frequency, returns the color with the highest numerical value.
    """
    # Flatten the grid and filter out white (0) pixels
    non_white_pixels = grid_np[grid_np != 0]

    if non_white_pixels.size == 0:
        # Handle cases where the grid is all white or empty
        return None 

    # Count frequencies of non-white colors
    color_counts = Counter(non_white_pixels)

    if not color_counts:
        # Should not happen if non_white_pixels is not empty, but for safety
        return None

    # Find the maximum frequency
    max_freq = 0
    for color in color_counts:
        if color_counts[color] > max_freq:
            max_freq = color_counts[color]

    # Find all colors with the maximum frequency
    most_frequent_colors = []
    for color in color_counts:
        if color_counts[color] == max_freq:
            most_frequent_colors.append(color)
            
    # If there's a tie, choose the color with the highest numerical value
    target_color = max(most_frequent_colors)
    
    return target_color

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Find the most frequent non-white color in the input grid. If there is a tie in frequency, 
       select the color with the highest numerical value among the tied colors. This is the 'target_color'.
    2. Create the output grid by copying the input grid.
    3. Iterate through each pixel of the output grid.
    4. If a pixel's color is not white (0) and not the 'target_color', change its color to the 'target_color'.
    5. White (0) pixels and pixels already having the 'target_color' remain unchanged.
    """
    
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the target color based on frequency and value
    target_color = find_most_frequent_color(input_np)
    
    # If no non-white pixels were found, return the original grid
    if target_color is None:
        return input_grid

    # Create a copy of the input grid to modify
    output_np = np.copy(input_np)
    
    # Get grid dimensions
    height, width = output_np.shape
    
    # Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            current_color = output_np[r, c]
            # Check if the color is not white and not the target color
            if current_color != 0 and current_color != target_color:
                # Change the color to the target color
                output_np[r, c] = target_color
                
    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid

```