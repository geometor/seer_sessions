
## train_1

**input:**
```
8 8 8 8 0 0
```


**output:**
```
8 8 8 8 0 0
8 8 8 8 8 0
8 8 8 8 8 8
```


## train_2

**input:**
```
2 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 2 0 0 0 0
```


## train_3

**input:**
```
5 5 5 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 0 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0
5 5 5 5 5 5 5 0 0 0
```


## train_4

**input:**
```
7 0 0 0 0 0
```


**output:**
```
7 0 0 0 0 0
7 7 0 0 0 0
7 7 7 0 0 0
```


## train_5

**input:**
```
1 1 0 0 0 0
```


**output:**
```
1 1 0 0 0 0
1 1 1 0 0 0
1 1 1 1 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

### Perception of Task Elements

1.  **Input:** A single string containing space-separated single digits. The sequence starts with one or more instances of the same non-zero digit, followed by zero or more zeros.
2.  **Output:** Multiple lines of space-separated single digits.
    *   The first line of the output is always identical to the input string.
    *   Each subsequent line is derived from the previous line.
    *   The transformation involves changing one '0' digit to the non-zero digit found at the beginning of the sequence in each step.
    *   The process starts by changing the first '0' encountered after the initial block of non-zero digits.
    *   The number of transformation steps (and thus the number of output lines beyond the first) varies between examples and depends on the input sequence.
3.  **Transformation Logic:** The core action is the progressive replacement of zeros with the initial non-zero digit. The key is to determine *how many* zeros are replaced. By analyzing the number of initial non-zero digits (N), the number of zeros (Z), and the total length (L=N+Z), a pattern emerges for the number of transformation steps (C).
    *   If the initial count of non-zero digits (N) is greater than the count of zeros (Z), all zeros are replaced (C=Z).
    *   Otherwise (if N <= Z), the process continues until the total count of the non-zero digit reaches a target value, calculated as `floor(L / 2) + N - 1`. The number of steps C is then `target_N - N`.

### Facts


```yaml
Objects:
  - Input_Sequence:
      type: List[int]
      description: A sequence of single digits derived from the input string.
  - Output_Sequences:
      type: List[List[int]]
      description: A list containing multiple sequences of digits, representing the lines of the output.

Properties:
  - dominant_digit (d):
      type: int
      description: The non-zero digit present at the beginning of the Input_Sequence.
  - initial_non_zero_count (N):
      type: int
      description: The number of occurrences of 'd' at the start of the Input_Sequence.
  - zero_count (Z):
      type: int
      description: The number of zeros in the Input_Sequence.
  - total_length (L):
      type: int
      description: The total number of digits in the Input_Sequence (L = N + Z).
  - target_non_zero_count (target_N):
      type: int
      description: The final number of 'd' digits present in the last Output_Sequence line. Calculated based on N, Z, and L.
  - transformation_steps (C):
      type: int
      description: The number of zeros replaced (C = target_N - N). Also, the number of output lines minus one.

Relationships:
  - L = N + Z
  - if N > Z:
      target_N = L
  - if N <= Z:
      target_N = floor(L / 2) + N - 1  # Using integer division for floor
  - C = target_N - N
  - Output_Sequences[0] == Input_Sequence
  - For i from 1 to C:
      Output_Sequences[i] is derived from Output_Sequences[i-1] by changing the digit at index (N + i - 1) from 0 to 'd'.

Actions:
  - Parse: Convert the input string into Input_Sequence (list of integers).
  - Identify: Determine 'd', 'N', 'Z', 'L' from Input_Sequence.
  - Calculate: Compute 'target_N' using the conditional logic based on N, Z, L. Compute 'C'.
  - Generate:
    - Initialize Output_Sequences with Input_Sequence.
    - Iterate 'C' times:
      - Copy the last sequence in Output_Sequences.
      - Modify the copy by changing the digit at index (N + current_step) to 'd'.
      - Append the modified copy to Output_Sequences.
  - Format: Convert each sequence in Output_Sequences back to a space-separated string for the final output.
```


### Natural Language Program

1.  Read the input string and parse it into a list of integers (let's call it `current_sequence`).
2.  Add `current_sequence` as the first line of the result.
3.  Identify the first digit in `current_sequence`; this is the `dominant_digit`.
4.  Count the number of initial occurrences of the `dominant_digit` (let this be `N`).
5.  Count the number of zeros in `current_sequence` (let this be `Z`).
6.  Calculate the total length `L = N + Z`.
7.  Determine the target number of `dominant_digit`s (`target_N`) for the final state:
    *   If `N` is greater than `Z`, set `target_N` to `L`.
    *   Otherwise (if `N` is less than or equal to `Z`), set `target_N` to `(L // 2) + N - 1` (using integer division for floor).
8.  Calculate the number of transformation steps required: `C = target_N - N`.
9.  Iterate `C` times (from step `i = 0` to `C-1`):
    a.  Find the index to modify: `index = N + i`.
    b.  Change the digit in `current_sequence` at the calculated `index` from 0 to the `dominant_digit`.
    c.  Add a copy of the modified `current_sequence` as the next line of the result.
10. Format the collected result lines into the required output string format (multiple lines of space-separated digits).
```python
import math

"""
The transformation takes a single sequence of digits as input. This sequence starts with N repetitions of a non-zero digit 'd', followed by Z zeros. 
The output consists of multiple sequences. 
The first output sequence is identical to the input sequence. 
Subsequent sequences are generated iteratively. In each step, the next zero in the sequence (starting from the position immediately after the initial block of 'd's) is replaced by 'd'. 
This process continues for a specific number of steps, C.
The number of steps C is determined as follows:
1. Calculate the total length L = N + Z.
2. Determine the target count of the dominant digit 'd' (target_N) in the final sequence:
   - If N > Z, target_N = L (all zeros are replaced).
   - If N <= Z, target_N = floor(L / 2) + N - 1.
3. The number of transformation steps (zeros to replace) is C = target_N - N.
The final output contains C+1 sequences (the initial one plus the C transformed ones).
"""

def parse_input_string(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output_sequences(sequences: list[list[int]]) -> list[str]:
    """Converts a list of integer sequences back to space-separated strings."""
    return [" ".join(map(str, seq)) for seq in sequences]

def transform(input_str: str) -> list[str]:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A single string containing space-separated digits.

    Returns:
        A list of strings, where each string represents a line of the output sequence.
    """

    # 1. Parse the input string into a list of integers
    current_sequence = parse_input_string(input_str)
    output_sequences = [] # To store intermediate and final sequences as lists of ints
    output_sequences.append(list(current_sequence)) # Add initial sequence

    # Handle empty or all-zero input gracefully although examples don't show this
    if not current_sequence or all(d == 0 for d in current_sequence):
        return format_output_sequences(output_sequences)

    # 3. Identify the dominant_digit
    dominant_digit = current_sequence[0]
    if dominant_digit == 0: # Should not happen based on examples, but handle defensively
         # Find the first non-zero digit if the sequence starts with zeros (not per spec, but robust)
         first_non_zero = next((d for d in current_sequence if d != 0), None)
         if first_non_zero is None: # All zeros case
             return format_output_sequences(output_sequences)
         dominant_digit = first_non_zero
         # Recalculate N based on this unusual case (assuming N=0 if starts with 0)
         N = 0
    else:
         # 4. Count initial occurrences of the dominant_digit (N)
         N = 0
         for digit in current_sequence:
             if digit == dominant_digit:
                 N += 1
             else:
                 break # Stop counting N once a different digit (should be 0) is found

    # 5. Count the number of zeros (Z)
    Z = current_sequence.count(0)

    # 6. Calculate the total length L
    L = len(current_sequence)
    # Basic check: L should equal N + Z based on problem description
    # If not, the input format deviates from expectations.
    # We'll proceed assuming L is the definitive length.

    # 7. Determine the target number of dominant_digits (target_N)
    if N > Z:
        target_N = L
    else:
        # Using integer division // for floor
        target_N = (L // 2) + N - 1

    # 8. Calculate the number of transformation steps (C)
    C = target_N - N

    # Ensure C is not negative (e.g., if target_N calculation somehow resulted < N)
    # Also ensure we don't try to replace more zeros than available
    C = max(0, min(C, Z))

    # 9. Iterate C times to generate subsequent sequences
    for i in range(C):
        # Find the index to modify: index = N + i
        # This is the index of the i-th zero after the initial block of N digits.
        index_to_modify = N + i

        # Ensure the index is within bounds and points to a zero
        if index_to_modify < L and current_sequence[index_to_modify] == 0:
            # Change the digit at the calculated index from 0 to the dominant_digit
            current_sequence[index_to_modify] = dominant_digit
            # Add a copy of the modified sequence to the results
            output_sequences.append(list(current_sequence))
        else:
            # If the index is out of bounds or not a zero, something is wrong
            # with the logic or input assumptions. Stop generating further steps.
             # print(f"Warning: Unexpected state at step {i+1}. Index: {index_to_modify}, Value: {current_sequence[index_to_modify] if index_to_modify < L else 'OOB'}. Stopping.")
            break


    # 10. Format the collected sequences into strings
    return format_output_sequences(output_sequences)

```

Previous Code:
```python
import math

"""
The transformation takes a single sequence of digits as input. This sequence starts with N repetitions of a non-zero digit 'd', followed by Z zeros. 
The output consists of multiple sequences. 
The first output sequence is identical to the input sequence. 
Subsequent sequences are generated iteratively. In each step, the next zero in the sequence (starting from the position immediately after the initial block of 'd's) is replaced by 'd'. 
This process continues for a specific number of steps, C.
The number of steps C is determined as follows:
1. Calculate the total length L = N + Z.
2. Determine the target count of the dominant digit 'd' (target_N) in the final sequence:
   - If N > Z, target_N = L (all zeros are replaced).
   - If N <= Z, target_N = floor(L / 2) + N - 1.
3. The number of transformation steps (zeros to replace) is C = target_N - N.
The final output contains C+1 sequences (the initial one plus the C transformed ones).
"""

def parse_input_string(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output_sequences(sequences: list[list[int]]) -> list[str]:
    """Converts a list of integer sequences back to space-separated strings."""
    return [" ".join(map(str, seq)) for seq in sequences]

def transform(input_str: str) -> list[str]:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A single string containing space-separated digits.

    Returns:
        A list of strings, where each string represents a line of the output sequence.
    """

    # 1. Parse the input string into a list of integers
    current_sequence = parse_input_string(input_str)
    output_sequences = [] # To store intermediate and final sequences as lists of ints
    output_sequences.append(list(current_sequence)) # Add initial sequence

    # Handle empty or all-zero input gracefully although examples don't show this
    if not current_sequence or all(d == 0 for d in current_sequence):
        return format_output_sequences(output_sequences)

    # 3. Identify the dominant_digit
    dominant_digit = current_sequence[0]
    if dominant_digit == 0: # Should not happen based on examples, but handle defensively
         # Find the first non-zero digit if the sequence starts with zeros (not per spec, but robust)
         first_non_zero = next((d for d in current_sequence if d != 0), None)
         if first_non_zero is None: # All zeros case
             return format_output_sequences(output_sequences)
         dominant_digit = first_non_zero
         # Recalculate N based on this unusual case (assuming N=0 if starts with 0)
         N = 0
    else:
         # 4. Count initial occurrences of the dominant_digit (N)
         N = 0
         for digit in current_sequence:
             if digit == dominant_digit:
                 N += 1
             else:
                 break # Stop counting N once a different digit (should be 0) is found

    # 5. Count the number of zeros (Z)
    Z = current_sequence.count(0)

    # 6. Calculate the total length L
    L = len(current_sequence)
    # Basic check: L should equal N + Z based on problem description
    # If not, the input format deviates from expectations.
    # We'll proceed assuming L is the definitive length.

    # 7. Determine the target number of dominant_digits (target_N)
    if N > Z:
        target_N = L
    else:
        # Using integer division // for floor
        target_N = (L // 2) + N - 1

    # 8. Calculate the number of transformation steps (C)
    C = target_N - N

    # Ensure C is not negative (e.g., if target_N calculation somehow resulted < N)
    # Also ensure we don't try to replace more zeros than available
    C = max(0, min(C, Z))

    # 9. Iterate C times to generate subsequent sequences
    for i in range(C):
        # Find the index to modify: index = N + i
        # This is the index of the i-th zero after the initial block of N digits.
        index_to_modify = N + i

        # Ensure the index is within bounds and points to a zero
        if index_to_modify < L and current_sequence[index_to_modify] == 0:
            # Change the digit at the calculated index from 0 to the dominant_digit
            current_sequence[index_to_modify] = dominant_digit
            # Add a copy of the modified sequence to the results
            output_sequences.append(list(current_sequence))
        else:
            # If the index is out of bounds or not a zero, something is wrong
            # with the logic or input assumptions. Stop generating further steps.
             # print(f"Warning: Unexpected state at step {i+1}. Index: {index_to_modify}, Value: {current_sequence[index_to_modify] if index_to_modify < L else 'OOB'}. Stopping.")
            break


    # 10. Format the collected sequences into strings
    return format_output_sequences(output_sequences)

```
Results for code_00.py:

Train Set Results:

## Example 1:
Error: Execution Error: 'list' object has no attribute 'split'

## Example 2:
Error: Execution Error: 'list' object has no attribute 'split'

## Example 3:
Error: Execution Error: 'list' object has no attribute 'split'

## Example 4:
Error: Execution Error: 'list' object has no attribute 'split'

## Example 5:
Error: Execution Error: 'list' object has no attribute 'split'
## General Assessment

The error message `Execution Error: 'list' object has no attribute 'split'` consistently occurs across all examples. This indicates that the `transform` function, specifically the `parse_input_string` helper function inside it, is receiving input as a Python list object instead of the expected string format (e.g., `"8 8 8 8 0 0"`). The `split()` method is a string method, hence the error when called on a list.

This error points to a problem in the *calling environment* or *testing harness* rather than the internal logic of the transformation rule derived from the input/output examples. The previously formulated understanding of the transformation logic appears consistent with the examples provided.

**Strategy:**

1.  **Verify Metrics:** Re-calculate key metrics (N, Z, L, number of steps C) for each example to confirm the derived rule for determining the number of transformation steps.
2.  **Refine Documentation:** Update the Facts (YAML) and Natural Language Program to be precise and unambiguous, incorporating the confirmed calculation for the number of steps.
3.  **Inform Coder:** Explicitly note that the implementation (coder phase) must handle the input correctly, likely expecting a string as per the original analysis, or the testing harness must be adjusted to provide string input. The core logic described in the natural language program remains valid based on the examples.

## Metrics Gathering

Let's calculate the key parameters for each example to verify the transformation rule.

*   `d`: dominant non-zero digit
*   `N`: initial count of `d`
*   `Z`: count of zeros
*   `L`: total length (`N + Z`)
*   `C_expected`: number of transformation steps (output lines - 1)
*   `Rule`: Condition for calculating `target_N` (N > Z or N <= Z)
*   `target_N_calculated`: Final count of `d` based on the rule
*   `C_calculated`: Calculated steps (`target_N_calculated - N`)



*code_execution:*
```python
import math

def analyze_example(input_str, output_lines):
    input_list = [int(x) for x in input_str.split()]
    if not input_list or all(d == 0 for d in input_list):
        return {"input_str": input_str, "error": "Invalid input format"}

    d = input_list[0]
    if d == 0: # Find first non-zero if needed (defensive)
        first_non_zero = next((digit for digit in input_list if digit != 0), None)
        if first_non_zero is None:
             return {"input_str": input_str, "error": "All zeros input"}
        d = first_non_zero
        N = 0 # Assumption: if starts with 0, N=0 for rule calc
    else:
        N = 0
        for digit in input_list:
            if digit == d:
                N += 1
            else:
                break

    Z = input_list.count(0)
    L = len(input_list)
    C_expected = len(output_lines) - 1

    if N > Z:
        rule_condition = "N > Z"
        target_N_calculated = L
    else: # N <= Z
        rule_condition = "N <= Z"
        target_N_calculated = (L // 2) + N - 1 # floor(L/2) + N - 1

    C_calculated = target_N_calculated - N
    # Ensure C calculation doesn't exceed available zeros
    C_calculated = max(0, min(C_calculated, Z))

    return {
        "input_str": input_str,
        "d": d,
        "N": N,
        "Z": Z,
        "L": L,
        "C_expected": C_expected,
        "Rule_Condition": rule_condition,
        "target_N_calculated": target_N_calculated,
        "C_calculated": C_calculated,
        "Rule_Matches": C_expected == C_calculated
    }

examples = [
    {"input": "8 8 8 8 0 0", "output": ["8 8 8 8 0 0", "8 8 8 8 8 0", "8 8 8 8 8 8"]},
    {"input": "2 0 0 0 0 0 0 0", "output": ["2 0 0 0 0 0 0 0", "2 2 0 0 0 0 0 0", "2 2 2 0 0 0 0 0", "2 2 2 2 0 0 0 0"]},
    {"input": "5 5 5 0 0 0 0 0 0 0", "output": ["5 5 5 0 0 0 0 0 0 0", "5 5 5 5 0 0 0 0 0 0", "5 5 5 5 5 0 0 0 0 0", "5 5 5 5 5 5 0 0 0 0", "5 5 5 5 5 5 5 0 0 0"]},
    {"input": "7 0 0 0 0 0", "output": ["7 0 0 0 0 0", "7 7 0 0 0 0", "7 7 7 0 0 0"]},
    {"input": "1 1 0 0 0 0", "output": ["1 1 0 0 0 0", "1 1 1 0 0 0", "1 1 1 1 0 0"]},
]

results = [analyze_example(ex["input"], ex["output"]) for ex in examples]
import json
print(json.dumps(results, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
[
  {
    "input_str": "8 8 8 8 0 0",
    "d": 8,
    "N": 4,
    "Z": 2,
    "L": 6,
    "C_expected": 2,
    "Rule_Condition": "N > Z",
    "target_N_calculated": 6,
    "C_calculated": 2,
    "Rule_Matches": true
  },
  {
    "input_str": "2 0 0 0 0 0 0 0",
    "d": 2,
    "N": 1,
    "Z": 7,
    "L": 8,
    "C_expected": 3,
    "Rule_Condition": "N <= Z",
    "target_N_calculated": 4,
    "C_calculated": 3,
    "Rule_Matches": true
  },
  {
    "input_str": "5 5 5 0 0 0 0 0 0 0",
    "d": 5,
    "N": 3,
    "Z": 7,
    "L": 10,
    "C_expected": 4,
    "Rule_Condition": "N <= Z",
    "target_N_calculated": 7,
    "C_calculated": 4,
    "Rule_Matches": true
  },
  {
    "input_str": "7 0 0 0 0 0",
    "d": 7,
    "N": 1,
    "Z": 5,
    "L": 6,
    "C_expected": 2,
    "Rule_Condition": "N <= Z",
    "target_N_calculated": 3,
    "C_calculated": 2,
    "Rule_Matches": true
  },
  {
    "input_str": "1 1 0 0 0 0",
    "d": 1,
    "N": 2,
    "Z": 4,
    "L": 6,
    "C_expected": 2,
    "Rule_Condition": "N <= Z",
    "target_N_calculated": 4,
    "C_calculated": 2,
    "Rule_Matches": true
  }
]

```
**Metrics Summary:**
The calculations confirm that the derived rule for determining the number of transformation steps (`C`) holds true for all provided training examples. The rule is:
1.  Identify `N` (initial count of dominant digit `d`) and `Z` (count of zeros). Calculate total length `L = N + Z`.
2.  If `N > Z`, the number of steps `C = Z` (all zeros are replaced).
3.  If `N <= Z`, the number of steps `C = (L // 2) + N - 1 - N = (L // 2) - 1`. Alternatively stated, calculate `target_N = (L // 2) + N - 1`, and then `C = target_N - N`.
4.  The total number of output lines is `C + 1`.

## Facts


```yaml
Objects:
  - Input_String:
      type: str
      description: A single string containing space-separated single digits.
  - Input_Sequence:
      type: List[int]
      description: A sequence of single digits derived by parsing the Input_String. It starts with N instances of a non-zero digit 'd', followed by Z zeros.
  - Output_Collection:
      type: List[List[int]]
      description: A list containing multiple sequences of digits (as lists of integers), representing the state at each step of the transformation.
  - Output_Strings:
      type: List[str]
      description: The final output, where each sequence in Output_Collection is formatted back into a space-separated string.

Properties:
  - dominant_digit (d):
      type: int
      description: The non-zero digit present at the beginning of the Input_Sequence.
  - initial_non_zero_count (N):
      type: int
      description: The number of occurrences of 'd' at the start of the Input_Sequence.
  - zero_count (Z):
      type: int
      description: The number of zeros in the Input_Sequence.
  - total_length (L):
      type: int
      description: The total number of digits in the Input_Sequence (L = N + Z).
  - transformation_steps (C):
      type: int
      description: The number of zeros that will be replaced by 'd'. Calculated based on N, Z, and L.
  - target_non_zero_count (target_N):
      type: int
      description: The final count of 'd' digits in the last sequence of Output_Collection. (target_N = N + C).

Relationships:
  - L = N + Z
  - Calculation of C:
      - if N > Z:
          C = Z
      - if N <= Z:
          C = (L // 2) + N - 1 - N  # simplified: C = (L // 2) - 1
          # Alternatively: target_N = (L // 2) + N - 1; C = target_N - N
  - C = max(0, min(C, Z)) # Ensure C is non-negative and doesn't exceed available zeros.
  - Output_Collection[0] == Input_Sequence
  - For i from 1 to C:
      Output_Collection[i] is derived from Output_Collection[i-1] by changing the digit at index (N + i - 1) from 0 to 'd'.
  - len(Output_Collection) == C + 1

Actions:
  - Parse: Convert the Input_String into Input_Sequence (list of integers).
  - Identify: Determine 'd', 'N', 'Z', 'L' from Input_Sequence.
  - Calculate_Steps: Compute 'C' using the conditional logic based on N, Z, L.
  - Generate_Transformations:
    - Initialize Output_Collection with a copy of Input_Sequence.
    - Create a working copy of Input_Sequence.
    - Iterate 'C' times (from step `i = 0` to `C-1`):
      - Modify the working copy by changing the digit at index (N + i) from 0 to 'd'.
      - Append a copy of the modified working copy to Output_Collection.
  - Format_Output: Convert each sequence in Output_Collection into a space-separated string and collect them into Output_Strings.
```


## Natural Language Program

1.  **Input:** Receive the input as a single string of space-separated digits.
2.  **Parse:** Convert the input string into a list of integers, called `sequence`.
3.  **Initialization:** Create a list called `result_sequences` and add a copy of the initial `sequence` to it.
4.  **Analyze:**
    *   Identify the first digit in `sequence` as the `dominant_digit` (`d`). Assume it's non-zero based on examples.
    *   Count the number of initial consecutive occurrences of `d` to get `N`.
    *   Count the total number of zeros in `sequence` to get `Z`.
    *   Calculate the total length `L` of the `sequence`.
5.  **Calculate Steps (`C`):**
    *   If `N` is greater than `Z`, set the number of steps `C` equal to `Z`.
    *   Otherwise (if `N` is less than or equal to `Z`), calculate `C = (L // 2) - 1`.
    *   Ensure `C` is not negative (set `C = max(0, C)`). Ensure `C` does not exceed the number of available zeros (set `C = min(C, Z)`).
6.  **Transform:** Create a working copy of the `sequence`. Iterate `C` times (e.g., using a loop counter `i` from 0 to `C-1`):
    *   Determine the index to change: `index = N + i`.
    *   If `index` is within the bounds of the working copy and the element at `index` is 0:
        *   Change the digit at `index` in the working copy to the `dominant_digit` (`d`).
        *   Add a *new copy* of the current state of the working copy to `result_sequences`.
    *   Else (index out of bounds or not zero), stop the transformation process (this indicates an issue or edge case not covered by examples).
7.  **Format Output:** Convert each integer list in `result_sequences` back into a space-separated string.
8.  **Output:** Return the list of formatted strings.
