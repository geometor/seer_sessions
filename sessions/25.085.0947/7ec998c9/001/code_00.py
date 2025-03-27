import numpy as np

def find_most_frequent_color(grid):
    """Finds the most frequent color in the grid."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    return unique_colors[np.argmax(counts)]

def find_unique_pixel(grid, background_color):
    """Finds the position and color of the unique pixel different from the background."""
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color:
                return r, c, grid[r, c]
    return None # Should not happen based on task description

def transform(input_grid):
    """
    Transforms the input grid by drawing a blue path based on a unique marker pixel.

    1. Determines the background color (most frequent).
    2. Locates the single 'marker' pixel (different color).
    3. Initializes the output grid as a copy of the input.
    4. Draws a blue path (color 1) on the output grid, starting from the top-left,
       going right along the top edge to the marker's column, then down that column
       (skipping the marker), then along the bottom edge.
    5. The direction along the bottom edge depends on the marker's horizontal position:
       - If marker_col < width / 2, the path goes right from marker_col to the end.
       - Otherwise, the path goes left from marker_col to the beginning.
    6. Only pixels matching the background color are changed to blue along the path.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Find background color
    background_color = find_most_frequent_color(input_array)

    # Find marker pixel position and color
    marker_info = find_unique_pixel(input_array, background_color)
    if marker_info is None:
        # Handle case where no unique pixel is found (though description implies one exists)
        return input_grid # Or raise an error
    marker_row, marker_col, marker_color = marker_info

    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_array)

    # Define the path color
    path_color = 1 # blue

    # --- Draw the path ---

    # Segment 1: Top Row (from (0, 0) to (0, marker_col))
    for c in range(marker_col + 1):
        if output_grid[0, c] == background_color:
            output_grid[0, c] = path_color

    # Segment 2: Marker Column (from (0, marker_col) to (height - 1, marker_col), excluding marker)
    for r in range(height):
        if r != marker_row: # Skip the marker pixel itself
            if output_grid[r, marker_col] == background_color:
                output_grid[r, marker_col] = path_color

    # Segment 3: Bottom Row
    # Check if marker is in the left half (strictly)
    if marker_col < width / 2:
        # Path runs from (height - 1, marker_col) rightwards to (height - 1, width - 1)
        for c in range(marker_col, width):
             if output_grid[height - 1, c] == background_color:
                output_grid[height - 1, c] = path_color
    else:
        # Path runs from (height - 1, 0) leftwards to (height - 1, marker_col)
        # Note: The NL description says "from (height - 1, 0) to (height - 1, marker_col)"
        # which implies going right, but the examples show going left *from* the marker column
        # Let's implement the example behavior: from col 0 up to and including marker_col
        for c in range(marker_col + 1):
             if output_grid[height - 1, c] == background_color:
                output_grid[height - 1, c] = path_color


    # Convert back to list of lists for the expected output format
    return output_grid.tolist()