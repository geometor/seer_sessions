
## train_1

**input:**
```
5 0 5 0 4 0 2 0 1 8 0 0
```


**output:**
```
0 0 0 0 0 0 5 5 4 2 1 8
```


## train_2

**input:**
```
0 4 5 0 5 0 0 8 8 0 9 0
```


**output:**
```
0 0 0 0 0 0 4 5 5 8 8 9
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 7 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 7 2
```


## train_4

**input:**
```
0 0 9 0 3 0 0 0 0 0 9 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 9 3 9
```


## train_5

**input:**
```
0 0 0 8 0 0 0 5 4 0 0 1
```


**output:**
```
0 0 0 0 0 0 0 0 8 5 4 1
```


## train_6

**input:**
```
9 0 0 0 0 3 2 0 0 2 2 5
```


**output:**
```
0 0 0 0 0 0 9 3 2 2 2 5
```


## train_7

**input:**
```
0 6 0 0 0 1 0 0 0 0 0 6
```


**output:**
```
0 0 0 0 0 0 0 0 0 6 1 6
```

Okay, let's analyze the provided task examples.

**Perception of the Elements:**

1.  **Input/Output Format:** Both input and output are strings containing space-separated single-digit integers.
2.  **Content:** The inputs and outputs consist of the digit `0` and other non-zero digits (1-9).
3.  **Length Preservation:** The number of integers in the output sequence is always the same as the number of integers in the input sequence.
4.  **Element Preservation:** All the specific non-zero digits present in the input appear in the output, and the count of zeros in the input matches the count of zeros in the output. No new numbers are introduced, and none are removed.
5.  **Reordering:** The core transformation appears to be a reordering of the input elements. Specifically, all the `0`s from the input are moved to the beginning of the sequence in the output.
6.  **Relative Order of Non-Zeros:** The non-zero digits in the output appear in the *same relative order* as they appeared in the input sequence. For instance, in `train_1`, the non-zeros are `5, 5, 4, 2, 1, 8` in the input, and they appear in exactly that sequence after the zeros in the output.

**Facts:**


```yaml
Task: Reorder sequence elements based on value (zero vs. non-zero)

Input:
  - object: input_sequence
    properties:
      - type: string
      - content: space-separated single-digit integers (0-9)
      - elements: contains a mix of zeros and non-zero digits

Output:
  - object: output_sequence
    properties:
      - type: string
      - content: space-separated single-digit integers (0-9)
      - length: identical to input_sequence length
      - composition: contains the same multiset of digits as input_sequence

Transformation:
  - action: partition
    description: Separate the elements of the input_sequence into two groups.
    operands:
      - input_sequence
    based_on: element value (is zero or is non-zero)
    outputs:
      - group_zeros: a sequence containing all '0's from the input.
      - group_non_zeros: a sequence containing all non-zero digits from the input, preserving their original relative order.
  - action: concatenate
    description: Combine the two groups to form the output sequence.
    operands:
      - group_zeros
      - group_non_zeros
    order: group_zeros first, followed by group_non_zeros.
    output: ordered_sequence
  - action: format
    description: Convert the ordered sequence of integers back into a space-separated string.
    operands:
      - ordered_sequence
    output: output_sequence (final string format)

Relationships:
  - The output_sequence is a permutation of the input_sequence.
  - All zeros from the input_sequence precede all non-zeros in the output_sequence.
  - The relative order of non-zero elements is maintained from input_sequence to output_sequence.
```


**Natural Language Program:**

1.  Read the input string of space-separated integers.
2.  Convert the input string into a sequence (e.g., a list) of integer values.
3.  Create two new empty sequences: one for zeros (`zeros_list`) and one for non-zeros (`non_zeros_list`).
4.  Iterate through the sequence of integers from the input:
    *   If the current integer is `0`, append it to the `zeros_list`.
    *   If the current integer is not `0`, append it to the `non_zeros_list`.
5.  Concatenate the `zeros_list` and the `non_zeros_list` together, with the `zeros_list` coming first.
6.  Convert the elements of the resulting concatenated sequence back into strings.
7.  Join the string elements with spaces to create the final output string.
8.  Return the final output string.
```python
import math

"""
Takes an input string of space-separated integers. 
Separates the integers into two groups: zeros and non-zeros.
Concatenates the group of zeros followed by the group of non-zeros, 
preserving the original relative order of the non-zero integers.
Finally, formats the resulting sequence back into a space-separated string.
"""

def partition_by_zero(numbers):
    """Separates a list of numbers into zeros and non-zeros."""
    zeros = [num for num in numbers if num == 0]
    non_zeros = [num for num in numbers if num != 0]
    return zeros, non_zeros

def format_numbers_to_string(numbers):
    """Converts a list of numbers to a space-separated string."""
    return " ".join(map(str, numbers))

def transform(input_str: str) -> str:
    """
    Reorders a sequence of space-separated integers by moving all zeros
    to the beginning while maintaining the relative order of non-zero elements.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the reordered space-separated integers.
    """
    # 1. Parse the input string into a list of integers
    try:
        # Split the string by spaces and convert each part to an integer
        input_numbers = [int(x) for x in input_str.split()]
    except ValueError:
        # Handle potential errors if the input string contains non-integer values
        print(f"Error: Input string '{input_str}' contains non-integer elements.")
        return "" # Or raise an exception, depending on desired error handling

    # 2. Partition the list into zeros and non-zeros
    # The partition_by_zero helper function performs this separation.
    # Crucially, list comprehensions preserve the order of elements they process.
    zeros_list, non_zeros_list = partition_by_zero(input_numbers)

    # 3. Concatenate the lists: zeros first, then non-zeros
    # This places all zeros at the beginning, followed by the non-zeros
    # in their original relative order.
    output_numbers = zeros_list + non_zeros_list

    # 4. Format the resulting list back into a space-separated string
    # The format_numbers_to_string helper function handles this conversion.
    output_str = format_numbers_to_string(output_numbers)

    # 5. Return the final output string
    return output_str

```
