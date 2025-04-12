import numpy as np
from collections import defaultdict

"""
Transformation Rule:

1.  Examine the main diagonal of the input grid (elements from top-left to bottom-right).
2.  If the main diagonal is not empty AND all elements on the main diagonal are identical:
    a.  The output is a 1x1 grid containing that identical element value.
3.  Otherwise (if the main diagonal has different elements, is empty, or the grid is smaller than 2x2):
    a.  If the input grid is smaller than 2x2 in height or width, return an empty grid (as no 2x2 subgrid can be formed).
    b.  Identify all unique 2x2 subgrid patterns present in the input grid.
    c.  For each unique 2x2 pattern, calculate three properties:
        i.  Its sum (total of its four elements).
        ii. Its frequency (how many times it appears in the input grid).
        iii. Its last position (the row and column index of the top-left corner of its final appearance when scanning the grid row by row, then column by column).
    d.  Find the maximum sum achieved by any 2x2 pattern.
    e.  Consider only those patterns that have this maximum sum.
    f.  Among these maximum-sum patterns, find the minimum frequency.
    g.  Consider only those patterns that have both the maximum sum and this minimum frequency.
    h.  If only one pattern remains, select this pattern.
    i.  If multiple patterns remain (tied on maximum sum and minimum frequency), compare their last positions. Select the pattern whose last position has the largest row index. If there's still a tie (same largest row index), select the one among them with the largest column index.
    j.  The selected 2x2 pattern is the output.
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

def analyze_subgrids(grid: list[list[int]], subgrid_size: int = 2) -> dict:
    """
    Finds all unique subgrids of a given size, calculating their sum,
    frequency, and the position of their last occurrence.

    Args:
        grid: The input grid (list of lists of ints).
        subgrid_size: The dimension of the square subgrids to analyze (e.g., 2 for 2x2).

    Returns:
        A dictionary where keys are subgrid patterns (tuple of tuples) and
        values are dictionaries containing {'sum', 'freq', 'last_pos'}.
        Returns an empty dictionary if no subgrids can be formed.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    # Store: {pattern_tuple: {'sum': int, 'freq': int, 'last_pos': (r,c)}}
    subgrid_info = defaultdict(lambda: {'sum': 0, 'freq': 0, 'last_pos': (-1, -1)})

    if rows < subgrid_size or cols < subgrid_size:
        return {} # Cannot form subgrids of the specified size

    for r in range(rows - subgrid_size + 1):
        for c in range(cols - subgrid_size + 1):
            # Extract the subgrid
            subgrid = [row[c:c+subgrid_size] for row in grid[r:r+subgrid_size]]
            # Use a tuple representation for the key
            subgrid_tuple = tuple(tuple(row) for row in subgrid)
            current_pos = (r, c)

            # Calculate sum if first time seeing this pattern
            if subgrid_info[subgrid_tuple]['freq'] == 0:
                 subgrid_info[subgrid_tuple]['sum'] = int(np.sum(subgrid))

            # Update frequency and last position
            subgrid_info[subgrid_tuple]['freq'] += 1
            subgrid_info[subgrid_tuple]['last_pos'] = current_pos

    return dict(subgrid_info) # Convert back to regular dict


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = []
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Rule 1: Check for monochromatic diagonal
    diagonal = get_main_diagonal(input_grid)
    if diagonal and is_monochromatic(diagonal):
        # Rule 1a: Output 1x1 grid
        output_grid = [[diagonal[0]]]
        return output_grid

    # Rule 3: Handle non-monochromatic diagonal or small grids
    # Rule 3a: Check if grid is too small for 2x2 subgrids
    if rows < 2 or cols < 2:
        return [] # Return empty list as per rule 3a

    # Rule 3b, 3c: Analyze 2x2 subgrids
    subgrid_analysis = analyze_subgrids(input_grid, 2)

    # Check if any subgrids were found (redundant check given rows/cols check, but safe)
    if not subgrid_analysis:
        return []

    # Rule 3d: Find the maximum sum
    max_sum = -1
    for info in subgrid_analysis.values():
        if info['sum'] > max_sum:
            max_sum = info['sum']

    # Rule 3e: Filter by max sum
    max_sum_patterns = []
    for pattern, info in subgrid_analysis.items():
        if info['sum'] == max_sum:
             # Store pattern along with its info for easy access later
            max_sum_patterns.append({'pattern': pattern, **info})

    # Rule 3f: Find minimum frequency among max-sum patterns
    min_freq = float('inf')
    for item in max_sum_patterns:
        if item['freq'] < min_freq:
            min_freq = item['freq']

    # Rule 3g: Filter by min frequency
    candidate_patterns = [item for item in max_sum_patterns if item['freq'] == min_freq]

    # Rule 3h, 3i: Select based on last position if needed
    if not candidate_patterns:
         # This case should ideally not happen if subgrid_analysis was non-empty
         return []
    elif len(candidate_patterns) == 1:
        best_pattern_tuple = candidate_patterns[0]['pattern']
    else:
        # Sort candidates by last position: highest row first, then highest col first
        candidate_patterns.sort(key=lambda item: item['last_pos'], reverse=True)
        best_pattern_tuple = candidate_patterns[0]['pattern']

    # Rule 3j: Convert the selected pattern tuple back to list of lists
    output_grid = [list(row) for row in best_pattern_tuple]

    return output_grid