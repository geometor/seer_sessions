import numpy as np

"""
Transform the input grid based on a rule defined by a 5x5 key region in the top-left corner.

1.  Isolate the 5x5 key region (top-left) and the source region (columns 6 onwards).
2.  Identify the two distinct non-white colors (C1, C2) in the central 3x3 area of the key region.
3.  Determine the target color (T) in the source region based on the pair {C1, C2}:
    - {yellow(4), orange(7)} -> target green(3)
    - {blue(1), red(2)} -> target azure(8)
    - {green(3), azure(8)} -> target gray(5)
4.  Generate a 3x3 replacement pattern by swapping C1 and C2 within the central 3x3 area of the key region.
5.  Create the output grid by copying the source region.
6.  Replace every pixel in the output grid that matches the target color (T) with the corresponding pixel from the replacement pattern, tiling the pattern across the grid using modulo 3 indexing (row % 3, col % 3).
"""

def find_key_colors(key_pattern_source):
    """Finds the two distinct non-white colors in the 3x3 key pattern source."""
    unique_colors = np.unique(key_pattern_source)
    non_white_colors = unique_colors[unique_colors != 0] # Assuming 0 is white/background
    if len(non_white_colors) != 2:
        # This case might need more robust handling depending on task variations
        # For now, assume exactly two non-white colors based on examples
        raise ValueError(f"Expected 2 non-white key colors, found {len(non_white_colors)}: {non_white_colors}")
    return tuple(sorted(non_white_colors)) # Sort for consistent order

def determine_target_color(key_colors_tuple):
    """Determines the target color based on the pair of key colors."""
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
    pattern = np.copy(key_pattern_source)
    pattern[key_pattern_source == color1] = color2
    pattern[key_pattern_source == color2] = color1
    return pattern

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)

    # 1. Isolate Regions
    key_region = input_array[0:5, 0:5]
    source_region = input_array[:, 6:]
    
    # Ensure source_region is not empty
    if source_region.shape[1] == 0:
        # Handle cases where the input might not have columns beyond the separator
        # Depending on task constraints, return empty, error, or source_region itself
        # Based on examples, this shouldn't happen, but good practice to consider.
        # For now, let's assume source_region is always present and non-empty
         return [] # Or raise error, or return source_region.tolist() if allowed

    # 2. Analyze Key (Central 3x3)
    key_pattern_source = key_region[1:4, 1:4]
    key_colors = find_key_colors(key_pattern_source)
    color1, color2 = key_colors[0], key_colors[1] # Already sorted

    # 3. Determine Target Color
    target_color = determine_target_color(key_colors)

    # 4. Generate Replacement Pattern
    replacement_pattern = generate_replacement_pattern(key_pattern_source, color1, color2)

    # 5. Create the output grid (start as copy of source)
    output_grid = np.copy(source_region)
    rows, cols = source_region.shape

    # 6. Replace target pixels using the tiled pattern
    for r in range(rows):
        for c in range(cols):
            if source_region[r, c] == target_color:
                # Use modulo arithmetic to tile the 3x3 pattern
                output_grid[r, c] = replacement_pattern[r % 3, c % 3]

    # Convert back to list of lists for the required output format
    return output_grid.tolist()