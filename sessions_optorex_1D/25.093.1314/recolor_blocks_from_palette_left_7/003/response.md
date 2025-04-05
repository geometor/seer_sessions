```python
import math
from collections import Counter

"""
Transforms a list or array of 12 integers based on the following rules:

1.  Accept the input, which is a list (or array) of 12 integers.
2.  Designate the first 10 integers as the `main_sequence` and the last two integers as the `control_digits`, referred to as `c1` (the 11th digit) and `c2` (the 12th digit).
3.  Create a copy of the full 12-integer input list; this copy will be modified to become the output list.
4.  Analyze the `main_sequence` to find the `target_digit`:
    *   Count the occurrences of each non-zero digit.
    *   Identify the maximum frequency count among these digits.
    *   If no non-zero digits exist, the process stops, and the original input list is the output.
    *   If one or more non-zero digits exist, find all digits that have the maximum frequency.
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


def find_target_digit(sequence: list[int]) -> int | None:
    """
    Finds the most frequent non-zero digit in the sequence.
    Handles ties by selecting the smallest digit among the most frequent ones.
    Returns None if no non-zero digits are present.
    """
    non_zero_digits = [d for d in sequence if d != 0]
    if not non_zero_digits:
        return None # No non-zero digits found

    counts = Counter(non_zero_digits)
    if not counts:
         return None # Should not happen if non_zero_digits is not empty

    # Find the maximum frequency
    max_freq = 0
    for digit in counts:
        if counts[digit] > max_freq:
            max_freq = counts[digit]

    # Find all digits with that maximum frequency
    most_frequent_digits = [digit for digit, count in counts.items() if count == max_freq]

    # Return the smallest digit among those with the maximum frequency
    return min(most_frequent_digits)


def find_other_digits(sequence: list[int], target_digit: int | None) -> list[int]:
    """Finds unique non-zero digits in the sequence, excluding the target_digit, and returns them sorted."""
    if target_digit is None:
        # If there's no target, technically all non-zeros are "other", but based on logic,
        # if there's no target, replacement won't happen anyway. Return empty.
        return []
    other_digits_set = set(d for d in sequence if d != 0 and d != target_digit)
    return sorted(list(other_digits_set))

def construct_replacement_values(other_digits: list[int], control_digits: list[int]) -> list[int]:
    """Constructs the ordered list of replacement values from other_digits and non-zero control digits."""
    replacement_values = list(other_digits) # Start with sorted other digits
    c1, c2 = control_digits
    if c1 != 0:
        replacement_values.append(c1)
    if c2 != 0:
        replacement_values.append(c2)
    return replacement_values


def transform(input_list: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input list of 12 integers.
    """
    # Ensure input is a list of 12 integers (basic check)
    if not isinstance(input_list, list) or len(input_list) != 12:
         # The framework might handle this, but good practice to check
         # Or raise ValueError("Input must be a list of 12 integers.")
         # Returning input as per instructions if processing can't occur
         return input_list

    # Separate main sequence and control digits
    main_sequence = input_list[:10]
    control_digits = input_list[10:]

    # Create a copy to modify for the output
    output_list = list(input_list)

    # --- Core Logic ---
    # 1. Find the target digit (most frequent non-zero, smallest in case of tie)
    target_digit = find_target_digit(main_sequence)

    # 2. Early exit if no target digit (e.g., all zeros in main sequence)
    if target_digit is None:
        return output_list # Return original list

    # 3. Find other non-zero digits (excluding target)
    other_digits = find_other_digits(main_sequence, target_digit)

    # 4. Construct the list of replacement values
    replacement_values = construct_replacement_values(other_digits, control_digits)

    # 5. Early exit if no replacement values are available
    if not replacement_values:
        return output_list # Return original list, as no replacements can be made

    # 6. Iterate through the main sequence to find and replace target groups
    replacement_cycle_index = 0 # Tracks which replacement value to use next
    i = 0
    while i < 10:
        # Check if the current digit is the target digit
        if main_sequence[i] == target_digit:
            # Found the start of a target group
            start_index = i

            # Determine the replacement value for this entire group
            current_replacement = replacement_values[replacement_cycle_index % len(replacement_values)]

            # Find the end of the contiguous group
            j = i
            while j < 10 and main_sequence[j] == target_digit:
                j += 1
            end_index = j - 1 # The last index included in the group

            # Replace the group in the output list
            for k in range(start_index, end_index + 1):
                output_list[k] = current_replacement

            # Move to the next replacement value for the next group
            replacement_cycle_index += 1

            # Advance the main loop index past this processed group
            i = end_index

        # Move to the next position in the main sequence
        i += 1

    # Return the modified list
    return output_list
```