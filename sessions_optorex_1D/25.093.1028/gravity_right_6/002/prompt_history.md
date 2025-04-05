
## train_1

**input:**
```
7 0 4 3 0 9 0 2 5 0 7 0
```


**output:**
```
0 0 0 0 0 7 4 3 9 2 5 7
```


## train_2

**input:**
```
0 0 0 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 5
```


## train_3

**input:**
```
8 5 1 1 5 0 0 2 4 0 3 0
```


**output:**
```
0 0 0 0 8 5 1 1 5 2 4 3
```


## train_4

**input:**
```
4 0 2 0 0 0 0 3 0 7 0 3
```


**output:**
```
0 0 0 0 0 0 0 4 2 3 7 3
```


## train_5

**input:**
```
0 5 0 0 9 0 0 2 0 7 9 7
```


**output:**
```
0 0 0 0 0 0 5 9 2 7 9 7
```


## train_6

**input:**
```
0 9 0 3 0 0 4 0 7 1 2 0
```


**output:**
```
0 0 0 0 0 0 9 3 4 7 1 2
```


## train_7

**input:**
```
1 1 9 0 0 9 0 2 0 9 6 0
```


**output:**
```
0 0 0 0 0 1 1 9 9 2 9 6
```

*   **Perception of Elements:**
    *   The input consists of a sequence of integers, represented as a space-separated string. These integers can be zero or non-zero.
    *   The output is also a sequence of integers of the same length as the input, represented in the same format.
    *   The core elements are the individual integers within the sequence. A key property distinguishing them is whether they are zero or non-zero.

*   **YAML Fact Document:**
    
```yaml
    task_description: "Rearrange a sequence of integers by moving all zeros to the beginning."
    input_data:
      type: "string"
      format: "space-separated integers"
      elements:
        - type: "integer"
        properties:
          - value: "zero or non-zero"
          - original_position: "index in the sequence"
    output_data:
      type: "string"
      format: "space-separated integers"
      length: "same as input sequence"
    transformation:
      action: "partition and reorder"
      partition_criteria: "element value is zero or non-zero"
      reordering_rule: "place all zero elements first, then all non-zero elements"
      constraints:
        - "maintain relative order of non-zero elements"
        - "output length must match input length"
    relationships:
      - input_element -> output_element: "Each element from the input appears exactly once in the output."
      - non_zero_input_elements -> non_zero_output_elements: "The subsequence of non-zero elements in the output is identical to the subsequence of non-zero elements in the input."
      - zero_input_elements -> zero_output_elements: "The count of zero elements in the input equals the count of zero elements in the output."
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of integers.
    2.  Count the total number of elements in the input list.
    3.  Create two empty lists: one for zero elements (`zeros`) and one for non-zero elements (`non_zeros`).
    4.  Iterate through the input list of integers:
        *   If an element is zero, add it to the `zeros` list.
        *   If an element is non-zero, add it to the `non_zeros` list.
    5.  Concatenate the `zeros` list and the `non_zeros` list to form the output list.
    6.  Format the output list back into a space-separated string.
```python
"""
Rearrange a sequence of integers by moving all zeros to the beginning, 
preserving the relative order of the non-zero elements.
"""

import math  # Example import, though not strictly needed for this task

def parse_input(input_str):
  """Converts a space-separated string of integers into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output(output_list):
  """Converts a list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def separate_elements(integer_list):
  """Separates a list of integers into two lists: zeros and non-zeros."""
  zeros = []
  non_zeros = []
  for num in integer_list:
    if num == 0:
      zeros.append(num)
    else:
      non_zeros.append(num)
  return zeros, non_zeros

def transform(input_str):
  """
  Takes a space-separated string of integers, moves all zeros to the beginning,
  preserves the relative order of non-zeros, and returns the result as a 
  space-separated string.
  """
  # 1. Parse the input string into a list of integers.
  input_list = parse_input(input_str)

  # 2 & 3 & 4. Create two empty lists, iterate through input, 
  #             and add elements appropriately.
  zeros, non_zeros = separate_elements(input_list)
  
  # 5. Concatenate the zeros list and the non_zeros list.
  output_list = zeros + non_zeros

  # 6. Format the output list back into a space-separated string.
  output_str = format_output(output_list)

  return output_str

```
