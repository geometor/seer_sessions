
## train_1

**input:**
```
1 1 0 0 0 0 1 1 1 0 0 0
```


**output:**
```
1 1 3 0 0 0 1 1 1 0 0 0
```


## train_2

**input:**
```
1 1 0 0 0 1 1 0 0 0 0 0
```


**output:**
```
1 1 3 0 3 1 1 3 0 0 0 0
```


## train_3

**input:**
```
1 1 1 0 0 0 0 1 0 0 0 0
```


**output:**
```
1 1 1 0 0 0 0 1 0 0 0 0
```


## train_4

**input:**
```
0 0 1 0 0 0 1 1 0 0 0 0
```


**output:**
```
0 0 1 0 0 3 1 1 3 0 0 0
```


## train_5

**input:**
```
0 1 1 1 0 0 0 1 1 1 0 0
```


**output:**
```
0 1 1 1 0 0 0 1 1 1 0 0
```


## train_6

**input:**
```
1 0 0 0 0 0 1 1 0 0 0 0
```


**output:**
```
1 0 0 0 0 3 1 1 3 0 0 0
```


## train_7

**input:**
```
0 1 0 0 0 0 0 0 1 1 1 0
```


**output:**
```
0 1 0 0 0 0 0 0 1 1 1 0
```

*   **Perception of the elements:**
    *   The input and output are both sequences (lists) of integers.
    *   The integers present in the input are primarily 0 and 1.
    *   The output sequence sometimes contains the integer 3, which is not present in the corresponding input.
    *   The transformation appears to involve conditionally changing some 0s in the input sequence to 3s in the output sequence.
    *   The change from 0 to 3 seems dependent on the values of the neighboring elements in the sequence. Specifically, it looks for the pattern `1 1` either immediately before or immediately after the `0`.
    *   Elements that are not 0, or 0s that do not meet the neighbor condition, remain unchanged.
    *   The length of the sequence remains the same between input and output.

*   **Facts:**
    
```yaml
    task_type: sequence transformation
    input_elements: integers (0, 1)
    output_elements: integers (0, 1, 3)
    data_structure: list/sequence
    transformation: conditional element replacement
    objects:
      - name: input_sequence
        type: list of integers
      - name: output_sequence
        type: list of integers
      - name: element
        type: integer
        properties:
          - value: (0, 1) in input, (0, 1, 3) in output
          - index: position in the sequence
    relationships:
      - type: adjacency
        description: Elements have preceding and succeeding neighbors within the sequence.
    actions:
      - name: replace_value
        target: element in input_sequence
        condition: |
          The element's value is 0 AND
          (the two immediately preceding elements have values [1, 1] OR
           the two immediately succeeding elements have values [1, 1])
        result: The corresponding element in the output_sequence has value 3.
      - name: copy_value
        target: element in input_sequence
        condition: The conditions for replace_value are not met.
        result: The corresponding element in the output_sequence has the same value as the input element.
    invariants:
      - sequence length remains constant
    ```


*   **Natural Language Program:**
    1.  Initialize an empty output sequence with the same length as the input sequence.
    2.  Iterate through each element of the input sequence using its index, from the first element to the last.
    3.  For the current element at index `i`:
        a.  Check if the element's value is 0.
        b.  If the value is 0, check two conditions:
            i.  Boundary check: Is there a preceding pair? (i.e., `i >= 2`?) If yes, check if the elements at indices `i-2` and `i-1` are both 1.
            ii. Boundary check: Is there a succeeding pair? (i.e., `i <= length - 3`?) If yes, check if the elements at indices `i+1` and `i+2` are both 1.
        c.  If the element's value is 0 AND (condition `i` is true OR condition `ii` is true), set the element at index `i` in the output sequence to 3.
        d.  Otherwise (if the element's value is not 0, or if it is 0 but neither neighbor condition is met), copy the value of the input element at index `i` to the output sequence at index `i`.
    4.  Return the completed output sequence.
```python
import math
import collections
import itertools

"""
Transforms a sequence of integers (0s and 1s) by changing certain 0s to 3s.
A 0 is changed to a 3 if it is immediately preceded by two 1s OR immediately
followed by two 1s. Otherwise, elements retain their original values.
"""

def transform(input_sequence: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers (0s and 1s).

    Returns:
        A new list of integers where specific 0s are replaced by 3s based
        on neighboring 1s.
    """
    # Initialize the output sequence as a copy of the input
    output_sequence = list(input_sequence)
    n = len(input_sequence)

    # Iterate through each element of the input sequence by index
    for i in range(n):
        # Check if the current element is 0
        if input_sequence[i] == 0:
            # Initialize flags for neighbor conditions
            preceded_by_ones = False
            followed_by_ones = False

            # Check preceding neighbors: requires at least two elements before
            # current index i (i.e., indices i-2 and i-1 must be valid)
            if i >= 2:
                if input_sequence[i-2] == 1 and input_sequence[i-1] == 1:
                    preceded_by_ones = True

            # Check succeeding neighbors: requires at least two elements after
            # current index i (i.e., indices i+1 and i+2 must be valid)
            if i <= n - 3:
                if input_sequence[i+1] == 1 and input_sequence[i+2] == 1:
                    followed_by_ones = True

            # If the element is 0 and either neighbor condition is met,
            # change the corresponding element in the output sequence to 3
            if preceded_by_ones or followed_by_ones:
                output_sequence[i] = 3

    # Return the modified sequence
    return output_sequence

```
