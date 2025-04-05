import math

"""
Takes an input string of space-separated integers. 
Separates the integers into two groups: zeros and non-zeros.
Concatenates the group of zeros followed by the group of non-zeros, 
preserving the original relative order of the non-zero integers.
Finally, formats the resulting sequence back into a space-separated string.
"""

def partition_by_zero(numbers):
    """Separates a list of numbers into zeros and non-zeros."""
    zeros = [num for num in numbers if num == 0]
    non_zeros = [num for num in numbers if num != 0]
    return zeros, non_zeros

def format_numbers_to_string(numbers):
    """Converts a list of numbers to a space-separated string."""
    return " ".join(map(str, numbers))

def transform(input_str: str) -> str:
    """
    Reorders a sequence of space-separated integers by moving all zeros
    to the beginning while maintaining the relative order of non-zero elements.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the reordered space-separated integers.
    """
    # 1. Parse the input string into a list of integers
    try:
        # Split the string by spaces and convert each part to an integer
        input_numbers = [int(x) for x in input_str.split()]
    except ValueError:
        # Handle potential errors if the input string contains non-integer values
        print(f"Error: Input string '{input_str}' contains non-integer elements.")
        return "" # Or raise an exception, depending on desired error handling

    # 2. Partition the list into zeros and non-zeros
    # The partition_by_zero helper function performs this separation.
    # Crucially, list comprehensions preserve the order of elements they process.
    zeros_list, non_zeros_list = partition_by_zero(input_numbers)

    # 3. Concatenate the lists: zeros first, then non-zeros
    # This places all zeros at the beginning, followed by the non-zeros
    # in their original relative order.
    output_numbers = zeros_list + non_zeros_list

    # 4. Format the resulting list back into a space-separated string
    # The format_numbers_to_string helper function handles this conversion.
    output_str = format_numbers_to_string(output_numbers)

    # 5. Return the final output string
    return output_str
