import numpy as np
from collections import Counter

"""
The transformation identifies a specific color from the input grid based on the presence and uniqueness of solid or mono-color horizontal and vertical lines.

The rules are applied in a specific order:

1.  **Solid Horizontal Line Uniqueness:** If exactly one color forms a solid horizontal line (a row containing only that non-white color) exactly once, that color is the output.
2.  **Solid Vertical Line Uniqueness:** If Rule 1 doesn't apply, and exactly one color forms a solid vertical line (a column containing only that non-white color) exactly once, that color is the output.
3.  **Single Solid Horizontal Color:** If Rules 1 & 2 don't apply, and only one distinct color forms *any* solid horizontal lines (even if multiple lines of that color exist), that color is the output.
4.  **Single Solid Vertical Color:** If Rules 1-3 don't apply, and only one distinct color forms *any* solid vertical lines (even if multiple lines of that color exist), that color is the output.
5.  **Mono-color Vertical Line Uniqueness:** If Rules 1-4 don't apply, and exactly one color forms a mono-color vertical line (a column where all non-white pixels are of that same color) exactly once, that color is the output.
6.  **Mono-color Horizontal Line Uniqueness:** If Rules 1-5 don't apply, and exactly one color forms a mono-color horizontal line (a row where all non-white pixels are of that same color) exactly once, that color is the output.

The output is a 1x1 grid containing the selected color.
"""

def is_solid_line(line, color):
    """Checks if a 1D array 'line' consists entirely of the given non-white 'color'."""
    if color == 0:  # White is the background, not a solid line color
        return False
    return np.all(line == color)

def get_mono_color(line):
    """
    Finds the single non-white color in a line, if one exists.
    Returns the color if the line is mono-color (ignoring white), otherwise None.
    Returns None if the line is all white.
    """
    non_white_pixels = line[line != 0]
    if non_white_pixels.size == 0:
        return None  # All white
    unique_colors = np.unique(non_white_pixels)
    if len(unique_colors) == 1:
        return unique_colors[0]
    return None # Mixed non-white colors

def transform(input_grid):
    """
    Applies the transformation rules to find the output color.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    solid_h_colors = []
    solid_v_colors = []
    mono_h_colors = []
    mono_v_colors = []

    # --- Step 1 & 3: Analyze Rows ---
    for r in range(height):
        row = grid[r, :]
        # Check for solid horizontal lines
        unique_in_row = np.unique(row)
        if len(unique_in_row) == 1 and unique_in_row[0] != 0:
             solid_h_colors.append(unique_in_row[0])
             
        # Check for mono-color horizontal lines
        mono_color = get_mono_color(row)
        if mono_color is not None:
            mono_h_colors.append(mono_color)


    # --- Step 2 & 4: Analyze Columns ---
    for c in range(width):
        col = grid[:, c]
        # Check for solid vertical lines
        unique_in_col = np.unique(col)
        if len(unique_in_col) == 1 and unique_in_col[0] != 0:
             solid_v_colors.append(unique_in_col[0])

        # Check for mono-color vertical lines
        mono_color = get_mono_color(col)
        if mono_color is not None:
            mono_v_colors.append(mono_color)

    # --- Apply Rules ---

    # Rule 1: Unique Solid H Color (appears exactly once)
    solid_h_counts = Counter(solid_h_colors)
    unique_solid_h = [color for color, count in solid_h_counts.items() if count == 1]
    if len(unique_solid_h) == 1:
        return np.array([[unique_solid_h[0]]], dtype=int)

    # Rule 2: Unique Solid V Color (appears exactly once)
    solid_v_counts = Counter(solid_v_colors)
    unique_solid_v = [color for color, count in solid_v_counts.items() if count == 1]
    if len(unique_solid_v) == 1:
        return np.array([[unique_solid_v[0]]], dtype=int)

    # Rule 3: Single distinct Solid H Color (even if multiple lines)
    distinct_solid_h = set(solid_h_colors)
    if len(distinct_solid_h) == 1:
        return np.array([[list(distinct_solid_h)[0]]], dtype=int)

    # Rule 4: Single distinct Solid V Color (even if multiple lines)
    distinct_solid_v = set(solid_v_colors)
    if len(distinct_solid_v) == 1:
        return np.array([[list(distinct_solid_v)[0]]], dtype=int)
        
    # Rule 5: Unique Mono V Color (appears exactly once)
    mono_v_counts = Counter(mono_v_colors)
    unique_mono_v = [color for color, count in mono_v_counts.items() if count == 1]
    if len(unique_mono_v) == 1:
         return np.array([[unique_mono_v[0]]], dtype=int)

    # Rule 6: Unique Mono H Color (appears exactly once)
    mono_h_counts = Counter(mono_h_colors)
    unique_mono_h = [color for color, count in mono_h_counts.items() if count == 1]
    if len(unique_mono_h) == 1:
        return np.array([[unique_mono_h[0]]], dtype=int)


    # Fallback or error case if none of the rules match (though examples suggest one always will)
    # Based on examples, this part shouldn't be reached. 
    # If it were, returning a default like 0 or raising an error might be appropriate.
    # Let's assume one rule must match based on the task structure.
    # For safety, let's return the most frequent mono vertical color if absolutely nothing else matches
    # or just the first one found if frequencies are equal. This is a guess.
    if mono_v_colors:
         most_common_v = mono_v_counts.most_common(1)
         if most_common_v:
              return np.array([[most_common_v[0][0]]], dtype=int)
    if mono_h_colors:
         most_common_h = mono_h_counts.most_common(1)
         if most_common_h:
              return np.array([[most_common_h[0][0]]], dtype=int)
              
    # Absolute last resort
    return np.array([[0]], dtype=int) # Default to white if truly nothing found

