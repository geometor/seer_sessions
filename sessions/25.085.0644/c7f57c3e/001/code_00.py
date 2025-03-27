import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Identifies the two least frequent colors in the input grid (excluding the 
    most frequent color, assumed to be the background). Swaps all occurrences 
    of these two colors. If there are fewer than two non-background colors, 
    no changes are made.

    Args:
        input_grid (list of lists of int): The input grid.

    Returns:
        list of lists of int: The transformed grid.
    """
    
    # Convert input grid to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    
    # Flatten the array to count color frequencies
    flat_array = input_array.flatten()
    
    # Count the occurrences of each color
    color_counts = Counter(flat_array)
    
    # If there are fewer than 3 unique colors (background + 2 others), 
    # no swap is possible/needed
    if len(color_counts) < 3:
        return output_array.tolist()
        
    # Find the most frequent color (background)
    background_color = color_counts.most_common(1)[0][0]
    
    # Remove the background color from the counts
    del color_counts[background_color]

    # If there are fewer than 2 non-background colors after removing background,
    # no swap is possible/needed
    if len(color_counts) < 2:
         return output_array.tolist()

    # Sort the remaining colors by frequency (ascending)
    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1])
    
    # Identify the two least frequent colors
    color1, _ = sorted_colors[0]
    color2, _ = sorted_colors[1]
    
    # Iterate through the grid and swap the colors
    rows, cols = input_array.shape
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == color1:
                output_array[r, c] = color2
            elif input_array[r, c] == color2:
                output_array[r, c] = color1
                
    # Return the transformed grid as a list of lists
    return output_array.tolist()
