import numpy as np
from collections import Counter

"""
The transformation identifies four quadrants in the input grid. It finds the dominant background color for each quadrant. 
It also identifies a single 'scatter' color that appears sparsely across the quadrants. 
The transformation counts the occurrences of the scatter color within each quadrant. 
The final output is the background color of the quadrant that contains the highest number of scatter pixels.
"""

def get_quadrants(grid):
    """Divides the grid into four equal quadrants."""
    rows, cols = grid.shape
    mid_row = rows // 2
    mid_col = cols // 2
    
    # Slicing to get the four quadrants
    top_left = grid[0:mid_row, 0:mid_col]
    top_right = grid[0:mid_row, mid_col:cols]
    bottom_left = grid[mid_row:rows, 0:mid_col]
    bottom_right = grid[mid_row:rows, mid_col:cols]
    
    return top_left, top_right, bottom_left, bottom_right

def get_most_frequent_color(arr):
    """Finds the most frequent color (pixel value) in a numpy array."""
    if arr.size == 0:
        return None # Handle empty quadrants if they ever occur
    counts = Counter(arr.flatten())
    # Return the color with the highest count
    return counts.most_common(1)[0][0]

def transform(input_grid):
    """
    Transforms the input grid according to the described logic.

    1. Divide the input grid into four equal quadrants.
    2. Identify the primary background color of each quadrant.
    3. Identify the single 'scatter' color.
    4. Count scatter pixels in each quadrant.
    5. Return the background color of the quadrant with the most scatter pixels.
    """
    
    # Convert input list of lists to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    
    # 1. Divide into quadrants
    quadrants = get_quadrants(grid)
    tl, tr, bl, br = quadrants
    
    # 2. Identify background colors
    bg_colors = []
    quadrant_list = [tl, tr, bl, br] # Keep order consistent
    for quad in quadrant_list:
        bg_colors.append(get_most_frequent_color(quad))
        
    # 3. Identify the scatter color
    all_colors = np.unique(grid)
    scatter_color = None
    for color in all_colors:
        # The scatter color is the one that is NOT a background color
        if color not in bg_colors:
            scatter_color = color
            break
            
    # Handle edge case where maybe all colors are background colors (unlikely based on examples)
    if scatter_color is None:
        # This case isn't represented in training data. 
        # If it happened, maybe default logic or error needed.
        # Based on examples, there's always one non-background color.
        # A possible fallback: if only one non-zero color exists besides backgrounds, use that.
        # Or, if multiple non-backgrounds, maybe the least frequent overall?
        # For now, assume the logic holds per examples.
         # Let's refine: the scatter color *must* appear in the grid. If a unique color isn't found
         # that isn't a background, something is wrong with the assumption or the data pattern.
         # We trust the examples pattern for now.
         pass 


    # 4. Count scatter pixels in each quadrant
    scatter_counts = []
    for quad in quadrant_list:
        count = np.count_nonzero(quad == scatter_color)
        scatter_counts.append(count)
        
    # 5. Find the max count and the corresponding background color
    max_count = -1
    output_color = -1 # Initialize with an invalid color
    
    # Iterate through quadrants, counts, and background colors simultaneously
    for i in range(len(quadrant_list)):
        count = scatter_counts[i]
        bg = bg_colors[i]
        if count > max_count:
            max_count = count
            output_color = bg
            
    # The output is just the single integer color value
    return output_color