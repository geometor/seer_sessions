import math
import numpy as np
import re # Added for potential regex use, though list operations might be simpler here

"""
Reverses the contiguous subsequence containing all non-zero digits within a sequence of digits, 
leaving leading and trailing zeros in their original positions.

1.  Receive the input sequence of digits (as a string).
2.  Convert the input string into a list of digit strings.
3.  Find the index of the first non-zero digit in the sequence.
4.  Find the index of the last non-zero digit in the sequence.
5.  If no non-zero digits are found, return the original input string.
6.  Extract the leading zeros (elements before the first non-zero).
7.  Extract the subsequence containing digits from the first non-zero up to and including the last non-zero.
8.  Extract the trailing zeros (elements after the last non-zero).
9.  Reverse the extracted subsequence.
10. Concatenate the leading zeros, the reversed subsequence, and the trailing zeros.
11. Join the elements of the resulting list back into a space-separated string.
12. Return the constructed output string.
"""

def _find_first_nonzero_index(digit_list):
    """Finds the index of the first non-zero digit string."""
    for i, digit in enumerate(digit_list):
        if digit != '0':
            return i
    return -1 # Return -1 if no non-zero digit is found

def _find_last_nonzero_index(digit_list):
    """Finds the index of the last non-zero digit string."""
    for i in range(len(digit_list) - 1, -1, -1):
        if digit_list[i] != '0':
            return i
    return -1 # Return -1 if no non-zero digit is found

def transform(input_str: str) -> str:
    """
    Reverses the subsequence of non-zero digits within a space-separated string of digits.

    Args:
        input_str: A string containing space-separated single digits.

    Returns:
        A string with the non-zero subsequence reversed, preserving leading/trailing zeros.
    """
    
    # 1 & 2. Convert the input string into a list of digit strings.
    input_list = input_str.split(' ')
    
    # 3. Find the index of the first non-zero digit.
    start_index = _find_first_nonzero_index(input_list)
    
    # 5. If no non-zero digits are found, return the original input string.
    if start_index == -1:
        return input_str
        
    # 4. Find the index of the last non-zero digit.
    end_index = _find_last_nonzero_index(input_list) # We know at least one exists now
    
    # 6. Extract the leading zeros.
    leading_zeros = input_list[:start_index]
    
    # 7. Extract the subsequence.
    # Note: Python slicing is exclusive of the end index, so add 1 to end_index.
    subsequence = input_list[start_index : end_index + 1] 
    
    # 8. Extract the trailing zeros.
    trailing_zeros = input_list[end_index + 1 :]
    
    # 9. Reverse the extracted subsequence.
    reversed_subsequence = subsequence[::-1]
    
    # 10. Concatenate the parts.
    output_list = leading_zeros + reversed_subsequence + trailing_zeros
    
    # 11. Join the elements back into a space-separated string.
    output_str = ' '.join(output_list)
    
    # 12. Return the constructed output string.
    return output_str
