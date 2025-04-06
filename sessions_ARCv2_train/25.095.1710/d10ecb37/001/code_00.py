import sys
# Add the directory containing the 'parse_grid' module to the Python path
sys.path.append('/Users/bendevera/Code/ARC/arc_solving_framework/utils')
from grid_utils import parse_grid, format_grid

"""
The transformation rule involves the following steps:
1. Parse the input string into a grid of integers.
2. Identify the unique rows from the input grid, preserving the order of their first appearance.
3. Extract the top-left 2x2 subgrid from these unique rows.
4. Format this 2x2 subgrid back into the required string format.
"""

def find_unique_rows(grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies unique rows in a grid, preserving the order of first appearance.
    Args:
        grid: A list of lists representing the input grid.
    Returns:
        A list of lists containing only the unique rows in their original order.
    """
    unique_rows = []
    seen_rows = set()
    for row in grid:
        # Convert row to tuple for hashability to use in the set
        row_tuple = tuple(row)
        if row_tuple not in seen_rows:
            unique_rows.append(row)
            seen_rows.add(row_tuple)
    return unique_rows

def extract_top_left_2x2(grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts the top-left 2x2 subgrid from a given grid.
    Args:
        grid: A list of lists representing the grid (must have at least 2 rows and 2 columns).
    Returns:
        A 2x2 list of lists representing the top-left subgrid.
    """
    # Ensure the grid is large enough
    if len(grid) < 2 or len(grid[0]) < 2:
        raise ValueError("Grid must be at least 2x2 to extract a 2x2 subgrid.")
        
    output_grid = []
    # Extract the first two elements of the first row
    output_grid.append(grid[0][:2])
    # Extract the first two elements of the second row
    output_grid.append(grid[1][:2])
    return output_grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation: finds unique rows, then extracts the top-left 2x2 subgrid.
    Args:
        input_grid: A list of lists representing the input grid.
    Returns:
        A 2x2 list of lists representing the transformed output grid.
    """
    # Step 2: Identify unique rows, preserving order
    unique_rows_grid = find_unique_rows(input_grid)

    # Step 3 & 4: Extract the top-left 2x2 subgrid from the unique rows
    # Assumes the unique rows grid will always have at least 2 rows and 2 columns based on examples
    output_grid = extract_top_left_2x2(unique_rows_grid)

    # Step 5: Return the resulting 2x2 grid
    return output_grid

# Example usage with parsing and formatting (similar to how it might be called)
# Note: parse_grid and format_grid would need to be defined elsewhere or imported

# train_1_input_str = """
# 2 4 2 2 5 2 4 5
# 2 5 5 4 4 2 2 2
# 4 5 5 2 2 2 2 4
# 2 2 4 2 5 4 2 5
# 2 4 2 2 5 2 4 5
# 2 5 5 4 4 2 2 2
# 4 5 5 2 2 2 2 4
# 2 2 4 2 5 4 2 5
# """

# train_1_input_grid = parse_grid(train_1_input_str)
# train_1_output_grid = transform(train_1_input_grid)
# print("Train 1 Output:")
# print(format_grid(train_1_output_grid))

# train_2_input_str = """
# 4 3 6 4 0 6
# 6 0 0 3 3 4
# 6 4 4 3 3 0
# 0 3 6 0 4 6
# 0 6 3 0 4 3
# 3 4 4 6 6 0
# """
# train_2_input_grid = parse_grid(train_2_input_str)
# train_2_output_grid = transform(train_2_input_grid)
# print("\nTrain 2 Output:")
# print(format_grid(train_2_output_grid))

# train_3_input_str = """
# 3 2 1 3 4 1
# 1 4 4 2 2 3
# 1 3 3 2 2 4
# 4 2 1 4 3 1
# 4 1 2 4 3 2
# 2 3 3 1 1 4
# 2 4 4 1 1 3
# 3 1 2 3 4 2
# 3 2 1 3 4 1
# 1 4 4 2 2 3
# 1 3 3 2 2 4
# 4 2 1 4 3 1
# """
# train_3_input_grid = parse_grid(train_3_input_str)
# train_3_output_grid = transform(train_3_input_grid)
# print("\nTrain 3 Output:")
# print(format_grid(train_3_output_grid))