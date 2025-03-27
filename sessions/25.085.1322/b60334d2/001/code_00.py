import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the following rule:
    1. Initialize a new output grid with the same dimensions as the input grid, filling it entirely with white (0) pixels.
    2. Iterate through each cell (pixel) of the input grid.
    3. If a cell contains a gray (5) pixel at location (row, col):
        a. Define the 3x3 pattern: [[5, 1, 5], [1, 0, 1], [5, 1, 5]].
        b. For each cell within this 3x3 pattern, calculate its target coordinates in the output grid relative to the center (row, col). The pattern cell at relative position (dr, dc) (where dr and dc range from -1 to 1) corresponds to the output grid cell at (row + dr, col + dc).
        c. Check if the target coordinates (row + dr, col + dc) are within the bounds of the output grid.
        d. If the target coordinates are valid, update the pixel at (row + dr, col + dc) in the output grid with the corresponding color value from the 3x3 pattern.
    4. Return the completed output grid.
    """

    # Get input grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid with the same dimensions as input, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Define the 3x3 pattern to be placed
    # Rows: -1, 0, +1 relative to center
    # Cols: -1, 0, +1 relative to center
    pattern = np.array([
        [5, 1, 5],
        [1, 0, 1],
        [5, 1, 5]
    ])
    pattern_height, pattern_width = pattern.shape
    pattern_center_offset_row = pattern_height // 2 # Should be 1
    pattern_center_offset_col = pattern_width // 2  # Should be 1


    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current input cell is gray (5)
            if input_grid[r, c] == 5:
                # If it's gray, apply the pattern centered at (r, c) to the output grid
                for pr in range(pattern_height): # 0, 1, 2
                    for pc in range(pattern_width): # 0, 1, 2
                        # Calculate the target coordinates in the output grid
                        # dr = pr - pattern_center_offset_row -> -1, 0, 1
                        # dc = pc - pattern_center_offset_col -> -1, 0, 1
                        target_r = r + (pr - pattern_center_offset_row)
                        target_c = c + (pc - pattern_center_offset_col)

                        # Check if the target coordinates are within the grid boundaries
                        if 0 <= target_r < height and 0 <= target_c < width:
                            # Get the color value from the pattern
                            pattern_value = pattern[pr, pc]
                            # Place the pattern value onto the output grid
                            output_grid[target_r, target_c] = pattern_value

    return output_grid