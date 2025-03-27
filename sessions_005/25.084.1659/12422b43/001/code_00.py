import numpy as np
import collections

"""
Transformation Rule:

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the pixels belonging to the gray (5) vertical bar in the first column (column 0).
3.  Find all colored pixels (not white 0 and not gray 5) in the input grid.
4.  Identify which of these colored pixels are adjacent (horizontally, vertically, or diagonally) to any pixel of the gray bar.
5.  If no colored pixels are adjacent to the gray bar, return the unchanged input grid copy.
6.  Determine the minimum (`min_row_sel`) and maximum (`max_row_sel`) row indices spanned by these adjacent colored pixels.
7.  Define the "pattern block" as the rectangular region of the *input* grid covering rows from `min_row_sel` to `max_row_sel` and all columns *except* the first one (column 0).
8.  Determine the maximum row index (`max_row_orig`) occupied by any non-white (0), non-gray (5) pixel in the *entire* input grid.
9.  Set the starting destination row for copying the pattern, `current_dest_row`, to be `max_row_orig + 1`.
10. Calculate the height of the pattern block.
11. Repeatedly copy the pattern block vertically downwards into the output grid, starting at `current_dest_row`. Each subsequent copy starts immediately below the previous one. Copying stops when the bottom of the grid is reached. If a copy would extend beyond the grid boundary, only the part that fits within the grid is copied.
12. Return the modified output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Replicates a pattern derived from objects adjacent to a leftmost gray bar
    downwards into the empty space of the grid.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify gray bar pixels in column 0
    gray_bar_coords = set()
    for r in range(height):
        if input_grid[r, 0] == 5:
            gray_bar_coords.add((r, 0))

    # If no gray bar, maybe return original (though examples imply it exists)
    if not gray_bar_coords:
        # According to examples, gray bar seems mandatory.
        # If it could be missing, this would be the place to handle it.
        # For now, assume it exists based on training data.
        pass # Proceed assuming it exists or the logic below handles empty sets gracefully.

    # 2. Find all non-white (0), non-gray (5) pixels
    colored_pixels = set()
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] not in [0, 5]:
                colored_pixels.add((r, c))

    # 3. Identify colored pixels adjacent to the gray bar
    adjacent_colored_pixels = set()
    neighbor_offsets = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

    for r, c in colored_pixels:
        # Only consider pixels not in the first column for adjacency check source
        # (though colored pixels are defined as non-gray, so c==0 shouldn't happen anyway)
        if c == 0: continue 
        
        is_adj = False
        for dr, dc in neighbor_offsets:
            nr, nc = r + dr, c + dc
            # Check if neighbor coordinates are within bounds and are part of the gray bar
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) in gray_bar_coords:
                is_adj = True
                break
        if is_adj:
            adjacent_colored_pixels.add((r, c))

    # 4. If no adjacent colored pixels, return the original grid copy
    if not adjacent_colored_pixels:
        return output_grid

    # 5. Determine the row range of adjacent colored pixels
    selected_rows = {r for r, c in adjacent_colored_pixels}
    min_row_sel = min(selected_rows)
    max_row_sel = max(selected_rows)

    # 6. Define the pattern block (excluding column 0)
    # Ensure width > 1 before slicing column 1 onwards
    if width <= 1:
         # If only one column, pattern block is empty, nothing to copy
         return output_grid
         
    pattern_block = input_grid[min_row_sel : max_row_sel + 1, 1:width]
    pattern_height = pattern_block.shape[0]

    if pattern_height == 0:
         # Should not happen if adjacent_colored_pixels is not empty, but safety check
         return output_grid

    # 7. Determine the max row index of any original non-white, non-gray pixel
    if colored_pixels:
        max_row_orig = max(r for r, c in colored_pixels)
    else:
        # This case should not be reachable if adjacent_colored_pixels is not empty
        max_row_orig = -1 

    # 8. Set the starting row for the first copy
    current_dest_row = max_row_orig + 1

    # 9. Replicate the pattern downwards
    while current_dest_row < height:
        # Calculate how many rows of the pattern can fit
        rows_to_copy = min(pattern_height, height - current_dest_row)

        # If no rows can be copied, stop
        if rows_to_copy <= 0:
            break
            
        # Get the slice of the pattern block to copy
        source_block_slice = pattern_block[:rows_to_copy, :]

        # Determine destination slice in the output grid
        dest_slice_rows = slice(current_dest_row, current_dest_row + rows_to_copy)
        dest_slice_cols = slice(1, width) # Copy to columns 1 onwards

        # Perform the copy
        output_grid[dest_slice_rows, dest_slice_cols] = source_block_slice

        # Update the destination row for the next potential copy
        current_dest_row += pattern_height

    # 10. Return the modified grid
    return output_grid