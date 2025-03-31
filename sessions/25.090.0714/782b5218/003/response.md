```python
import numpy as np
from collections import Counter

def find_fill_color(grid_np):
    """
    Finds the most frequent color in the grid, excluding white (0) and red (2).
    Returns the color value or None if no such color exists.
    Handles ties by returning one of the most frequent.
    """
    # Flatten the grid to easily count colors
    flat_grid = grid_np.flatten()
    
    # Filter out white (0) and red (2)
    filtered_colors = [color for color in flat_grid if color != 0 and color != 2]
    
    # Count frequencies
    if not filtered_colors:
        # If only 0s and 2s exist, default behavior might need clarification,
        # but based on examples, there's always another dominant color.
        # Returning 0 (white) as a fallback might be safe if needed.
        return 0 
        
    color_counts = Counter(filtered_colors)
    
    # Find the most common color
    dominant_color, _ = color_counts.most_common(1)[0]
    
    return dominant_color

def transform(input_grid):
    """
    Processes a grid column-wise based on the highest red pixel (2).
    1. Determines the most frequent color excluding white (0) and red (2) ('fill_color').
    2. For each column:
       - Finds the highest red pixel's row ('r_red').
       - If no red pixel, the output column is white (0).
       - If a red pixel exists:
         - Pixels above 'r_red' in the output are white (0).
         - Pixels at or below 'r_red' in the output are red (2) if the corresponding input pixel is red (2),
           otherwise they are set to the 'fill_color'.
    """
    # Convert input list of lists to a numpy array
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize the output grid with white (0)
    output_np = np.zeros_like(input_np)
    
    # Step 1: Find the global fill color
    fill_color = find_fill_color(input_np)
    
    # Step 2 & 3: Process each column
    for c in range(width):
        column = input_np[:, c]
        
        # Find the indices of red pixels (color 2) in the current column
        red_indices = np.where(column == 2)[0]
        
        # Step 3a: Handle No Red Case - output column remains white (already initialized)
        if len(red_indices) == 0:
            continue
            
        # Step 3b: Handle Red Found Case
        # Find the highest red pixel (minimum row index)
        r_red = np.min(red_indices)
        
        # Fill Above: Output rows 0 to r_red-1 are already white (0) from initialization.
        
        # Fill At and Below: Iterate from r_red down to the bottom
        for r in range(r_red, height):
            # Check the input pixel color at this position
            if input_np[r, c] == 2:
                # If input is red, output is red
                output_np[r, c] = 2
            else:
                # Otherwise, output is the determined fill_color
                output_np[r, c] = fill_color
                
    # Convert the numpy array back to a list of lists for the final output
    return output_np.tolist()

```