import numpy as np

"""
Transforms a 1D NumPy array of digit strings based on the following rule:
Iterate through the input array starting from the second element (index 1). 
If an element is the string '2' and the preceding element is also the string '2', 
the corresponding output element becomes the string '8'. 
Otherwise, the output element is the same as the input element. 
The first element of the input array is never changed and is copied directly to the output.
The final output is a single string with elements joined by spaces.
"""

def format_output(output_list):
  """Converts the list of output digits (strings) back into a space-separated string."""
  return ' '.join(output_list)

def transform(input_array: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_array: A 1D NumPy array of strings, where each string is a digit.

    Returns:
        A string representing the transformed sequence with elements joined by spaces.
    """
    # Get the size of the input array
    n = len(input_array)

    # Handle empty input array
    if n == 0:
        return ""

    # Initialize the output list
    output_digits = []

    # Copy the first element directly (it never changes)
    output_digits.append(input_array[0])

    # Iterate through the input array starting from the second element (index 1)
    for i in range(1, n):
        # Get the current element and the previous element
        current_digit = input_array[i]
        previous_digit = input_array[i-1]

        # Check the transformation condition: current is '2' and previous is '2'
        if current_digit == '2' and previous_digit == '2':
            # If the condition is met, append '8' to the output list
            output_digits.append('8')
        else:
            # Otherwise, append the original current element to the output list
            output_digits.append(current_digit)

    # Format the output list into a space-separated string
    output_str = format_output(output_digits)

    return output_str