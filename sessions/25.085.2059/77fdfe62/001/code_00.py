import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a rule involving corner colors and an inner grid pattern.

    1. Identify the dimensions (H, W) of the input grid.
    2. Extract the four corner pixel colors: TopLeft, TopRight, BottomLeft, BottomRight.
    3. Extract the inner grid (rows 2 to H-3, cols 2 to W-3). Let its dimensions be h x w.
    4. Create an output grid of size h x w.
    5. Iterate through each cell (r, c) of the inner grid:
        a. If the inner grid cell color is white (0), the output grid cell (r, c) is white (0).
        b. If the inner grid cell color is azure (8), determine the quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) of the cell (r, c) within the inner grid.
        c. Set the output grid cell (r, c) to the corner color corresponding to its quadrant:
            - Top-Left Quadrant -> TopLeft Corner Color
            - Top-Right Quadrant -> TopRight Corner Color
            - Bottom-Left Quadrant -> BottomLeft Corner Color
            - Bottom-Right Quadrant -> BottomRight Corner Color
    6. Return the output grid.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Extract corner colors
    top_left_color = input_np[0, 0]
    top_right_color = input_np[0, W - 1]
    bottom_left_color = input_np[H - 1, 0]
    bottom_right_color = input_np[H - 1, W - 1]

    # Extract the inner grid (excluding the 2-pixel border: corners + blue frame)
    # Rows: 2 to H-3 (inclusive indices are 2 and H-3) -> slice is [2:H-2]
    # Cols: 2 to W-3 (inclusive indices are 2 and W-3) -> slice is [2:W-2]
    # Check bounds: Ensure H > 3 and W > 3
    if H <= 4 or W <= 4:
         # Handle edge case where the grid is too small for an inner grid + border
         # Based on examples, this shouldn't happen, but good practice.
         # Let's assume the transformation implies a minimum size.
         # Returning an empty grid or raising an error might be options.
         # For now, let's try extracting, it might yield empty dimensions handled later.
         pass

    inner_grid = input_np[2:H - 2, 2:W - 2]
    h, w = inner_grid.shape

    # Initialize the output grid - a copy of the inner grid is a good starting point
    output_grid = np.copy(inner_grid)

    # Calculate midpoints for quadrant determination (using integer division)
    mid_row = h // 2
    mid_col = w // 2

    # Iterate through each cell of the inner grid (and corresponding output grid cell)
    for r in range(h):
        for c in range(w):
            # Get the color of the current cell in the inner grid
            inner_color = inner_grid[r, c]

            # Apply transformation rule
            if inner_color == 0:
                # If inner color is white (0), output is white (0)
                output_grid[r, c] = 0
            elif inner_color == 8:
                # If inner color is azure (8), determine quadrant and assign corner color
                if r < mid_row and c < mid_col:  # Top-Left Quadrant
                    output_grid[r, c] = top_left_color
                elif r < mid_row and c >= mid_col:  # Top-Right Quadrant
                    output_grid[r, c] = top_right_color
                elif r >= mid_row and c < mid_col:  # Bottom-Left Quadrant
                    output_grid[r, c] = bottom_left_color
                elif r >= mid_row and c >= mid_col:  # Bottom-Right Quadrant
                    output_grid[r, c] = bottom_right_color
            # else: # If there were other colors in the inner grid, handle them.
                     # Based on description, only 0 and 8 are expected.
                     # Keep the original inner_grid value if unexpected colors appear.
                     # output_grid[r, c] = inner_color # This is already true due to np.copy

    # Convert the result back to a list of lists, as required by ARC format
    return output_grid.tolist()
