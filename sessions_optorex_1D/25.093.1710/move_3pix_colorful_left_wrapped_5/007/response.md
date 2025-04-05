```python
"""
Moves the first three elements of a 1D NumPy array of length 12 to the end of the array,
preserving the relative order of both the moved elements and the remaining elements.
"""

import numpy as np
from typing import List, Any # Although input/output are numpy arrays, keep for potential compatibility


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms a 1D NumPy array of 12 elements by moving the first three elements to the end.

    Args:
        input_grid: A NumPy array of shape (12,) containing the input elements.

    Returns:
        A new NumPy array of shape (12,) with the first three elements moved to the end.
    """

    # Expected length of the input array
    expected_length = 12

    # Basic validation (optional, depending on environment guarantees)
    if not isinstance(input_grid, np.ndarray):
        # Convert if possible, e.g., from list, otherwise raise error or handle as needed
        try:
            input_grid = np.array(input_grid)
        except Exception as e:
             raise TypeError(f"Input must be a NumPy array or convertible to one. Got type: {type(input_grid)}. Error: {e}")

    if input_grid.ndim != 1 or input_grid.shape[0] != expected_length:
        raise ValueError(f"Input array must be 1D with exactly {expected_length} elements. Got shape: {input_grid.shape}")


    # --- Transformation Steps ---

    # 1. Extract the first three elements (indices 0, 1, 2)
    # Slicing a NumPy array creates a view or a copy depending on the context,
    # but for concatenation, the actual values are used.
    first_three_elements = input_grid[:3]

    # 2. Extract the remaining nine elements (from index 3 onwards)
    remaining_elements = input_grid[3:]

    # 3. Concatenate the remaining elements followed by the first three elements
    # np.concatenate joins a sequence of arrays along an existing axis.
    # For 1D arrays, it joins them end-to-end.
    output_grid = np.concatenate((remaining_elements, first_three_elements))

    # 4. Return the resulting array
    return output_grid
```