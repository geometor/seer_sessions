import re

def find_dominant_digit(input_str):
    """
    Finds the single non-zero digit present in the input string.
    Assumes there is exactly one type of non-zero digit.
    """
    # Find all non-zero digits
    non_zero_digits = set(re.findall(r'[1-9]', input_str))
    
    # Check if exactly one non-zero digit type was found
    if len(non_zero_digits) == 1:
        return list(non_zero_digits)[0]
    elif len(non_zero_digits) == 0:
        # Handle case where input is all zeros (although not in examples)
        # Return '0' or raise an error, depending on desired behavior.
        # For this task, based on examples, we expect a non-zero digit.
        # Let's assume the target pattern should still use '0' if input is all '0'.
        return '0' 
    else:
        # Handle unexpected case with multiple non-zero digit types
        raise ValueError("Input string contains multiple different non-zero digits.")


def transform(input_str: str) -> str:
    """
    Transforms the input string based on a fixed pattern.

    The transformation identifies the single non-zero digit (X) present 
    in the input string. It then constructs a new string of 12 digits 
    where X is placed at indices 0, 2, 3, 5, 6, and 7, and '0' is placed 
    at all other indices (1, 4, 8, 9, 10, 11). The original positions 
    of X in the input are ignored.
    """
    
    # 1. Identify the dominant non-zero digit from the input string.
    dominant_digit = find_dominant_digit(input_str)
    
    # 2. Define the fixed positions for the dominant digit and zero.
    #    Indices for the dominant digit: 0, 2, 3, 5, 6, 7
    #    Indices for zero: 1, 4, 8, 9, 10, 11
    output_list = ['0'] * 12 # Initialize with zeros
    dominant_indices = [0, 2, 3, 5, 6, 7]
    
    # 3. Place the dominant digit at the specified indices.
    for index in dominant_indices:
        # Ensure index is within bounds (though it should be for length 12)
        if 0 <= index < 12:
             output_list[index] = dominant_digit
             
    # 4. Join the list elements into a space-separated string.
    output_str = " ".join(output_list)
    
    return output_str
