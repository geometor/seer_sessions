import numpy as np

"""
Transform the input grid based on a rule defined by a 5x5 key region in the top-left corner.

1.  Isolate the 5x5 key region (rows 0-4, columns 0-4) and the source region (all rows, columns 6 onwards).
2.  Identify the two distinct non-white colors (C1, C2) in the central 3x3 area of the key region (`key_region[1:4, 1:4]`).
3.  Determine the target color (T) to be replaced in the source region based on the pair {C1, C2}:
    - {yellow(4), orange(7)} -> target green(3)
    - {blue(1), red(2)} -> target azure(8)
    - {green(3), azure(8)} -> target gray(5)
4.  Generate a 3x3 replacement pattern by swapping C1 and C2 within the central 3x3 key pattern source. Other colors remain unchanged.
5.  Determine the background fill color for the output grid based on the key colors and the unique non-target colors in the source region:
    - If key colors are {blue(1), red(2)}, the background fill color is azure (8).
    - Otherwise, find unique colors in the source region excluding the target color (T).
        - If exactly one unique non-target color exists, use that color as the background fill.
        - If zero or multiple unique non-target colors exist, use gray (5) as the background fill.
6.  Initialize the output grid with the same dimensions as the source region, filled with the determined background fill color.
7.  Iterate through the source region. For every pixel that matches the target color (T), update the corresponding pixel in the output grid using the replacement pattern, tiled using modulo 3 indexing (row % 3, col % 3).
"""

def find_key_colors(key_pattern_source):
    """Finds the two distinct non-white colors in the 3x3 key pattern source."""
    # Find unique colors in the 3x3 pattern
    unique_colors = np.unique(key_pattern_source)
    # Filter out white (0)
    non_white_colors = unique_colors[unique_colors != 0] 
    # Expect exactly two non-white colors based on examples
    if len(non_white_colors) != 2:
        raise ValueError(f"Expected 2 non-white key colors, found {len(non_white_colors)}: {non_white_colors}")
    # Sort for consistent order when mapping
    return tuple(sorted(non_white_colors))

def determine_target_color(key_colors_tuple):
    """Determines the target color based on the pair of key colors."""
    # Predefined mapping from key color pairs to target colors
    mapping = {
        (4, 7): 3,  # yellow, orange -> green
        (1, 2): 8,  # blue, red -> azure
        (3, 8): 5   # green, azure -> gray
    }
    if key_colors_tuple not in mapping:
        raise ValueError(f"Unknown key color combination: {key_colors_tuple}")
    return mapping[key_colors_tuple]

def generate_replacement_pattern(key_pattern_source, color1, color2):
    """Generates the 3x3 replacement pattern by swapping color1 and color2."""
    # Create a copy of the 3x3 key pattern
    pattern = np.copy(key_pattern_source)
    # Swap the two key colors within the pattern
    pattern[key_pattern_source == color1] = color2
    pattern[key_pattern_source == color2] = color1
    return pattern

def determine_background_color(source_region, target_color, key_colors_tuple):
    """Determines the background fill color for the output grid."""
    # Special case for key colors blue(1) and red(2)
    if key_colors_tuple == (1, 2):
        return 8 # Background is always azure(8)

    # General case: analyze unique colors in the source region
    unique_source_colors = np.unique(source_region)
    # Find unique colors excluding the target color
    non_target_unique_colors = unique_source_colors[unique_source_colors != target_color]

    # If exactly one unique non-target color exists, use it
    if len(non_target_unique_colors) == 1:
        return non_target_unique_colors[0]
    # Otherwise (zero or multiple unique non-target colors), use gray(5)
    else:
        return 5

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)

    # 1. Isolate Regions
    key_region = input_array[0:5, 0:5]
    source_region = input_array[:, 6:]
    
    # Handle empty source region (though unlikely based on examples)
    if source_region.shape[1] == 0:
        return [] 
    
    rows, cols = source_region.shape

    # 2. Analyze Key (Central 3x3)
    key_pattern_source = key_region[1:4, 1:4]
    key_colors = find_key_colors(key_pattern_source)
    color1, color2 = key_colors # Already sorted

    # 3. Determine Target Color
    target_color = determine_target_color(key_colors)

    # 4. Generate Replacement Pattern
    replacement_pattern = generate_replacement_pattern(key_pattern_source, color1, color2)

    # 5. Determine Background Fill Color
    background_fill = determine_background_color(source_region, target_color, key_colors)

    # 6. Initialize Output Grid
    # Create output grid with same dimensions as source, filled with background color
    output_grid = np.full_like(source_region, fill_value=background_fill)

    # 7. Transform Source: Overwrite pixels matching the target color
    for r in range(rows):
        for c in range(cols):
            # Check if the original pixel in the source was the target color
            if source_region[r, c] == target_color:
                # If it was, replace the corresponding pixel in the output grid
                # using the tiled replacement pattern
                output_grid[r, c] = replacement_pattern[r % 3, c % 3]

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()