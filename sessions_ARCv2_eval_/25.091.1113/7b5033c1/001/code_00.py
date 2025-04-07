import numpy as np
from collections import Counter

def find_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    flat_grid = grid.flatten()
    counts = Counter(flat_grid)
    background_color = counts.most_common(1)[0][0]
    return background_color

def scan_and_order_colors(grid, background_color):
    """
    Scans the grid row-by-row, left-to-right to find non-background colors.
    Returns a list of unique colors in the order they were first encountered
    and a dictionary mapping each color to its total count.
    """
    ordered_colors = []
    color_counts = Counter()
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != background_color:
                # Add to ordered list if it's the first time seeing this color
                if color not in ordered_colors:
                    ordered_colors.append(color)
                # Increment the count for this color
                color_counts[color] += 1
                
    return ordered_colors, color_counts

def transform(input_grid_list):
    """
    Transforms an input grid according to the following rules:
    1. Identifies the most frequent color as the background.
    2. Scans the grid top-to-bottom, left-to-right to find the order of first appearance of non-background colors.
    3. Counts the occurrences of each non-background color.
    4. Creates a single-column output grid containing all non-background pixels,
       grouped by color, with the groups ordered according to their first appearance in the scan.
    """
    input_grid = np.array(input_grid_list)
    
    # 1. Identify the background color
    background_color = find_background_color(input_grid)
    
    # 2. Scan grid to find the order of first appearance of non-background colors
    #    and count the total occurrences of each non-background color.
    ordered_colors, color_counts = scan_and_order_colors(input_grid, background_color)
    
    # 3. Construct the output list of pixels
    output_pixels = []
    for color in ordered_colors:
        count = color_counts[color]
        output_pixels.extend([color] * count)
        
    # 4. Format the output as a single-column grid (Nx1 numpy array)
    if not output_pixels: # Handle case where input has only background color
        output_grid = np.empty((0, 1), dtype=int)
    else:
        output_grid = np.array(output_pixels).reshape(-1, 1)
        
    return output_grid.tolist() # Convert back to list of lists for consistency with ARC format if needed
