```python
import copy

"""
Transforms an input grid by finding two cells marked with '8', drawing a digital 
straight line (using Bresenham's algorithm) between them, and marking the 
intermediate cells of this line with '3'. The original '8' markers remain unchanged.
"""

def bresenham_line(r1: int, c1: int, r2: int, c2: int) -> list[tuple[int, int]]:
    """
    Calculates the grid coordinates for a line between (r1, c1) and (r2, c2) 
    using Bresenham's line algorithm.

    Args:
        r1: Row coordinate of the starting point.
        c1: Column coordinate of the starting point.
        r2: Row coordinate of the ending point.
        c2: Column coordinate of the ending point.

    Returns:
        A list of (row, col) tuples representing the cells on the line, 
        including the start and end points.
    """
    points = []
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    r, c = r1, c1
    step_r = 1 if r1 < r2 else -1
    step_c = 1 if c1 < c2 else -1

    points.append((r, c))

    if dr > dc: # Steep line (more change in row)
        error = dr // 2
        while r != r2:
            error -= dc
            if error < 0:
                c += step_c
                error += dr
            r += step_r
            points.append((r, c))
    else: # Shallow line (more change in column) or diagonal
        error = dc // 2
        while c != c2:
            error -= dr
            if error < 0:
                r += step_r
                error += dc
            c += step_c
            points.append((r, c))
            
    # Ensure the last point is included if the loop condition stopped it
    # (This handles cases where the loop terminates exactly on the target,
    # but Bresenham often calculates one step at a time).
    # Re-checking the core logic, the standard algorithm usually ensures
    # the endpoint is reached correctly by the loop condition or the final point add.
    # Let's stick to the standard structure first. If the endpoint is missed, we'll adjust.
    # After testing the logic, the standard loop covers the endpoint correctly.

    return points

def find_markers(grid: list[list[int]], marker_value: int) -> list[tuple[int, int]]:
    """
    Finds all occurrences of a specific marker value in the grid.

    Args:
        grid: The 2D list representing the grid.
        marker_value: The integer value to search for.

    Returns:
        A list of (row, col) tuples where the marker value was found.
    """
    locations = []
    num_rows = len(grid)
    if num_rows == 0:
        return []
    num_cols = len(grid[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r][c] == marker_value:
                locations.append((r, c))
    return locations

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)

    # Find the locations of the two '8' markers
    marker_locations = find_markers(input_grid, 8)

    # Ensure exactly two markers were found
    if len(marker_locations) != 2:
        # Handle error case or return input/output grid as is, depending on requirements.
        # For this problem, we assume exactly two '8's exist based on examples.
        # Returning the current output grid (copy of input) if assumption fails.
        print(f"Warning: Expected 2 markers (8), but found {len(marker_locations)}. Returning input copy.")
        return output_grid 

    p1, p2 = marker_locations
    r1, c1 = p1
    r2, c2 = p2

    # Calculate the points on the line between the two markers
    line_points = bresenham_line(r1, c1, r2, c2)

    # Draw the line on the output grid using '3'
    for r, c in line_points:
        # Check grid bounds just in case, though Bresenham should stay within reasonable limits
        # if start/end points are valid.
        if 0 <= r < len(output_grid) and 0 <= c < len(output_grid[0]):
             # Only change the cell to '3' if it's not one of the original '8' markers
            if output_grid[r][c] != 8:
                 output_grid[r][c] = 3
        # else:
            # Optional: Handle or log points falling outside grid bounds if that's possible/a concern

    return output_grid
```