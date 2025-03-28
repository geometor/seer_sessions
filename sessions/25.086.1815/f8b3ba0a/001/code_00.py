import numpy as np
from collections import Counter

"""
The transformation identifies all 2x1 horizontal rectangles of non-white colors in the input grid. 
It counts the occurrences of each color represented by these rectangles. 
It then filters out the color(s) that appear most frequently. 
The remaining colors are sorted first by their frequency count (descending) and then by the row index 
of their last (bottom-most) appearance in the grid (descending). 
The final output is a column vector containing these sorted colors.
"""

def find_rectangles(grid):
    """
    Finds all 2x1 horizontal rectangles of non-white colors.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (color, row, col) 
              representing a found rectangle and its top-left corner.
    """
    rectangles = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width - 1):
            # Check for a non-white pixel
            if grid[r, c] != 0:
                # Check if the pixel to the right has the same color
                if grid[r, c] == grid[r, c + 1]:
                    # Check if this is the start of the rectangle (prev pixel is different or edge)
                    is_start = (c == 0 or grid[r, c-1] != grid[r, c])
                    # Check if this is the end of the rectangle (next pixel is different or edge)
                    is_end = (c + 1 == width - 1 or grid[r, c+2] != grid[r, c])
                    
                    # Ensure it's exactly a 2x1 rectangle horizontally
                    if is_start and is_end:
                        rectangles.append((grid[r, c], r, c))
    return rectangles

def transform(input_grid):
    """
    Transforms the input grid based on the frequency and position of 2x1 rectangles.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        np.array: A column vector (Nx1 NumPy array) containing the sorted colors.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Scan the input grid to identify all 2x1 horizontal rectangles
    rectangles = find_rectangles(grid)

    if not rectangles:
        # Handle cases with no rectangles found
        return np.array([]).reshape(0, 1)

    # 2. Count occurrences and find the last row for each color
    color_counts = Counter()
    last_rows = {}
    for color, r, c in rectangles:
        color_counts[color] += 1
        last_rows[color] = max(last_rows.get(color, -1), r)

    if not color_counts:
         # Should not happen if rectangles is not empty, but good practice
        return np.array([]).reshape(0, 1)
        
    # 3. Find the color(s) with the highest count
    max_count = 0
    if color_counts:
      max_count = max(color_counts.values())
      
    most_frequent_colors = {color for color, count in color_counts.items() if count == max_count}

    # 4. Create a candidate list excluding the most frequent color(s)
    candidate_data = []
    for color, count in color_counts.items():
        if color not in most_frequent_colors:
            candidate_data.append({
                'color': color,
                'count': count,
                'last_row': last_rows[color]
            })
            
    if not candidate_data:
        # Handle cases where only one color exists or all remaining colors were most frequent
         return np.array([]).reshape(0, 1)

    # 6. Sort the candidate list
    # Primary key: count (descending), Secondary key: last_row (descending)
    sorted_candidates = sorted(
        candidate_data,
        key=lambda item: (-item['count'], -item['last_row'])
    )

    # 7. Construct the output
    sorted_colors = [item['color'] for item in sorted_candidates]
    output_grid = np.array(sorted_colors).reshape(-1, 1)

    return output_grid