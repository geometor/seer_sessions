
## train_1

**input:**
```
0 5 5 0 5 5 0 5 5 9 2 3
```


**output:**
```
0 9 9 0 2 2 0 3 3 9 2 3
```


## train_2

**input:**
```
0 0 0 5 5 0 0 0 0 0 0 1
```


**output:**
```
0 0 0 1 1 0 0 0 0 0 0 1
```


## train_3

**input:**
```
0 0 5 5 0 0 5 5 0 0 7 1
```


**output:**
```
0 0 7 7 0 0 1 1 0 0 7 1
```


## train_4

**input:**
```
0 0 5 5 0 0 5 5 0 0 6 1
```


**output:**
```
0 0 6 6 0 0 1 1 0 0 6 1
```


## train_5

**input:**
```
5 5 5 0 0 5 5 5 0 0 2 9
```


**output:**
```
2 2 2 0 0 9 9 9 0 0 2 9
```


## train_6

**input:**
```
0 0 0 0 0 5 5 5 0 0 0 8
```


**output:**
```
0 0 0 0 0 8 8 8 0 0 0 8
```


## train_7

**input:**
```
0 0 5 5 0 0 0 5 5 0 3 5
```


**output:**
```
0 0 3 3 0 0 0 5 5 0 3 5
```

Okay, let's break down the transformation logic.

**Perception of the Elements:**

1.  **Input/Output Structure:** Both input and output are sequences of 12 single digits, separated by spaces.
2.  **Sequence Partition:** The sequence can be conceptually divided into two parts:
    *   The main data sequence: The first 10 digits.
    *   The control digits: The last 2 digits (11th and 12th).
3.  **Core Transformation:** The primary action involves identifying a specific 'target' digit within the main data sequence and replacing its occurrences based on the control digits and potentially other digits in the main sequence.
4.  **Identifying the Target:** In all provided examples, the digit '5' is the one being replaced. Observing the frequency of digits in the first 10 positions of the inputs, '5' is consistently the most frequent non-zero digit. This suggests the target digit is determined by frequency analysis.
5.  **Replacement Values:** The values used for replacement seem to be derived from the control digits and any other non-zero digits present in the main sequence (excluding the target digit itself).
6.  **Group-Based Replacement:** The replacement doesn't apply uniformly to all target digits. Instead, consecutive occurrences (groups) of the target digit are treated as units. Each group is replaced entirely by a single value from a derived sequence of replacement values.
7.  **Replacement Sequence:** The sequence of replacement values appears to be constructed from:
    *   Any non-zero digits in the first 10 positions *other than* the target digit. (In the examples, there's at most one such digit, '9' in train_1). If there are multiple, their order might matter (e.g., sorted or order of appearance). Given only one example, let's assume they form the start of the sequence.
    *   The 11th digit (first control digit), if it's non-zero.
    *   The 12th digit (second control digit), if it's non-zero.
    *   These values are used cyclically for subsequent groups of the target digit.
8.  **Constants:** Digits in the main sequence that are *not* the target digit, and the two control digits themselves, remain unchanged in the output.

**Facts:**


```yaml
Input:
  type: string
  format: sequence of 12 space-separated digits (0-9)
  structure:
    - data_sequence: list of first 10 digits
    - control_digits: list of last 2 digits [c1, c2]

Output:
  type: string
  format: sequence of 12 space-separated digits (0-9)
  relation_to_input: same length, modified based on transformation rule

Transformation_Elements:
  - target_digit (T):
      definition: Most frequent non-zero digit in the input data_sequence.
      source: input data_sequence
  - other_digits (O):
      definition: Set of unique non-zero digits in the input data_sequence, excluding T.
      source: input data_sequence
  - replacement_values (R):
      definition: Ordered list constructed from O (e.g., sorted) followed by non-zero control digits.
      construction: R = sorted(list(O)) + [c1 if c1 != 0] + [c2 if c2 != 0]
      source: O, control_digits
  - target_groups:
      definition: Consecutive sequences of T within the data_sequence.
      source: input data_sequence

Actions:
  1. Identify T from the data_sequence.
  2. Identify O from the data_sequence.
  3. Construct R using O and control_digits [c1, c2].
  4. Iterate through the data_sequence:
     - Identify the k-th target_group.
     - Select the k-th replacement value from R (cycling if necessary).
     - Replace all digits within the k-th target_group with the selected replacement value.
  5. Keep non-target digits in the data_sequence unchanged.
  6. Keep control_digits unchanged.
  7. Format the resulting 12 digits as a space-separated string.

Relationships:
  - The output data_sequence depends on the input data_sequence, T, and R.
  - The output control_digits are identical to the input control_digits.
  - T depends on the frequency of non-zero digits in the input data_sequence.
  - R depends on O, c1, and c2.
```


**Natural Language Program:**

1.  Read the input string and convert it into a list of 12 integer digits.
2.  Separate the list into the `main_sequence` (first 10 digits) and the `control_digits` (last 2 digits, `c1` and `c2`).
3.  Analyze the `main_sequence` to find the `target_digit` (T), which is the non-zero digit appearing most frequently. (Assume a unique most frequent digit exists).
4.  Identify the set of `other_digits` (O), containing unique non-zero digits from the `main_sequence` that are not equal to T.
5.  Construct the ordered list of `replacement_values` (R): Start with the sorted list of `other_digits`, then append `c1` if it's not zero, and finally append `c2` if it's not zero.
6.  Create a copy of the original 12-digit list to serve as the `output_sequence`.
7.  Initialize a `replacement_index` to 0.
8.  Iterate through the `main_sequence` using an index `i` from 0 to 9.
9.  If the digit at `main_sequence[i]` is the `target_digit` (T):
    a.  This marks the beginning of a potential group of target digits.
    b.  Select the next replacement value from the `replacement_values` list `R` using the current `replacement_index` (modulo the length of `R`). Store this value as `current_replacement`.
    c.  Enter an inner loop: While index `i` is less than 10 AND `main_sequence[i]` is equal to T:
        i.  Set the digit in the `output_sequence` at index `i` to `current_replacement`.
        ii. Increment index `i`.
    d.  Increment the `replacement_index`.
    e.  Decrement index `i` by 1 (to counteract the extra increment from the inner loop and the outer loop's next increment).
10. If the digit is not the `target_digit`, leave the corresponding digit in `output_sequence` unchanged.
11. Continue iterating until the end of the `main_sequence` is reached.
12. Convert the final `output_sequence` back into a string with digits separated by spaces.
```python
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

```
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
