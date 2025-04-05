import re

"""
The transformation rule identifies the digit '2' in a sequence of digits. 
If a contiguous block of '0's exists immediately adjacent (left or right) to a '2', 
the rule attempts to find the first non-zero digit bordering that block of '0's 
on the side opposite the '2'. If such a non-zero digit is found before reaching 
the sequence boundary or another '2', the entire block of '0's is replaced 
by that non-zero digit. This process is applied independently for the left and 
right sides of each '2' found in the sequence. If no '2' is present, or if the 
conditions for replacement are not met (e.g., no adjacent '0's, or adjacent '0's 
are not bordered by a non-zero digit on the other side), the sequence remains unchanged.
"""

def transform(input_str: str) -> str:
    """
    Applies the described transformation rule to a space-separated string of digits.

    Args:
        input_str: A string containing space-separated digits.

    Returns:
        A string containing the transformed sequence of space-separated digits.
    """

    # Convert the input string to a list of integers
    digits = [int(d) for d in input_str.split()]
    n = len(digits)
    
    # Create a copy to modify, ensuring changes don't affect index lookup during iteration
    output_digits = list(digits) 

    # Find indices of all '2's
    two_indices = [i for i, digit in enumerate(digits) if digit == 2]

    # Process each '2' found
    for idx in two_indices:
        
        # --- Check Left ---
        # Find the start of the contiguous block of zeros to the left of '2'
        zero_end_left = idx - 1
        zero_start_left = -1
        if zero_end_left >= 0 and digits[zero_end_left] == 0:
            # Scan left to find the beginning of the zero block
            i = zero_end_left
            while i >= 0 and digits[i] == 0:
                zero_start_left = i
                i -= 1
            
            # Find the first non-zero digit further left (the fill digit)
            fill_digit_left = 0
            fill_digit_idx_left = zero_start_left - 1
            if fill_digit_idx_left >= 0:
                 # We only fill if the bordering digit is non-zero and not another '2'
                 # (though the '2' condition isn't explicitly required by examples, it prevents infinite loops in theoretical cases like 2 0 2)
                 # Considering the examples, the fill only happens if the source is not 0.
                 if digits[fill_digit_idx_left] != 0:
                     fill_digit_left = digits[fill_digit_idx_left]


            # If a valid fill digit was found, replace the zeros
            if zero_start_left != -1 and fill_digit_left != 0:
                for i in range(zero_start_left, zero_end_left + 1):
                    # Modify the output list, not the original list used for lookups
                    output_digits[i] = fill_digit_left 

        # --- Check Right ---
        # Find the end of the contiguous block of zeros to the right of '2'
        zero_start_right = idx + 1
        zero_end_right = -1
        if zero_start_right < n and digits[zero_start_right] == 0:
            # Scan right to find the end of the zero block
            i = zero_start_right
            while i < n and digits[i] == 0:
                zero_end_right = i
                i += 1

            # Find the first non-zero digit further right (the fill digit)
            fill_digit_right = 0
            fill_digit_idx_right = zero_end_right + 1
            if fill_digit_idx_right < n:
                 # We only fill if the bordering digit is non-zero and not another '2'
                 if digits[fill_digit_idx_right] != 0:
                     fill_digit_right = digits[fill_digit_idx_right]

            # If a valid fill digit was found, replace the zeros
            if zero_end_right != -1 and fill_digit_right != 0:
                for i in range(zero_start_right, zero_end_right + 1):
                     # Modify the output list
                    output_digits[i] = fill_digit_right

    # Convert the potentially modified list back to a space-separated string
    return " ".join(map(str, output_digits))
