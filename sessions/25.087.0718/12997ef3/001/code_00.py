import numpy as np

"""
1.  **Identify the Template:** Scan the input grid to find all blue (1) pixels. Determine the smallest bounding box that encloses all blue pixels. Extract this subgrid, normalized to a 3x3 grid where blue pixels are 1 and others are 0; this is the "template".
2.  **Identify Color Pixels:** Scan the input grid to find all pixels whose color is *not* white (0) and *not* blue (1). Record the color value and the (row, column) coordinates of each such "color pixel".
3.  **Determine Arrangement and Order:**
    a.  Examine the coordinates of the identified color pixels. Find the minimum and maximum row indices (`min_row`, `max_row`) and the minimum and maximum column indices (`min_col`, `max_col`).
    b.  Calculate the row range (`row_range = max_row - min_row`) and column range (`col_range = max_col - min_col`).
    c.  If `row_range` is strictly greater than `col_range`, the arrangement is **vertical**. Sort the color pixels primarily by their row index, and secondarily by their column index.
    d.  Otherwise (if `col_range >= row_range` or there's only one color pixel), the arrangement is **horizontal**. Sort the color pixels primarily by their column index, and secondarily by their row index.
4.  **Generate Colored Blocks:** Create an empty list to store the output blocks. Iterate through the *sorted* color pixels:
    a.  For each color pixel, take its color value.
    b.  Create a new 3x3 grid by copying the template.
    c.  In this new grid, replace every cell containing the blue (1) value with the current color pixel's value. Leave the white (0) cells unchanged.
    d.  Add this newly created 3x3 colored block to the list of output blocks.
5.  **Assemble Final Output:** Concatenate the generated 3x3 colored blocks:
    a.  If the arrangement was **vertical**, stack the blocks vertically using `np.vstack`.
    b.  If the arrangement was **horizontal**, place the blocks side-by-side horizontally using `np.hstack`.
6.  The resulting combined grid is the final output.
"""

def find_bounding_box(grid, color):
    """Finds the min/max row/col for cells of a specific color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return min_row, max_row, min_col, max_col

def find_pixels_of_interest(grid, colors_to_exclude):
    """Finds coordinates and colors of pixels, excluding specified colors."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color not in colors_to_exclude:
                pixels.append({'color': color, 'row': r, 'col': c})
    return pixels

def transform(input_grid):
    """
    Transforms the input grid based on a blue template and scattered color pixels.
    The template shape is replicated and filled with each color pixel's color.
    These colored shapes are then arranged horizontally or vertically based on the
    spatial distribution of the original color pixels.
    """
    input_grid_np = np.array(input_grid)

    # 1. Identify the Template
    blue_pixels = np.argwhere(input_grid_np == 1)
    if blue_pixels.size == 0:
        # Handle error: No blue template found (though examples suggest it's always present)
        return np.array([[]]) # Or raise an error

    min_row_t, max_row_t = blue_pixels[:, 0].min(), blue_pixels[:, 0].max()
    min_col_t, max_col_t = blue_pixels[:, 1].min(), blue_pixels[:, 1].max()

    # Ensure template fits in 3x3 - it might be smaller
    # Create a 3x3 grid, place the relative shape
    template = np.zeros((3, 3), dtype=int)
    for r, c in blue_pixels:
        relative_r = r - min_row_t
        relative_c = c - min_col_t
        # Check bounds just in case, though problem implies it fits 3x3
        if 0 <= relative_r < 3 and 0 <= relative_c < 3:
            template[relative_r, relative_c] = 1 # Use 1 for the template shape marker


    # 2. Identify Color Pixels
    color_pixels = find_pixels_of_interest(input_grid_np, colors_to_exclude=[0, 1])

    if not color_pixels:
        # Handle error: No color pixels found (examples suggest always present)
        return np.array([[]]) # Or raise an error

    # 3. Determine Arrangement and Order
    if len(color_pixels) == 1:
        # Default to horizontal if only one color pixel
        arrangement = 'horizontal'
        sorted_color_pixels = color_pixels # Already sorted
    else:
        rows = [p['row'] for p in color_pixels]
        cols = [p['col'] for p in color_pixels]
        min_row_c, max_row_c = min(rows), max(rows)
        min_col_c, max_col_c = min(cols), max(cols)

        row_range = max_row_c - min_row_c
        col_range = max_col_c - min_col_c

        if row_range > col_range:
            arrangement = 'vertical'
            # Sort primarily by row, secondarily by column
            sorted_color_pixels = sorted(color_pixels, key=lambda p: (p['row'], p['col']))
        else:
            arrangement = 'horizontal'
            # Sort primarily by column, secondarily by row
            sorted_color_pixels = sorted(color_pixels, key=lambda p: (p['col'], p['row']))

    # 4. Generate Colored Blocks
    colored_blocks = []
    for pixel_info in sorted_color_pixels:
        color = pixel_info['color']
        # Create a copy of the template grid (which has 0s and 1s)
        colored_block = template.copy()
        # Replace the template marker (1) with the target color
        colored_block[colored_block == 1] = color
        colored_blocks.append(colored_block)

    # 5. Assemble Final Output
    if not colored_blocks:
         return np.array([[]]) # Should not happen if color_pixels were found

    if arrangement == 'vertical':
        output_grid = np.vstack(colored_blocks)
    else: # horizontal
        output_grid = np.hstack(colored_blocks)

    return output_grid.tolist() # Convert back to list of lists if required by framework