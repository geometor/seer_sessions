
## train_1

**input:**
```
0 0 0 0 0 1 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 1 0 0 0 1 0 0
```


## train_2

**input:**
```
0 0 1 1 0 0 0 0 0 1 0 0
```


**output:**
```
0 3 1 1 3 0 0 0 0 1 0 0
```


## train_3

**input:**
```
1 1 1 0 0 0 0 0 0 1 0 0
```


**output:**
```
1 1 1 0 0 0 0 0 0 1 0 0
```


## train_4

**input:**
```
0 1 0 0 0 0 0 1 1 0 0 0
```


**output:**
```
0 1 0 0 0 0 3 1 1 3 0 0
```


## train_5

**input:**
```
0 0 1 1 1 0 0 0 0 0 1 0
```


**output:**
```
0 0 1 1 1 0 0 0 0 0 1 0
```


## train_6

**input:**
```
0 0 0 1 0 0 0 0 0 0 1 0
```


**output:**
```
0 0 0 1 0 0 0 0 0 0 1 0
```


## train_7

**input:**
```
1 1 0 0 0 1 1 0 0 0 1 0
```


**output:**
```
1 1 3 0 3 1 1 3 0 0 1 0
```

*   **Perception:** The task involves transforming a sequence of integers (0s and 1s) into another sequence of integers (0s, 1s, and 3s). The transformation rule appears to be local, modifying elements based on their neighbors. Specifically, the transformation focuses on identifying sequences of exactly two consecutive '1's. When such a sequence (`1 1`) is found, any '0' immediately preceding it or immediately following it is changed to a '3'. Other elements, including single '1's, sequences of three or more '1's, and '0's not adjacent to a `1 1` sequence, remain unchanged.

*   **Facts:**
    
```yaml
    task_elements:
      - name: input_sequence
        type: list of integers
        description: The initial sequence containing 0s and 1s.
      - name: output_sequence
        type: list of integers
        description: The transformed sequence containing 0s, 1s, and potentially 3s.
        relationship: Derived from input_sequence based on a specific rule.
      - name: target_pattern
        type: sequence of integers
        value: [1, 1]
        description: The specific pattern being searched for in the input sequence.
      - name: replacement_value
        type: integer
        value: 3
        description: The value used to replace adjacent 0s when the target_pattern is found.
      - name: context_values
        type: list of integers
        value: [0]
        description: The value(s) adjacent to the target_pattern that trigger the replacement.

    actions:
      - name: scan_sequence
        input: input_sequence
        output: identified locations of target_pattern
        description: Iterate through the input sequence to find all occurrences of the target_pattern [1, 1].
      - name: check_neighbors
        input: input_sequence, location of target_pattern
        output: indices of neighbors to modify
        description: For each found target_pattern, check the element immediately before and immediately after it.
      - name: modify_element
        input: input_sequence, index, replacement_value
        output: modified sequence
        description: If a neighbor exists at the checked index and its value is 0, change its value to 3.

    process_flow:
      - Start with a copy of the input_sequence to create the initial output_sequence.
      - Iterate through the input_sequence from the first element up to the second-to-last element.
      - At each position `i`, check if the elements at `input_sequence[i]` and `input_sequence[i+1]` match the target_pattern [1, 1].
      - If the pattern matches:
        - Check the element *before* the pattern: If `i > 0` (an element exists before) and `input_sequence[i-1]` is 0, change the corresponding element in the output_sequence (`output_sequence[i-1]`) to 3.
        - Check the element *after* the pattern: If `i + 2 < length(input_sequence)` (an element exists after) and `input_sequence[i+2]` is 0, change the corresponding element in the output_sequence (`output_sequence[i+2]`) to 3.
      - Ensure that modifications are made to the output_sequence copy, not the input_sequence being iterated over, to avoid affecting subsequent checks within the same pass.
      - Return the final output_sequence.

    constraints:
      - The transformation only applies to sequences of *exactly* two consecutive 1s.
      - Longer sequences of 1s (e.g., `1 1 1`) do not trigger the transformation.
      - Single 1s do not trigger the transformation.
      - Only adjacent 0s are modified. Adjacent 1s or the 1s in the pattern itself are not changed.
      - Modifications happen based on the original input state; a 0 changed to 3 does not affect later checks in the same pass.
    ```


*   **Natural Language Program:**
    1.  Initialize the `output_sequence` as a copy of the `input_sequence`.
    2.  Iterate through the `input_sequence` using an index `i` from the start up to the second-to-last element.
    3.  At each index `i`, check if the element at `input_sequence[i]` is 1 and the element at `input_sequence[i+1]` is also 1.
    4.  If this condition (`input_sequence[i] == 1` and `input_sequence[i+1] == 1`) is true:
        a.  Check the element preceding the pattern: If the index `i-1` is valid (i.e., `i > 0`) and the element `input_sequence[i-1]` is 0, update the element at index `i-1` in the `output_sequence` to 3.
        b.  Check the element following the pattern: If the index `i+2` is valid (i.e., `i+2 < length of input_sequence`) and the element `input_sequence[i+2]` is 0, update the element at index `i+2` in the `output_sequence` to 3.
    5.  After iterating through all possible starting positions `i`, return the modified `output_sequence`.
```python
"""
Transforms an input sequence of integers (0s and 1s) based on a local rule.
The rule identifies sequences of exactly two consecutive '1's ([1, 1]).
When such a sequence is found at index i and i+1 in the input sequence:
1. If an element exists before the sequence (at index i-1) and its value is 0,
   that element's value in the output sequence is changed to 3.
2. If an element exists after the sequence (at index i+2) and its value is 0,
   that element's value in the output sequence is changed to 3.
All other elements from the input sequence remain unchanged in the output sequence.
Modifications are based on the original input state and applied to a separate output sequence.
"""

import math # Although not used in this specific logic, good practice to import common libraries if potentially needed
import copy  # Used for creating a mutable copy of the input

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers (0s and 1s).

    Returns:
        A new list of integers representing the transformed sequence (0s, 1s, and 3s).
    """
    # Initialize output_sequence as a copy of the input_sequence
    # This ensures modifications don't affect subsequent checks based on the original input
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Iterate through the input sequence to find the [1, 1] pattern
    # We only need to check up to the second-to-last element (n-2)
    # because we are looking at pairs input_sequence[i] and input_sequence[i+1]
    for i in range(n - 1):
        # Check if the current element and the next element form the [1, 1] pattern
        if input_sequence[i] == 1 and input_sequence[i+1] == 1:
            # If the pattern is found, check neighbors in the original input_sequence

            # Check the element *before* the pattern (at index i-1)
            # Ensure the index i-1 is valid (i > 0)
            if i > 0:
                # Check if the preceding element in the original sequence is 0
                if input_sequence[i-1] == 0:
                    # If it is 0, change the corresponding element in the output_sequence to 3
                    output_sequence[i-1] = 3

            # Check the element *after* the pattern (at index i+2)
            # Ensure the index i+2 is valid (i+2 < n)
            if i + 2 < n:
                # Check if the succeeding element in the original sequence is 0
                if input_sequence[i+2] == 0:
                    # If it is 0, change the corresponding element in the output_sequence to 3
                    output_sequence[i+2] = 3

    # Return the modified sequence
    return output_sequence

```
```python
"""
Transforms an input sequence of integers (0s and 1s) based on a local rule.
The rule identifies sequences of exactly two consecutive '1's ([1, 1]) that are "isolated",
meaning they are not immediately preceded or followed by another '1'.
When such an isolated sequence is found at index i and i+1 in the input sequence:
1. If an element exists before the sequence (at index i-1) and its value is 0,
   that element's value in the output sequence is changed to 3.
2. If an element exists after the sequence (at index i+2) and its value is 0,
   that element's value in the output sequence is changed to 3.
All other elements from the input sequence, including non-isolated [1, 1] sequences
and their neighbors, remain unchanged in the output sequence.
Modifications are based on the original input state and applied to a separate output sequence.
"""

import copy

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers (0s and 1s).

    Returns:
        A new list of integers representing the transformed sequence (0s, 1s, and 3s).
    """
    # Initialize output_sequence as a deep copy of the input_sequence
    # This ensures modifications don't affect subsequent checks based on the original input
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Iterate through the input sequence to find the [1, 1] pattern
    # Loop up to n-2 because we check pairs input_sequence[i] and input_sequence[i+1]
    for i in range(n - 1):
        # Check if the current element and the next element form the [1, 1] pattern
        if input_sequence[i] == 1 and input_sequence[i+1] == 1:

            # Check if the pattern is isolated
            # Is it preceded by 1? Check index i-1 (must be >= 0)
            is_preceded_by_1 = (i > 0 and input_sequence[i-1] == 1)
            # Is it followed by 1? Check index i+2 (must be < n)
            is_followed_by_1 = (i + 2 < n and input_sequence[i+2] == 1)

            # The pattern is isolated if it's NOT preceded by 1 AND NOT followed by 1
            is_isolated = not is_preceded_by_1 and not is_followed_by_1

            # If the pattern is isolated, check its neighbors for 0s and modify output_sequence
            if is_isolated:
                # Check the element *before* the pattern (at index i-1)
                # Ensure the index i-1 is valid (i > 0)
                if i > 0:
                    # Check if the preceding element in the original sequence is 0
                    if input_sequence[i-1] == 0:
                        # If it is 0, change the corresponding element in the output_sequence to 3
                        output_sequence[i-1] = 3

                # Check the element *after* the pattern (at index i+2)
                # Ensure the index i+2 is valid (i+2 < n)
                if i + 2 < n:
                    # Check if the succeeding element in the original sequence is 0
                    if input_sequence[i+2] == 0:
                        # If it is 0, change the corresponding element in the output_sequence to 3
                        output_sequence[i+2] = 3

    # Return the modified sequence
    return output_sequence
```
