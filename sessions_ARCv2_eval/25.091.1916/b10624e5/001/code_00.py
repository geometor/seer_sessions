import numpy as np

"""
Transformation Rule Natural Language Description:

1.  Identify the central horizontal and vertical blue (1) dividing lines in the input grid.
2.  Identify the background color, which is yellow (4).
3.  Initialize an output grid of the same dimensions as the input, filled with the background color (yellow).
4.  Copy the central horizontal and vertical blue lines from the input to the output grid.
5.  Iterate through each cell in the top-left quadrant of the input grid (defined by the area above the horizontal line and to the left of the vertical line).
6.  For each cell in the input's top-left quadrant containing a color other than the background (yellow) or the dividing line (blue):
    a. Copy this color to the corresponding cell in the output grid's top-left quadrant.
    b. Reflect this color horizontally across the central vertical line and place it in the corresponding cell of the output grid's top-right quadrant.
    c. Reflect this color vertically across the central horizontal line and place it in the corresponding cell of the output grid's bottom-left quadrant.
    d. Reflect this color both horizontally and vertically (diagonally across the center point) and place it in the corresponding cell of the output grid's bottom-right quadrant.
7.  Return the completed output grid.
"""

def find_center_lines(grid):
    """Finds the indices of the single horizontal and vertical blue lines."""
    H, W = grid.shape
    center_row = -1
    center_col = -1
    
    # Find horizontal blue line (assuming only one)
    for r in range(H):
        if np.all(grid[r, :] == 1):
            center_row = r
            break
        # Check if it's a horizontal line partially obscured by vertical
        is_partial_line = True
        temp_col = -1
        for c in range(W):
             if grid[r,c] != 1:
                 if temp_col == -1: # First non-blue
                     temp_col = c   # Store column index
                 elif grid[r,c] != 1: # Second non-blue
                     is_partial_line = False
                     break
        if is_partial_line and temp_col != -1: # Found a row that's all blue except one column
            # Double check if that column is the vertical line
            if np.all(grid[:, temp_col] == 1):
                 center_row = r
                 break

    # Find vertical blue line (assuming only one)
    for c in range(W):
        if np.all(grid[:, c] == 1):
            center_col = c
            break
        # Check if it's a vertical line partially obscured by horizontal
        is_partial_line = True
        temp_row = -1
        for r in range(H):
             if grid[r,c] != 1:
                 if temp_row == -1: # First non-blue
                     temp_row = r   # Store row index
                 elif grid[r,c] != 1: # Second non-blue
                     is_partial_line = False
                     break
        if is_partial_line and temp_row != -1: # Found a col that's all blue except one row
            # Double check if that row is the horizontal line
             if np.all(grid[temp_row, :] == 1):
                 center_col = c
                 break


    if center_row == -1 or center_col == -1:
        # Fallback: Assume center if full lines not found (might happen in test cases?)
        center_row = H // 2
        center_col = W // 2
        # Attempt to confirm based on partial lines if needed
        if not np.all(grid[center_row, np.arange(W) != center_col] == 1):
             raise ValueError("Could not reliably determine horizontal center line.")
        if not np.all(grid[np.arange(H) != center_row, center_col] == 1):
             raise ValueError("Could not reliably determine vertical center line.")

    return center_row, center_col


def transform(input_grid):
    """
    Reflects the pattern from the top-left quadrant into the other three quadrants,
    using the central blue lines as axes of reflection.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    H, W = input_grid_np.shape
    
    # Define known colors
    background_color = 4 # yellow
    line_color = 1       # blue

    # Find the center dividing lines
    try:
        center_row, center_col = find_center_lines(input_grid_np)
    except ValueError as e:
        print(f"Error finding center lines: {e}")
        # As a robust fallback, maybe just copy input if lines aren't clear?
        # For now, let's stick to the pattern or fail.
        return input_grid # Or raise the error

    # Initialize output grid with background color
    output_grid = np.full((H, W), background_color, dtype=int)

    # Copy the blue dividing lines
    output_grid[center_row, :] = input_grid_np[center_row, :]
    output_grid[:, center_col] = input_grid_np[:, center_col]
    # Ensure the center pixel is blue
    output_grid[center_row, center_col] = line_color

    # Iterate through the top-left quadrant of the input grid
    for r in range(center_row):
        for c in range(center_col):
            color = input_grid_np[r, c]

            # Process only non-background and non-line colors
            if color != background_color and color != line_color:
                # Calculate reflected coordinates
                # Distance from horizontal line: center_row - 1 - r
                # Reflected row: center_row + 1 + (center_row - 1 - r) = 2 * center_row - r
                # Distance from vertical line: center_col - 1 - c
                # Reflected col: center_col + 1 + (center_col - 1 - c) = 2 * center_col - c
                # Let's use the simpler distance logic:
                # dist_r = center_row - r
                # dist_c = center_col - c
                r_reflected = center_row + (center_row - r)
                c_reflected = center_col + (center_col - c)

                # Check bounds just in case, although shouldn't be necessary if logic is right
                if 0 <= r_reflected < H and 0 <= c_reflected < W:

                    # 1. Copy to Top-Left
                    output_grid[r, c] = color
                    # 2. Reflect Horizontally to Top-Right
                    output_grid[r, c_reflected] = color
                    # 3. Reflect Vertically to Bottom-Left
                    output_grid[r_reflected, c] = color
                    # 4. Reflect Diagonally to Bottom-Right
                    output_grid[r_reflected, c_reflected] = color
                # else:
                    # This case should ideally not happen with correct reflection logic
                    # print(f"Warning: Reflected coordinates ({r_reflected}, {c_reflected}) out of bounds for original ({r},{c})")


    return output_grid.tolist() # Return as list of lists per ARC standard
