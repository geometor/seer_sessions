import copy

"""
Identify the coordinates of the two cells containing the value 8. 
Determine the bounding box defined by these coordinates (minimum and maximum row and column indices).
Create an output grid, initially identical to the input grid.
Iterate through the cells within the bounding box. If a cell is on the perimeter of the bounding box and its original value in the input grid was 0, change its value in the output grid to 3. 
The original 8s remain unchanged.
"""

def find_coords(grid: list[list[int]], value: int) -> list[tuple[int, int]]:
    """Finds the coordinates (row, col) of all cells with the given value."""
    coords = []
    for r, row in enumerate(grid):
        for c, cell_value in enumerate(row):
            if cell_value == value:
                coords.append((r, c))
    return coords

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Draws the perimeter of a bounding box defined by two '8' cells with the value '3', 
    leaving the original '8's and other '0's intact.
    """
    # Make a deep copy to avoid modifying the original input grid
    output_grid = copy.deepcopy(input_grid)

    # Find the coordinates of the two '8' anchor points
    anchor_coords = find_coords(input_grid, 8)

    # Ensure exactly two anchors were found (as per problem description)
    if len(anchor_coords) != 2:
        # Handle error or unexpected input if necessary, 
        # for now, just return the original grid if assumption fails
        print("Warning: Expected exactly two '8' values, found:", len(anchor_coords))
        return output_grid 
        
    (r1, c1), (r2, c2) = anchor_coords

    # Determine the bounding box coordinates
    min_r = min(r1, r2)
    max_r = max(r1, r2)
    min_c = min(c1, c2)
    max_c = max(c1, c2)

    # Iterate through the bounding box area
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check if the current cell is on the perimeter
            is_on_perimeter = (r == min_r or r == max_r or c == min_c or c == max_c)

            # Check if the cell in the *original* input was 0
            is_originally_zero = (input_grid[r][c] == 0)

            # If it's on the perimeter and was originally 0, change it to 3 in the output
            if is_on_perimeter and is_originally_zero:
                output_grid[r][c] = 3

    return output_grid