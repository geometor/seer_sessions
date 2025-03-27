import numpy as np

"""
The transformation rule depends on whether the input grid contains orange (7) or azure (8) pixels.

1.  **Check for presence of 7 or 8:** Scan the input grid to see if any pixel has the value 7 or 8.

2.  **Identify Yellow (4) Markers:** Find the coordinates (row, column) of all yellow pixels (value 4).

3.  **Determine Number of Rows with Yellow Markers:** Count how many distinct rows contain at least one yellow marker.

4.  **Apply Transformation based on Conditions:**

    a.  **If 7 or 8 IS present in the input:**
        - The transformation maps orange (7) to magenta (6) and azure (8) to white (0).
        - This transformation is applied only *between* pairs of yellow markers on the same row.
        - For each row containing two or more yellow markers, find the leftmost (min column index) and rightmost (max column index) yellow markers. Apply the 7->6 and 8->0 mapping to all pixels in that row strictly between these column indices.

    b.  **If 7 or 8 is NOT present in the input:**
        - The transformation maps white (0) to azure (8) and magenta (6) to orange (7).
        - The application area depends on the number of rows containing yellow markers:
            i.  **If exactly ONE row contains yellow markers:**
                - Find that row.
                - Find the leftmost (min column index) and rightmost (max column index) yellow markers in that row.
                - Apply the 0->8 and 6->7 mapping to all pixels in that row strictly between these column indices.
            ii. **If MORE THAN ONE row contains yellow markers:**
                - Identify all rows (`R_yellow`) that contain any yellow markers.
                - Identify all columns (`C_yellow`) that contain any yellow markers.
                - Apply the 0->8 and 6->7 mapping to all pixels `(r, c)` such that the row index `r` is NOT in `R_yellow` AND the column index `c` IS in `C_yellow`.

5.  **Output:** The modified grid is the output. Pixels not matching the transformation criteria or application area remain unchanged.
"""

def transform(input_grid):
    """
    Applies a transformation to the input grid based on the presence of colors 7/8
    and the positions of color 4 markers.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Check if color 7 or 8 is present
    has_7_or_8 = np.any((input_np == 7) | (input_np == 8))

    # Find yellow marker positions and rows/columns containing them
    yellow_coords = np.argwhere(input_np == 4)
    yellow_rows = set(r for r, c in yellow_coords)
    yellow_cols = set(c for r, c in yellow_coords)
    num_yellow_rows = len(yellow_rows)

    if has_7_or_8:
        # Rule A: 7 -> 6, 8 -> 0, between horizontal yellow pairs
        for r in range(height):
            row_yellow_cols = [c for yr, c in yellow_coords if yr == r]
            if len(row_yellow_cols) >= 2:
                c_min = min(row_yellow_cols)
                c_max = max(row_yellow_cols)
                for c in range(c_min + 1, c_max):
                    if output_np[r, c] == 7:
                        output_np[r, c] = 6
                    elif output_np[r, c] == 8:
                        output_np[r, c] = 0
    else:
        # Rule B: 0 -> 8, 6 -> 7
        if num_yellow_rows == 1:
            # Apply only on the single row with yellow markers, between them
            r = list(yellow_rows)[0] # The single row index
            row_yellow_cols = [c for yr, c in yellow_coords if yr == r]
            if len(row_yellow_cols) >= 2:
                 c_min = min(row_yellow_cols)
                 c_max = max(row_yellow_cols)
                 for c in range(c_min + 1, c_max):
                    if output_np[r, c] == 0:
                        output_np[r, c] = 8
                    elif output_np[r, c] == 6:
                        output_np[r, c] = 7
        elif num_yellow_rows > 1:
             # Apply in columns with yellow markers, but only in rows without yellow markers
            for r in range(height):
                # Skip rows that contain yellow markers
                if r in yellow_rows:
                    continue
                for c in range(width):
                    # Apply only in columns that contain yellow markers
                    if c in yellow_cols:
                        if output_np[r, c] == 0:
                            output_np[r, c] = 8
                        elif output_np[r, c] == 6:
                            output_np[r, c] = 7

    return output_np.tolist()