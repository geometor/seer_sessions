"""
Transforms an input grid by splitting it vertically into two halves. The left half serves as a mask or frame, 
and the right half provides content keys. The unique non-zero values from the right half (content keys) are mapped 
to new values based on a rule determined by their relationship to all unique non-zero values in the input grid. 
Specifically, if the index 0 is present among the indices of the right-half values within the sorted list of all 
non-zero values, a 'Reverse' mapping is used. Otherwise, a 'Cyclic Shift' mapping is applied. The output grid is 
initialized with the left half, and its zero cells are filled with the mapped values corresponding to the content keys 
from the right half.
"""

import copy

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
    # Handle empty input
    if not input_grid or not input_grid[0]:
        return []

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    mid_col = num_cols // 2

    # Split the grid into left and right halves
    left_grid = [row[:mid_col] for row in input_grid]
    right_grid = [row[mid_col:] for row in input_grid]

    # Find all unique non-zero values in the entire input grid
    all_non_zeros_sorted = _find_unique_non_zeros(input_grid)

    # Find unique non-zero values (content keys) in the right grid
    content_keys_sorted = _find_unique_non_zeros(right_grid)

    # If there are no content keys, the output is just the left grid
    if not content_keys_sorted:
        # Need a deep copy to avoid modifying the original input structure if it were passed directly
        return copy.deepcopy(left_grid)

    # Determine the indices of content keys within the list of all non-zeros
    # Create a lookup map for faster index finding
    all_non_zeros_map = {val: idx for idx, val in enumerate(all_non_zeros_sorted)}
    indices = []
    for key in content_keys_sorted:
        if key in all_non_zeros_map:
             indices.append(all_non_zeros_map[key])
        # This case shouldn't happen if logic is correct, but added for robustness
        # else: handle error or unexpected value

    # Determine the mapping rule based on the presence of index 0
    use_reverse_mapping = 0 in indices

    # Create the value map based on the rule
    value_map = {}
    n_keys = len(content_keys_sorted)
    if use_reverse_mapping:
        # Reverse mapping
        for i in range(n_keys):
            value_map[content_keys_sorted[i]] = content_keys_sorted[n_keys - 1 - i]
    else:
        # Cyclic shift mapping
        for i in range(n_keys):
            value_map[content_keys_sorted[i]] = content_keys_sorted[(i + 1) % n_keys]

    # Initialize the output grid as a deep copy of the left grid
    output_grid = copy.deepcopy(left_grid)

    # Iterate through the output grid and apply the mapping
    for r in range(num_rows):
        for c in range(mid_col):
            # Check if the cell in the output grid (from left_grid) is 0
            if output_grid[r][c] == 0:
                # Get the corresponding content key from the right grid
                content_key = right_grid[r][c]
                # If the content key is non-zero (and thus in our map)
                if content_key in value_map:
                    # Replace the 0 in the output grid with the mapped value
                    output_grid[r][c] = value_map[content_key]
            # Otherwise (if output_grid[r][c] is not 0), leave it as part of the frame

    return output_grid