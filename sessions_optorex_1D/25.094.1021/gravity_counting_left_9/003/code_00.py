import numpy as np

"""
Transforms an input NumPy array of 12 integers (0-9) into an output string.
The transformation rule is as follows:
1. Count the number of 0 values in the input array. Let this be N.
2. The number of non-zero values (1-9) in the input array will be M = 12 - N.
3. The output string consists of N '0' characters followed by M '1' characters, separated by spaces.
"""

def count_zeros_in_array(arr):
  """Counts the number of zero elements in a NumPy array."""
  return np.count_nonzero(arr == 0)

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid: A NumPy array of shape (12,) containing integers from 0 to 9.

    Returns:
        A string containing space-separated '0's and '1's based on the rule.
    """
    # Ensure input is a NumPy array (though the type hint already suggests this)
    if not isinstance(input_grid, np.ndarray):
       # Handle potential non-numpy input if necessary, or raise error
       # For this task, we assume it's always a numpy array as per analysis
       pass 
       
    # Get the total number of elements (should be 12)
    total_elements = input_grid.size 

    # Count the number of zeros in the input array
    zero_count = count_zeros_in_array(input_grid)
    # zero_count = (input_grid == 0).sum() # Alternative NumPy way

    # Calculate the number of non-zeros
    non_zero_count = total_elements - zero_count

    # Construct the output list of strings
    # Create a list with N '0' strings
    output_zeros = ['0'] * zero_count
    # Create a list with M '1' strings
    output_ones = ['1'] * non_zero_count
    # Concatenate the two lists
    output_list = output_zeros + output_ones

    # Format the output list into a space-separated string
    output_str = ' '.join(output_list)

    return output_str