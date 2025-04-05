
## train_1

**input:**
```
3 3 3 3 3 3 0 0 3 3 3 3
```


**output:**
```
1 1 1 1 1 1 0 0 2 2 2 2
```


## train_2

**input:**
```
3 3 3 0 0 3 3 3 3 3 3 0
```


**output:**
```
2 2 2 0 0 1 1 1 1 1 1 0
```


## train_3

**input:**
```
0 3 3 3 3 3 0 3 3 3 3 0
```


**output:**
```
0 1 1 1 1 1 0 2 2 2 2 0
```


## train_4

**input:**
```
0 0 0 3 3 3 3 3 3 0 3 3
```


**output:**
```
0 0 0 1 1 1 1 1 1 0 2 2
```


## train_5

**input:**
```
0 0 0 0 3 3 0 3 3 3 3 0
```


**output:**
```
0 0 0 0 2 2 0 1 1 1 1 0
```


## train_6

**input:**
```
0 0 3 3 0 0 0 0 0 3 3 3
```


**output:**
```
0 0 2 2 0 0 0 0 0 1 1 1
```


## train_7

**input:**
```
3 3 0 0 3 3 3 3 3 0 0 0
```


**output:**
```
2 2 0 0 1 1 1 1 1 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences of integers of the same length (12 elements).
    *   Input sequences contain only the integers `0` and `3`.
    *   Output sequences contain the integers `0`, `1`, and `2`.
    *   The value `0` in the input sequence consistently maps to `0` in the output sequence at the same position.
    *   The value `3` in the input sequence maps to either `1` or `2` in the output sequence.
    *   The transformation of `3`s appears to depend on contiguous groups (runs) of `3`s within the input sequence.
    *   There seem to be two distinct groups of `3`s in each input example, separated by `0`s or the sequence boundaries.
    *   The length of these groups of `3`s determines whether they are transformed into `1`s or `2`s. Specifically, the longer group of `3`s becomes `1`s, and the shorter group becomes `2`s.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: input_sequence
        properties:
          - type: list_of_integers
          - allowed_values: [0, 3]
          - length: 12
      - object: output_sequence
        properties:
          - type: list_of_integers
          - allowed_values: [0, 1, 2]
          - length: 12
      - object: sequence_element
        properties:
          - value: integer
          - position: index
      - object: group_of_threes
        properties:
          - type: contiguous_subsequence
          - element_value: 3
          - length: integer
          - start_index: integer
          - end_index: integer
    relationships:
      - type: mapping
        from: input_sequence.element[i]
        to: output_sequence.element[i]
      - condition: input_sequence.element[i] == 0
        implies: output_sequence.element[i] == 0
      - condition: input_sequence.element[i] == 3
        implies: output_sequence.element[i] in [1, 2]
    actions:
      - action: identify_groups
        description: Find all contiguous subsequences consisting solely of the value 3 in the input sequence.
        inputs: input_sequence
        outputs: list_of_group_of_threes
      - action: compare_group_lengths
        description: Compare the lengths of the identified groups of threes. Assume there are exactly two groups.
        inputs: list_of_group_of_threes
        outputs: longer_group, shorter_group
      - action: transform_elements
        description: Create the output sequence based on the input sequence and group comparison.
        inputs: input_sequence, longer_group, shorter_group
        outputs: output_sequence
        steps:
          - Initialize output_sequence as a copy of input_sequence.
          - For elements corresponding to the longer_group in the input, set their value to 1 in the output_sequence.
          - For elements corresponding to the shorter_group in the input, set their value to 2 in the output_sequence.
          - Keep elements with value 0 unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of the same length as the input sequence.
    2.  Identify all distinct contiguous groups (runs) of the number `3` in the input sequence. Record the start index, end index, and length of each group. Assume there will be exactly two such groups.
    3.  Compare the lengths of the two identified groups of `3`s.
    4.  Determine which group is longer and which is shorter.
    5.  Iterate through the input sequence by index:
        a.  If the element at the current index is `0`, place `0` at the corresponding index in the output sequence.
        b.  If the element at the current index belongs to the *longer* group of `3`s (identified in step 3), place `1` at the corresponding index in the output sequence.
        c.  If the element at the current index belongs to the *shorter* group of `3`s (identified in step 3), place `2` at the corresponding index in the output sequence.
    6.  Return the generated output sequence.
```python
import math

def find_groups_of_threes(sequence):
    """
    Identifies contiguous groups (runs) of the number 3 in a sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start' (index), 'end' (index), and 'length'.
        Returns an empty list if no groups of 3 are found.
    """
    groups = []
    in_group = False
    start_index = -1
    for i, val in enumerate(sequence):
        if val == 3 and not in_group:
            # Start of a new group
            in_group = True
            start_index = i
        elif val != 3 and in_group:
            # End of the current group because a non-3 is encountered
            in_group = False
            end_index = i - 1
            length = end_index - start_index + 1
            groups.append({'start': start_index, 'end': end_index, 'length': length})
            start_index = -1 # Reset start index

    # Check if the sequence ends while inside a group of 3s
    if in_group:
        end_index = len(sequence) - 1
        length = end_index - start_index + 1
        groups.append({'start': start_index, 'end': end_index, 'length': length})

    return groups

def transform(input_sequence):
    """
    Transforms an input sequence containing 0s and 3s based on the lengths
    of contiguous groups of 3s.

    Rule:
    1. Identify all distinct contiguous groups of 3s. Assume there are exactly two such groups.
    2. Compare the lengths of the two groups.
    3. Elements corresponding to the longer group of 3s in the input are replaced with 1s.
    4. Elements corresponding to the shorter group of 3s in the input are replaced with 2s.
    5. Elements that are 0 in the input remain 0 in the output.
    """

    # Initialize the output sequence with zeros, same length as input
    output_sequence = [0] * len(input_sequence)

    # Find all contiguous groups of 3s in the input sequence
    groups = find_groups_of_threes(input_sequence)

    # The derived rule assumes exactly two groups of 3s exist
    if len(groups) != 2:
        # If there are no 3s, the output is already correct (all 0s)
        if len(groups) == 0:
             return output_sequence
        # If the number of groups is not 2 (and not 0), the rule is ambiguous based on examples.
        # For robustness or different constraints, this part might need adjustment.
        # Based on the provided analysis, we expect exactly two groups.
        # We could return the initial zero sequence, the input, or raise an error.
        # Let's return the initial zero sequence as a safe default if assumption fails.
        print(f"Warning: Expected 2 groups of 3s, but found {len(groups)}. Returning default output.")
        return output_sequence # Or raise ValueError("Input does not conform to expected pattern of two groups of 3s.")


    # Identify the longer and shorter groups
    group1 = groups[0]
    group2 = groups[1]

    # Determine which group is longer and which is shorter.
    # If lengths are equal, the first group encountered is treated as 'longer'.
    if group1['length'] >= group2['length']:
        longer_group = group1
        shorter_group = group2
    else:
        longer_group = group2
        shorter_group = group1

    # Populate the output sequence based on group membership
    # Elements corresponding to the longer group become 1
    for i in range(longer_group['start'], longer_group['end'] + 1):
        output_sequence[i] = 1

    # Elements corresponding to the shorter group become 2
    for i in range(shorter_group['start'], shorter_group['end'] + 1):
        output_sequence[i] = 2

    # Elements that were 0 in the input are already 0 in the output_sequence initialization

    return output_sequence
```
```python
import math  # Although not strictly needed for this specific logic, it's good practice to include if math ops were anticipated.

"""
Transforms an input sequence containing 0s and 3s based on the lengths
of contiguous groups of 3s.

Rule:
1. Identify all distinct contiguous groups (runs) of the number 3 in the input sequence. Assume there are exactly two such groups.
2. Compare the lengths of the two groups.
3. Elements corresponding to the longer group of 3s in the input are replaced with 1s in the output sequence.
4. Elements corresponding to the shorter group of 3s in the input are replaced with 2s in the output sequence.
5. Elements that are 0 in the input remain 0 in the output.
6. If the two groups of 3s have the same length, the group that appears earlier in the sequence is treated as the 'longer' one (mapped to 1s).
"""

def find_groups_of_threes(sequence):
    """
    Identifies contiguous groups (runs) of the number 3 in a sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start' (index), 'end' (index), and 'length'.
        Returns an empty list if no groups of 3 are found.
    """
    groups = []
    in_group = False
    start_index = -1
    # Ensure input is a list
    sequence_list = list(sequence)

    for i, val in enumerate(sequence_list):
        if val == 3 and not in_group:
            # Start of a new group
            in_group = True
            start_index = i
        elif val != 3 and in_group:
            # End of the current group because a non-3 is encountered
            in_group = False
            end_index = i - 1
            length = end_index - start_index + 1
            groups.append({'start': start_index, 'end': end_index, 'length': length})
            start_index = -1 # Reset start index

    # Check if the sequence ends while inside a group of 3s
    if in_group:
        end_index = len(sequence_list) - 1
        length = end_index - start_index + 1
        groups.append({'start': start_index, 'end': end_index, 'length': length})

    return groups

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # Ensure input is treated as a standard Python list
    input_list = list(input_sequence)
    n = len(input_list)

    # 1. Initialize an output sequence of the same length as the input sequence, filled with 0s.
    output_sequence = [0] * n

    # 2. Find all contiguous groups of 3s in the input sequence.
    groups = find_groups_of_threes(input_list)

    # Based on observations, we assume exactly two groups. Handle deviations gracefully.
    if len(groups) != 2:
        # If there are no 3s or a number of groups other than 2, return the initial zero sequence.
        # This covers cases where the rule assumptions aren't met.
        # The 0s from the input are already correctly handled by the initialization.
        # If input contains only 3s (one group), this will also return all zeros based on this condition.
        return output_sequence

    # 3. Compare the lengths of the two identified groups of 3s.
    group1 = groups[0]
    group2 = groups[1]

    # 4. Determine which group is longer and which is shorter. Handle ties.
    # If lengths are equal, the first group (group1) is designated 'longer'.
    if group1['length'] >= group2['length']:
        longer_group = group1
        shorter_group = group2
    else:
        longer_group = group2
        shorter_group = group1

    # 5. Iterate through the input sequence positions:
    #   a. If the element was 0, the output remains 0 (already initialized).
    #   b. Map elements belonging to the longer group to 1.
    for i in range(longer_group['start'], longer_group['end'] + 1):
        output_sequence[i] = 1

    #   c. Map elements belonging to the shorter group to 2.
    for i in range(shorter_group['start'], shorter_group['end'] + 1):
        output_sequence[i] = 2

    # 6. Return the generated output sequence.
    return output_sequence
```
```python
import numpy as np # Import numpy to handle potential array inputs

"""
Transforms an input sequence containing 0s and 3s based on the lengths of contiguous groups of 3s.

Rule:
1.  Identify all distinct contiguous groups (runs) of the number 3 in the input sequence. Assume there are exactly two such groups.
2.  Convert the input (potentially a NumPy array) to a Python list.
3.  Compare the lengths of the two groups.
4.  Elements corresponding to the longer group of 3s in the input are replaced with 1s in the output sequence.
5.  Elements corresponding to the shorter group of 3s in the input are replaced with 2s in the output sequence.
6.  Elements that are 0 in the input remain 0 in the output.
7.  If the two groups of 3s have the same length, the group that appears earlier in the sequence (smaller start index) is treated as the 'longer' one (mapped to 1s).
"""


def find_groups_of_threes(sequence_list):
    """
    Identifies contiguous groups (runs) of the number 3 in a sequence list.

    Args:
        sequence_list: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a group
        and contains 'start' (index), 'end' (index), and 'length'.
        Returns an empty list if no groups of 3 are found.
    """
    groups = []
    in_group = False
    start_index = -1

    # Iterate through the list to find groups
    for i, val in enumerate(sequence_list):
        val_int = int(val) # Ensure comparison with integer
        if val_int == 3 and not in_group:
            # Start of a new group
            in_group = True
            start_index = i
        elif val_int != 3 and in_group:
            # End of the current group because a non-3 is encountered
            in_group = False
            end_index = i - 1
            length = end_index - start_index + 1
            groups.append({'start': start_index, 'end': end_index, 'length': length})
            start_index = -1 # Reset start index

    # Check if the sequence ends while inside a group of 3s
    if in_group:
        end_index = len(sequence_list) - 1
        length = end_index - start_index + 1
        groups.append({'start': start_index, 'end': end_index, 'length': length})

    return groups

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    """
    # 1. Convert the input sequence into a standard Python list format.
    #    Handles both list and numpy array inputs.
    input_list = list(input_sequence)
    n = len(input_list)

    # 2. Initialize an output list of the same length as the input, filled with 0s.
    #    This correctly handles the mapping of 0s from input to output.
    output_sequence = [0] * n

    # 3. Identify the two distinct contiguous groups (runs) of the number 3.
    groups = find_groups_of_threes(input_list)

    # 4. Check if exactly two groups were found. If not, return the default (all zeros) output.
    #    This aligns with the observation that all valid examples have two groups.
    if len(groups) != 2:
        # Covers cases with 0, 1, or >2 groups.
        return output_sequence

    # 5. Compare the lengths of the two identified groups.
    group1 = groups[0]
    group2 = groups[1]

    # 6. Designate 'longer' and 'shorter' groups. Apply tie-breaking rule.
    #    If lengths are equal, group1 (appearing first) is 'longer'.
    if group1['length'] >= group2['length']:
        longer_group = group1
        shorter_group = group2
    else:
        longer_group = group2
        shorter_group = group1

    # 7. Map elements of the 'longer' group to 1 in the output list.
    for i in range(longer_group['start'], longer_group['end'] + 1):
        output_sequence[i] = 1

    # 8. Map elements of the 'shorter' group to 2 in the output list.
    for i in range(shorter_group['start'], shorter_group['end'] + 1):
        output_sequence[i] = 2

    # 9. Return the generated output list.
    return output_sequence
```
