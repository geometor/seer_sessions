import numpy as np

"""
Transforms the input grid based on horizontal segments of non-background colors within each row.
The background color is azure (8).
The transformation rule depends on the width of these horizontal segments and their position relative to the left and right edges of the grid.

1.  Identify the background color, which is azure (8).
2.  Initialize the output grid as a copy of the input grid.
3.  For each row in the grid:
    a.  Find all contiguous horizontal segments of non-background colors.
    b.  For each segment found:
        i.  Determine its width (number of pixels) and its starting and ending column indices.
        ii. If the segment's width is greater than 2: Change the color of the pixels at the starting column index and the starting column index + 1 in the output grid's current row to the background color (azure 8).
        iii. If the segment's width is 2 or less: Check if the segment's starting column index is 0 OR if its ending column index is the last column index of the grid.
            1.  If either condition is true (it touches a vertical edge): Change the color of all pixels within this segment's column range in the output grid's current row to the background color (azure 8).
            2.  If neither condition is true (it does not touch a vertical edge): Leave the segment's pixels unchanged in the output grid.
4.  Return the modified output grid.
"""

def find_and_process_segments(output_grid, row_index, grid_width, background_color=8):
    """
    Finds horizontal segments in a row and applies transformation rules.
    Modifies the output_grid in place for the given row_index.
    """
    current_segment_start = None
    row = output_grid[row_index] # Get a view of the row

    for col_index in range(grid_width):
        pixel_color = row[col_index]
        is_foreground = (pixel_color != background_color)

        if is_foreground and current_segment_start is None:
            # Start of a new segment
            current_segment_start = col_index
        elif not is_foreground and current_segment_start is not None:
            # End of the current segment (hit background)
            start_col = current_segment_start
            end_col = col_index - 1
            segment_width = end_col - start_col + 1

            # Process the ended segment
            apply_segment_rule(output_grid, row_index, start_col, end_col, segment_width, grid_width, background_color)

            current_segment_start = None # Reset for next potential segment
        # If foreground and segment already started, continue
        # If background and no segment started, continue

    # After the loop, check if a segment was ongoing until the end of the row
    if current_segment_start is not None:
        start_col = current_segment_start
        end_col = grid_width - 1
        segment_width = end_col - start_col + 1

        # Process the final segment
        apply_segment_rule(output_grid, row_index, start_col, end_col, segment_width, grid_width, background_color)


def apply_segment_rule(output_grid, row_index, start_col, end_col, width, grid_width, background_color):
    """Applies the transformation rules to a single detected segment."""
    touches_left_edge = (start_col == 0)
    touches_right_edge = (end_col == grid_width - 1)

    if width > 2:
        # Rule: Width > 2 -> Replace the 2 leftmost pixels with background color.
        # Ensure we don't go out of bounds, although slice handles this nicely.
        output_grid[row_index, start_col : start_col + 2] = background_color
    elif width <= 2 and (touches_left_edge or touches_right_edge):
        # Rule: Width <= 2 AND touches edge -> Replace the whole segment with background color.
        output_grid[row_index, start_col : end_col + 1] = background_color
    # Else: Width <= 2 AND not touching edges -> No change needed, segment remains as copied.


def transform(input_grid):
    """
    Applies the row-based segment transformation rules to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = output_grid.shape
    
    # Define background color
    background_color = 8

    # Iterate through each row
    for r in range(height):
        # Find and process segments for the current row
        find_and_process_segments(output_grid, r, width, background_color)

    # Convert the result back to a list of lists for the standard ARC format
    return output_grid.tolist()