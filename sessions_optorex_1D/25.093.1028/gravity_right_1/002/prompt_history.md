
## train_1

**input:**
```
9 0 0 0 9 0 0 7 6 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 9 9 7 6 6
```


## train_2

**input:**
```
0 0 0 9 0 0 0 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 1
```


## train_3

**input:**
```
1 9 0 0 0 4 0 8 0 0 7 0
```


**output:**
```
0 0 0 0 0 0 0 1 9 4 8 7
```


## train_4

**input:**
```
8 7 8 5 0 2 4 0 4 0 0 3
```


**output:**
```
0 0 0 0 8 7 8 5 2 4 4 3
```


## train_5

**input:**
```
4 0 8 9 0 9 3 9 6 7 8 0
```


**output:**
```
0 0 0 4 8 9 9 3 9 6 7 8
```


## train_6

**input:**
```
8 0 0 0 0 0 6 8 0 0 0 9
```


**output:**
```
0 0 0 0 0 0 0 0 8 6 8 9
```


## train_7

**input:**
```
2 0 2 0 8 7 0 4 6 9 6 5
```


**output:**
```
0 0 0 2 2 8 7 4 6 9 6 5
```

**Perception of task elements:**

The input and output are both sequences of single-digit integers, represented as space-separated strings. The length of the input sequence is always the same as the length of the output sequence (12 in all provided examples). The core transformation involves rearranging the elements of the input sequence. Specifically, all the '0' digits are moved to the beginning of the sequence, while all the non-zero digits are moved to the end. Importantly, the relative order of the non-zero digits amongst themselves is preserved from the input to the output.

**Facts:**


```yaml
objects:
  - name: input_sequence
    type: List[Integer]
    description: A sequence of single-digit integers derived from the input string.
  - name: output_sequence
    type: List[Integer]
    description: A sequence of single-digit integers representing the transformed output.
  - name: zero_digit
    type: Integer
    value: 0
    description: The digit '0'.
  - name: non_zero_digit
    type: Integer
    value_range: 1-9
    description: Any digit from '1' to '9'.

properties:
  - object: input_sequence
    property: length
    description: The number of digits in the input sequence.
  - object: output_sequence
    property: length
    description: The number of digits in the output sequence (equal to input length).
  - object: non_zero_digit
    property: relative_order
    description: The order in which non-zero digits appear relative to each other in the sequence.

actions:
  - name: parse_input
    input: input_string
    output: input_sequence
    description: Convert the space-separated string of digits into a list of integers.
  - name: partition_digits
    input: input_sequence
    outputs: [list_of_zeros, list_of_non_zeros]
    description: Iterate through the input sequence, separating digits into two lists based on whether they are zero or non-zero, preserving the original relative order within the non-zero list.
  - name: concatenate_lists
    inputs: [list_of_zeros, list_of_non_zeros]
    output: output_sequence
    description: Combine the list of zeros and the list of non-zeros to form the final output sequence.
  - name: format_output
    input: output_sequence
    output: output_string
    description: Convert the list of integers back into a space-separated string.

relationships:
  - type: equality
    between: [input_sequence.length, output_sequence.length]
    description: The input and output sequences have the same number of elements.
  - type: preservation
    element: non_zero_digit
    property: relative_order
    description: The relative order of non-zero digits in the input_sequence is the same as their relative order in the output_sequence.
  - type: composition
    result: output_sequence
    components: [list_of_zeros, list_of_non_zeros]
    description: The output sequence is formed by appending the list of non-zeros to the list of zeros.
```


**Natural Language Program:**

1.  Receive the input as a string of space-separated digits.
2.  Convert this input string into a list of integer digits.
3.  Create a new list containing only the non-zero digits from the input list, maintaining their original relative order.
4.  Count the number of zero digits in the input list.
5.  Create the output list by first adding the counted number of zeros, and then appending the list of non-zero digits (created in step 3).
6.  Convert the resulting output list back into a string of space-separated digits.
```python
import math

"""
Moves all zero digits to the beginning of the sequence while preserving the relative order of the non-zero digits.
"""

def parse_input_string(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output_list(output_list: list[int]) -> str:
    """Converts a list of integers back into a space-separated string."""
    return ' '.join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated digits by moving all zeros
    to the front while maintaining the relative order of non-zero digits.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing the transformed sequence of space-separated digits.
    """
    # 1. Convert the input string into a list of integer digits.
    input_sequence = parse_input_string(input_str)

    # 2. Create lists for zero and non-zero digits.
    zeros = []
    non_zeros = []

    # 3. Iterate through the input sequence and partition digits.
    #    Keep track of non-zeros in their original relative order.
    for digit in input_sequence:
        if digit == 0:
            zeros.append(digit)
        else:
            non_zeros.append(digit)

    # 4. Combine the list of zeros and the list of non-zeros.
    #    The zeros come first, followed by the non-zeros in their preserved order.
    output_sequence = zeros + non_zeros

    # 5. Convert the resulting output list back into a space-separated string.
    output_str = format_output_list(output_sequence)

    return output_str

```
