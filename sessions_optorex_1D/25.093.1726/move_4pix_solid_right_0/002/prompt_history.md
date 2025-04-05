
## train_1

**input:**
```
0 0 0 0 0 0 9 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 0
```


## train_2

**input:**
```
0 0 0 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 0 0 0 0
```


## train_3

**input:**
```
0 0 0 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 5 5 5 0 0
```


## train_4

**input:**
```
0 0 0 6 6 6 6 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 6 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 4
```


## train_6

**input:**
```
0 0 0 0 9 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 9 9 0 0
```


## train_7

**input:**
```
0 8 8 8 8 8 8 8 0 0 0 0
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 8 8
```

*   **Perception**:
    *   The input and output are sequences (lists or arrays) of single digits.
    *   All sequences provided have a length of 12.
    *   The sequences contain primarily zeros (0) and contiguous or single blocks of non-zero digits.
    *   The transformation involves repositioning the non-zero digits within the sequence.
    *   The non-zero digits maintain their values and relative order from input to output.
    *   The block of non-zero digits appears to be shifted consistently to the right by a fixed amount.
    *   Comparing the index of the first non-zero digit in the input and output reveals a shift of 4 positions to the right in all examples.
    *   The positions vacated by the shift, and positions to the left of the original block, are filled with zeros in the output. Positions to the right remain zero unless filled by the shifted block.

*   **Facts**:
    
```yaml
    task_type: sequence transformation
    data_representation: list of integers
    sequence_length: 12 (constant)
    elements:
        - type: zero (0) - acts as background/filler
        - type: non-zero digit (1-9) - represents the object(s) to be moved
    properties:
        - non-zero digits appear in contiguous blocks or as single elements
        - relative order of non-zero digits is preserved
    actions:
        - identify: locate all non-zero elements and their indices in the input sequence
        - shift: move each identified non-zero element 4 positions to the right
        - fill: place zeros in all positions not occupied by the shifted non-zero elements
    relationships:
        - input_index(non_zero_element) + 4 = output_index(non_zero_element)
    constraints:
        - sequence length is maintained
        - shift operation does not exceed sequence bounds in the examples
    ```


*   **Natural Language Program**:
    1.  Receive the input sequence of 12 digits.
    2.  Create a new output sequence of 12 digits, initialized with all zeros.
    3.  Iterate through the input sequence from left to right (index 0 to 11).
    4.  For each element in the input sequence:
        a.  If the element is not zero:
            i.  Calculate the target index in the output sequence by adding 4 to the current element's index.
            ii. Place the non-zero element at this target index in the output sequence.
    5.  Return the completed output sequence.
```python
"""
Transforms an input sequence of 12 digits by shifting all non-zero digits 4 positions to the right.

1. Receive the input sequence of 12 digits.
2. Create a new output sequence of 12 digits, initialized with all zeros.
3. Iterate through the input sequence from left to right (index 0 to 11).
4. For each element in the input sequence:
    a. If the element is not zero:
        i. Calculate the target index in the output sequence by adding 4 to the current element's index.
        ii. Place the non-zero element at this target index in the output sequence.
5. Return the completed output sequence.
"""

import numpy as np

def transform(input_sequence):
    """
    Shifts non-zero elements in a sequence 4 positions to the right.

    Args:
        input_sequence: A list or numpy array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Determine the length of the sequence
    sequence_length = len(input_sequence)
    
    # Initialize the output sequence with zeros
    output_sequence = [0] * sequence_length 
    
    # Define the shift amount
    shift_amount = 4

    # Iterate through the input sequence with index
    for index, element in enumerate(input_sequence):
        # Check if the element is non-zero
        if element != 0:
            # Calculate the new index after shifting
            new_index = index + shift_amount
            # Ensure the new index is within the bounds of the sequence
            if 0 <= new_index < sequence_length:
                # Place the non-zero element at the new index in the output sequence
                output_sequence[new_index] = element
                
    return output_sequence

```
