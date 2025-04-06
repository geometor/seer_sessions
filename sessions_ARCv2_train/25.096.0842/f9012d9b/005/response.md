```python
import math
from collections import defaultdict
import numpy as np

"""
Transforms an input square grid of integers into an output square grid based on the following rules:

1.  Determine the dimension (`Dim`) of the input square grid.
2.  Calculate the subgrid dimension (`M`) as `floor(sqrt(Dim))`.
3.  Extract all unique `M x M` subgrid patterns from the input grid. For each unique pattern, record its frequency, the sum of its elements, and the list of top-left (row, col) locations where it occurs.
4.  Filter the patterns to keep only those with the maximum sum of elements found across all patterns.
5.  From the filtered set, further filter to keep only those patterns with the maximum frequency.
6.  If only one pattern remains, select it as the target pattern (`P`).
7.  If multiple patterns remain tied after the sum and frequency filters, apply a location-based tie-breaker:
    a. For each tied pattern, find its occurrence(s) with the maximum row index.
    b. Among these, find the occurrence with the maximum column index.
    c. Select the pattern associated with this winning (max row, max col) location.
8.  Determine the output grid dimension (`N`): `N = M // 2` if `Dim` is even, otherwise `N = M`.
9.  Construct the output grid by taking the top-left `N x N` portion of the selected pattern `P`.
"""

def _get_subgrid_data(grid: list[list[int]], m: int) -> dict:
    """
    Extracts M x M subgrids, calculates sum, frequency, and locations for each unique pattern.

    Args:
        grid: The input 2D list of integers.
        m: The dimension of the subgrids to extract.

    Returns:
        A dictionary where keys are tuple representations of subgrid patterns
        and values are dictionaries containing 'count', 'sum', and 'locations'.
        Example: { ((1,2),(3,4)): {'count': 2, 'sum': 10, 'locations': [(0,0), (5,5)]} }
    """
    dim = len(grid)
    pattern_data = defaultdict(lambda: {'count': 0, 'sum': 0, 'locations': []})

    if m <= 0 or m > dim:
        return {}

    for r in range(dim - m + 1):
        for c in range(dim - m + 1):
            subgrid_rows = []
            current_sum = 0
            for i in range(m):
                row_tuple = tuple(grid[r + i][c : c + m])
                subgrid_rows.append(row_tuple)
                current_sum += sum(row_tuple)
            
            pattern_tuple = tuple(subgrid_rows)
            
            # Update data for this pattern
            pattern_data[pattern_tuple]['count'] += 1
            pattern_data[pattern_tuple]['locations'].append((r, c))
            # Sum is calculated only once when the pattern is first encountered implicitly
            if pattern_data[pattern_tuple]['count'] == 1:
                 pattern_data[pattern_tuple]['sum'] = current_sum
                 
    return dict(pattern_data)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Determine input dimension (Dim)
    dim = len(input_grid)
    if dim == 0:
        return []

    # 2. Calculate subgrid dimension (M)
    m = math.floor(math.sqrt(dim))
    if m == 0:
        return [] # Cannot proceed with M=0

    # 3. Extract subgrids and their data (frequency, sum, locations)
    all_pattern_data = _get_subgrid_data(input_grid, m)
    if not all_pattern_data:
        return [] # No subgrids found

    # 4. Filter by maximum sum
    max_sum = -1
    for data in all_pattern_data.values():
        if data['sum'] > max_sum:
            max_sum = data['sum']
    
    sum_filtered_patterns = {
        p: data for p, data in all_pattern_data.items() if data['sum'] == max_sum
    }

    if not sum_filtered_patterns:
        # This case implies max_sum remained -1, should not happen if all_pattern_data is not empty
        return [] 

    # 5. Filter by maximum frequency (among max_sum patterns)
    max_freq = 0
    for data in sum_filtered_patterns.values():
        if data['count'] > max_freq:
            max_freq = data['count']

    freq_filtered_patterns = {
        p: data for p, data in sum_filtered_patterns.items() if data['count'] == max_freq
    }

    # 6. & 7. Select the target pattern (P), handling ties with location
    selected_pattern_tuple = None
    patterns_after_freq_filter = list(freq_filtered_patterns.keys())

    if len(patterns_after_freq_filter) == 1:
        selected_pattern_tuple = patterns_after_freq_filter[0]
    elif len(patterns_after_freq_filter) > 1:
        # Location-based tie-breaking
        best_location = (-1, -1) # (row, col)
        winning_pattern = None

        for pattern in patterns_after_freq_filter:
            locations = freq_filtered_patterns[pattern]['locations']
            # Find the location for *this* pattern with max row, then max col
            current_max_loc = (-1, -1)
            for loc in locations:
                # Check if current location `loc` is better than `current_max_loc`
                if loc[0] > current_max_loc[0] or \
                   (loc[0] == current_max_loc[0] and loc[1] > current_max_loc[1]):
                    current_max_loc = loc
            
            # Check if this pattern's best location (`current_max_loc`) 
            # is better than the overall best found so far (`best_location`)
            if current_max_loc[0] > best_location[0] or \
               (current_max_loc[0] == best_location[0] and current_max_loc[1] > best_location[1]):
                best_location = current_max_loc
                winning_pattern = pattern
        
        selected_pattern_tuple = winning_pattern
    else:
         # No patterns left after filtering, should not happen if initial data existed
         return []

    if selected_pattern_tuple is None:
        # Should not be reachable if logic above is correct
        return []

    # 8. Determine output dimension (N)
    if dim % 2 == 0:
        n = m // 2
    else:
        n = m
        
    if n <= 0:
        return [] # Output is empty if N is 0 or less

    # 9. Construct the output grid (top-left N x N of selected pattern)
    output_grid = []
    # Ensure N doesn't exceed M (which it shouldn't by calculation)
    actual_n = min(n, m) 
    if actual_n == 0: return []

    for i in range(actual_n):
        # Ensure pattern has enough rows
        if i < len(selected_pattern_tuple):
            row = selected_pattern_tuple[i]
            # Ensure row has enough columns and take the first N elements
            output_grid.append(list(row[:actual_n]))
        else:
            # Should not happen if N <= M
            break 

    return output_grid
```