"""
Transforms an input grid by splitting it vertically into two halves. The left half serves as a mask or frame, 
and the right half provides content keys. The unique non-zero values from the right half (content keys) are mapped 
to new values based on a rule determined by their relationship to all unique non-zero values in the input grid. 
Specifically, if the smallest content key is also the smallest non-zero value in the entire input grid, 
a 'Reverse' mapping (within the sorted content keys) is used. Otherwise, a 'Cyclic Shift' mapping (within the 
sorted content keys) is applied. The output grid is initialized with the left half, and its zero cells are filled 
with the mapped values corresponding to the non-zero content keys from the right half. If a cell in the right half 
corresponding to a zero cell in the left half is zero, the output cell remains zero.
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
    
    # Ensure columns are even for splitting
    if num_cols % 2 != 0:
        # Or handle this error condition as appropriate for the task constraints
        raise ValueError("Input grid must have an even number of columns.")
        
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

    # 3. Determine Map Rule: Check if the smallest content key matches the smallest overall non-zero
    use_reverse_mapping = False
    # Check only if both lists are non-empty
    if content_keys_sorted and all_non_zeros_sorted:
        if content_keys_sorted[0] == all_non_zeros_sorted[0]:
            use_reverse_mapping = True

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
                # If the content key is non-zero and exists in our map
                if content_key in value_map:
                     # Replace the 0 in the output grid with the mapped value
                     output_grid[r][c] = value_map[content_key]
                # Else if content_key is 0, output_grid[r][c] remains 0 (already initialized)

            # Else (if output_grid[r][c] is not 0), it's part of the frame, leave it unchanged.

    return output_grid