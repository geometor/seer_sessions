
## train_1

**input:**
```
0 0 0 0 3 3 3 0 3 3 0 3
```


**output:**
```
0 0 0 0 3 3 3 0 3 3 0 3
```


## train_2

**input:**
```
0 0 0 0 1 0 1 1 0 1 1 1
```


**output:**
```
0 0 0 0 1 1 1 0 1 1 0 1
```


## train_3

**input:**
```
0 0 0 0 3 3 3 0 3 0 3 3
```


**output:**
```
0 0 0 0 3 3 3 0 3 3 0 3
```


## train_4

**input:**
```
0 0 0 0 1 1 1 0 1 0 1 1
```


**output:**
```
0 0 0 0 1 1 1 0 1 1 0 1
```


## train_5

**input:**
```
0 0 0 0 2 2 2 0 2 2 0 2
```


**output:**
```
0 0 0 0 2 2 2 0 2 2 0 2
```


## train_6

**input:**
```
0 0 0 0 3 0 3 3 3 0 3 3
```


**output:**
```
0 0 0 0 3 3 3 0 3 3 0 3
```


## train_7

**input:**
```
0 0 0 0 9 9 9 0 9 0 9 9
```


**output:**
```
0 0 0 0 9 9 9 0 9 9 0 9
```

*   **Perception of Task Elements:**
    *   The input and output are sequences of 12 integers.
    *   The inputs generally start with four zeros (`0 0 0 0`).
    *   Following the initial zeros, there is typically a non-zero digit (e.g., 1, 2, 3, 9) that appears frequently in the rest of the sequence. Let's call this the 'dominant digit' (`X`).
    *   The transformation seems to involve rearranging or correcting the sequence based on this dominant digit `X`.
    *   In some cases (train\_1, train\_5), the input sequence is identical to the output sequence. These specific sequences follow the pattern `0 0 0 0 X X X 0 X X 0 X`.
    *   In other cases, the input sequence deviates from this pattern, and the output sequence is always transformed *into* this pattern: `0 0 0 0 X X X 0 X X 0 X`, using the dominant digit `X` identified from the input.
    *   The dominant digit `X` consistently appears at index 4 of the input sequence.

*   **Facts:**
    
```yaml
    objects:
      - name: input_sequence
        properties:
          - type: list of integers
          - length: 12
          - structure: Typically starts with [0, 0, 0, 0], followed by a mix of 0s and a dominant non-zero digit (X).
          - dominant_digit_index: 4
      - name: output_sequence
        properties:
          - type: list of integers
          - length: 12
          - structure: Always follows the pattern [0, 0, 0, 0, X, X, X, 0, X, X, 0, X]
      - name: dominant_digit (X)
        properties:
          - type: integer
          - value: Determined from input_sequence[4]
      - name: target_pattern
        properties:
          - type: list of integers
          - structure: [0, 0, 0, 0, X, X, X, 0, X, X, 0, X]
          - relationship: The output_sequence always matches this pattern.
    actions:
      - name: identify_dominant_digit
        inputs: [input_sequence]
        outputs: [dominant_digit]
        description: Extract the integer value at index 4 of the input sequence.
      - name: construct_target_sequence
        inputs: [dominant_digit]
        outputs: [output_sequence]
        description: Create a new 12-element sequence following the target_pattern using the identified dominant_digit.
    relationships:
      - The output_sequence is derived from the input_sequence by first identifying the dominant_digit (X) at input_sequence[4] and then constructing the target_pattern sequence using that digit X.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 integers.
    2.  Identify the dominant non-zero digit `X` by taking the value at index 4 of the input sequence.
    3.  Construct a new sequence of 12 integers according to the fixed pattern: `[0, 0, 0, 0, X, X, X, 0, X, X, 0, X]`, using the value of `X` determined in the previous step.
    4.  Return the newly constructed sequence as the output.
```python
"""
Identify the dominant non-zero digit 'X' from the input sequence at index 4.
Construct and return a new 12-element sequence following the fixed pattern:
[0, 0, 0, 0, X, X, X, 0, X, X, 0, X].
"""

import numpy as np
import math # Include common math libraries just in case, though not needed for this specific logic

# Helper functions (not strictly necessary for this simple task, but good practice)
def get_dominant_digit(sequence):
  """Extracts the digit at index 4."""
  if len(sequence) > 4:
    return sequence[4]
  else:
    # Handle potential edge case if input is unexpectedly short
    # Based on the examples, this shouldn't happen, but defensive coding is good.
    # Returning 0 or raising an error might be options depending on requirements.
    # Let's return 0 as a default, assuming it fits the pattern logic if no X is found.
    print("Warning: Input sequence shorter than expected.")
    return 0 

def construct_target_sequence(dominant_digit):
  """Constructs the target sequence based on the dominant digit."""
  X = dominant_digit
  # Define the fixed pattern structure
  pattern_structure = [0, 0, 0, 0, X, X, X, 0, X, X, 0, X]
  return pattern_structure

def transform(input_sequence):
    """
    Transforms the input sequence based on the digit at index 4.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A list of 12 integers following the pattern [0, 0, 0, 0, X, X, X, 0, X, X, 0, X],
        where X is the digit from input_sequence[4].
    """
    
    # 1. Identify the dominant non-zero digit 'X' (value at index 4)
    dominant_digit = get_dominant_digit(input_sequence)
    
    # 2. Construct the target output sequence using the fixed pattern and 'X'
    output_sequence = construct_target_sequence(dominant_digit)

    # 3. Return the newly constructed sequence
    return output_sequence

```
