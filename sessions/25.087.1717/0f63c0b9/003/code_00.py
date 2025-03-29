import numpy as np

"""
Transforms an input grid containing sparse colored pixels into an output grid with horizontal zones and vertical borders defined by those pixels.

1.  Identify all non-white pixels in the input grid, recording their color and row index. If no non-white pixels are found, return an all-white grid of the same dimensions.
2.  Determine the unique rows containing non-white pixels and associate each unique row with the color found in that row. If multiple colors exist in the same row, use the color of the first encountered non-white pixel in that row during a top-to-bottom, left-to-right scan (though examples suggest consistency or irrelevance of column).
3.  Sort these unique rows in ascending order. Let the sorted unique rows be `R_1, R_2, ..., R_n` and their corresponding colors be `C_1, C_2, ..., C_n`.
4.  Create an output grid of the same dimensions as the input, initialized to white (0).
5.  Draw a solid horizontal line of color `C_1` (color associated with the topmost row `R_1`) across the full width of the output grid at row 0 (the very top row).
6.  Draw a solid horizontal line of color `C_n` (color associated with the bottommost row `R_n`) across the full width of the output grid at the last row (`height - 1`).
7.  For each unique row `R_i` (from `i=1` to `n`), draw a solid horizontal line of color `C_i` across the full width of the output grid at row `R_i`.
8.  Draw vertical lines in the leftmost column (column 0) and the rightmost column (last column) to connect the horizontal lines:
    *   Fill the vertical segment from row 1 up to (but not including) row `R_1` with color `C_1`. This applies only if `R_1 > 1`.
    *   For each pair of consecutive unique rows `R_i` and `R_{i+1}` (where `i` goes from 1 to `n-1`), fill the vertical segment from row `R_i + 1` up to (but not including) row `R_{i+1}` with color `C_{i+1}` (the color associated with the lower row `R_{i+1}`). This applies only if `R_{i+1} > R_i + 1`.
    *   Fill the vertical segment from row `R_n + 1` up to (but not including) the last row (`height - 1`) with color `C_n`. This applies only if `height - 1 > R_n + 1`.
9.  Return the completed output grid.
"""

def transform(input_grid):
    """
    Applies the zone-filling transformation based on non-white input pixels.

    Args:
        input_grid (list of lists): The input grid containing pixels 0-9.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize with white (0)

    # 1 & 2. Identify non-white pixels and unique rows with their colors
    row_colors = {}
    pixel_locations = []
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:
                pixel_locations.append((r, c, color))
                # Store the first color encountered for this row
                if r not in row_colors:
                    row_colors[r] = color

    # Handle case with no non-white pixels
    if not row_colors:
        return output_grid.tolist()

    # 3. Sort unique rows and get corresponding (row, color) pairs
    sorted_rows = sorted(row_colors.keys())
    sorted_pixel_data = [(r, row_colors[r]) for r in sorted_rows]

    # Get colors for top and bottom boundaries/segments
    first_color = sorted_pixel_data[0][1]
    last_color = sorted_pixel_data[-1][1]

    # 4. Initialize output grid (already done)

    # 5. Draw top boundary line
    output_grid[0, :] = first_color

    # 6. Draw bottom boundary line
    output_grid[height - 1, :] = last_color

    # 7. Draw horizontal lines for each identified pixel's row
    for r, c in sorted_pixel_data:
        output_grid[r, :] = c

    # 8. Draw vertical borders
    # Segment above the first pixel row
    first_row = sorted_pixel_data[0][0]
    if first_row > 0: # Ensure there's space between row 0 and first_row
        # Vertical lines go from row 1 up to (but not including) first_row
        if 1 < first_row:
            output_grid[1:first_row, 0] = first_color
            output_grid[1:first_row, width - 1] = first_color

    # Segments between consecutive pixel rows
    for i in range(len(sorted_pixel_data) - 1):
        current_row = sorted_pixel_data[i][0]
        next_row = sorted_pixel_data[i+1][0]
        next_color = sorted_pixel_data[i+1][1]

        start_vert_row = current_row + 1
        end_vert_row = next_row # Slice goes up to, but not including, end_vert_row

        if start_vert_row < end_vert_row: # Only draw if there's space
            output_grid[start_vert_row:end_vert_row, 0] = next_color
            output_grid[start_vert_row:end_vert_row, width - 1] = next_color

    # Segment below the last pixel row
    last_row = sorted_pixel_data[-1][0]
    start_vert_row_final = last_row + 1
    end_vert_row_final = height - 1 # Slice goes up to, but not including, end_vert_row_final

    if start_vert_row_final < end_vert_row_final: # Only draw if there's space
        output_grid[start_vert_row_final:end_vert_row_final, 0] = last_color
        output_grid[start_vert_row_final:end_vert_row_final, width - 1] = last_color

    # 9. Return the completed grid
    return output_grid.tolist()