"""
1.  **Find Topmost Azure Segment:** Examine the input grid row by row, starting from the top. Identify the *first* (topmost) row that contains azure (8) pixels. Within this row, find the starting column index of the *first* continuous azure segment. Determine the *actual* width of this continuous azure segment (how many contiguous azure pixels are there, starting from the start column).  The maximum width to consider is 3.
2.  **Create Output Grid:** Create a 3x3 output grid and initialize all its cells with the value 0 (white).
3. **Fill First Row Based on width from Topmost Azure**: Starting from the first column (index 0) of the *top row* of the output grid, place azure (8) pixels, moving from left to right. The maximum number of azure pixels to place on the top row is equal to width of the continuous azure section on the top-most azure row, as calculated in step 1. The remaining columns in the top row, if any, should remain 0 (white).
4. **Check next row, place matching segment:** After placing azure pixels on the top row, if the *actual* azure width is greater than 0, check the row below the top-most azure row. If the next row has the same continuous azure segment width (step 1) and starts at the same column, then proceed to fill remaining grid, excluding the first row already filled, with the continuous azure segment. Continue until either all the remaining slots are filled or the segment is done, whichever comes first.
5. **Result**: The 3x3 output grid contains the extracted azure pixels.
"""

import numpy as np

def get_top_azure_row_and_width(grid):
    """Finds the topmost row with azure and the width of its continuous segment."""
    for r, row in enumerate(grid):
        if 8 in row:
            azure_cols = np.where(row == 8)[0]
            if len(azure_cols) > 0:
                # find the continuous segment width
                width = 0
                start_col = azure_cols[0]
                for col in azure_cols:
                    if col == start_col + width:
                        width +=1
                    else:
                        break

                return r, start_col, width # return actual width
    return 0, 0, 0

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # find top azure row index, left most col, and the continuous azure segment width
    top_azure_row_index, left_most_col, azure_width = get_top_azure_row_and_width(input_grid)

    # Extract up to azure_width azure pixels, from left to right, and place in output, up to max width of 3
    for output_col in range(min(azure_width,3)):
        output_grid[0, output_col] = 8

    # handle edge case
    if azure_width > 0 :
        next_row = top_azure_row_index + 1
        if next_row < len(input_grid):
            next_row_azure_cols = np.where(input_grid[next_row] == 8)[0]
            # check to see if we have a segment of matching width
            if len(next_row_azure_cols) >= azure_width:
                match = True
                for i in range(min(azure_width,3)): # limit range to max width of 3
                    if next_row_azure_cols[i] != left_most_col + i:
                        match = False
                        break
                if match: # place the segment in output
                    for output_col in range(min(azure_width,3)): # use actual width, max 3
                        placed = False
                        for r in range(1,3): # skip top row
                            for c in range(3):
                                if output_grid[r,c] == 0 and not placed:
                                    output_grid[r,c] = 8
                                    placed = True

    return output_grid