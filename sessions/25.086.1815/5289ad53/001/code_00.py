"""
Determine the background color (most frequent). Identify contiguous horizontal
segments (objects) of non-background colors. Count the number of objects for each
unique non-background color. Sort these colors in descending order by their
numerical value. Create a 2x3 output grid initialized to white (0). Fill this
grid row by row, left to right, using the sorted colors. For each color, fill
a number of cells equal to its object count.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flat)
    # If there's a tie, np.argmax might not be deterministic, but in ARC it's usually clear.
    # A more robust approach might be needed if ties are common and meaningful.
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_horizontal_objects(grid, background_color):
    """
    Identifies horizontal segments of non-background colors and counts them by color.

    Returns:
        A dictionary mapping color -> count of segments.
    """
    rows, cols = grid.shape
    object_counts = Counter()

    for r in range(rows):
        current_color = -1 # Sentinel value different from any possible color
        in_segment = False
        for c in range(cols):
            pixel_color = grid[r, c]
            if pixel_color != background_color:
                if not in_segment:
                    # Start of a new segment
                    in_segment = True
                    current_color = pixel_color
                elif pixel_color != current_color:
                     # End of the previous segment (different color), start of a new one
                    object_counts[current_color] += 1
                    current_color = pixel_color
            elif in_segment:
                # End of the segment (hit background or end of row)
                object_counts[current_color] += 1
                in_segment = False
                current_color = -1
        
        # Handle segment ending at the edge of the grid
        if in_segment:
            object_counts[current_color] += 1
            
    return object_counts


def transform(input_grid):
    """
    Transforms the input grid based on counting horizontal segments of non-background colors.

    Args:
        input_grid (np.ndarray): The input 2D array representing the grid.

    Returns:
        np.ndarray: The transformed 2x3 output grid.
    """
    input_grid_np = np.array(input_grid)

    # 1. Determine the background color
    background_color = find_background_color(input_grid_np)

    # 2. Identify all horizontal line objects and count by color
    object_counts = find_horizontal_objects(input_grid_np, background_color)

    # 3. Get unique colors and sort them descending
    unique_colors = sorted(object_counts.keys(), reverse=True)

    # 4. Initialize a 2x3 output grid with white (0)
    output_grid = np.zeros((2, 3), dtype=int)
    
    # 5. Fill the output grid
    current_row, current_col = 0, 0
    for color in unique_colors:
        count = object_counts[color]
        for _ in range(count):
            if current_row < 2: # Check if we are within the bounds of the output grid
                output_grid[current_row, current_col] = color
                current_col += 1
                if current_col >= 3:
                    current_col = 0
                    current_row += 1
            else:
                # Stop filling if we exceed the 2x3 grid size
                break 
        if current_row >= 2:
            break # Stop if grid is full

    return output_grid.tolist() # Return as list of lists per spec