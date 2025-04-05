
## train_1

**input:**
```
0 0 7 7 0 7 7 7 7 7 0 0
```


**output:**
```
0 0 7 7 0 1 1 1 1 1 0 0
```


## train_2

**input:**
```
0 0 9 9 9 0 0 0 0 9 9 0
```


**output:**
```
0 0 1 1 1 0 0 0 0 9 9 0
```


## train_3

**input:**
```
0 0 8 8 8 0 8 8 8 8 8 8
```


**output:**
```
0 0 8 8 8 0 1 1 1 1 1 1
```


## train_4

**input:**
```
0 5 5 5 5 5 0 0 0 5 5 0
```


**output:**
```
0 1 1 1 1 1 0 0 0 5 5 0
```


## train_5

**input:**
```
3 3 0 0 3 3 3 3 0 0 0 0
```


**output:**
```
3 3 0 0 1 1 1 1 0 0 0 0
```


## train_6

**input:**
```
6 6 6 6 6 0 6 6 0 0 0 0
```


**output:**
```
1 1 1 1 1 0 6 6 0 0 0 0
```


## train_7

**input:**
```
5 5 5 0 5 5 5 5 5 0 0 0
```


**output:**
```
5 5 5 0 1 1 1 1 1 0 0 0
```

Okay, analyzing the provided examples.

**Perception of Task Elements:**

1.  **Input/Output Data:** Both input and output are sequences (lists or arrays) of single-digit integers.
2.  **Core Operation:** The transformation modifies a specific portion of the input sequence while leaving the rest unchanged.
3.  **Target Identification:** The modification targets contiguous subsequences (runs) of identical non-zero digits. For example, in `0 0 7 7 0 7 7 7 7 7 0 0`, the runs are `7 7` and `7 7 7 7 7`. `0`s are ignored when identifying these runs.
4.  **Selection Criterion:** Among all identified runs of identical non-zero digits, the *longest* run is selected for modification. If there are multiple runs of the same maximum length, the first one encountered (from left to right) seems to be the one selected based on the examples (though no example explicitly tests this tie-breaker).
5.  **Modification Rule:** The selected longest run is replaced by a sequence of the digit `1`, with the same length as the original run.

**YAML Fact Documentation:**


```yaml
objects:
  - name: sequence
    properties:
      - type: list_of_integers
      - contains: digits (0-9)
  - name: run
    properties:
      - type: contiguous_subsequence
      - composed_of: identical_non_zero_digits
      - attributes:
          - start_index: integer
          - end_index: integer
          - length: integer
          - digit_value: integer (1-9)
relationships:
  - type: containment
    subject: run
    object: sequence
    details: A sequence can contain zero or more runs.
actions:
  - name: identify_runs
    input: sequence
    output: list_of_runs
    description: Finds all contiguous subsequences of identical non-zero digits within the input sequence.
  - name: find_longest_run
    input: list_of_runs
    output: selected_run (or null if no runs)
    description: >
      Selects the run with the maximum length from the list.
      If multiple runs share the maximum length, selects the one with the smallest start_index.
  - name: replace_run_with_ones
    input:
      - sequence
      - selected_run
    output: modified_sequence
    description: >
      Replaces the digits within the sequence corresponding to the selected_run's start_index and end_index
      with the digit '1'. The length of the replacement is the same as the length of the selected_run.
```


**Natural Language Program:**

1.  Scan the input sequence to identify all contiguous runs (subsequences) consisting of identical non-zero digits. Record the start index, end index, and length of each identified run.
2.  Compare the lengths of all identified runs.
3.  Select the run that has the greatest length. If there is a tie for the greatest length, select the run that appears earliest in the sequence (i.e., has the smallest start index).
4.  If no non-zero runs are found, the output sequence is identical to the input sequence.
5.  If a longest run is selected, create the output sequence by copying the input sequence, but replace the digits within the selected run (from its start index to its end index, inclusive) with the digit `1`. The number of `1`s will be equal to the length of the selected run.
```python
import math
from typing import List, Dict, Any

"""
Transforms a sequence of integers by performing the following steps:
1. Identifies all contiguous subsequences (runs) consisting of identical non-zero digits.
2. Determines the maximum length among these identified runs.
3. Selects the run with the maximum length. If multiple runs share the maximum length, the one that appears earliest (leftmost) in the sequence is chosen.
4. If no non-zero runs are found, the original sequence is returned unchanged.
5. If a longest run is selected, a new sequence is created where the elements corresponding to the selected run are replaced by the digit '1'. The length of the replacement sequence of '1's is equal to the length of the original selected run.
"""

def find_runs(sequence: List[int]) -> List[Dict[str, int]]:
    """
    Identifies all contiguous runs of identical non-zero digits in a sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a run
        and contains 'start' (index) and 'length'. Returns an empty list
        if no non-zero runs are found.
    """
    runs = []
    n = len(sequence)
    i = 0
    while i < n:
        # Skip zeros
        if sequence[i] == 0:
            i += 1
            continue

        # Found the start of a potential non-zero run
        current_digit = sequence[i]
        start_index = i
        run_length = 1
        i += 1

        # Extend the run while the digit matches and within bounds
        while i < n and sequence[i] == current_digit:
            run_length += 1
            i += 1

        # Store the found run
        runs.append({'start': start_index, 'length': run_length})
        # The outer loop continues from the current 'i', which is already
        # positioned at the start of the next potential run or past the end.

    return runs

def transform(input_sequence: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: The list of integers to transform.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # 1. Identify all non-zero runs
    runs = find_runs(input_sequence)

    # 4. If no non-zero runs are found, return a copy of the input sequence
    if not runs:
        return list(input_sequence)

    # 2. Determine the maximum length among the runs
    max_length = 0
    for run in runs:
        # Using max() is slightly cleaner than manual tracking
        max_length = max(max_length, run['length'])

    # 3. Select the longest run (first one if tie)
    selected_run = None
    for run in runs:
        if run['length'] == max_length:
            selected_run = run
            # Since find_runs finds runs from left to right,
            # the first one we encounter with max_length is the leftmost one.
            break

    # This should theoretically not happen if runs is not empty, but check defensively
    if selected_run is None:
         return list(input_sequence) # Should not be reached if runs is not empty

    # 5. Create the output sequence by modifying a copy of the input
    output_sequence = list(input_sequence) # Make a copy

    # Replace the elements of the selected run with '1'
    start_index = selected_run['start']
    run_length = selected_run['length']
    for i in range(start_index, start_index + run_length):
        # Ensure index is within bounds (should be, based on find_runs)
        if i < len(output_sequence):
            output_sequence[i] = 1

    return output_sequence

```
