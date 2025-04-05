"""
Rearrange digits in a space-separated string, moving all '0' digits to the beginning while preserving the relative order of the non-zero digits.
"""

# No specific imports needed for basic string and list manipulation

def transform(input_str: str) -> str:
    """
    Moves all '0' digits to the beginning of a space-separated string sequence 
    while maintaining the relative order of the non-zero digits.

    Args:
        input_str: A string containing space-separated single digits.

    Returns:
        A string with digits rearranged according to the rule, 
        also space-separated.
    """
    
    # 1. Split the input string by spaces to get a list of digit strings.
    digits = input_str.split(' ')

    # 2. Initialize two empty lists to hold zero and non-zero digits.
    zeros_list = []
    non_zeros_list = []

    # 3. Iterate through the list of digit strings.
    for digit in digits:
        # 4. Partition the digits based on whether they are '0' or not.
        if digit == '0':
            zeros_list.append(digit)
        else:
            non_zeros_list.append(digit) # Preserves relative order of non-zeros

    # 5. Concatenate the list of zeros followed by the list of non-zeros.
    final_ordered_list = zeros_list + non_zeros_list

    # 6. Join the elements of the final list back into a space-separated string.
    output_str = ' '.join(final_ordered_list)

    # 7. Return the resulting string.
    return output_str
