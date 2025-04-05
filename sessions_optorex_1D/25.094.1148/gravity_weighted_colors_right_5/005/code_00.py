import numpy as np

"""
Sorts the input sequence of integers (represented as a 1D NumPy array) in ascending order.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Takes a 1D NumPy array of integers, sorts them in ascending order,
    and returns the sorted array.

    Args:
        input_grid: A 1D NumPy array containing integers (0, 1, or 2).

    Returns:
        A 1D NumPy array containing the sorted integers in ascending order.
    """
    # Sort the input array in ascending order
    # Example: [1, 2, 0, 2] -> [0, 1, 2, 2]
    # NumPy's sort function sorts in ascending order by default.
    output_grid = np.sort(input_grid)

    # Return the final sorted array
    return output_grid