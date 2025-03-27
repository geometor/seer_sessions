import numpy as np

"""
Constructs a nested square grid based on color frequency from the input grid.

1.  Counts the occurrences of each unique color in the input grid.
2.  Identifies the background color as the one with the highest frequency. If there's a tie in frequency, the color with the lower index is chosen as the background.
3.  Identifies all other colors (non-background colors).
4.  Sorts these non-background colors based on their frequency in descending order. If counts are tied, colors are sorted by their index in ascending order.
5.  Determines the output grid size (S x S) where S = 2 * N - 1, and N is the number of unique non-background colors.
6.  Constructs the output grid by creating nested square frames:
    - The outermost frame uses the most frequent non-background color.
    - The next inner frame uses the second most frequent non-background color.
    - This continues inwards, with the least frequent non-background color filling the center.
7.  Handles edge cases:
    - Empty input grid returns an empty grid.
    - Input grid with only one color returns a 1x1 grid of that color.
    - Input grid where only the background color exists (after identifying it) returns a 1x1 grid of the background color.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on color frequency and nested frame construction.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Convert input to numpy array if it isn't already
    input_grid = np.array(input_grid)

    # 1. Count colors
    colors, counts = np.unique(input_grid, return_counts=True)
    color_counts = dict(zip(colors, counts))

    # Handle simple cases: empty grid or grid with only one color
    if len(color_counts) == 0:
         # Return empty grid for empty input
         return np.array([[]])
    if len(color_counts) == 1:
         # Return 1x1 grid of the single color present
         single_color = colors[0]
         return np.array([[single_color]], dtype=int)

    # 2. Determine background color (most frequent, lowest index tie-breaker)
    max_count = 0
    for count in color_counts.values():
        if count > max_count:
            max_count = count
    
    # Find all colors with the maximum count
    potential_background_colors = [color for color, count in color_counts.items() if count == max_count]
    # Choose the one with the smallest color index as background
    background_color = min(potential_background_colors)

    # 3. Identify non-background colors and their counts
    non_background_colors = []
    for color, count in color_counts.items():
        if color != background_color:
            non_background_colors.append((color, count))

    # Handle case: only background color is present (no non-background colors)
    if not non_background_colors:
         # Return 1x1 grid of the background color
         return np.array([[background_color]], dtype=int)

    # N is the number of unique non-background colors
    N = len(non_background_colors)

    # 4. Sort non-background colors: by count descending, then by color index ascending
    # The key uses a tuple: (-count, color) ensures descending count, ascending color for ties
    sorted_colors_with_counts = sorted(non_background_colors, key=lambda item: (-item[1], item[0]))
    # Extract just the sorted colors
    sorted_colors = [item[0] for item in sorted_colors_with_counts]

    # 5. Calculate output grid size
    S = 2 * N - 1

    # 6. Initialize output grid: create an S x S grid
    # We will fill it layer by layer, starting from the outermost
    # It's efficient to start with the outermost color filling the whole grid
    output_grid = np.full((S, S), sorted_colors[0], dtype=int)

    # 7. Fill nested frames
    # Iterate from the second color (index 1) up to the last color (index N-1)
    # 'k' represents the layer index (0 is outermost, N-1 is innermost)
    for k in range(1, N):
        color_to_fill = sorted_colors[k] # Get the color for the current layer

        # Calculate the boundaries for the current layer's square region
        # The k-th layer fills the square from (k, k) to (S-1-k, S-1-k)
        top_left_row = k
        top_left_col = k
        bottom_right_row = S - 1 - k
        bottom_right_col = S - 1 - k

        # Ensure the indices are valid (should always be true if N >= 1)
        if top_left_row <= bottom_right_row and top_left_col <= bottom_right_col:
            # Fill the inner square region corresponding to this layer
            # Numpy slicing uses exclusive end index for range, so add 1
            output_grid[top_left_row : bottom_right_row + 1, top_left_col : bottom_right_col + 1] = color_to_fill

    return output_grid