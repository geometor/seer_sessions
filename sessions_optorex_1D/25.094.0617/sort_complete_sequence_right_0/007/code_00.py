"""
Transforms a 1D NumPy array (input as shape (1, 12)) of 12 integer digits 
by identifying the unique non-zero digit ('X') present in the input array. 
If the array contains only zeros, 'X' is considered 0. It then constructs a 
new 12-digit sequence where 'X' is placed at fixed indices 
[0, 2, 3, 5, 6, 7], and all other indices are filled with '0'. 
The final output is a string with these 12 digits separated by single spaces.
"""

import numpy as np

def find_dominant_digit(input_array: np.ndarray) -> int:
    """
    Finds the single unique non-zero digit present in the input NumPy array.
    Assumes there is at most one type of non-zero digit.

    Args:
        input_array: A 1D NumPy array of integers (after flattening).

    Returns:
        The dominant non-zero integer digit, or 0 if only zeros are found.
        
    Raises:
        ValueError: If multiple different non-zero digits are found.
    """
    # Find all non-zero elements in the array
    non_zero_elements = input_array[input_array != 0]
    
    # Find the unique values among the non-zero elements
    unique_non_zeros = np.unique(non_zero_elements)
    
    # Determine the dominant digit based on the unique non-zero values found
    if len(unique_non_zeros) == 1:
        # If exactly one unique non-zero digit exists, return it
        return int(unique_non_zeros[0]) # Cast to ensure standard int type
    elif len(unique_non_zeros) == 0:
        # If no non-zero digits were found, the dominant digit is effectively 0
        return 0 
    else:
        # If multiple different non-zero digits are found, raise an error
        # as this violates the assumption based on the examples.
        raise ValueError("Input array contains multiple different non-zero digits.")


def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A 2D NumPy array of shape (1, 12) containing integer digits.

    Returns:
        The transformed sequence as a space-separated string.
    """
    # 1. Validate input shape and flatten if necessary
    #    The input is expected as (1, 12) based on previous errors.
    if input_grid.shape != (1, 12):
         # If shape is already (12,), proceed; otherwise, raise error.
         # This handles potential variations but prioritizes the observed (1, 12).
         if input_grid.shape == (12,):
             flattened_input = input_grid
         else:
             raise ValueError(f"Input array must have shape (1, 12) or (12,), but got {input_grid.shape}")
    else:
        # Flatten the (1, 12) array to (12,) for easier processing
        flattened_input = input_grid.flatten()

    # 2. Identify the dominant non-zero digit from the flattened input array.
    dominant_digit = find_dominant_digit(flattened_input)
    
    # 3. Initialize the output array with 12 zeros. 
    #    Ensure integer type for consistency.
    output_array = np.zeros(12, dtype=int) 
    
    # 4. Define the fixed indices where the dominant digit should be placed.
    dominant_indices = [0, 2, 3, 5, 6, 7]
    
    # 5. Place the dominant digit at the specified indices in the output array.
    #    NumPy allows direct assignment using a list of indices.
    output_array[dominant_indices] = dominant_digit
             
    # 6. Convert the elements of the output array to strings.
    output_strings = [str(digit) for digit in output_array]
    
    # 7. Join the string elements into a single space-separated string.
    output_str = " ".join(output_strings)
    
    # 8. Return the final formatted string.
    return output_str