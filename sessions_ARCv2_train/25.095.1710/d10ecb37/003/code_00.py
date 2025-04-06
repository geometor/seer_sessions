"""
The transformation rule involves identifying the unique rows from the input grid, preserving the order of their first appearance, and then extracting the top-left 2x2 subgrid from these unique rows.
"""

from typing import List, Tuple, Set

def find_unique_rows(grid: List[List[int]]) -> List[List[int]]:
    """
    Identifies unique rows in a grid, preserving the order of first appearance.
    Args:
        grid: A list of lists representing the input grid.
    Returns:
        A list of lists containing only the unique rows in their original order.
    """
    unique_rows: List[List[int]] = []
    seen_rows: Set[Tuple[int, ...]] = set() # Use a set for efficient checking of seen rows
    for row in grid:
        # Convert row to tuple for hashability (required for set membership)
        row_tuple = tuple(row)
        if row_tuple not in seen_rows:
            # If the row hasn't been seen, add it to the unique list and the seen set
            unique_rows.append(row)
            seen_rows.add(row_tuple)
    return unique_rows

def extract_top_left_2x2(grid: List[List[int]]) -> List[List[int]]:
    """
    Extracts the top-left 2x2 subgrid from a given grid.
    Args:
        grid: A list of lists representing the grid (assumed to have at least 2 rows and 2 columns).
    Returns:
        A 2x2 list of lists representing the top-left subgrid.
    """
    # Extract the first two elements of the first row
    row1 = grid[0][:2]
    # Extract the first two elements of the second row
    row2 = grid[1][:2]
    # Combine into the output grid
    output_grid = [row1, row2]
    return output_grid

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    # Step 1: Identify unique rows from the input grid, preserving order of first appearance.
    # This filters out duplicate rows while keeping the sequence of the first occurrences.
    unique_rows_grid = find_unique_rows(input_grid)

    # Step 2: Extract the top-left 2x2 subgrid from the grid of unique rows.
    # This takes the first two elements from the first two unique rows found.
    # Assumption: The unique rows grid will always have at least 2 rows and 2 columns,
    # based on the problem's examples.
    output_grid = extract_top_left_2x2(unique_rows_grid)

    # Step 3: Return the resulting 2x2 grid.
    return output_grid