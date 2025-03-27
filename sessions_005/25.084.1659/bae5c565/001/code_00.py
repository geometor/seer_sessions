import numpy as np
from collections import Counter

"""
Transformation Rule:

1. Identify the sequence of colors in the first row of the input grid.
2. Identify the background color (most frequent color, excluding the first row).
3. Locate the single vertical line present in the input grid (distinct from the background), recording its color, column index, start row, and end row.
4. Initialize an output grid of the same dimensions as the input, filled with the background color.
5. Starting one row below the vertical line's start row, paint a V-shaped pattern onto the output grid.
6. This pattern uses colors from the first-row sequence, centered horizontally on the vertical line's column.
7. The width of the painted segment increases by two pixels for each subsequent row downwards.
8. The painting continues for floor(sequence_length / 2) rows.
9. At the central column (the original vertical line's column), the vertical line's original color overrides the sequence color during painting.
10. After the V-pattern is complete, if the original vertical line extended further down, copy the last painted row's pattern into all subsequent rows down to the original end row of the vertical line.
"""

def _find_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    # Exclude the first row if it's distinctly the sequence
    if grid.shape[0] > 1:
        counts = Counter(grid[1:].flatten())
    else:
        counts = Counter(grid.flatten())
        
    if not counts: # Handle empty or 1-row grid edge case
         if grid.size > 0:
             return grid[0,0] # Best guess
         else:
             return 0 # Default to white/black if grid is empty

    # Find the most common color, often the background
    background_color = counts.most_common(1)[0][0]
    return background_color

def _find_vertical_line(grid, background_color):
    """Finds the properties of the single vertical line."""
    height, width = grid.shape
    
    for c in range(width):
        line_color = -1
        start_row = -1
        end_row = -1
        in_line = False
        possible_line = True
        
        for r in range(height):
            pixel_color = grid[r, c]
            
            # Ignore the sequence row for finding the line itself
            if r == 0: 
                continue

            if pixel_color != background_color:
                if not in_line:
                    # Starting a potential line segment
                    if line_color == -1:
                        line_color = pixel_color
                        start_row = r
                        end_row = r
                        in_line = True
                    else:
                        # Found a different color in the same column, not a single line
                        possible_line = False
                        break
                elif pixel_color == line_color:
                    # Continuing the line segment
                    end_row = r
                else:
                    # Found a different color after the line started, not a single line
                    possible_line = False
                    break
            elif in_line:
                # Found background color after line started, line segment ended
                in_line = False 
                # If we find non-background later in this column, it's not a single line
                # We can continue scanning just in case, but mark as potential failure if needed
                
        # After checking all rows in column c:
        if possible_line and line_color != -1 and start_row > 0: # Ensure line isn't just in row 0
             # Check if it's truly vertical (only this column has this color pattern)
             # This check might be overly strict for some ARC tasks, but fits these examples.
             is_unique_line = True
             for other_c in range(width):
                 if other_c == c: continue
                 for r in range(start_row, end_row + 1):
                     if grid[r, other_c] == line_color:
                         # Found the same color elsewhere in the line's height range
                         # Let's be more lenient: is it part of another VERTICAL line of the same color?
                         # For this specific task, assume the line is unique.
                         pass # Simpler assumption based on examples.

             if is_unique_line:
                return line_color, c, start_row, end_row

    # Should not happen based on task description/examples
    raise ValueError("Vertical line not found")


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    # 1. Identify the sequence
    sequence = input_grid[0, :]

    # 2. Identify the background color
    background_color = _find_background_color(input_grid)

    # 3. Locate the vertical line
    line_color, line_col, line_start_row, line_end_row = _find_vertical_line(input_grid, background_color)

    # 4. Initialize output grid
    output_grid = np.full((height, width), background_color, dtype=int)

    # 5. Determine paint area parameters
    # Number of rows the expanding pattern will cover
    paint_rows_count = width // 2 
    # Start painting one row below the line's start
    paint_start_row = line_start_row + 1
    # Calculate the theoretical end row of the V shape painting
    paint_end_row_theoretical = paint_start_row + paint_rows_count -1
    
    # Ensure painting doesn't go beyond grid boundaries or the original line end
    # The actual end row for painting might be limited by the grid height
    actual_paint_end_row = min(paint_end_row_theoretical, height - 1)

    # 6. Paint the pattern
    last_row_painted = -1 # Keep track of the last row actually painted
    for r_offset in range(paint_rows_count):
        current_row = paint_start_row + r_offset
        
        # Stop if we go past the grid height
        if current_row >= height:
            break
            
        # Calculate width of the segment for this row
        # Width increases by 2 each row. Max width is 'width'.
        # The V starts narrowest and expands.
        # Offset from the 'full width' row (paint_end_row_theoretical)
        # Example: if width=9, paint_rows_count=4. Theoretical end row = start+3.
        # row = start + 0: offset_from_end = 3. width = 9 - 2*3 = 3
        # row = start + 1: offset_from_end = 2. width = 9 - 2*2 = 5
        # row = start + 2: offset_from_end = 1. width = 9 - 2*1 = 7
        # row = start + 3: offset_from_end = 0. width = 9 - 2*0 = 9
        offset_from_theoretical_end = paint_end_row_theoretical - current_row
        segment_width = width - 2 * offset_from_theoretical_end
        segment_width = max(1, segment_width) # Ensure width is at least 1

        # Calculate start and end columns for the segment, centered on line_col
        half_width_floor = segment_width // 2
        col_start = line_col - half_width_floor
        # For odd width, end col is line_col + half_width_floor
        # For even width, end col is line_col + half_width_floor - 1 ? No, needs testing.
        # Let's use indices relative to sequence
        seq_start_idx = (width - segment_width) // 2
        seq_end_idx = seq_start_idx + segment_width

        # Apply sequence colors
        for c_idx in range(segment_width):
            output_col = col_start + c_idx
            sequence_idx = seq_start_idx + c_idx

            # Check bounds before writing
            if 0 <= output_col < width and 0 <= sequence_idx < width:
                # 9. Override with line color at the center column
                if output_col == line_col:
                    output_grid[current_row, output_col] = line_color
                else:
                    output_grid[current_row, output_col] = sequence[sequence_idx]
        
        last_row_painted = current_row # Update the last row we successfully painted

    # 10. Copy last painted row downwards if needed
    # Check if the painting finished *before* the original line ended
    # and also check if we actually painted any row (last_row_painted != -1)
    if last_row_painted != -1 and last_row_painted < line_end_row:
        # Get the pattern from the last row we painted
        last_pattern = output_grid[last_row_painted, :].copy()
        # Copy this pattern to rows below it, up to the original line end row
        for r in range(last_row_painted + 1, min(line_end_row + 1, height)):
            output_grid[r, :] = last_pattern

    # Special case: If the line itself extended beyond the calculated paint area initially
    # Ensure the central column below the painted part still shows the line color down to line_end_row
    # This seems to be covered by the copy mechanism if the last row included the line color.
    # Let's double check train_1 output: row 12 duplicates row 11.
    # The paint ends at row 11 (index starting 0). line_end_row is 12.
    # R_start=5, C=6. W=13. paint_rows_count=6. R_paint_start=6. R_paint_end_theoretical=6+6-1=11.
    # Loop runs for r_offset 0 to 5. current_row 6 to 11.
    # last_row_painted = 11. line_end_row = 12.
    # 11 < 12 is true. Copy row 11 to row 12. Correct.

    # Let's check train_2 output: row 8 duplicates row 7.
    # R_start=3, C=4. W=9. paint_rows_count=4. R_paint_start=4. R_paint_end_theoretical=4+4-1=7.
    # Loop runs for r_offset 0 to 3. current_row 4 to 7.
    # last_row_painted = 7. line_end_row = 8.
    # 7 < 8 is true. Copy row 7 to row 8. Correct.

    # Final check: Ensure the original line's pixels (if they fall outside the painted/copied area)
    # are restored in the output. The current logic initializes with background and then paints/copies.
    # It seems the examples imply the line *only* persists where it intersects the painted/copied area.
    # Re-examine train_1: The azure line originally goes from row 5 to 12 at col 6.
    # In output, azure is present from row 5 (incorrect based on my logic - paint starts row 6) to 12 at col 6.
    # Ah, the rule should be: The *entire* original vertical line segment should persist in the output,
    # potentially being overwritten by the sequence *except* at the line's own column.
    # Let's adjust:
    # 1. Initialize output with background
    # 2. Copy the original vertical line segment into the output
    # 3. Paint the pattern, overriding background and potentially the line *except* at line_col
    # 4. Copy last row down. This will correctly propagate the line color at line_col if it was in the last painted row.

    # Revision:
    output_grid = np.full((height, width), background_color, dtype=int) # Step 4

    # Copy original line segment first
    for r in range(line_start_row, line_end_row + 1):
         if 0 <= r < height: # Boundary check
              output_grid[r, line_col] = line_color

    # Now paint, potentially overwriting parts of the line *away* from line_col
    last_row_painted = -1
    for r_offset in range(paint_rows_count):
        current_row = paint_start_row + r_offset
        if current_row >= height: break

        offset_from_theoretical_end = paint_end_row_theoretical - current_row
        segment_width = width - 2 * offset_from_theoretical_end
        segment_width = max(1, segment_width)

        col_start = line_col - (segment_width // 2)
        seq_start_idx = (width - segment_width) // 2

        for c_idx in range(segment_width):
            output_col = col_start + c_idx
            sequence_idx = seq_start_idx + c_idx

            if 0 <= output_col < width and 0 <= sequence_idx < width:
                # CRITICAL: Do NOT overwrite the line color at the line's column
                if output_col != line_col:
                    output_grid[current_row, output_col] = sequence[sequence_idx]
                # If output_col == line_col, we *keep* the line_color already placed.
        
        last_row_painted = current_row

    # Copy last painted row downwards
    if last_row_painted != -1 and last_row_painted < line_end_row:
        last_pattern = output_grid[last_row_painted, :].copy()
        for r in range(last_row_painted + 1, min(line_end_row + 1, height)):
             # When copying, make sure the central column retains the line color
             # The last_pattern already has the correct color at line_col due to the logic above.
             output_grid[r, :] = last_pattern

    # One final check: Does the original line top pixel (at line_start_row) need special handling?
    # In train_1: row 5, col 6 is azure (8) in output. paint starts row 6. Copying starts row 12.
    # In train_2: row 3, col 4 is azure (8) in output. paint starts row 4. Copying starts row 8.
    # Yes, the initial copy of the vertical line segment handles placing the line color
    # before the painting starts below it. The revised logic seems correct.


    return output_grid.tolist() # Return as list of lists per ARC standard