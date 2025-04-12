```python
import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling segments of white pixels with yellow based on row index and proximity to red pixels.

    The rules for filling white segments with yellow (4) depend on the row index (r) and the distance (interval length)
    between the defining red (2) pixels or between a red pixel and the grid edge:

    - Row 0:
        - Fill right edge segment if distance to edge is 1.
        - Fill internal segment if interval length between red pixels is 4.
    - Row 1:
        - Fill left edge segment if distance to edge is 1.
        - Fill internal segment if interval length between red pixels is 2.
    - Row 2:
        - Fill left edge segment if distance to edge is 2.
        - Fill internal segment if interval length between red pixels is 4.
    """

    # Initialize output_grid as a deep copy of the input grid to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    height = len(output_grid)
    if height == 0:
        return output_grid  # Handle empty grid case
    width = len(output_grid[0])
    if width == 0:
        return output_grid # Handle empty row case


    # Iterate through each row
    for r in range(height):
        # Find the column indices of all red (2) pixels in the current row
        red_cols = [c for c, pixel in enumerate(output_grid[r]) if pixel == 2]

        # If there are no red pixels in the row, continue to the next row
        if not red_cols:
            continue

        # Process segments based on red pixel locations
        
        # 1. Check Left Edge Segment (between column 0 and the first red pixel)
        c_first = red_cols[0]
        if c_first > 0: # Check if there's space before the first red pixel
            d_left = c_first # Distance from left edge to first red pixel
            # Apply row-specific rules for filling the left edge segment
            if r == 1 and d_left == 1:
                for c in range(c_first):
                    output_grid[r][c] = 4 # Fill with yellow
            elif r == 2 and d_left == 2:
                for c in range(c_first):
                     output_grid[r][c] = 4 # Fill with yellow

        # 2. Check Right Edge Segment (between the last red pixel and the last column)
        c_last = red_cols[-1]
        if c_last < width - 1: # Check if there's space after the last red pixel
            d_right = (width - 1) - c_last # Distance from last red pixel to right edge
             # Apply row-specific rules for filling the right edge segment
            if r == 0 and d_right == 1:
                for c in range(c_last + 1, width):
                    output_grid[r][c] = 4 # Fill with yellow

        # 3. Check Internal Segments (between consecutive red pixels)
        for i in range(len(red_cols) - 1):
            c1 = red_cols[i]
            c2 = red_cols[i+1]
            interval_length = c2 - c1 # Distance between the two red pixels
            
            # Check if there are white pixels between the red pixels
            if interval_length > 1:
                # Apply row-specific rules for filling internal segments
                if (r == 0 or r == 2) and interval_length == 4:
                    for c in range(c1 + 1, c2):
                        output_grid[r][c] = 4 # Fill with yellow
                elif r == 1 and interval_length == 2:
                     # interval_length == 2 means only one pixel between c1 and c2
                     output_grid[r][c1 + 1] = 4 # Fill with yellow


    return output_grid
```