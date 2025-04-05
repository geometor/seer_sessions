import collections

def transform(input_str: str) -> str:
    """
    Performs a left cyclic shift on a sequence of digits represented as a space-separated string.
    The first digit is moved to the end of the sequence.
    """
    # 1. Read the input sequence of digits.
    # Split the input string into a list of digit strings
    digits = input_str.split(' ')

    # Check if the list is empty or has only one element, in which case no shift is needed
    if len(digits) <= 1:
        return input_str

    # 2. Identify the first digit in the sequence.
    first_digit = digits[0]

    # 3. Create a new sequence containing all digits from the second position to the end.
    remaining_digits = digits[1:]

    # 4. Append the identified first digit to the end of this new sequence.
    shifted_digits = remaining_digits + [first_digit]

    # 5. Output the resulting sequence.
    # Join the shifted list back into a space-separated string
    output_str = ' '.join(shifted_digits)

    return output_str
