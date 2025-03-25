"""
Examine the input grid. Ignore all '0' values (background). From the set of non-zero values present in the input grid, select one of them. Output the single digit.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Find all unique non-zero values in the input array.
    non_zero_values = np.unique(input_array[input_array != 0])

    # If there are no non-zero values, return 0 (or some other default). This handles the edge case
    # where the input grid is all zeros. We are constrained to always output a single digit, and never 0.
    # This is impossible if there are no non-zero values. In that case we select arbitrarily.
    if non_zero_values.size == 0:
        return 1 # Arbitrary default choice

    # Select the first non-zero value found.  The problem appears under-constrained
    # as there is no consistent rule for selecting which non-zero value.
    selected_value = non_zero_values[0]

    return int(selected_value)