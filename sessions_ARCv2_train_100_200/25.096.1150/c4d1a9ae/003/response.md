```python
import copy
import numpy as np

"""
Transforms a 2D grid of integers based on a mode selected by detecting a 
'marker' digit (6 or 9) within the input grid. 

If the digit 6 is present, Mode 1 is selected: 
The target value is 4. Occurrences of 4 are replaced based on their column index 
according to the rule set {0: 6, 1: 6, 3: 5, 4: 5, 6: 2}. 
If 4 appears in other columns, it remains unchanged.

If the digit 9 is present (and 6 is not), Mode 2 is selected:
The target value is 0. Occurrences of 0 are replaced based on their column index 
according to the rule set {0: 3, 1: 3, 2: 3, 4: 9, 6: 4, 7: 4}.
If 0 appears in other columns, it remains unchanged.

All other digits in the grid that do not match the selected mode's target value 
remain unchanged in the output.
"""


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a conditional transformation based on detected marker digits.

    Args:
        input_grid: A list of lists representing the 2D input grid of integers.

    Returns:
        A list of lists representing the 2D output grid after transformation.
    """
    # Convert input to numpy array for easier analysis
    input_array = np.array(input_grid, dtype=int)

    # Initialize output_grid as a deep copy of the input grid
    # Use deepcopy to ensure modifications don't affect the original input list structure
    output_grid = copy.deepcopy(input_grid)

    # --- Analyze Input and Select Mode ---
    # Check for the presence of marker digits
    contains_6 = np.any(input_array == 6)
    contains_9 = np.any(input_array == 9)

    target_value = None
    column_rules = {}

    # Select mode based on marker digits
    if contains_6:
        # Mode 1: Triggered by presence of 6
        target_value = 4
        column_rules = {
            0: 6,
            1: 6,
            # Column 2: 4 remains 4
            3: 5,
            4: 5,
            # Column 5: 4 remains 4
            6: 2,
            # Column 7: 4 remains 4
        }
    elif contains_9:
        # Mode 2: Triggered by presence of 9
        target_value = 0
        column_rules = {
            0: 3,
            1: 3,
            2: 3,
            # Column 3: 0 remains 0
            4: 9,
            # Column 5: 0 remains 0
            6: 4,
            7: 4,
        }
    else:
        # No specific mode triggered, return the original grid copy
        # (or define default behavior if needed)
        return output_grid

    # --- Iterate and Transform ---
    # Get grid dimensions
    num_rows = len(input_grid)
    if num_rows == 0:
        return [] # Handle empty grid case
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return [[] for _ in range(num_rows)] # Handle empty rows case

    # Iterate through each cell of the grid
    for r in range(num_rows):
        for c in range(num_cols):
            # Get the value of the current cell from the original input
            current_value = input_grid[r][c]

            # Check if the current value is the target value for the selected mode
            if current_value == target_value:
                # Check if there is a specific replacement rule for this column
                if c in column_rules:
                    # Apply the rule: replace the value in the output grid
                    replacement_value = column_rules[c]
                    output_grid[r][c] = replacement_value
                # If it's the target value but no rule exists for this column,
                # the value remains unchanged (already copied to output_grid).

            # If the current value is not the target value,
            # it remains unchanged (already copied to output_grid).

    # Return the transformed grid
    return output_grid
```