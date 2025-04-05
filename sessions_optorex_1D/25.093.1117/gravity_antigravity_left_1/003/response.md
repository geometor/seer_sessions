```python
import numpy as np
import collections

"""
Rearrange the elements of an input NumPy array containing integers (0, 1, 2) 
such that all 2s appear first, followed by all 0s, and finally all 1s, 
maintaining the original counts of each integer.
"""

def count_elements(arr: np.ndarray) -> collections.Counter:
    """Counts the occurrences of each element in a NumPy array."""
    return collections.Counter(arr)

def construct_sorted_array(counts: collections.Counter) -> np.ndarray:
    """Constructs a NumPy array sorted according to the order 2, 0, 1."""
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)
    count_2 = counts.get(2, 0)

    # Create lists for each element type based on counts
    twos = [2] * count_2
    zeros = [0] * count_0
    ones = [1] * count_1

    # Combine lists in the desired order (2, 0, 1)
    sorted_list = twos + zeros + ones

    # Convert the final list to a NumPy array
    return np.array(sorted_list, dtype=int)


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms an input NumPy array of integers (0, 1, 2)
    by rearranging them according to the custom sort order: 2, 0, 1.

    Args:
        input_grid: A NumPy array containing integers (0, 1, or 2).

    Returns:
        A NumPy array containing the rearranged integers.
    """
    # Ensure the input is treated as a 1D array for counting purposes
    # This handles cases where the input might be multidimensional, although
    # the examples suggest 1D input. Flattening makes it robust.
    flat_input = input_grid.flatten()

    # Count the occurrences of each number (0, 1, 2)
    element_counts = count_elements(flat_input)

    # Construct the output array based on the custom sort order (2, 0, 1)
    output_grid = construct_sorted_array(element_counts)

    # Reshape the output to match the original input shape if needed.
    # For the provided examples (1D arrays), this step might not change anything,
    # but it's good practice if the original shape must be preserved.
    # However, the examples show 1D output even for potentially 2D interpretable inputs
    # if they were grids. Sticking to 1D output as per examples.
    # If preserving original shape was required: output_grid = output_grid.reshape(input_grid.shape)

    return output_grid
```