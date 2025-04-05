import numpy as np

"""
Transformation Rule:

1. Identify distinct structures in the input grid. Each structure consists of:
   a. A horizontal line segment of a specific color (L).
   b. A single cell of a different color (S), located exactly one row above the row of the horizontal line L. The column position of S relative to L does not affect the output placement.

2. For each identified structure (S, L):
   a. Find the center column (c_center) of the horizontal line L.
      - If the line has length 'len', the start column 'c_start', the center is at c_start + (len - 1) // 2.
   b. Erase the original single cell S from the grid (set its value to 0).
   c. Draw a vertical line segment of color S, three cells high, centered vertically on the original row of line L, and horizontally at the calculated center column c_center. The vertical line occupies cells (r_l - 1, c_center), (r_l, c_center), and (r_l + 1, c_center), where r_l is the row index of the horizontal line L.

3. The output grid contains the modified structures along with any unchanged parts of the input grid.
"""

def find_horizontal_lines(grid):
    """
    Finds all horizontal line segments in the grid.

    Args:
        grid: A numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary represents a line
        and contains 'color', 'row', 'start_col', 'end_col'.
    """
    lines = []
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                start_col = c
                end_col = c
                # Explore horizontally to the right
                while end_col + 1 < cols and grid[r, end_col + 1] == color and not visited[r, end_col+1] :
                    end_col += 1
                
                # Check if it's truly horizontal (no same-color neighbors vertically)
                # And length > 1 
                is_line = True
                # Actually, the examples show lines of length 1 are possible if associated with a marker.
                # The critical factor is the marker *above* it. Let's assume any contiguous horizontal segment is a potential line base.
                # If length is 1, c_start = c_end.
                
                # Simplified: Find any horizontal segment.
                # Mark visited cells for this segment
                for k in range(start_col, end_col + 1):
                    visited[r, k] = True
                
                # Store the found segment
                lines.append({
                    'color': color,
                    'row': r,
                    'start_col': start_col,
                    'end_col': end_col
                })
                # Continue scanning from end_col + 1 in the outer loop
                # The outer loop variable 'c' will be incremented naturally.

    return lines

def find_potential_markers(grid):
    """
    Finds all non-zero cells that could potentially be markers (S).

    Args:
        grid: A numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary contains 'color', 'row', 'col'.
    """
    markers = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                markers.append({'color': grid[r, c], 'row': r, 'col': c})
    return markers


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier manipulation
    np_grid = np.array(input_grid, dtype=int)
    output_grid = np_grid.copy()
    rows, cols = np_grid.shape

    # Find all potential horizontal lines (L candidates)
    lines = find_horizontal_lines(np_grid)
    
    # Find all potential single cell markers (S candidates)
    markers = find_potential_markers(np_grid)

    # Iterate through markers and lines to find valid (S, L) pairs
    for marker in markers:
        s_color = marker['color']
        r_s = marker['row']
        c_s = marker['col']

        for line in lines:
            l_color = line['color']
            r_l = line['row']
            c_start = line['start_col']
            c_end = line['end_col']

            # Check for the structural relationship:
            # 1. Marker color S is different from Line color L
            # 2. Marker S is exactly one row above Line L (r_s = r_l - 1)
            if s_color != l_color and r_s == r_l - 1:
                
                # This marker corresponds to this line - perform the transformation
                
                # Calculate the center column of the line L
                length = c_end - c_start + 1
                c_center = c_start + (length - 1) // 2

                # Erase the original marker S in the output grid
                # Check bounds just in case, though r_s should be valid if found
                if 0 <= r_s < rows and 0 <= c_s < cols:
                     output_grid[r_s, c_s] = 0 # Erase original S

                # Draw the new vertical line of color S in the output grid
                # Ensure drawing coordinates are within grid bounds
                
                # Cell above the line's original row
                if 0 <= r_l - 1 < rows and 0 <= c_center < cols:
                    output_grid[r_l - 1, c_center] = s_color
                
                # Cell on the line's original row
                if 0 <= r_l < rows and 0 <= c_center < cols:
                    output_grid[r_l, c_center] = s_color
                    
                # Cell below the line's original row
                if 0 <= r_l + 1 < rows and 0 <= c_center < cols:
                    output_grid[r_l + 1, c_center] = s_color
                    
                # Found the corresponding line for this marker, no need to check other lines for *this specific marker*
                # (Assumption: one marker S belongs to at most one line L directly below it)
                # Although, if multiple lines were below, the logic would apply the rule for each. Let's stick to the examples.
                # If we assume one S per L structure, we could 'break' here, but let's allow for potential complex cases unless proven otherwise.

    # Convert the result back to a list of lists
    return output_grid.tolist()
