```python
"""
Transforms an input grid by remapping its non-zero values based on their frequency.
1. Count the frequency of each unique non-zero value in the input grid.
2. Create two ranked lists of these unique non-zero values:
   - InputRank: Sorted primarily by frequency descending, secondarily by value ascending.
   - TargetRank: Sorted primarily by frequency ascending, secondarily by value descending.
3. Establish a mapping where the i-th value in InputRank maps to the i-th value in TargetRank.
4. Create the output grid by replacing each non-zero value in the input grid with its corresponding mapped value, while keeping zero values unchanged.
"""

import numpy as np
from collections import Counter

def _get_value_frequencies(grid):
    """Counts the frequency of each non-zero value in the grid."""
    flat_grid = grid.flatten()
    # Filter out zeros before counting
    non_zero_values = flat_grid[flat_grid != 0]
    frequencies = Counter(non_zero_values)
    return dict(frequencies)

def _create_mapping(frequencies):
    """Creates the value mapping based on frequency rankings."""
    if not frequencies: # Handle cases with no non-zero numbers
        return {}

    # Get unique non-zero values
    unique_values = list(frequencies.keys())

    # Sort for InputRank: frequency descending, value ascending
    ranked_input_values = sorted(
        unique_values,
        key=lambda val: (-frequencies[val], val)
    )

    # Sort for TargetRank: frequency ascending, value descending
    ranked_target_values = sorted(
        unique_values,
        key=lambda val: (frequencies[val], -val)
    )

    # Create the mapping dictionary
    mapping = {
        input_val: target_val
        for input_val, target_val in zip(ranked_input_values, ranked_target_values)
    }
    return mapping

def transform(input_grid):
    """
    Applies the frequency-based value remapping transformation to the input grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # Step 1: Count frequencies of non-zero values
    frequencies = _get_value_frequencies(input_array)

    # Step 2 & 3: Determine the value mapping based on frequency rankings
    value_map = _create_mapping(frequencies)

    # Step 4: Create the output grid by applying the mapping
    # Initialize output grid as a copy of the input to preserve dimensions and zeros
    output_array = np.copy(input_array)

    # Iterate through the cells and apply the mapping
    rows, cols = input_array.shape
    for r in range(rows):
        for c in range(cols):
            input_val = input_array[r, c]
            # Only map non-zero values
            if input_val != 0 and input_val in value_map:
                output_array[r, c] = value_map[input_val]

    # Convert the result back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```