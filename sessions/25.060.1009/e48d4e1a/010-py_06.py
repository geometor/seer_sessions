"""
1.  **Remove Gray:** Eliminate all gray (color 5) pixels from the input grid, replacing them with black (color 0) pixels.

2.  **Identify Red Segments:** Identify all contiguous red (color 2) segments. A segment is a set of one or more adjacent red pixels in either a horizontal or vertical line.

3.  **Calculate Shifts:** For each red segment:
    *   Determine the segment's orientation (horizontal or vertical).
    *   Determine the presence and position of gray pixels relative to each red segment.
        *   If the segment is horizontal, calculate how many rows of gray pixels were *above* it in the input grid. This is the vertical shift amount.
        *   If the segment is vertical, calculate how many columns of gray pixels were to the *left* of it in the input grid. This is the horizontal shift amount.

4.  **Apply Shifts:** Create a copy of the grid *after* gray removal. For each red segment in this new grid, apply the calculated shift.
    * Move horizontal segments *up* by their vertical shift amount.
    * Move vertical segments *left* by their horizontal shift amount.
5. **Preserve**: If a pixel is not grey and not a moved red segment, its value from the input is preserved in the output.
"""

import numpy as np

def remove_color(grid, color):
    """Removes all pixels of a specified color from the grid."""
    return np.where(grid == color, 0, grid)

def find_red_segments(grid):
    """Identifies all contiguous red segments (horizontal or vertical)."""
    rows, cols = grid.shape
    segments = []
    visited = np.zeros((rows, cols), dtype=bool)

    def is_red(r, c):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == 2

    def dfs(r, c, segment, orientation):
        if not is_red(r, c) or visited[r, c]:
            return
        visited[r, c] = True
        segment.append((r, c))

        if orientation == 'horizontal':
            dfs(r, c + 1, segment, orientation)  # Check right
        elif orientation == 'vertical':
            dfs(r + 1, c, segment, orientation)  # Check down

    for r in range(rows):
        for c in range(cols):
            if is_red(r, c) and not visited[r, c]:
                # Check horizontal first
                if is_red(r, c + 1):
                    segment = []
                    dfs(r, c, segment, 'horizontal')
                    segments.append({'coords': segment, 'orientation': 'horizontal'})
                # Then check vertical
                elif is_red(r + 1, c):
                    segment = []
                    dfs(r, c, segment, 'vertical')
                    segments.append({'coords': segment, 'orientation': 'vertical'})
                # if one pixel segment, add it.
                else:
                    segments.append({'coords': [(r,c)], 'orientation': 'single'})

    return segments

def calculate_shift(grid, segment):
    """Calculates the shift amount for a red segment based on gray pixels."""
    rows, cols = grid.shape
    coords = segment['coords']
    orientation = segment['orientation']

    if orientation == 'horizontal':
        min_row = min(r for r, _ in coords)
        shift_amount = 0
        for r in range(min_row):
            for c in range(cols):  # check full row, since grey can be anywhere
               if grid[r,c] == 5:
                    shift_amount +=1
                    break # only count once per row

        return shift_amount

    elif orientation == 'vertical':
        min_col = min(c for _, c in coords)
        shift_amount = 0
        for c in range(min_col):
             for r in range(rows):   #check full column
                if grid[r,c] == 5:
                    shift_amount+=1
                    break # only count once per col
        return shift_amount
    else: # single pixel segment
        return 0


def transform(input_grid):
    # Remove gray pixels
    grid_no_gray = remove_color(input_grid, 5)

    # initialize output_grid, preserving all non-grey pixels from input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    for r in range(rows):
      for c in range(cols):
        if output_grid[r,c] != 5:
          output_grid[r,c] = input_grid[r,c]
        else:
            output_grid[r,c] = 0 # remove grey


    # Identify red segments
    red_segments = find_red_segments(input_grid)

    # Calculate and apply shifts
    for segment in red_segments:
        shift_amount = calculate_shift(input_grid, segment)
        coords = segment['coords']
        orientation = segment['orientation']


        #clear old positions in output
        for r, c in coords:
            output_grid[r,c] = 0


        if orientation == 'horizontal':
            for r, c in coords:
                new_r = r - shift_amount
                if 0 <= new_r < rows: # Check new position
                    output_grid[new_r, c] = 2

        elif orientation == 'vertical':
            for r, c in coords:
                new_c = c - shift_amount
                if 0 <= new_c < cols:  #check new position
                    output_grid[r, new_c] = 2
        else:  #single pixel
            for r, c in coords:
              output_grid[r,c] = 2 # no shift.


    return output_grid