"""
Transforms the input grid based on color frequency. 
1. Calculate the frequency of each color in the input grid.
2. Identify the highest frequency count (`max_freq`).
3. If more than one color shares this `max_freq`, these tied colors are the 'special' colors to keep.
4. If only one color has the `max_freq`:
    a. Identify the second highest frequency count (`second_max_freq`).
    b. The 'special' colors are the unique color with `max_freq` and all colors sharing `second_max_freq`.
5. Iterate through the input grid. If a pixel's color is 'special', keep it. Otherwise, change it to orange (7).
"""

import numpy as np
from collections import Counter

def find_special_colors_revised(grid):
    """
    Finds the 'special' colors to keep based on the revised frequency rules.
    Handles ties for the highest frequency differently.
    """
    # Flatten the grid to get a list of all pixel values
    pixels = grid.flatten()
    
    # Handle empty grid case
    if pixels.size == 0:
        return set()
        
    # Count occurrences of each color
    color_counts = Counter(pixels)
    
    # If no colors were found (e.g., empty counter from empty grid)
    if not color_counts:
        return set()

    # Sort colors by frequency in descending order
    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)

    # If there are no colors after sorting (should not happen if color_counts is not empty)
    if not sorted_colors:
        return set()

    # Find the highest frequency
    max_freq = sorted_colors[0][1]
    
    # Find all colors with the highest frequency
    colors_with_max_freq = {color for color, count in color_counts.items() if count == max_freq}
    
    special_colors = set()

    # Check if there's a tie for the highest frequency
    if len(colors_with_max_freq) > 1:
        # Rule 3: Keep only colors tied for the highest frequency
        special_colors = colors_with_max_freq
    else:
        # Rule 4: Unique highest frequency color. Keep it.
        unique_max_freq_color = sorted_colors[0][0]
        special_colors.add(unique_max_freq_color)
        
        # Find the second highest frequency
        second_max_freq = 0
        # Iterate through the sorted list starting from the second element
        for i in range(1, len(sorted_colors)):
            current_freq = sorted_colors[i][1]
            # Find the first frequency that is lower than max_freq
            if current_freq < max_freq:
                second_max_freq = current_freq
                break # Found the second highest frequency value
        
        # If a second highest frequency exists (i.e., there are other colors)
        if second_max_freq > 0:
            # Find all colors with the second highest frequency
            colors_with_second_max_freq = {color for color, count in color_counts.items() if count == second_max_freq}
            # Add them to the special colors
            special_colors.update(colors_with_second_max_freq)
            
    return special_colors


def transform(input_grid):
    """
    Transforms the input grid based on the revised color frequency rules.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input grid
    if input_array.size == 0:
        return []
        
    # Find the set of 'special' colors based on the revised logic
    special_colors = find_special_colors_revised(input_array)
    
    # Create an output grid, initially as a copy of the input
    output_array = np.copy(input_array)
    
    # Define the replacement color
    replacement_color = 7 # Orange
    
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
                output_array[r, c] = replacement_color
                
    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
