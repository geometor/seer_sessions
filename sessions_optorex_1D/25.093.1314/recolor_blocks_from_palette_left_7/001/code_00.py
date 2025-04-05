import math
from collections import Counter

"""
Transforms a sequence of 12 digits based on the following rules:
1. Identify the 'target_digit' as the most frequent non-zero digit within the first 10 digits ('main_sequence').
2. Identify 'other_digits' as the set of unique non-zero digits in the 'main_sequence', excluding the 'target_digit'.
3. Construct an ordered list of 'replacement_values' by taking the sorted 'other_digits', followed by the 11th digit (if non-zero), and then the 12th digit (if non-zero).
4. Iterate through the 'main_sequence'. When a consecutive group of 'target_digits' is found, replace all digits in that group with the next value from the 'replacement_values' list, cycling through the list if necessary.
5. Digits in the 'main_sequence' that are not the 'target_digit' remain unchanged.
6. The 11th and 12th digits ('control_digits') remain unchanged.
7. Format the resulting 12 digits as a space-separated string.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string of digits into a list of integers."""
    return [int(d) for d in input_str.split()]

def find_target_digit(sequence: list[int]) -> int | None:
    """Finds the most frequent non-zero digit in the sequence."""
    non_zero_digits = [d for d in sequence if d != 0]
    if not non_zero_digits:
        return None # No non-zero digits found
    
    counts = Counter(non_zero_digits)
    # Find the digit with the maximum count. 
    # If there are ties, this will return one of the most frequent ones,
    # which matches the observed behavior where '5' was consistently the target.
    # For a more robust tie-breaking (e.g., smallest digit), additional logic would be needed.
    most_common = counts.most_common(1)
    if not most_common:
         return None # Should not happen if non_zero_digits is not empty
    
    target_digit, _ = most_common[0]
    return target_digit

def find_other_digits(sequence: list[int], target_digit: int | None) -> list[int]:
    """Finds unique non-zero digits in the sequence, excluding the target_digit."""
    if target_digit is None:
        return []
    other_digits_set = set(d for d in sequence if d != 0 and d != target_digit)
    return sorted(list(other_digits_set))

def construct_replacement_values(other_digits: list[int], control_digits: list[int]) -> list[int]:
    """Constructs the ordered list of replacement values."""
    replacement_values = list(other_digits) # Start with sorted other digits
    c1, c2 = control_digits
    if c1 != 0:
        replacement_values.append(c1)
    if c2 != 0:
        replacement_values.append(c2)
    return replacement_values

def format_output(digits: list[int]) -> str:
    """Formats the list of digits back into a space-separated string."""
    return " ".join(map(str, digits))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.
    """
    # Parse the input string into a list of digits
    digits = parse_input(input_str)
    if len(digits) != 12:
        raise ValueError("Input string must contain exactly 12 digits.")

    # Separate main sequence and control digits
    main_sequence = digits[:10]
    control_digits = digits[10:]

    # Identify the target digit based on frequency
    target_digit = find_target_digit(main_sequence)

    # If no target digit found (e.g., all zeros in main_sequence), return original
    if target_digit is None:
        return input_str

    # Identify other non-zero digits
    other_digits = find_other_digits(main_sequence, target_digit)

    # Construct the sequence of replacement values
    replacement_values = construct_replacement_values(other_digits, control_digits)

    # If there are no replacement values, no replacements can occur.
    if not replacement_values:
        return input_str
        
    # Initialize the output sequence as a copy of the input
    output_digits = list(digits)
    
    # Initialize index for cycling through replacement values
    replacement_index = 0
    
    # Iterate through the main sequence to find and replace target groups
    i = 0
    while i < 10:
        # Check if the current digit is the target digit
        if main_sequence[i] == target_digit:
            # Found the start of a potential group
            start_index = i
            
            # Determine the replacement value for this group
            current_replacement = replacement_values[replacement_index % len(replacement_values)]
            
            # Replace all consecutive target digits in this group
            while i < 10 and main_sequence[i] == target_digit:
                output_digits[i] = current_replacement
                i += 1
                
            # Move to the next replacement value for the next group
            replacement_index += 1
            
            # Decrement i because the outer loop will increment it, 
            # ensuring we don't skip the digit immediately after the group
            i -= 1 
            
        # Move to the next digit in the main sequence
        i += 1

    # Format the transformed digits back into a string
    return format_output(output_digits)
