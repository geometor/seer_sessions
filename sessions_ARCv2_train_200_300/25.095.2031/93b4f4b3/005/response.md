```python
"""
Transforms an input grid by splitting it vertically into two halves. The left half serves as a mask or frame, 
and the right half provides content keys. The unique non-zero values from the right half (content keys) are mapped 
to new values based on a rule determined by their relationship to all unique non-zero values in the input grid. 
Specifically, if the index 0 is present among the indices of the right-half values within the sorted list of all 
non-zero values, a 'Reverse' mapping is used. Otherwise, a 'Cyclic Shift' mapping is applied. The output grid is 
initialized with the left half, and its zero cells are filled with the mapped values corresponding to the content keys 
from the right half. If a cell in the right half corresponding to a zero cell in the left half is zero, the output cell remains zero.
"""

import copy

# Helper function to find unique non-zero values in a grid
def _find_unique_non_zeros(grid: list[list[int]]) -> list[int]:
    """Finds and sorts unique non-zero values in a grid."""
    non_zeros = set()
    for row in grid:
        for cell in row:
            if cell != 0:
                non_zeros.add(cell)
    return sorted(list(non_zeros))

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation rule to the input grid.
    """
    # Handle empty input case
    if not input_grid or not input_grid[0]:
        return []

    # Get dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    mid_col = num_cols // 2

    # 1. Split the grid into left (mask) and right (content key) halves
    left_grid = [row[:mid_col] for row in input_grid]
    right_grid = [row[mid_col:] for row in input_grid]

    # 2. Analyze: Find unique non-zero values globally and in the right grid
    all_non_zeros_sorted = _find_unique_non_zeros(input_grid)
    content_keys_sorted = _find_unique_non_zeros(right_grid)

    # If there are no content keys in the right grid, the output is just the left grid
    if not content_keys_sorted:
        # Return a deep copy to avoid modifying potential external references to input_grid
        return copy.deepcopy(left_grid)

    # 3. Determine Rule: Check indices of content keys within all non-zeros
    # Create a lookup map for efficient index finding
    all_non_zeros_map = {val: idx for idx, val in enumerate(all_non_zeros_sorted)}
    indices = []
    for key in content_keys_sorted:
        # Ensure the key exists in the map (it should, logically)
        if key in all_non_zeros_map:
             indices.append(all_non_zeros_map[key])

    # Determine the mapping rule based on the presence of index 0
    use_reverse_mapping = 0 in indices

    # 4. Build Map: Create the value map based on the determined rule
    value_map = {}
    n_keys = len(content_keys_sorted)
    if use_reverse_mapping:
        # Reverse mapping: key[i] maps to key[n-1-i]
        for i in range(n_keys):
            value_map[content_keys_sorted[i]] = content_keys_sorted[n_keys - 1 - i]
    else:
        # Cyclic Shift mapping: key[i] maps to key[(i+1) % n]
        for i in range(n_keys):
            value_map[content_keys_sorted[i]] = content_keys_sorted[(i + 1) % n_keys]

    # 5. Apply: Initialize output grid and fill based on the map
    # Initialize the output grid as a deep copy of the left grid
    output_grid = copy.deepcopy(left_grid)

    # Iterate through the output grid (which has the dimensions of the left grid)
    for r in range(num_rows):
        for c in range(mid_col):
            # Check if the cell in the output grid (originally from left_grid) is 0 (needs filling)
            if output_grid[r][c] == 0:
                # Get the corresponding content key from the right grid
                content_key = right_grid[r][c]
                # If the content key is non-zero (and thus should be in our map)
                if content_key != 0:
                    # Replace the 0 in the output grid with the mapped value
                    # Check if key is in map defensively, though it should be if logic is correct
                    if content_key in value_map:
                         output_grid[r][c] = value_map[content_key]
                    # else: # Optional: handle unexpected case where key isn't in map
                    #     pass # Or raise an error, or log
                # If the content_key is 0, the output cell remains 0 (already initialized)

            # Else (if output_grid[r][c] is not 0), it's part of the frame, leave it unchanged.

    return output_grid
```