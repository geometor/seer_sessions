import numpy as np

"""
Transforms an input NumPy array of 12 integers by moving the last 3 elements to the beginning, maintaining the relative order of both the moved elements and the remaining elements, and returns the result as a space-separated string.
"""

# --- Helper Functions ---

def get_slice(sequence: np.ndarray, start_index: int, end_index: int = None) -> np.ndarray:
    """
    Extracts a slice from a NumPy array.
    If end_index is None, slices from start_index to the end.
    """
    if end_index is None:
        return sequence[start_index:]
    else:
        # Handle numpy slicing where end index is exclusive
        # Adjust for negative indices if needed, but direct slicing works
        return sequence[start_index:end_index]

def concatenate_arrays(arr1: np.ndarray, arr2: np.ndarray) -> np.ndarray:
    """
    Concatenates two NumPy arrays.
    """
    return np.concatenate((arr1, arr2))

def format_array_to_string(arr: np.ndarray) -> str:
    """
    Converts a NumPy array of numbers into a space-separated string.
    """
    # Convert each element to string
    string_elements = [str(item) for item in arr]
    # Join with spaces
    return " ".join(string_elements)

# --- Main Transformation Function ---

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A NumPy array containing 12 integers.

    Returns:
        A string containing the transformed sequence of 12 space-separated digits.
    """

    # 1. Define the number of elements to move
    num_elements_to_move = 3

    # 2. Extract the last 3 elements using the helper function
    #    Negative indexing starts from -num_elements_to_move
    last_part = get_slice(input_grid, -num_elements_to_move) # end_index is None here

    # 3. Extract the first 9 elements using the helper function
    #    Slices from the beginning (index 0) up to the start of the last part
    first_part = get_slice(input_grid, 0, -num_elements_to_move)

    # 4. Concatenate the parts in the new order (last part first)
    reordered_array = concatenate_arrays(last_part, first_part)

    # 5. Format the resulting array into a space-separated string
    output_str = format_array_to_string(reordered_array)

    # 6. Return the final string
    return output_str