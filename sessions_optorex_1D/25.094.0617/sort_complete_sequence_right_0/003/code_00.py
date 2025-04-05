"""
Transforms an input sequence of 12 digits (represented as a space-separated 
string within a bytes object) based on a fixed pattern. 

The transformation involves:
1. Decoding the input bytes into a string (assuming UTF-8).
2. Identifying the single unique non-zero digit ('X') present in the string. 
   If only zeros are present, 'X' is '0'.
3. Constructing a new 12-digit sequence where 'X' is placed at indices 
   0, 2, 3, 5, 6, and 7 (0-based indexing).
4. All other indices (1, 4, 8, 9, 10, 11) are filled with '0'.
5. Formatting the resulting sequence as a space-separated string.
"""

import re

def find_dominant_digit(input_str: str) -> str:
    """
    Finds the single non-zero digit present in the input string.
    Assumes there is exactly one type of non-zero digit, or only zeros.
    
    Args:
        input_str: The decoded input string containing space-separated digits.
        
    Returns:
        The dominant non-zero digit as a string, or '0' if only zeros are found.
        
    Raises:
        ValueError: If multiple different non-zero digits are found.
    """
    # Find all unique non-zero digits using a regular expression
    non_zero_digits = set(re.findall(r'[1-9]', input_str))
    
    # Check the number of unique non-zero digits found
    if len(non_zero_digits) == 1:
        # Return the single dominant digit found
        return list(non_zero_digits)[0]
    elif len(non_zero_digits) == 0:
        # If no non-zero digits were found, the dominant digit is effectively '0'
        return '0' 
    else:
        # Raise an error if the input violates the assumption of a single dominant digit
        raise ValueError("Input string contains multiple different non-zero digits.")


def transform(input_bytes: bytes) -> str:
    """
    Applies the transformation rule to the input byte sequence.
    
    Args:
        input_bytes: The input sequence as a bytes object.
        
    Returns:
        The transformed sequence as a space-separated string.
    """
    
    # 1. Decode the input bytes into a string using UTF-8 encoding.
    try:
        input_str = input_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Handle potential decoding errors if the input is not valid UTF-8
        # For this specific problem based on examples, UTF-8 is assumed.
        # If other encodings are possible, more robust handling is needed.
        raise ValueError("Input could not be decoded as UTF-8.")

    # 2. Identify the dominant non-zero digit from the decoded string.
    dominant_digit = find_dominant_digit(input_str)
    
    # 3. Initialize the output list with 12 zeros.
    output_list = ['0'] * 12 
    
    # 4. Define the fixed indices where the dominant digit should be placed.
    dominant_indices = [0, 2, 3, 5, 6, 7]
    
    # 5. Place the dominant digit at the specified indices in the output list.
    for index in dominant_indices:
        # Basic bounds check, although indices are fixed and within range for length 12
        if 0 <= index < 12:
             output_list[index] = dominant_digit
             
    # 6. Join the list elements into a single space-separated string.
    output_str = " ".join(output_list)
    
    # 7. Return the final formatted string.
    return output_str