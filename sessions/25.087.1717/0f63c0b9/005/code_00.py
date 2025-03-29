import numpy as np

"""
Transforms a grid with sparse colored pixels into a grid with colored horizontal zones defined by these pixels.

1.  Identify all non-white pixels in the input grid, recording their color and row index. If no non-white pixels are found, return an all-white grid of the same dimensions.
2.  Determine the unique rows containing non-white pixels and associate each unique row with the color found in that row (using the first encountered color in that row during scan).
3.  Sort these unique rows in ascending order. Let the sorted unique rows be R_1, R_2, ..., R_n and their corresponding colors be C_1, C_2, ..., C_n.
4.  Create an output grid of the same dimensions as the input, initialized to white (0).
5.  Draw a solid horizontal line of color C_1 across the full width of the output grid at row 0 (the very top row).
6.  Draw a solid horizontal line of color C_n across the full width of the output grid at the last row (height - 1).
7.  For each unique row R_i (from i=1 to n), draw a solid horizontal line of color C_i across the full width of the output grid at row R_i.
8.  Draw vertical lines in the leftmost column (column 0) and the rightmost column (last column) to connect the horizontal lines:
    *   Fill the vertical segment from row 1 up to (but not including) row R_1 with color C_1.
    *   For each pair of consecutive unique rows R_i and R_{i+1} (where i goes from 1 to n-1), fill the vertical segment from row R_i + 1 up to (but not including) row R_{i+1} with color C_i (the color associated with the upper row R_i).
    *   Fill the vertical segment from row R_n + 1 up to (but not including) the last row (height - 1) with color C_n.
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
    # Scan top-to-bottom, left-to-right to respect "first encountered color" rule
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:
                # Store the first color encountered for this row
                if r not in row_colors:
                    row_colors[r] = color

    # Handle edge case: no non-white pixels
    if not row_colors:
        return output_grid.tolist()

    # 3. Sort unique rows and get corresponding (row, color) pairs
    sorted_rows = sorted(row_colors.keys())
    sorted_pixel_data = [(r, row_colors[r]) for r in sorted_rows]

    # Get colors for top and bottom boundaries/segments
    first_color = sorted_pixel_data[0][1]
    last_color = sorted_pixel_data[-1][1]

    # 4. Initialize output grid (already done)

    # 5. Draw top boundary line (row 0)
    output_grid[0, :] = first_color

    # 6. Draw bottom boundary line (last row)
    output_grid[height - 1, :] = last_color

    # 7. Draw horizontal lines for each identified pixel's row
    for r, c in sorted_pixel_data:
        output_grid[r, :] = c

    # 8. Draw vertical borders (column 0 and width - 1)
    # Segment above the first pixel row (R_1)
    first_row = sorted_pixel_data[0][0]
    if first_row > 0: # Ensure there's space between row 0 and first_row
        # Vertical lines go from row 1 up to (but not including) first_row
        # Color is C_1 (first_color)
        if 1 < first_row:
            output_grid[1:first_row, 0] = first_color
            output_grid[1:first_row, width - 1] = first_color

    # Segments between consecutive pixel rows (R_i and R_{i+1})
    # Loop from the first pair up to the second-to-last pair
    for i in range(len(sorted_pixel_data) - 1):
        current_row, current_color = sorted_pixel_data[i] # R_i, C_i
        next_row = sorted_pixel_data[i+1][0]             # R_{i+1}

        start_vert_row = current_row + 1
        end_vert_row = next_row # Slice goes up to, but not including, end_vert_row

        # Only draw if there's space between the rows
        if start_vert_row < end_vert_row:
            # Fill segment with C_i (current_color) - THIS IS THE FIX
            output_grid[start_vert_row:end_vert_row, 0] = current_color
            output_grid[start_vert_row:end_vert_row, width - 1] = current_color

    # Segment below the last pixel row (R_n)
    last_row = sorted_pixel_data[-1][0]
    # Vertical lines go from last_row + 1 up to (but not including) height - 1
    start_vert_row_final = last_row + 1
    end_vert_row_final = height - 1 # Slice goes up to, but not including, end_vert_row_final

    # Only draw if there's space between the last row and the bottom boundary
    if start_vert_row_final < end_vert_row_final:
        # Color is C_n (last_color)
        output_grid[start_vert_row_final:end_vert_row_final, 0] = last_color
        output_grid[start_vert_row_final:end_vert_row_final, width - 1] = last_color

    # 9. Return the completed grid
    return output_grid.tolist()