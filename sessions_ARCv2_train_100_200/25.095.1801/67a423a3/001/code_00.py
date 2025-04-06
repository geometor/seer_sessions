import copy
from collections import Counter

"""
Identifies the intersection point of a unique horizontal and a unique vertical line segment of non-zero digits in a grid. 
Then, modifies the grid by changing the values of the 8 cells immediately surrounding the intersection point to 4, 
while leaving the intersection point itself and all other cells unchanged.
"""

def find_intersection(grid: list[list[int]]) -> tuple[int, int] | None:
    """
    Finds the intersection point of the horizontal and vertical non-zero lines.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    non_zero_rows = []
    non_zero_cols = []

    # Collect coordinates of all non-zero cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:
                non_zero_rows.append(r)
                non_zero_cols.append(c)

    if not non_zero_rows or not non_zero_cols:
        return None # Should not happen based on problem description, but good practice

    # Count frequencies of row and column indices among non-zero cells
    row_counts = Counter(non_zero_rows)
    col_counts = Counter(non_zero_cols)

    # The intersection row is the one with the most non-zero entries (part of the horizontal line)
    # The intersection column is the one with the most non-zero entries (part of the vertical line)
    # Use max(..., key=counts.get) to find the element with the highest count
    intersection_row = max(row_counts, key=row_counts.get)
    intersection_col = max(col_counts, key=col_counts.get)
    
    # Validate that the cell at the determined intersection is actually non-zero
    # This implicitly checks if the most frequent row/col truly corresponds to the lines
    if grid[intersection_row][intersection_col] != 0:
        return intersection_row, intersection_col
    else:
         # Fallback/alternative logic if the simple max frequency doesn't work
         # Find the row index that appears in most columns containing non-zero numbers
         # Find the col index that appears in most rows containing non-zero numbers
         # This handles cases where one line might be short or density varies
         h_line_row = -1
         v_line_col = -1
         max_h_count = 0
         for r in range(rows):
             count = sum(1 for c in range(cols) if grid[r][c] != 0)
             if count > max_h_count:
                 max_h_count = count
                 h_line_row = r

         max_v_count = 0
         for c in range(cols):
             count = sum(1 for r in range(rows) if grid[r][c] != 0)
             if count > max_v_count:
                 max_v_count = count
                 v_line_col = c
                 
         if h_line_row != -1 and v_line_col != -1 and grid[h_line_row][v_line_col] != 0:
             return h_line_row, v_line_col
             
    return None # Return None if no clear intersection is found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rule.
    """
    # Ensure the input grid is not empty
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)

    # Find the intersection point
    intersection_coords = find_intersection(input_grid)

    if intersection_coords is None:
        # If no intersection is found (e.g., empty grid or no lines), return the original grid
        return output_grid

    ix, iy = intersection_coords

    # Iterate through the 3x3 neighborhood centered at the intersection point
    for r_offset in range(-1, 2): # -1, 0, 1
        for c_offset in range(-1, 2): # -1, 0, 1
            # Calculate the coordinates of the neighbor cell
            r = ix + r_offset
            c = iy + c_offset

            # Check if the neighbor cell is within the grid boundaries
            if 0 <= r < rows and 0 <= c < cols:
                # Check if the current cell is NOT the intersection point itself
                if r != ix or c != iy:
                    # Update the value in the output grid to 4
                    output_grid[r][c] = 4

    # Return the modified output grid
    return output_grid