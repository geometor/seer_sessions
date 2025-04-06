import copy

"""
Transform an input grid based on the location of a single non-zero element.

1. Find the single non-zero number 'N' and its location (row 'r', column 'c') in the input grid.
2. Determine the grid dimensions (height 'H', width 'W').
3. Create an output grid of the same dimensions, initialized with zeros.
4. Construct a 'pattern row' P of length W: P[j] = 4 if column j has the same parity (even/odd) as column 'c', otherwise P[j] = 0.
5. Fill the first 'r+1' rows (from 0 to r inclusive) of the output grid with this pattern row P.
6. Place the original non-zero number 'N' in the output grid at position (row r+1, column c).
7. Return the modified output grid.
"""

def find_non_zero(grid: list[list[int]]) -> tuple[int, int, int, int, int] | None:
    """
    Finds the first non-zero element in the grid.

    Args:
        grid: The input grid (list of lists of integers).

    Returns:
        A tuple containing (value, row_index, col_index, height, width) 
        if a non-zero element is found, otherwise None.
        Returns height and width for convenience.
    """
    height = len(grid)
    if height == 0:
        return None # Or handle as error
    width = len(grid[0])
    if width == 0:
         return None # Or handle as error
         
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                return value, r, c, height, width
    # Optional: Handle case where no non-zero element is found,
    # though the problem description implies one always exists.
    # For now, assume one exists based on examples.
    # Returning dimensions even if no non-zero is found might be useful
    # return None, -1, -1, height, width # Example of handling no non-zero
    return 0, -1, -1, height, width # Return 0 value if none found, although problem implies one exists

def create_pattern_row(width: int, base_col_parity: int) -> list[int]:
    """
    Creates the pattern row based on grid width and column parity.

    Args:
        width: The width of the grid.
        base_col_parity: The parity (0 for even, 1 for odd) of the 
                         original non-zero element's column.

    Returns:
        A list representing the pattern row (e.g., [4, 0, 4, 0, 4]).
    """
    pattern_row = [0] * width
    for j in range(width):
        if j % 2 == base_col_parity:
            pattern_row[j] = 4
    return pattern_row

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Moves the single non-zero element down one row and fills rows above
    its original position with a pattern based on its original column parity.
    """
    # 1. Find the non-zero element N and its location (r, c), and dimensions H, W
    result = find_non_zero(input_grid)
    if result is None or result[1] == -1: # Handle empty grid or no non-zero found
        # Return a copy or handle error as appropriate
        # Based on examples, we expect a non-zero element.
        # If no non-zero, maybe return input as-is or an empty grid?
        # Let's return a copy for now if grid is valid but no non-zero found.
        height = len(input_grid)
        if height == 0: return []
        width = len(input_grid[0]) if height > 0 else 0
        return [[0 for _ in range(width)] for _ in range(height)] 
        
    n_value, r_orig, c_orig, height, width = result

    # 2. Initialize the output grid with zeros
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # 3. Determine the parity of the original column
    col_parity = c_orig % 2

    # 4. Create the pattern row
    pattern = create_pattern_row(width, col_parity)

    # 5. Fill the output grid with the pattern row from row 0 to r_orig (inclusive)
    for i in range(r_orig + 1):
         # Ensure we don't write past the grid boundary if r_orig is near the bottom
         # (although problem examples don't show this case for the pattern)
         if i < height:
            output_grid[i] = list(pattern) # Use list() to copy pattern

    # 6. Place the original non-zero number N at position (r_orig + 1, c_orig)
    new_row_index = r_orig + 1
    # Check bounds before placing N
    if new_row_index < height:
         # Ensure we don't overwrite the pattern if pattern row is same as new N row
         # (This happens if r_orig + 1 == r_orig which is impossible, 
         #  or if the pattern filling went up to r_orig and new N is at r_orig+1)
         # The current logic is correct: pattern fills up to r_orig, N is placed at r_orig+1.
        output_grid[new_row_index][c_orig] = n_value
    # Else: N is moved off the grid (handle as needed, though not shown in examples)
    # Current implementation implicitly drops N if it moves off grid.

    # 7. Return the transformed grid
    return output_grid