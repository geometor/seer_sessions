
## train_1

**input:**
```
0 0 9 0 0 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 8
```


## train_2

**input:**
```
8 0 4 4 9 0 0 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 8 4 4 9 1
```


## train_3

**input:**
```
0 0 5 0 1 0 6 1 3 9 8 0
```


**output:**
```
0 0 0 0 0 5 1 6 1 3 9 8
```


## train_4

**input:**
```
9 4 0 0 0 6 1 6 9 0 0 0
```


**output:**
```
0 0 0 0 0 0 9 4 6 1 6 9
```


## train_5

**input:**
```
0 2 0 0 6 0 5 2 0 5 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 6 5 2 5
```


## train_6

**input:**
```
0 0 0 6 6 8 4 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 8 4 2
```


## train_7

**input:**
```
9 9 9 0 7 4 0 0 8 3 0 2
```


**output:**
```
0 0 0 0 9 9 9 7 4 8 3 2
```

Okay, let's analyze the transformation.

**Perception of Task Elements:**

*   **Input/Output Format:** Both input and output are single-line strings representing sequences of space-separated integers.
*   **Sequence Length:** The length of the input sequence is consistent across examples (12 elements) and matches the length of the corresponding output sequence.
*   **Element Values:** The elements are single digits (0-9).
*   **Key Observation:** The non-zero numbers present in the input sequence are also present in the output sequence, and their relative order is preserved. The zero elements ('0') appear to be treated differently.
*   **Transformation:** The core transformation seems to involve rearranging the elements. Specifically, all non-zero elements are shifted towards the right end of the sequence, maintaining their original relative order, while all zero elements are shifted to the left end.

**YAML Fact Document:**


```yaml
task_elements:
  - object: input_sequence
    type: list of integers
    properties:
      - length: fixed (12 in examples)
      - elements: integers between 0 and 9
  - object: output_sequence
    type: list of integers
    properties:
      - length: same as input_sequence
      - elements: integers between 0 and 9
actions:
  - action: partition
    target: input_sequence
    based_on: element value (zero vs. non-zero)
    result: two sub-sequences (zeros, non-zeros)
  - action: concatenate
    source_1: sub-sequence of zeros
    source_2: sub-sequence of non-zeros (preserving relative order)
    result: output_sequence
relationships:
  - type: preservation
    between: non-zero elements in input_sequence and non-zero elements in output_sequence
    property: relative order
  - type: equality
    property: count
    between: zeros in input_sequence and zeros in output_sequence
  - type: equality
    property: count
    between: non-zeros in input_sequence and non-zeros in output_sequence
  - type: equality
    property: length
    between: input_sequence and output_sequence
```


**Natural Language Program:**

1.  Receive the input sequence of integers.
2.  Create a new list containing only the non-zero elements from the input sequence, maintaining their original relative order.
3.  Count the number of zero elements present in the input sequence.
4.  Construct the output sequence by first creating a list containing the counted number of zero elements.
5.  Append the list of non-zero elements (created in step 2) to the end of the list of zeros (created in step 4).
6.  Return the resulting combined sequence.
```python
import math
import numpy as np

"""
Takes a sequence of integers represented as a space-separated string. 
Separates the zero elements from the non-zero elements.
Constructs a new sequence where all the zero elements from the input are placed at the beginning, 
followed by all the non-zero elements from the input, maintaining their original relative order.
Returns the resulting sequence as a space-separated string.
"""

def parse_input(input_str):
  """Converts a space-separated string of integers into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output(output_list):
  """Converts a list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def separate_zeros_nonzeros(int_list):
  """Separates a list of integers into two lists: one for zeros and one for non-zeros."""
  zeros = [x for x in int_list if x == 0]
  non_zeros = [x for x in int_list if x != 0]
  return zeros, non_zeros

def transform(input_str):
  """
  Applies the transformation rule: moves all zeros to the left and non-zeros to the right,
  preserving the relative order of non-zeros.
  """
  # Parse the input string into a list of integers
  input_list = parse_input(input_str)

  # Separate the list into zeros and non-zeros
  # The relative order of non-zeros is preserved by list comprehension
  zeros, non_zeros = separate_zeros_nonzeros(input_list)

  # Construct the output list by concatenating the zeros list and the non-zeros list
  # This places all zeros first, followed by non-zeros in their original relative order
  output_list = zeros + non_zeros

  # Format the output list back into a space-separated string
  output_str = format_output(output_list)

  return output_str

# Example usage (based on train_1)
# input_example = "0 0 9 0 0 8 0 0 0 0 0 0"
# output_example = transform(input_example)
# print(f"Input: {input_example}")
# print(f"Output: {output_example}")
# Expected: 0 0 0 0 0 0 0 0 0 0 9 8
```
