```python
import re # Use re for splitting based on whitespace, handling potential multiple spaces

"""
Transforms a space-separated string of digits by replacing every non-zero digit 
with the digit '5', while keeping all '0' digits unchanged. The original spacing 
and order are preserved.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing space-separated single digits (e.g., "0 0 7 8 0 3 0 0 8 1 7 0").

    Returns:
        A string with non-zero digits replaced by '5', preserving zeros and spacing.
    """
    
    # Split the input string into a list of individual digit characters using whitespace as delimiter.
    # Handles multiple spaces between digits if present.
    input_digits = re.split(r'\s+', input_str.strip()) 
    
    # Initialize an empty list to store the output digit characters.
    output_digits = []
    
    # Iterate through each digit character in the input list.
    for digit_char in input_digits:
        # Check if the digit character is '0'.
        if digit_char == '0':
            # If it is '0', append '0' to the output list.
            output_digits.append('0')
        else:
            # If it is not '0' (i.e., '1' through '9'), append '5' to the output list.
            # No need to convert to int, string comparison is sufficient and avoids errors for non-digit inputs if they occurred.
            output_digits.append('5')
            
    # Join the characters in the output list back into a single string, separated by spaces.
    output_str = ' '.join(output_digits)
    
    # Return the resulting transformed string.
    return output_str

```