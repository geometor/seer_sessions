import numpy as np
from collections import Counter

"""
Transforms an input grid by drawing concentric square/rectangular layers centered on the grid. The color of each layer is determined by the color of a non-background pixel from the input grid. The layers are ordered based on the corresponding input pixel's Manhattan distance from the grid center.

1. Analyze Input: Determine dimensions (H, W) and identify the most frequent color as input_background_color.
2. Identify Pixels: Locate all non-background pixels, recording their color, row (r), and column (c).
3. Calculate Center: Find center coordinates: center_r = (H - 1) // 2, center_c = (W - 1) // 2.
4. Calculate Distances: Compute Manhattan distance from each non-background pixel to the center.
5. Sort Pixels: Sort non-background pixels based on:
    a. Manhattan distance (ascending).
    b. Original row index (descending).
    c. Original column index (descending).
   Let the sorted list be sorted_pixels with n pixels.
6. Determine Output Background: The color of the last pixel (index n-1) in sorted_pixels.
7. Initialize Output Grid: Create an H x W grid filled with the output_background_color.
8. Draw Concentric Layers: Iterate through sorted_pixels from index i = n - 2 down to 0.
    a. Get color C_i from sorted_pixels[i].
    b. Define layer boundaries: min/max row/col = center +/- i.
    c. Fill the region within these boundaries in the output grid with C_i, overwriting previous colors. Clip to grid dimensions.
9. Return Output: The final grid.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default for empty grid
    # Find the color with the highest count
    background_color = counts.most_common(1)[0][0]
    return background_color

def get_non_background_pixels(grid, background_color):
    """Finds all pixels that are not the background color."""
    pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color:
                pixels.append({'color': color, 'r': r, 'c': c})
    return pixels

def calculate_center(height, width):
    """Calculates the center coordinates of the grid."""
    # Note: uses integer division for potentially even dimensions
    center_r = (height - 1) // 2
    center_c = (width - 1) // 2
    return center_r, center_c

def calculate_manhattan_distance(r1, c1, r2, c2):
    """Calculates the Manhattan distance between two points."""
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid):
    """Applies the transformation logic to the input grid."""
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Analyze Input: Find background color
    background_color = find_background_color(input_grid_np)

    # 2. Identify Pixels: Get non-background pixels
    non_bg_pixels_info = get_non_background_pixels(input_grid_np, background_color)

    # Handle case with no non-background pixels (return grid filled with input background)
    if not non_bg_pixels_info:
        output_grid = np.full((height, width), background_color, dtype=int)
        return output_grid.tolist()

    # 3. Calculate Center
    center_r, center_c = calculate_center(height, width)

    # 4. Calculate Distances
    pixels_with_dist = []
    for pixel in non_bg_pixels_info:
        dist = calculate_manhattan_distance(pixel['r'], pixel['c'], center_r, center_c)
        pixels_with_dist.append({
            'color': pixel['color'],
            'dist': dist,
            'r': pixel['r'],
            'c': pixel['c']
        })

    # 5. Sort Pixels: distance (asc), row (desc), column (desc)
    # Use negative row/col for descending sort order with tuple sorting
    sorted_pixels = sorted(pixels_with_dist, key=lambda p: (p['dist'], -p['r'], -p['c']))

    num_layers = len(sorted_pixels)

    # 6. Determine Output Background: color of the furthest pixel (last in sorted list)
    output_background_color = sorted_pixels[num_layers - 1]['color']

    # 7. Initialize Output Grid: Fill with the determined background color
    output_grid = np.full((height, width), output_background_color, dtype=int)

    # Handle case with only one non-background pixel (already handled by background fill)
    if num_layers <= 1:
        return output_grid.tolist()

    # 8. Draw Concentric Layers: Iterate from second-furthest (n-2) down to closest (0)
    # The index 'i' corresponds to the distance rank and also the layer size extension
    for i in range(num_layers - 2, -1, -1):
        color_to_draw = sorted_pixels[i]['color']

        # Calculate layer boundaries for layer 'i'
        # The layer size is effectively (2*i + 1) x (2*i + 1) centered
        min_r = center_r - i
        max_r = center_r + i
        min_c = center_c - i
        max_c = center_c + i

        # Clip boundaries to the grid dimensions
        # Using max(0, ...) and min(dim-1, ...) ensures indices are valid
        start_row = max(0, min_r)
        end_row = min(height - 1, max_r)
        start_col = max(0, min_c)
        end_col = min(width - 1, max_c)

        # Fill the layer using numpy slicing (inclusive end index needed for slicing)
        # Check if the calculated bounds are valid before slicing
        if start_row <= end_row and start_col <= end_col:
             output_grid[start_row : end_row + 1, start_col : end_col + 1] = color_to_draw

    # 9. Return Output: Convert back to list of lists
    return output_grid.tolist()