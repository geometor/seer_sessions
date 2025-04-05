
## train_1

**input:**
```
2 0 3 0 0 0 2 0 3 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 2 3 2 3 4
```


## train_2

**input:**
```
9 3 4 9 0 9 2 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 9 3 4 9 9 2 2
```


## train_3

**input:**
```
2 0 1 0 0 0 4 0 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 1 4 3
```


## train_4

**input:**
```
0 8 0 0 0 3 0 0 0 6 7 0
```


**output:**
```
0 0 0 0 0 0 0 0 8 3 6 7
```


## train_5

**input:**
```
0 0 0 0 0 0 6 2 6 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 6 2 6 6
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 0 8 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 8 2
```


## train_7

**input:**
```
4 0 0 0 0 9 0 1 5 0 0 1
```


**output:**
```
0 0 0 0 0 0 0 4 9 1 5 1
```

Okay, let's break down the transformation.

**Perception of Task Elements:**

*   The input and output are sequences of digits, represented as space-separated strings.
*   Each input and output sequence in the examples has a length of 12 digits.
*   The core operation appears to be rearranging the digits from the input to form the output.
*   The digit '0' seems to play a special role. In all output examples, all the '0's from the input are grouped together at the beginning.
*   The non-zero digits from the input appear in the output after all the '0's.
*   Crucially, the relative order of the non-zero digits amongst themselves seems to be preserved from the input to the output. For example, in `train_1`, the non-zero digits are `2, 3, 2, 3, 4` in that order in the input, and they appear as `2 3 2 3 4` at the end of the output.

**Fact Documentation:**


```yaml
objects:
  - name: input_sequence
    type: list of digits (derived from space-separated string)
    properties:
      - length (e.g., 12 in examples)
      - contains digits 0-9
  - name: output_sequence
    type: list of digits (formatted as space-separated string)
    properties:
      - length (same as input)
      - contains the same multiset of digits as input
  - name: zero_digit
    type: digit
    value: 0
  - name: non_zero_digit
    type: digit
    value: 1-9

actions:
  - name: parse_input
    description: Convert the input string into a list of digits.
  - name: filter_zeros
    description: Identify and collect all '0' digits from the input list.
  - name: filter_non_zeros
    description: Identify and collect all non-zero digits from the input list, maintaining their original relative order.
  - name: concatenate_sequences
    description: Combine the collected '0' digits followed by the collected non-zero digits.
  - name: format_output
    description: Join the digits in the combined sequence with spaces to create the output string.

relationships:
  - type: preservation
    description: The relative order of non-zero digits in the input_sequence is maintained in the non-zero part of the output_sequence.
  - type: partitioning
    description: The input_sequence is partitioned into zero_digits and non_zero_digits.
  - type: ordering
    description: In the output_sequence, all zero_digits precede all non_zero_digits.
  - type: conservation
    description: The count of each specific digit (0-9) is the same in the input_sequence and the output_sequence.
```


**Natural Language Program:**

1.  Read the input string and convert it into a list of individual digits.
2.  Create an empty list called `zeros` to store the '0' digits.
3.  Create an empty list called `non_zeros` to store the non-zero digits.
4.  Iterate through the input list of digits:
    *   If the current digit is '0', add it to the `zeros` list.
    *   If the current digit is not '0', add it to the `non_zeros` list.
5.  Combine the `zeros` list and the `non_zeros` list, in that order, to form the rearranged list of digits.
6.  Convert the rearranged list of digits back into a space-separated string for the final output.
```python
import math
import collections

"""
Processes a space-separated string of digits. It rearranges the digits such that all '0's appear first, followed by all non-zero digits. The relative order of the non-zero digits is preserved from the input string.
"""

def parse_input_string(input_str):
  """Converts a space-separated string of digits into a list of strings."""
  return input_str.split(' ')

def filter_digits(digit_list):
  """Separates a list of digit strings into two lists: zeros and non-zeros."""
  zeros = []
  non_zeros = []
  for digit in digit_list:
    if digit == '0':
      zeros.append(digit)
    else:
      non_zeros.append(digit)
  return zeros, non_zeros

def format_output_string(digit_list):
  """Joins a list of digit strings into a single space-separated string."""
  return ' '.join(digit_list)

def transform(input_str):
  """
  Rearranges digits in a space-separated string, placing all zeros at the beginning
  while preserving the relative order of non-zero digits.

  Args:
    input_str: A string containing space-separated digits.

  Returns:
    A string with digits rearranged according to the rule.
  """
  # 1. Parse the input string into a list of individual digits (as strings).
  input_digits = parse_input_string(input_str)

  # 2 & 3 & 4. Filter the digits into two lists: one for zeros and one for non-zeros,
  # maintaining the order for non-zeros.
  zeros_list, non_zeros_list = filter_digits(input_digits)

  # 5. Combine the list of zeros followed by the list of non-zeros.
  rearranged_digits = zeros_list + non_zeros_list

  # 6. Convert the rearranged list back into a space-separated string.
  output_str = format_output_string(rearranged_digits)

  return output_str

```
