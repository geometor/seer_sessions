import collections

"""
Transformation Rule:

1. Examine the main diagonal of the input grid (elements from top-left to bottom-right).
2. If all elements on the main diagonal are identical (monochromatic):
   a. The output is a 1x1 grid containing that identical element value.
3. If the elements on the main diagonal are not all identical:
   a. Identify all unique 2x2 subgrids present in the input grid.
   b. For each unique 2x2 subgrid, count its total number of occurrences (frequency).
   c. For each unique 2x2 subgrid, find the coordinates (row, column) of the top-left corner of its first occurrence (scanning row by row, then column by column).
   d. Determine the maximum frequency achieved by any 2x2 subgrid.
   e. Select the 2x2 subgrid that has this maximum frequency.
   f. If multiple subgrids share the maximum frequency, select the one whose first occurrence has the smallest row index.
   g. If there is still a tie (same maximum frequency and same minimum row index), select the one among them with the smallest column index.
   h. The selected 2x2 subgrid is the output.

(Note: This implements Hypothesis A from the analysis, which fits train_1 and train_2 but may not fully explain train_3).
"""

def get_main_diagonal(grid: list[list[int]]) -> list[int]:
    """Extracts the main diagonal elements from a grid."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    size = min(rows, cols)
    return [grid[i][i] for i in range(size)]

def is_monochromatic(sequence: list[int]) -> bool:
    """Checks if all elements in a sequence are the same."""
    if not sequence:
        return True # An empty sequence can be considered monochromatic
    first_element = sequence[0]
    return all(element == first_element for element in sequence)

def get_subgrid(grid: list[list[int]], r: int, c: int, height: int, width: int) -> list[list[int]]:
    """Extracts a subgrid of specified size starting at (r, c)."""
    return [row[c:c+width] for row in grid[r:r+height]]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Checks for monochromatic diagonal first. If not found, finds the most frequent
    2x2 subgrid, breaking ties by the earliest position (top-most, then left-most).
    """
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Check Rule Case 1: Monochromatic diagonal
    diagonal = get_main_diagonal(input_grid)
    if is_monochromatic(diagonal) and diagonal: # Ensure diagonal is not empty
        # Output the single element as a 1x1 grid
        return [[diagonal[0]]]

    # Rule Case 2: Not monochromatic diagonal (or grid too small for diagonal)
    # Find all 2x2 subgrids, their frequencies, and first positions
    subgrid_info = {} # key: tuple(tuple(subgrid)), value: [count, first_row, first_col]

    if rows < 2 or cols < 2:
         # Cannot form 2x2 subgrids, return empty or handle as error?
         # Based on examples, this case shouldn't occur, but good to consider.
         # Let's return an empty grid if no 2x2 can be formed.
         return []

    for r in range(rows - 1):
        for c in range(cols - 1):
            # Extract the 2x2 subgrid
            subgrid = get_subgrid(input_grid, r, c, 2, 2)
            # Use a tuple representation as dictionary key
            subgrid_tuple = tuple(tuple(row) for row in subgrid)

            # Store frequency and first position
            if subgrid_tuple not in subgrid_info:
                subgrid_info[subgrid_tuple] = [1, r, c] # [count, first_row, first_col]
            else:
                subgrid_info[subgrid_tuple][0] += 1 # Increment count

    if not subgrid_info:
        # Should not happen if rows>=2 and cols>=2, but defensive check
        return []

    # Find the best subgrid based on frequency and position
    best_subgrid_tuple = None
    max_freq = -1
    min_first_row = rows # Initialize higher than any possible row
    min_first_col = cols # Initialize higher than any possible col

    # Iterate through the collected subgrid information
    # Sort items primarily by frequency (desc), then row (asc), then col (asc)
    # This allows us to simply pick the first item after sorting
    # Sorting key: (-frequency, first_row, first_col)
    # negative frequency makes it descending sort for frequency
    sorted_subgrids = sorted(
        subgrid_info.items(),
        key=lambda item: (-item[1][0], item[1][1], item[1][2])
    )
    
    # The best subgrid according to the criteria is the first element
    best_subgrid_tuple = sorted_subgrids[0][0]

    # Convert the best subgrid tuple back to a list of lists
    output_grid = [list(row) for row in best_subgrid_tuple]

    return output_grid