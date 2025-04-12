import collections
import numpy as np # Using numpy for convenience, though not strictly necessary for this logic

"""
Transformation Rule:

1. Examine the main diagonal of the input grid (elements from top-left to bottom-right).
2. If the main diagonal is not empty AND all elements on the main diagonal are identical (monochromatic):
   a. The output is a 1x1 grid containing that single identical element value.
3. If the main diagonal is empty, or contains different element values (not monochromatic):
   a. The output grid size will be 2x2.
   b. Identify all unique 2x2 subgrids present within the input grid.
   c. For each unique 2x2 subgrid pattern, count its total number of occurrences (frequency) in the input grid.
   d. For each unique 2x2 subgrid pattern, find the coordinates (row, column) of the top-left corner of its *first* occurrence (scanning the input grid row by row, then column by column).
   e. Determine the maximum frequency (`max_freq`) achieved by any 2x2 subgrid pattern.
   f. Filter the set of unique 2x2 patterns to include only those whose frequency equals `max_freq`.
   g. If only one pattern remains, select this pattern as the output.
   h. If multiple patterns remain (tied for maximum frequency), compare their first occurrence positions. Select the pattern whose first occurrence has the smallest row index.
   i. If there is still a tie (same maximum frequency and same minimum row index), select the pattern among the remaining ties that has the smallest column index for its first occurrence.
   j. The selected 2x2 subgrid pattern is the output.

(Note: This rule is known to fail test cases 2 and 3 based on previous analysis,
 but accurately reflects the last specified Natural Language Program.)
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
    output_grid = []

    # Step 1 & 2: Examine the main diagonal
    diagonal = get_main_diagonal(input_grid)
    if diagonal and is_monochromatic(diagonal):
        # Step 2a: Output 1x1 grid with the diagonal element
        output_grid = [[diagonal[0]]]
        return output_grid

    # Step 3: Handle non-monochromatic diagonal (or empty grid)
    # Step 3a: Output size will be 2x2.
    # Check if a 2x2 subgrid can be formed.
    if rows < 2 or cols < 2:
         # Cannot form 2x2 subgrids. Return empty grid as per implied behavior.
         return []

    # Step 3b, 3c, 3d: Identify unique 2x2 subgrids, count frequency, find first position.
    subgrid_info = {} # key: tuple(tuple(subgrid)), value: [count, first_row, first_col]

    for r in range(rows - 1): # Iterate through possible top-left row positions
        for c in range(cols - 1): # Iterate through possible top-left col positions
            # Extract the 2x2 subgrid
            subgrid = get_subgrid(input_grid, r, c, 2, 2)
            # Use a tuple representation for dictionary key (lists are not hashable)
            subgrid_tuple = tuple(tuple(row) for row in subgrid)

            # Store frequency and first position
            if subgrid_tuple not in subgrid_info:
                # Record first occurrence: [frequency=1, row=r, col=c]
                subgrid_info[subgrid_tuple] = [1, r, c]
            else:
                # Increment frequency count
                subgrid_info[subgrid_tuple][0] += 1

    # Check if any subgrids were found (should be true if rows>=2 and cols>=2)
    if not subgrid_info:
        return [] # Return empty if no 2x2 subgrids exist

    # Step 3e-3i: Select the best subgrid based on frequency and position tie-breaking.
    # We can achieve this efficiently by sorting.
    # Sort key: (-frequency, first_row, first_col)
    #   - Negative frequency makes it sort descending by frequency (max first).
    #   - first_row makes it sort ascending by row index (min first).
    #   - first_col makes it sort ascending by col index (min first).
    sorted_subgrids = sorted(
        subgrid_info.items(),
        key=lambda item: (-item[1][0], item[1][1], item[1][2])
    )

    # The best subgrid according to the specified criteria is the first element after sorting
    best_subgrid_tuple = sorted_subgrids[0][0]

    # Step 3j: The selected 2x2 subgrid is the output. Convert back to list of lists.
    output_grid = [list(row) for row in best_subgrid_tuple]

    return output_grid