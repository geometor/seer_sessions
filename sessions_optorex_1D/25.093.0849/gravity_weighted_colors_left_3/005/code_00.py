import numpy as np

"""
Takes a 1D NumPy array of integers (0s, 1s, and 2s), sorts the elements in 
ascending order, and returns them as a single space-separated string.
"""

def transform(input_grid: np.ndarray) -> str:
    """
    Sorts the elements of a 1D NumPy array and returns a space-separated string.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A string containing the sorted integers, separated by spaces.
    """
    # Sort the input numpy array in ascending order.
    # Example: np.array([2, 2, 0, 1, 0]) -> np.array([0, 0, 1, 2, 2])
    sorted_array = np.sort(input_grid)

    # Convert each integer in the sorted array to its string representation.
    # Example: np.array([0, 0, 1, 2, 2]) -> ['0', '0', '1', '2', '2']
    string_elements = [str(x) for x in sorted_array]

    # Join the list of string elements with a space separator to form the final output string.
    # Example: ['0', '0', '1', '2', '2'] -> "0 0 1 2 2"
    output_str = " ".join(string_elements)

    # Return the final space-separated string.
    return output_str