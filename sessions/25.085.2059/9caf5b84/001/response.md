```python
import numpy as np
from collections import Counter

"""
Identify the two most frequent colors in the input grid. These colors, and any others with the same frequency count as either of the top two, are considered 'special'. Create the output grid by iterating through the input grid. If a pixel's color is one of the 'special' colors, keep it the same. If a pixel's color is not 'special', change its color to orange (7).
"""

def find_special_colors(grid):
    """
    Finds the colors with the two highest frequencies in the grid.
    Includes colors tied for the first or second highest frequency.
    Handles cases with fewer than two unique colors.
    """
    # Flatten the grid to get a list of all pixel values
    pixels = grid.flatten()
    
    # Handle empty grid case
    if pixels.size == 0:
        return set()
        
    # Count occurrences of each color
    color_counts = Counter(pixels)
    
    # If no colors were found (e.g., empty counter from empty grid, though handled above)
    if not color_counts:
        return set()

    # Get unique frequency counts and sort them in descending order
    sorted_unique_counts = sorted(list(set(color_counts.values())), reverse=True)
    
    special_colors = set()
    
    # Determine the target frequencies (top one or top two)
    target_frequencies = set()
    if len(sorted_unique_counts) >= 1:
        target_frequencies.add(sorted_unique_counts[0]) # Add the highest frequency
    if len(sorted_unique_counts) >= 2:
        target_frequencies.add(sorted_unique_counts[1]) # Add the second highest frequency
        
    # Collect all colors that have these target frequencies
    for color, count in color_counts.items():
        if count in target_frequencies:
            special_colors.add(color)
            
    return special_colors

def transform(input_grid):
    """
    Transforms the input grid based on color frequency.
    Keeps the two most frequent colors (and ties) and changes others to orange (7).
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input grid
    if input_array.size == 0:
        return []
        
    # Find the set of 'special' colors (the two most frequent, including ties)
    special_colors = find_special_colors(input_array)
    
    # Create an output grid, initially as a copy of the input
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape
    
    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            current_color = input_array[r, c]
            
            # Check if the current color is NOT one of the special colors
            if current_color not in special_colors:
                # If it's not special, change its color to orange (7)
                output_array[r, c] = 7
                
    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid

```