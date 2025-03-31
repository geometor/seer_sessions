import numpy as np
from collections import Counter

def find_most_frequent_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # Find the color with the maximum count
    most_common = counts.most_common(1)
    if most_common:
        return most_common[0][0]
    return 0 # Default if grid is empty or uniform

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels with the given color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def calculate_centroid(pixels):
    """Calculates the centroid (average row, col) of a list of pixel coordinates."""
    if not pixels:
        return None # Or handle as needed, e.g., return grid center
    avg_row = sum(r for r, c in pixels) / len(pixels)
    avg_col = sum(c for r, c in pixels) / len(pixels)
    return avg_row, avg_col

def find_unique_non_bg_non_white_pixel(grid, background_color):
    """Finds the single pixel that is not the background color and not white (0)."""
    height, width = grid.shape
    source_pixel = None
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color and color != 0:
                # Assuming there's only one such pixel based on examples
                source_pixel = ((r, c), color)
                break
        if source_pixel:
            break
    return source_pixel # Returns ((row, col), color) or None

def transform(input_grid):
    """
    Generates a diagonal trail extending downwards from a specific source pixel.
    The trail's color matches the source pixel.
    The trail direction (down-left or down-right) is determined by the source 
    pixel's horizontal position relative to the centroid of the white (0) pixels.
    If the source pixel is left of the white centroid, the trail goes down-left.
    Otherwise (right of or aligned with the centroid), it goes down-right.
    The trail stops when it hits the bottom edge of the grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 1. Identify the background color
    background_color = find_most_frequent_color(output_grid)

    # 2. Find white pixels and calculate centroid
    white_pixels = find_pixels_by_color(output_grid, 0)
    white_centroid = calculate_centroid(white_pixels)
    
    # Handle case where there are no white pixels (use grid center as fallback?)
    # For now, assume white pixels exist based on examples. If not, white_centroid will be None.

    # 3. Find the source pixel (not background, not white)
    source_info = find_unique_non_bg_non_white_pixel(output_grid, background_color)

    # If no source pixel or no white pixels found, return the original grid
    if not source_info or white_centroid is None:
        print("Warning: Could not find source pixel or white pixels. Returning original grid.")
        return output_grid 

    (source_row, source_col), source_color = source_info
    white_centroid_row, white_centroid_col = white_centroid

    # 4. Determine the trail direction
    delta_row = 1  # Always moves down
    if source_col < white_centroid_col:
        delta_col = -1 # Move down-left
    else:
        delta_col = 1  # Move down-right

    # 5. Generate the trail
    current_row = source_row + delta_row
    current_col = source_col + delta_col

    while 0 <= current_row < height:
        # Check column bounds before drawing
        if 0 <= current_col < width:
            output_grid[current_row, current_col] = source_color
        
        # Update position for the next step
        current_row += delta_row
        current_col += delta_col
        
        # Optional: Break if column goes out of bounds (though loop condition handles row)
        if not (0 <= current_col < width):
             break # Added for clarity, loop condition on row handles termination eventually

    return output_grid