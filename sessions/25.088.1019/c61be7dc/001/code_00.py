import numpy as np
import math

"""
Identifies a pair of parallel white (0) lines (horizontal or vertical) in the input grid.
Finds the gray (5) object enclosed between these lines.
Transforms the grid by:
1. Moving the white lines one step inwards towards each other.
2. Replacing the enclosed gray object with a single gray line segment.
3. The orientation of the output gray line matches the orientation of the input white lines.
4. If input lines are vertical: The output gray line is vertical, centered horizontally between the new white lines, and has a length equal to the grid height minus 2, centered vertically.
5. If input lines are horizontal: The output gray line is horizontal, centered vertically between the new white lines, and has a length equal to the number of gray pixels in the original enclosed object, centered horizontally.
6. The background is orange (7).
"""

def find_parallel_white_lines(grid):
    """Finds the pair of parallel white lines (rows or columns)."""
    height, width = grid.shape
    white_rows = []
    white_cols = []

    # Check for horizontal lines (full rows of white)
    for r in range(height):
        if np.all(grid[r, :] == 0):
            white_rows.append(r)

    # Check for vertical lines (full columns of white)
    for c in range(width):
        if np.all(grid[:, c] == 0):
            white_cols.append(c)

    if len(white_rows) == 2:
        return 'horizontal', white_rows[0], white_rows[1]
    elif len(white_cols) == 2:
        return 'vertical', white_cols[0], white_cols[1]
    else:
        # Fallback: check for lines that might be interrupted by gray pixels crossing them
        # (This seems less likely given the examples, but could be a variation)
        # Scan rows for potential horizontal lines (mostly 0, some 5 maybe)
        candidate_rows = []
        for r in range(height):
             if np.count_nonzero(grid[r, :] != 0) <= np.count_nonzero(grid[r, :] == 5): # Allow only 0s and 5s, mostly 0s? simpler: count 0s
                 if np.count_nonzero(grid[r,:] == 0) > width // 2 : # Heuristic: majority are 0
                     candidate_rows.append(r)
        if len(candidate_rows) == 2:
             # Check if gray pixels are ONLY between these rows
             gray_coords = np.argwhere(grid == 5)
             min_r_gray = np.min(gray_coords[:, 0]) if gray_coords.size > 0 else -1
             max_r_gray = np.max(gray_coords[:, 0]) if gray_coords.size > 0 else -1
             if gray_coords.size > 0 and min_r_gray > candidate_rows[0] and max_r_gray < candidate_rows[1]:
                 return 'horizontal', candidate_rows[0], candidate_rows[1]


        # Scan columns for potential vertical lines
        candidate_cols = []
        for c in range(width):
             if np.count_nonzero(grid[:, c] != 0) <= np.count_nonzero(grid[:, c] == 5):
                 if np.count_nonzero(grid[:,c] == 0) > height // 2 :
                      candidate_cols.append(c)
        if len(candidate_cols) == 2:
             # Check if gray pixels are ONLY between these cols
             gray_coords = np.argwhere(grid == 5)
             min_c_gray = np.min(gray_coords[:, 1]) if gray_coords.size > 0 else -1
             max_c_gray = np.max(gray_coords[:, 1]) if gray_coords.size > 0 else -1
             if gray_coords.size > 0 and min_c_gray > candidate_cols[0] and max_c_gray < candidate_cols[1]:
                 return 'vertical', candidate_cols[0], candidate_cols[1]

    # If no clear pair found by above methods, look for the two rows/cols with the most zeros
    # This is less robust but might catch cases missed by strict line checks
    row_zero_counts = [(r, np.sum(grid[r, :] == 0)) for r in range(height)]
    col_zero_counts = [(c, np.sum(grid[:, c] == 0)) for c in range(width)]

    row_zero_counts.sort(key=lambda x: x[1], reverse=True)
    col_zero_counts.sort(key=lambda x: x[1], reverse=True)

    # Check if the top 2 row counts are significantly higher and form potential lines
    if len(row_zero_counts) >= 2 and row_zero_counts[0][1] > width * 0.7 and row_zero_counts[1][1] > width * 0.7:
         rows = sorted([row_zero_counts[0][0], row_zero_counts[1][0]])
         # Check if gray is between
         gray_coords = np.argwhere(grid == 5)
         if gray_coords.size > 0:
             min_r_gray = np.min(gray_coords[:, 0])
             max_r_gray = np.max(gray_coords[:, 0])
             if min_r_gray > rows[0] and max_r_gray < rows[1]:
                 return 'horizontal', rows[0], rows[1]

    # Check if the top 2 col counts are significantly higher and form potential lines
    if len(col_zero_counts) >= 2 and col_zero_counts[0][1] > height * 0.7 and col_zero_counts[1][1] > height * 0.7:
         cols = sorted([col_zero_counts[0][0], col_zero_counts[1][0]])
          # Check if gray is between
         gray_coords = np.argwhere(grid == 5)
         if gray_coords.size > 0:
             min_c_gray = np.min(gray_coords[:, 1])
             max_c_gray = np.max(gray_coords[:, 1])
             if min_c_gray > cols[0] and max_c_gray < cols[1]:
                 return 'vertical', cols[0], cols[1]


    raise ValueError("Could not reliably find two parallel white lines.")


def count_enclosed_gray_pixels(grid, orientation, idx1, idx2):
    """Counts gray pixels strictly between the given lines."""
    count = 0
    if orientation == 'horizontal':
        for r in range(idx1 + 1, idx2):
            for c in range(grid.shape[1]):
                if grid[r, c] == 5:
                    count += 1
    elif orientation == 'vertical':
        for r in range(grid.shape[0]):
            for c in range(idx1 + 1, idx2):
                if grid[r, c] == 5:
                    count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid based on the described rules.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color (orange, 7)
    output_grid = np.full_like(input_np, 7)

    # Find the parallel white lines
    try:
        orientation, idx1, idx2 = find_parallel_white_lines(input_np)
    except ValueError as e:
        print(f"Error finding lines: {e}")
        # Default behavior if lines aren't found? Return input? Or orange grid?
        # Let's return orange grid for now, indicates processing happened but failed finding key features.
        return output_grid.tolist()


    # Count the gray pixels between the lines
    gray_pixel_count = count_enclosed_gray_pixels(input_np, orientation, idx1, idx2)

    # Calculate new line positions
    new_idx1 = idx1 + 1
    new_idx2 = idx2 - 1

    # Calculate the center index for the new gray line
    # Ensure it stays within bounds if lines become adjacent
    center_idx = math.floor((new_idx1 + new_idx2) / 2)

    # Draw the moved white lines onto the output grid
    if orientation == 'horizontal':
        if new_idx1 >= 0 and new_idx1 < height:
             output_grid[new_idx1, :] = 0
        if new_idx2 >= 0 and new_idx2 < height and new_idx1 != new_idx2: # Avoid overwriting if they meet
             output_grid[new_idx2, :] = 0
    elif orientation == 'vertical':
         if new_idx1 >= 0 and new_idx1 < width:
             output_grid[:, new_idx1] = 0
         if new_idx2 >= 0 and new_idx2 < width and new_idx1 != new_idx2:
             output_grid[:, new_idx2] = 0
             
    # Check if lines have merged or crossed (new_idx1 >= new_idx2)
    # If they meet, the center is ambiguous, maybe just draw white lines? Example 1 output suggests center pixel is orange if lines meet vertically.
    # Example 2 output suggests center row becomes white if lines meet horizontally.
    # Let's stick to the plan: if they meet or cross, maybe there's no gray line.
    # The derived NL program doesn't explicitly cover lines meeting/crossing.
    # Let's assume valid inputs always have space after moving lines inwards. idx2 > idx1 + 1 initially.
    # Thus new_idx2 will always be > new_idx1.

    # Determine and draw the new gray line
    if orientation == 'vertical':
        # Output line is vertical
        line_len = height - 2
        if line_len <= 0: # Handle very small grids
             line_len = 1 if height > 0 else 0

        start_row = math.floor((height - line_len) / 2)
        end_row = start_row + line_len
        
        # Ensure column index is valid
        if center_idx >= 0 and center_idx < width:
            # Draw the gray line, ensuring row indices are valid
            actual_start_row = max(0, start_row)
            actual_end_row = min(height, end_row)
            if actual_start_row < actual_end_row: # Check if there's anything to draw
                 output_grid[actual_start_row:actual_end_row, center_idx] = 5

    elif orientation == 'horizontal':
        # Output line is horizontal
        line_len = gray_pixel_count
        if line_len <= 0: # Handle cases with no gray pixels found
             line_len = 0

        start_col = math.floor((width - line_len) / 2)
        end_col = start_col + line_len

         # Ensure row index is valid
        if center_idx >= 0 and center_idx < height:
            # Draw the gray line, ensuring column indices are valid
            actual_start_col = max(0, start_col)
            actual_end_col = min(width, end_col)
            if actual_start_col < actual_end_col: # Check if there's anything to draw
                 output_grid[center_idx, actual_start_col:actual_end_col] = 5
                 
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()