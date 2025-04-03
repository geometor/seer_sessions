import collections
import copy

"""
Transforms the input grid by identifying the most frequent non-white color (dominant color) 
and replacing any pixel that is neither white (0) nor the dominant color with the dominant color. 
White pixels remain unchanged.
"""

def transform(input_grid):
    """
    Applies the color replacement transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    # 1. Analyze the input grid to determine the frequency of each color, excluding white (0).
    color_counts = collections.Counter()
    rows = len(input_grid)
    if rows == 0:
        return [] # Handle empty grid
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)] # Handle grid with empty rows

    for r in range(rows):
        for c in range(cols):
            color = input_grid[r][c]
            if color != 0:  # Exclude white
                color_counts[color] += 1

    # 2. Identify the color with the highest frequency (the 'dominant color').
    dominant_color = None
    if color_counts: # Check if there are any non-white colors
        # most_common returns a list of (element, count) tuples, sorted by count
        dominant_color = color_counts.most_common(1)[0][0]
    # If color_counts is empty (grid is all white or empty), dominant_color remains None.
    # The modification loop below will handle this correctly (no changes needed).

    # 3. Create a copy of the input grid to serve as the output grid.
    output_grid = copy.deepcopy(input_grid)

    # 4. Iterate through each pixel (cell) of the input grid.
    for r in range(rows):
        for c in range(cols):
            current_color = input_grid[r][c]

            # 5. Check if the pixel's color is different from both white (0) 
            #    and the identified dominant color.
            # 6. If the condition is met, change the corresponding pixel in the output grid 
            #    to the dominant color.
            if dominant_color is not None and current_color != 0 and current_color != dominant_color:
                 output_grid[r][c] = dominant_color
            # 7. Otherwise (pixel is white or the dominant color, or grid was all white), 
            #    the pixel in the output grid remains unchanged (due to the initial deepcopy).

    # 8. Return the modified output grid.
    return output_grid