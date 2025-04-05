```python
"""
Sorts the elements of an input NumPy grid based on the custom priority order 2 > 0 > 1,
preserving the original grid shape.
"""

import numpy as np
# collections is not needed if using NumPy counting methods

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Sorts the elements of the input NumPy grid according to the custom order (2, 0, 1)
    while preserving the original grid dimensions.

    Args:
        input_grid: A NumPy array containing integers 0, 1, or 2.

    Returns:
        A NumPy array with the same shape as input_grid, with elements sorted
        according to the custom order (2s first, then 0s, then 1s).
    """
    # Record the original shape of the input grid
    original_shape = input_grid.shape

    # Flatten the input grid into a 1D array to process all elements together
    flattened_elements = input_grid.flatten()

    # Count the occurrences of each digit (0, 1, 2) using NumPy functions
    count_2 = np.sum(flattened_elements == 2)
    count_0 = np.sum(flattened_elements == 0)
    count_1 = np.sum(flattened_elements == 1)

    # Create a new 1D array with elements sorted according to the custom order: 2, 0, 1
    # Use np.repeat for efficient array creation
    sorted_elements = np.concatenate([
        np.repeat(2, count_2),
        np.repeat(0, count_0),
        np.repeat(1, count_1)
    ])

    # Reshape the sorted 1D array back into the original grid shape
    output_grid = sorted_elements.reshape(original_shape)

    # Ensure the output dtype matches the input dtype
    output_grid = output_grid.astype(input_grid.dtype)

    return output_grid
```