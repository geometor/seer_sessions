import numpy as np

"""
Transforms a 6x6 input grid into a 5x5 output grid.
The transformation rule depends on the presence of a specific 3x3 pattern
within the input grid.

1. Define three constant row patterns of size 1x5:
   - P0 = [0, 0, 0, 0, 0]
   - P1 = [8, 8, 0, 8, 8]
   - P2 = [0, 8, 0, 0, 8]
2. Define the specific 3x3 trigger pattern:
   - TriggerPattern = [[8, 8, 8], [8, 8, 8], [0, 8, 8]]
3. Search the input 6x6 grid for any occurrence of the TriggerPattern.
4. If the TriggerPattern is found:
   - Construct the 5x5 output grid by stacking rows: P1, P1, P0, P1, P1.
5. If the TriggerPattern is not found:
   - Construct the 5x5 output grid by stacking rows: P2, P1, P0, P2, P1.
6. Return the constructed 5x5 grid.
"""

def find_specific_trigger_pattern(grid: list[list[int]], pattern: list[list[int]]) -> bool:
    """
    Searches a grid for a specific 3x3 subgrid pattern.

    Args:
        grid: The input grid (list of lists).
        pattern: The 3x3 pattern to search for (list of lists).

    Returns:
        True if the pattern is found, False otherwise.
    """
    # Convert lists to numpy arrays for easier slicing and comparison
    grid_np = np.array(grid)
    pattern_np = np.array(pattern)
    rows, cols = grid_np.shape
    p_rows, p_cols = pattern_np.shape

    # Ensure the grid is large enough to contain the pattern
    if rows < p_rows or cols < p_cols:
        return False

    # Iterate through all possible top-left corners of the subgrid
    for r in range(rows - p_rows + 1):
        for c in range(cols - p_cols + 1):
            # Extract the subgrid
            subgrid = grid_np[r:r+p_rows, c:c+p_cols]
            # Compare the subgrid with the pattern
            if np.array_equal(subgrid, pattern_np):
                return True # Pattern found
    return False # Pattern not found after checking all positions

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Define the constant 1x5 row patterns
    P0 = [0, 0, 0, 0, 0]
    P1 = [8, 8, 0, 8, 8]
    P2 = [0, 8, 0, 0, 8]

    # Define the specific 3x3 trigger pattern
    trigger_pattern_definition = [[8, 8, 8], [8, 8, 8], [0, 8, 8]]

    # Define the two possible output patterns (assemblies of P0, P1, P2)
    output_pattern_A = [P1, P1, P0, P1, P1] # Used when trigger pattern is found
    output_pattern_B = [P2, P1, P0, P2, P1] # Used when trigger pattern is NOT found

    # Search for the specific trigger pattern in the input grid
    trigger_found = find_specific_trigger_pattern(input_grid, trigger_pattern_definition)

    # Select the appropriate output pattern based on whether the trigger was found
    if trigger_found:
        output_grid = output_pattern_A
    else:
        output_grid = output_pattern_B

    # Return the selected 5x5 output grid
    return output_grid