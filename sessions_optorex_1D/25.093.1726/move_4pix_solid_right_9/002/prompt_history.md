
## train_1

**input:**
```
0 0 0 0 7 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 7 0 0 0
```


## train_2

**input:**
```
1 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 1 1 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 1 1
```


## train_4

**input:**
```
8 8 8 8 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 8 8 8 8 0 0 0 0
```


## train_5

**input:**
```
0 0 9 9 9 9 9 9 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 9 9 9 9 9 9
```


## train_6

**input:**
```
4 4 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 4 4 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 4 4
```

*   **Perception:** The task involves transforming a sequence of 12 numbers. The input sequences contain groups of identical non-zero numbers (or single non-zero numbers) surrounded by zeros. The transformation appears to move these non-zero numbers to the right within the sequence. The amount of shift seems constant across all examples. Zeros fill the space vacated by the shifted numbers and the original positions not occupied by shifted numbers.

*   **Facts:**
    
```yaml
    objects:
      - name: input_sequence
        type: list_of_integers
        length: 12
        properties: contains_non_zero_elements
      - name: output_sequence
        type: list_of_integers
        length: 12
        properties: derived_from_input
      - name: non_zero_element
        type: integer
        properties: value, position_index
      - name: zero_element
        type: integer
        value: 0
    actions:
      - name: shift_right
        actor: system
        object: non_zero_element
        amount: 4_positions
        constraints: stays_within_sequence_bounds
      - name: fill_with_zeros
        actor: system
        object: output_sequence
        locations: indices_not_occupied_by_shifted_elements
    relationships:
      - type: positional_mapping
        source: non_zero_element in input_sequence at index `i`
        target: same non_zero_element in output_sequence at index `i + 4`
    constants:
      - sequence_length: 12
      - shift_amount: 4
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of 12 zeros.
    2.  Iterate through the input sequence from index 0 to 11.
    3.  For each element at index `i` in the input sequence:
        a.  If the element is non-zero:
            i.  Calculate the target index `j` as `i + 4`.
            ii. If the target index `j` is within the bounds of the sequence (less than 12), place the non-zero element at index `j` in the output sequence.
    4.  Return the resulting output sequence.
```python
import math
import numpy as np

"""
Transforms an input sequence of 12 integers by shifting all non-zero elements 4 positions to the right.
The output sequence is initialized with zeros. For each non-zero element in the input sequence at index i,
if the target index i + 4 is within the bounds of the sequence (0 to 11), the non-zero element is placed
at that target index in the output sequence. Positions in the output sequence that do not receive a
shifted non-zero element remain zero.
"""

def transform(input_grid):
    """
    Shifts non-zero elements of a 1D list 4 positions to the right.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Define sequence length and shift amount based on observations
    sequence_length = 12
    shift_amount = 4

    # Initialize output_grid with zeros, matching the sequence length
    output_grid = [0] * sequence_length

    # Iterate through the input sequence with index
    for i, element in enumerate(input_grid):
        # Check if the element is non-zero
        if element != 0:
            # Calculate the target index by adding the shift amount
            target_index = i + shift_amount
            # Check if the target index is within the bounds of the sequence
            if target_index < sequence_length:
                # Place the non-zero element at the target index in the output grid
                output_grid[target_index] = element

    # Return the resulting output grid
    return output_grid

```
