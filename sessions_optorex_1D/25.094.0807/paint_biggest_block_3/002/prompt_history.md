
## train_1

**input:**
```
7 7 7 7 7 0 0 7 7 0 0 0
```


**output:**
```
1 1 1 1 1 0 0 7 7 0 0 0
```


## train_2

**input:**
```
0 7 7 0 0 7 7 7 7 7 0 0
```


**output:**
```
0 7 7 0 0 1 1 1 1 1 0 0
```


## train_3

**input:**
```
0 5 5 5 0 5 5 5 5 5 0 0
```


**output:**
```
0 5 5 5 0 1 1 1 1 1 0 0
```


## train_4

**input:**
```
0 3 3 3 3 0 0 0 0 3 3 3
```


**output:**
```
0 1 1 1 1 0 0 0 0 3 3 3
```


## train_5

**input:**
```
0 6 6 6 6 6 0 0 6 6 6 6
```


**output:**
```
0 1 1 1 1 1 0 0 6 6 6 6
```


## train_6

**input:**
```
6 6 0 6 6 0 6 6 6 0 0 0
```


**output:**
```
6 6 0 6 6 0 1 1 1 0 0 0
```


## train_7

**input:**
```
0 4 4 4 4 4 4 0 0 4 4 4
```


**output:**
```
0 1 1 1 1 1 1 0 0 4 4 4
```

*   **Perception of task elements:**
    *   The input and output are sequences of single-digit integers, separated by spaces.
    *   The transformation involves identifying a specific contiguous subsequence within the input and modifying it.
    *   The modification consists of replacing the digits in the identified subsequence with the digit `1`.
    *   The subsequence targeted for modification appears to be the *longest* contiguous run of identical non-zero digits.
    *   If multiple runs share the same maximum length, the *first* one encountered (from left to right) is the one modified.
    *   Digits equal to `0` act as separators for these runs and are never modified.
    *   Other runs of non-zero digits that are not the longest (or the first of the longest) remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_description: Modify a sequence of digits by replacing the first occurring longest contiguous run of identical non-zero digits with 1s.
    input_type: Sequence of single-digit integers.
    output_type: Sequence of single-digit integers.
    elements:
      - name: DigitSequence
        type: List[int]
        description: Represents the input and output data.
      - name: NonZeroRun
        type: Object
        description: A contiguous subsequence of identical non-zero digits within the DigitSequence.
        properties:
          - name: value
            type: int
            description: The digit value (1-9) repeated in the run.
          - name: start_index
            type: int
            description: The starting position (0-based index) of the run in the DigitSequence.
          - name: length
            type: int
            description: The number of digits in the run.
      - name: TargetRun
        type: NonZeroRun
        description: The specific NonZeroRun selected for modification based on length and position.
    actions:
      - name: find_non_zero_runs
        input: DigitSequence
        output: List[NonZeroRun]
        description: Identifies all NonZeroRuns in the input sequence.
      - name: select_target_run
        input: List[NonZeroRun]
        output: TargetRun | None
        description: Selects the run with the maximum length. If multiple runs have the maximum length, selects the one with the minimum start_index. Returns None if no NonZeroRuns exist.
      - name: replace_run_with_ones
        input:
          - DigitSequence
          - TargetRun
        output: DigitSequence
        description: Creates a new sequence where the digits corresponding to the TargetRun in the input sequence are replaced by the digit 1.
    relationships:
      - The TargetRun is the NonZeroRun with the maximum 'length' property.
      - In case of ties in 'length', the TargetRun is the one with the minimum 'start_index' property.
    constants:
      - name: replacement_digit
        value: 1
        description: The digit used to replace the elements of the TargetRun.
      - name: zero_digit
        value: 0
        description: Acts as a separator and is never part of a NonZeroRun.

    ```


*   **Natural Language Program:**
    1.  Initialize an empty list to store information about runs of identical non-zero digits found in the input sequence.
    2.  Iterate through the input sequence, identifying each contiguous run of identical non-zero digits. For each run found, record its starting index, its length, and the digit it consists of. Add this information to the list of runs.
    3.  If no non-zero runs were found, return the original input sequence unchanged.
    4.  Examine the recorded runs to find the maximum length among them.
    5.  Filter the list of runs to keep only those that have this maximum length.
    6.  From the filtered list (runs of maximum length), select the run that has the smallest starting index. This is the target run.
    7.  Create a copy of the input sequence to serve as the output sequence.
    8.  Iterate from the starting index of the target run up to (starting index + length - 1). For each position within this range in the output sequence, change the digit to `1`.
    9.  Return the modified output sequence.
```python
import math
from typing import List, Tuple, Optional

"""
Modify a sequence of digits by replacing the first occurring longest contiguous run of identical non-zero digits with 1s.
"""

def find_runs(sequence: List[int]) -> List[Tuple[int, int, int]]:
    """
    Identifies all contiguous runs of identical non-zero digits in the sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of tuples, where each tuple represents a run:
        (start_index, length, value). Returns an empty list if no runs are found.
    """
    runs = []
    if not sequence:
        return runs

    current_run_start = -1
    current_run_length = 0
    current_run_value = None

    for i, digit in enumerate(sequence):
        if digit != 0:
            # Start of a new run or continuation of the current one
            if current_run_length == 0:
                # Start a new run
                current_run_start = i
                current_run_length = 1
                current_run_value = digit
            elif digit == current_run_value:
                # Continue the current run
                current_run_length += 1
            else:
                # End the previous run and start a new one
                runs.append((current_run_start, current_run_length, current_run_value))
                current_run_start = i
                current_run_length = 1
                current_run_value = digit
        else:
            # Digit is 0, end any current run
            if current_run_length > 0:
                runs.append((current_run_start, current_run_length, current_run_value))
            # Reset run tracking
            current_run_start = -1
            current_run_length = 0
            current_run_value = None

    # Add the last run if the sequence doesn't end with 0
    if current_run_length > 0:
        runs.append((current_run_start, current_run_length, current_run_value))

    return runs

def select_target_run(runs: List[Tuple[int, int, int]]) -> Optional[Tuple[int, int, int]]:
    """
    Selects the target run based on maximum length and earliest start index.

    Args:
        runs: A list of runs, each represented as (start_index, length, value).

    Returns:
        The target run tuple (start_index, length, value), or None if the input list is empty.
    """
    if not runs:
        return None

    # Find the maximum length
    max_length = 0
    for _, length, _ in runs:
        if length > max_length:
            max_length = length

    # Filter runs with maximum length
    longest_runs = [run for run in runs if run[1] == max_length]

    # Find the run with the minimum start index among the longest ones
    target_run = min(longest_runs, key=lambda run: run[0])

    return target_run


def transform(input_str: str) -> str:
    """
    Transforms the input string sequence according to the specified rule:
    1. Parse the input string into a list of integers.
    2. Find all contiguous runs of identical non-zero digits.
    3. Identify the first occurring longest run.
    4. Replace the digits in that run with 1s.
    5. Format the modified list back into a space-separated string.

    Args:
        input_str: A string of space-separated single-digit integers.

    Returns:
        A string representing the transformed sequence.
    """
    # 1. Parse input string into a list of integers
    input_sequence = [int(d) for d in input_str.split()]
    
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence)

    # 2. Find all contiguous runs of identical non-zero digits
    runs = find_runs(input_sequence)

    # 3. Select the target run (first longest)
    target_run = select_target_run(runs)

    # 4. If a target run exists, replace its elements with 1s in the output sequence
    if target_run:
        start_index, length, _ = target_run
        replacement_digit = 1
        for i in range(start_index, start_index + length):
            output_sequence[i] = replacement_digit

    # 5. Format the modified list back into a space-separated string
    output_str = " ".join(map(str, output_sequence))
    
    return output_str

```
