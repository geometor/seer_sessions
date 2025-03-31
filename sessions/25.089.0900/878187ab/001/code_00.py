import numpy as np
from collections import Counter

"""
Identify the background color (most frequent color) in the input grid.
Count the number of non-background (foreground) pixels (N).
Determine the output grid dimensions: height = max(input_height, 16), width = input_width.
Create the output grid initialized with the background color.
Based on N, select a predefined 5-row high pattern (composed of red-2 and yellow-4 pixels) and its corresponding width (W).
Paste the selected pattern into the bottom-left corner of the output grid (last 5 rows, first W columns).
Return the modified output grid.
"""

# Predefined patterns based on the count of foreground pixels (N)
# Pattern for N = 10
PATTERN_10 = np.array([
    [2, 2, 4, 2, 4, 2, 2],
    [2, 2, 2, 4, 2, 2, 2],
    [2, 2, 4, 2, 4, 2, 2],
    [2, 4, 2, 2, 2, 4, 2],
    [4, 2, 2, 2, 2, 2, 4]
])

# Pattern for N = 11
PATTERN_11 = np.array([
    [2, 2, 2, 2, 4, 4, 2, 2, 2, 2],
    [2, 2, 2, 4, 2, 2, 4, 2, 2, 2],
    [2, 2, 4, 2, 2, 2, 2, 4, 2, 2],
    [2, 4, 2, 2, 2, 2, 2, 2, 4, 2],
    [4, 2, 2, 2, 2, 2, 2, 2, 2, 4]
])

# Map N to patterns and their widths
PATTERN_MAP = {
    10: (PATTERN_10, 7),
    11: (PATTERN_11, 10),
}

def get_background_color(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def count_foreground_pixels(grid, background_color):
    """Counts pixels that are not the background color."""
    return np.sum(grid != background_color)

def transform(input_grid):
    """
    Transforms the input grid based on the count of foreground pixels.
    Places a specific pattern in the bottom-left corner of the output grid.
    """
    input_np = np.array(input_grid)
    input_height, input_width = input_np.shape

    # 1. Identify background color
    background_color = get_background_color(input_np)

    # 2. Count foreground pixels
    n_foreground = count_foreground_pixels(input_np, background_color)

    # 3. Determine output grid dimensions
    output_height = max(input_height, 16)
    output_width = input_width

    # 4. Create the output grid initialized with background color
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # 5. Select the pattern based on N
    if n_foreground in PATTERN_MAP:
        pattern, pattern_width = PATTERN_MAP[n_foreground]
        pattern_height = 5 # All patterns are 5 rows high

        # 6. Copy the selected pattern onto the output grid
        # Check if pattern fits within the output grid dimensions
        if pattern_height <= output_height and pattern_width <= output_width:
            start_row = output_height - pattern_height
            start_col = 0
            end_row = start_row + pattern_height
            end_col = start_col + pattern_width

            output_grid[start_row:end_row, start_col:end_col] = pattern
        else:
            # Handle cases where the pattern is too large for the output grid (optional, based on task constraints)
            # For now, we assume patterns will fit or this indicates an issue.
            print(f"Warning: Pattern for N={n_foreground} does not fit in output grid.")
            pass # Or raise an error, or partially draw, depending on desired behavior

    # 7. Return the final output grid
    return output_grid.tolist()