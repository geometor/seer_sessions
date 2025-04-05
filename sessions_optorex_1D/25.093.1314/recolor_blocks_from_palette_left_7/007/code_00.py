import math
from collections import Counter

"""
Transforms a list or array of 12 integers based on the following rules:

1.  Accept the input, which is a list (or array) of 12 integers.
2.  Designate the first 10 integers as the `main_sequence` and the last two integers as the `control_digits`, referred to as `c1` (the 11th digit) and `c2` (the 12th digit).
3.  Create a copy of the full 12-integer input list; this copy will be modified to become the output list.
4.  Analyze the `main_sequence` to find the `target_digit`:
    *   Count the occurrences of each non-zero digit.
    *   If no non-zero digits exist, the process stops, and the original input list is the output.
    *   Identify the maximum frequency count among these digits.
    *   Find all digits that have the maximum frequency.
    *   The `target_digit` is the smallest digit among those with the maximum frequency.
5.  Identify the `other_digits`: Create a sorted list of all unique non-zero digits present in the `main_sequence` *except* for the `target_digit`.
6.  Construct the `replacement_values` list: Start with the `other_digits` list, then append `c1` if `c1` is not zero, and finally append `c2` if `c2` is not zero.
7.  If the `replacement_values` list is empty, no replacements can be made, so the process stops, and the original input list is the output.
8.  Initialize a counter, `replacement_group_counter`, to 0. This counter tracks which replacement value to use next.
9.  Iterate through the `main_sequence` using an index `i` from 0 to 9.
10. If the element at the current index `i` in the *original* `main_sequence` is equal to the `target_digit`:
    a.  This marks the beginning of a group of target digits.
    b.  Determine the value to use for replacement: Select the element from the `replacement_values` list at the index (`replacement_group_counter` modulo length of `replacement_values`). Store this as `current_replacement_value`.
    c.  Find the end index `j` of the contiguous block of `target_digit`s starting at `i`.
    d.  In the *output list*, replace all elements from index `i` up to and including index `j` with the `current_replacement_value`.
    e.  Increment the `replacement_group_counter` by 1.
    f.  Advance the main iteration index `i` to `j` (the loop's natural increment will then move it to `j+1` for the next check).
11. Continue the iteration until the end of the `main_sequence` is processed (index 9).
12. Return the final modified 12-integer output list.
"""

# === Helper Functions ===

def find_target_digit(sequence: list[int]) -> int | None:
    """
    Finds the most frequent non-zero digit in the sequence.
    Handles ties by selecting the smallest digit among the most frequent ones.
    Returns None if no non-zero digits are present.
    """
    # Filter out zeros
    non_zero_digits = [d for d in sequence if d != 0]
    if not non_zero_digits:
        return None # No non-zero digits found

    # Count frequencies
    counts = Counter(non_zero_digits)
    if not counts:
         # This case should not be reachable if non_zero_digits is not empty
         return None 

    # Find the maximum frequency
    max_freq = 0
    # Find the maximum frequency using max() on values
    # max_freq = max(counts.values()) # Alternatively
    for count in counts.values():
        if count > max_freq:
            max_freq = count

    # Find all digits with that maximum frequency
    most_frequent_digits = [digit for digit, count in counts.items() if count == max_freq]

    # Return the smallest digit among those with the maximum frequency
    return min(most_frequent_digits)


def find_other_digits(sequence: list[int], target_digit: int | None) -> list[int]:
    """Finds unique non-zero digits in the sequence, excluding the target_digit, and returns them sorted."""
    if target_digit is None:
        # If there's no target, no replacements will happen anyway.
        return []
    # Use a set for efficient uniqueness check, then sort
    other_digits_set = set(d for d in sequence if d != 0 and d != target_digit)
    return sorted(list(other_digits_set))

def construct_replacement_values(other_digits: list[int], control_digits: list[int]) -> list[int]:
    """Constructs the ordered list of replacement values from other_digits and non-zero control digits."""
    # Start with the sorted list of other non-zero digits found in the main sequence
    replacement_values = list(other_digits) 
    
    # Append control digits if they are non-zero
    c1, c2 = control_digits
    if c1 != 0:
        replacement_values.append(c1)
    if c2 != 0:
        replacement_values.append(c2)
    return replacement_values

# === Main Transformation Function ===

def transform(input_list: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input list of 12 integers.
    """
    # Basic input validation (optional, depends on framework)
    if not isinstance(input_list, list) or len(input_list) != 12:
         # Return unmodified input if invalid format/size
         return input_list 

    # Step 2: Separate main sequence and control digits
    main_sequence = input_list[:10]
    control_digits = input_list[10:]

    # Step 3: Create a copy of the input list to modify for the output
    output_list = list(input_list) 

    # Step 4: Find the target digit (most frequent non-zero, smallest in case of tie)
    target_digit = find_target_digit(main_sequence)

    # Step 4 (cont.) / Step 7 (implicit): Early exit if no target digit exists
    # If target_digit is None, no replacements are possible.
    if target_digit is None:
        return output_list # Return original list

    # Step 5: Find other non-zero digits (excluding target), sorted
    other_digits = find_other_digits(main_sequence, target_digit)

    # Step 6: Construct the ordered list of replacement values
    replacement_values = construct_replacement_values(other_digits, control_digits)

    # Step 7: Early exit if no replacement values are available
    # If the list is empty, no replacements can be made.
    if not replacement_values:
        return output_list # Return original list

    # Step 8: Initialize counter for cycling through replacement values
    replacement_group_counter = 0 

    # Step 9 & 11: Iterate through the main sequence (indices 0-9) using a while loop
    i = 0
    while i < 10:
        # Step 10: Check if the current digit in the *original* main sequence is the target digit
        if main_sequence[i] == target_digit:
            # Step 10.a: Found the start of a target group
            start_index = i

            # Step 10.b: Determine the replacement value for this entire group using modulo for cycling
            current_replacement = replacement_values[replacement_group_counter % len(replacement_values)]

            # Step 10.c: Find the end index 'j' of the contiguous group of target digits
            j = i
            # Look ahead to find where the sequence of target digits ends within the main_sequence bounds
            while j < 10 and main_sequence[j] == target_digit:
                j += 1
            # The end index is the last position where the digit was the target
            end_index = j - 1 

            # Step 10.d: Replace the identified group in the output list
            for k in range(start_index, end_index + 1):
                output_list[k] = current_replacement

            # Step 10.e: Increment the counter to use the next replacement value for the next group
            replacement_group_counter += 1

            # Step 10.f: Advance the main loop index 'i' past this processed group.
            # The next iteration will start checking from the element after the group.
            i = end_index + 1 
        else:
            # If the current digit is not the target, simply move to the next index
            i += 1

    # Step 12: Return the modified list
    return output_list