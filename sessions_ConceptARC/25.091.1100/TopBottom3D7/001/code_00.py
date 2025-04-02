import numpy as np
from collections import Counter

"""
Identify three key colors: background (BKG), vertical pattern (C_vert), and horizontal pattern (C_horz).
Determine the columns (Cols_vert) containing C_vert and rows (Rows_horz) containing C_horz.
Create a copy of the input grid.
Iterate through the intersections of Rows_horz and Cols_vert.
If a pixel at an intersection (r, c) in the input grid has color C_horz, change its color to C_vert in the output grid.
Otherwise, keep the original color.
Return the modified grid.
"""

def find_colors(grid):
    """
    Identifies background, horizontal pattern, and vertical pattern colors.

    The background color is assumed to be 0.
    The horizontal pattern color (C_horz) is the non-background color present in the fewest distinct rows.
    The vertical pattern color (C_vert) is the non-background color present in the fewest distinct columns.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (background_color, c_horz, c_vert)

    Raises:
        ValueError: If exactly two non-background colors are not found, or if
                    horizontal/vertical roles are ambiguous based on row/column counts.
    """
    unique_colors = np.unique(grid)

    # Assume background is 0
    if 0 in unique_colors:
        background_color = 0
    else:
        # This case is not expected based on the examples, but provides a fallback.
        # It might be better to raise an error if 0 is not present.
        raise ValueError("Background color 0 not found in the grid.")

    other_colors = [c for c in unique_colors if c != background_color]

    if len(other_colors) != 2:
        raise ValueError(f"Expected exactly two non-background colors, found {len(other_colors)}: {other_colors}")

    color1, color2 = other_colors

    # Calculate how many distinct rows/columns each color appears in
    rows1 = set(np.where(grid == color1)[0])
    cols1 = set(np.where(grid == color1)[1])
    rows2 = set(np.where(grid == color2)[0])
    cols2 = set(np.where(grid == color2)[1])

    num_rows1 = len(rows1)
    num_cols1 = len(cols1)
    num_rows2 = len(rows2)
    num_cols2 = len(cols2)

    # Identify C_horz: the color present in fewer distinct rows
    if num_rows1 < num_rows2:
        c_horz = color1
    elif num_rows2 < num_rows1:
        c_horz = color2
    else:
        raise ValueError(f"Ambiguous horizontal color: Color {color1} in {num_rows1} rows, Color {color2} in {num_rows2} rows.")

    # Identify C_vert: the color present in fewer distinct columns
    if num_cols1 < num_cols2:
        c_vert = color1
    elif num_cols2 < num_cols1:
        c_vert = color2
    else:
        raise ValueError(f"Ambiguous vertical color: Color {color1} in {num_cols1} cols, Color {color2} in {num_cols2} cols.")

    # Final sanity check: Ensure C_horz and C_vert are different colors
    if c_horz == c_vert:
        # This condition should technically not be reachable if the row/col counts are different
        # but serves as a safeguard against unexpected logic flaws.
        raise ValueError(f"Identified horizontal ({c_horz}) and vertical ({c_vert}) colors are the same. Check logic.")

    return background_color, c_horz, c_vert


def transform(input_grid):
    """
    Applies the transformation rule: Changes pixels at the intersection of
    horizontal pattern rows and vertical pattern columns from the horizontal
    color to the vertical color.

    Args:
        input_grid (list of lists): The input grid representing colors as integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # --- Workflow ---

    # 1. Identify the key colors: background, horizontal pattern (C_horz), vertical pattern (C_vert)
    try:
        _, c_horz, c_vert = find_colors(grid)
    except ValueError as e:
        # If colors cannot be determined unambiguously, return the original grid
        # This handles cases not fitting the expected pattern.
        print(f"Warning: Could not determine colors reliably - {e}. Returning original grid.")
        return input_grid

    # 2. Determine the set of column indices (Cols_vert) where C_vert appears
    # A column is included if it contains at least one C_vert pixel.
    cols_vert = set(np.where(np.any(grid == c_vert, axis=0))[0])

    # 3. Determine the set of row indices (Rows_horz) where C_horz appears
    # A row is included if it contains at least one C_horz pixel.
    rows_horz = set(np.where(np.any(grid == c_horz, axis=1))[0])

    # 4. Iterate through the identified rows and columns defining the intersections
    for r in rows_horz:
        for c in cols_vert:
            # 5. Check the color of the pixel at the intersection (r, c) in the *original* input grid
            if grid[r, c] == c_horz:
                # 6. If the pixel color is C_horz, change its color to C_vert in the output grid
                output_grid[r, c] = c_vert
            # 7. If the pixel color is not C_horz, it remains unchanged (already copied)

    # 8. Convert the result back to a list of lists format
    return output_grid.tolist()
