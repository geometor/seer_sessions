import numpy as np
from collections import defaultdict
import bisect

"""
Recolors azure (8) regions based on mapping vertical color lines to zones defined by the unique start columns of azure segments.

1.  Initialize an output grid of the same dimensions as the input grid, filled with white (0).
2.  Find all full-height vertical lines of a single, non-white (0), non-azure (8) color on the left. Sort them left-to-right by column index. Let N be the count of these lines.
3.  Find all horizontal segments of contiguous azure (8) pixels.
4.  Collect the unique starting column indices from these azure segments and sort them. Let M be the count of unique start columns.
5.  If N > 0 and N equals M, proceed. Otherwise, return the white grid.
6.  For each pixel (r, c) in the input grid:
    a.  If the pixel is azure (8):
        i.  Find the index `k` of the largest unique start column value that is less than or equal to `c`.
        ii. Get the color `C` from the k-th vertical line (using the same index `k`).
        iii. Set `OutputGrid[r, c]` to color `C`.
7.  Return the output grid.
"""

def find_vertical_lines(input_grid):
    """
    Finds full-height vertical lines of a single non-white(0), non-azure(8) color.
    Returns a list of dicts {'color': c, 'col_index': i}, sorted by col_index.
    """
    height, width = input_grid.shape
    lines = []
    if height == 0: # Handle empty grid case
        return lines

    for c in range(width):
        col = input_grid[:, c]
        first_color = col[0]
        # Check if the first pixel is a potential line color and if the column is non-empty
        if height > 0 and first_color != 0 and first_color != 8:
            is_line = True
            # Check if all pixels in the column match the first pixel's color
            for r in range(1, height):
                if col[r] != first_color:
                    is_line = False
                    break
            if is_line:
                lines.append({'color': first_color, 'col_index': c})
        # Optimization: If we encounter an azure pixel, we can assume lines won't appear further right based on examples
        # although this isn't strictly necessary based on the logic. Let's stick to the simpler rule first.
        # if height > 0 and 8 in col:
        #      break # Assuming lines are always fully to the left of any azure pixel

    # Sort lines by column index (already processed in order, but explicit sort is safer)
    lines.sort(key=lambda x: x['col_index'])
    return lines

def find_azure_segments(input_grid):
    """
    Finds all maximal contiguous horizontal segments of azure (8) pixels.
    Returns a list of tuples: (row_index, start_col, end_col).
    """
    height, width = input_grid.shape
    segments = []
    for r in range(height):
        c = 0
        while c < width:
            # Find the start of an azure segment
            if input_grid[r, c] == 8:
                start_col = c
                # Find the end of the segment
                while c + 1 < width and input_grid[r, c + 1] == 8:
                    c += 1
                end_col = c
                segments.append((r, start_col, end_col))
            c += 1
    return segments

def get_unique_sorted_start_cols(segments):
    """
    Extracts unique start column indices from segments and sorts them.
    Returns a sorted list of unique start column indices.
    """
    if not segments:
        return []
    start_cols = set(s[1] for s in segments)
    return sorted(list(start_cols))


def transform(input_grid):
    """
    Transforms the input grid by recoloring azure pixels based on vertical color lines
    and zones defined by unique azure segment start columns.
    """
    input_grid_np = np.array(input_grid, dtype=np.int64)
    height, width = input_grid_np.shape
    
    # 1. Initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid_np)

    # 2. Identify & Sort Color Lines
    vertical_lines = find_vertical_lines(input_grid_np)
    N = len(vertical_lines)

    # 3. Identify Azure Horizontal Segments
    azure_segments = find_azure_segments(input_grid_np)

    # 4. Get Unique Sorted Azure Start Columns
    unique_start_cols = get_unique_sorted_start_cols(azure_segments)
    M = len(unique_start_cols)

    # 5. Condition Check: N > 0 and N == M
    if N > 0 and N == M:
        # 6. Coloring based on zones
        for r in range(height):
            for c in range(width):
                # a. Check if pixel is azure
                if input_grid_np[r, c] == 8:
                    # i. Find the index k of the largest start column <= c
                    # `bisect_right` finds the insertion point for c in unique_start_cols.
                    # Subtracting 1 gives the index of the rightmost element <= c.
                    k = bisect.bisect_right(unique_start_cols, c) - 1
                    
                    # Ensure k is a valid index (should be if c came from an azure segment)
                    if 0 <= k < N:
                         # ii. Get the color C from the k-th vertical line
                         line_color = vertical_lines[k]['color']
                         # iii. Set output pixel color
                         output_grid[r, c] = line_color
                    # else: This case implies c is less than the smallest start_col,
                    # which shouldn't happen for an azure pixel if M > 0.
                    # Or k >= N which shouldn't happen if N == M.
                    # If it does, pixel remains white (0).

    # 7. Return the final output grid as a list of lists
    return output_grid.tolist()