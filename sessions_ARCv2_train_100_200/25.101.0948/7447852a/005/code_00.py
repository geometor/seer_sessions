import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selectively fills segments of white pixels (0) with yellow (4) based on 
    the row index, segment type (edge or internal), the interval length defined 
    by red pixels (2) or grid edges, and the segment's ordinal position among 
    other qualifying internal segments in the row.

    Rules:
    - Row 0 (Top Row):
        - Finds all internal segments between red pixels with an interval length of 4 (i.e., 3 white pixels between them). Let the count be 'count'.
        - Fills the right edge segment if the distance from the last red pixel to the right edge is 1 AND 'count' is greater than 2.
        - If 'count' is 2 or more, fills the second qualifying internal segment found.
    - Row 1 (Middle Row):
        - Fills the left edge segment if the distance from the left edge to the first red pixel is 1.
        - Finds all internal segments between red pixels with an interval length of 2 (i.e., 1 white pixel between them). Let the count be 'count'.
        - If 'count' is 3 or more, fills the third qualifying internal segment. 
        - If 'count' is 6 or more, also fills the sixth qualifying internal segment.
    - Row 2 (Bottom Row):
        - Fills the left edge segment if the distance from the left edge to the first red pixel is 2.
        - Finds all internal segments between red pixels with an interval length of 4 (i.e., 3 white pixels between them). Let the count be 'count'.
        - If 'count' is 3 or more, fills the third qualifying internal segment found.
    """
    
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    height = len(output_grid)
    if height == 0:
        return output_grid # Handle empty grid
    width = len(output_grid[0])
    if width == 0:
        return output_grid # Handle empty row

    # Iterate through each row (assumed height is 3 based on examples)
    for r in range(height):
        # Find the column indices of all red (2) pixels in the current row
        red_cols = [c for c, pixel in enumerate(output_grid[r]) if pixel == 2]

        # If no red pixels in the row, nothing to do for this row
        if not red_cols:
            continue

        # --- Process Internal Segments (Identify Qualifiers First) ---
        qualifying_intervals = [] # Stores (c1, c2) tuples for qualifying intervals
        
        # Iterate through consecutive pairs of red pixels to find internal segments
        for i in range(len(red_cols) - 1):
            c1 = red_cols[i]
            c2 = red_cols[i+1]
            interval_length = c2 - c1 # Distance between the two red pixels

            # Check if the interval length matches the requirement for the current row
            if (r == 0 or r == 2) and interval_length == 4:
                qualifying_intervals.append((c1, c2))
            elif r == 1 and interval_length == 2:
                qualifying_intervals.append((c1, c2))

        # Get the count of qualifying internal intervals
        count = len(qualifying_intervals)

        # --- Process Edge Segments ---
        c_first = red_cols[0]
        c_last = red_cols[-1]

        # 1. Left Edge Segment
        if c_first > 0: # Check if there's space before the first red pixel
            d_left = c_first # Distance from left edge to first red pixel (interval length)
            if r == 1 and d_left == 1:
                for c in range(c_first):
                    output_grid[r][c] = 4 # Fill with yellow
            elif r == 2 and d_left == 2:
                for c in range(c_first):
                    output_grid[r][c] = 4 # Fill with yellow

        # 2. Right Edge Segment (conditional on internal segment count for r=0)
        if c_last < width - 1: # Check if there's space after the last red pixel
            d_right = (width - 1) - c_last # Distance from last red pixel to right edge (interval length)
            # Apply fill rule for r=0: distance is 1 AND count of length-4 internal intervals > 2
            if r == 0 and d_right == 1 and count > 2:
                for c in range(c_last + 1, width):
                    output_grid[r][c] = 4 # Fill with yellow

        # --- Fill Specific Internal Segments ---
        # Fill based on row index 'r' and qualifying interval 'count'

        if r == 0 and count >= 2:
            # Fill the 2nd qualifying interval (index 1)
            c1, c2 = qualifying_intervals[1]
            for c in range(c1 + 1, c2): # Fill pixels between c1 and c2
                output_grid[r][c] = 4
        elif r == 1:
            if count >= 3:
                # Fill the 3rd qualifying interval (index 2)
                c1, c2 = qualifying_intervals[2] 
                # Interval length is 2, so only one pixel to fill
                output_grid[r][c1 + 1] = 4 
            if count >= 6:
                 # Fill the 6th qualifying interval (index 5)
                c1, c2 = qualifying_intervals[5]
                # Interval length is 2, so only one pixel to fill
                output_grid[r][c1 + 1] = 4
        elif r == 2 and count >= 3:
            # Fill the 3rd qualifying interval (index 2)
            c1, c2 = qualifying_intervals[2]
            for c in range(c1 + 1, c2): # Fill pixels between c1 and c2
                output_grid[r][c] = 4

    return output_grid