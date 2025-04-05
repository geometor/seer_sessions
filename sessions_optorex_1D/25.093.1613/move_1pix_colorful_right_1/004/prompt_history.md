
## train_1

**input:**
```
0 9 1 8 9 8 6 1 4 4 2 0
```


**output:**
```
0 0 9 1 8 9 8 6 1 4 4 2
```


## train_2

**input:**
```
8 7 9 9 9 8 1 3 9 0 0 0
```


**output:**
```
0 8 7 9 9 9 8 1 3 9 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 4 0 0 0
```


## train_4

**input:**
```
0 0 0 0 4 3 7 3 1 8 0 0
```


**output:**
```
0 0 0 0 0 4 3 7 3 1 8 0
```


## train_5

**input:**
```
0 0 0 0 2 9 5 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 9 5 6 0 0 0
```


## train_6

**input:**
```
0 5 8 6 2 3 6 8 7 8 9 0
```


**output:**
```
0 0 5 8 6 2 3 6 8 7 8 9
```


## train_7

**input:**
```
7 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 9 0 0 0 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are both sequences of single digits, represented as space-separated strings.
    *   All provided examples have an input sequence length of 12 and an output sequence length of 12.
    *   The output sequence appears to be derived from the input sequence by inserting a '0' at a specific position and then potentially truncating the result to maintain the original length.
    *   The position of the inserted '0' seems related to the position of the first non-zero digit in the input sequence.
    *   Comparing the input and output sequences reveals that the relative order of the original digits is preserved in the output, but shifted to the right starting from the insertion point. The last element of the sequence after insertion is effectively dropped to maintain the original length.

*   **Facts:**
    
```yaml
    objects:
      - name: input_sequence
        type: list of digits
        properties:
          - length: integer (e.g., 12 in examples)
          - elements: digits (0-9)
      - name: output_sequence
        type: list of digits
        properties:
          - length: integer (same as input_sequence length)
          - elements: digits (0-9)
      - name: target_digit
        value: 0
        role: digit to be inserted
    actions:
      - name: find_first_non_zero_index
        input: input_sequence
        output: index (integer)
        description: Locates the numerical index (0-based) of the first digit in the input_sequence that is not equal to 0.
      - name: insert_digit
        target_object: input_sequence (conceptually, a copy is modified)
        parameters:
          - digit_to_insert: target_digit (0)
          - insertion_index: result of find_first_non_zero_index
        output: intermediate_sequence (list of digits, length = input_sequence length + 1)
        description: Creates a new sequence by inserting the target_digit at the specified insertion_index within the input_sequence. Elements from the insertion_index onwards are shifted right.
      - name: truncate_sequence
        input: intermediate_sequence
        parameters:
          - desired_length: length of original input_sequence
        output: output_sequence
        description: Takes the first 'desired_length' elements of the intermediate_sequence.
    relationships:
      - The output_sequence is derived from the input_sequence through a series of actions: finding an index, inserting a digit at that index, and truncating the result.
      - The length of the output_sequence is constrained to be equal to the length of the input_sequence.
      - The insertion_index is determined by the position of the first non-zero element in the input_sequence.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of digits. Record its length.
    2.  Iterate through the input sequence from the beginning (index 0) to find the index of the first digit that is not '0'. Let this index be `insertion_index`.
    3.  Create a new sequence by inserting the digit '0' into the input sequence at the `insertion_index`.
    4.  Take the first N elements from the sequence created in step 3, where N is the original length of the input sequence recorded in step 1. This resulting sequence is the output.
```python
import math
import numpy as np
import re

"""
Transformation Rule:
1.  Receive the input sequence of digits (as a string). Record its original length (number of digits).
2.  Convert the input string into a list of integers.
3.  Find the index of the first digit in the list that is not equal to 0.
    - If no non-zero digit is found (i.e., all digits are 0), use index 0 as the insertion point.
4.  Create a new list by inserting the integer 0 into the list at the found index.
5.  Take the first N elements from the modified list, where N is the original length recorded in step 1.
6.  Convert this final list of integers back into a space-separated string. This is the output.
"""

def find_first_non_zero_index(digit_list):
    """
    Finds the index of the first non-zero digit in a list of integers.
    Returns 0 if all digits are zero or the list is empty.
    """
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    # If no non-zero digit is found, default to index 0
    return 0

def transform(input_str: str) -> str:
    """
    Transforms the input string of space-separated digits by inserting a '0'
    at the index of the first non-zero digit and truncating the result to the
    original length.
    """
    # 1. Parse the input string and record original length (as number of elements)
    input_digits_str = input_str.split()
    original_length = len(input_digits_str)
    
    # Handle empty input case
    if original_length == 0:
        return ""

    # 2. Convert the input string list into a list of integers.
    input_digits_int = [int(d) for d in input_digits_str]

    # 3. Find the index of the first non-zero digit.
    insertion_index = find_first_non_zero_index(input_digits_int)

    # 4. Create a new list by inserting 0 at the insertion_index.
    # Make a copy to avoid modifying the original list if it were needed elsewhere
    modified_digits_int = input_digits_int[:] 
    modified_digits_int.insert(insertion_index, 0)

    # 5. Take the first N elements from the modified list (truncate).
    output_digits_int = modified_digits_int[:original_length]

    # 6. Convert the final list of integers back into a space-separated string.
    output_str = " ".join(map(str, output_digits_int))

    return output_str

```
```python
import numpy as np
import math # math and numpy are available

"""
Transformation Rule:
1.  Receive the input sequence as a NumPy array of integers. Record its original length (number of elements), N.
2.  Convert the input NumPy array into a Python list of integers.
3.  Iterate through the list from the beginning (index 0) to find the index of the first integer that is not equal to 0. Let this index be `insertion_index`. If no non-zero integer is found, set `insertion_index` to 0.
4.  Create a new list by inserting the integer 0 into the list (from step 2) at the `insertion_index`.
5.  Take the first N elements from the list created in step 4.
6.  Convert this final list of N integers into a single string where each integer is separated by a space. This string is the output.
"""

def find_first_non_zero_index(digit_list):
    """
    Finds the index of the first non-zero digit in a list or 1D numpy array.
    Returns 0 if all digits are zero or the list/array is empty.
    """
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    # If no non-zero digit is found, default to index 0
    return 0

def transform(input_grid: np.ndarray) -> str:
    """
    Transforms the input numpy array of digits by inserting a '0'
    at the index of the first non-zero digit and truncating the result to the
    original length, returning a space-separated string.
    """
    # 1. Record original length (number of elements)
    original_length = len(input_grid)

    # Handle empty input case
    if original_length == 0:
        return ""

    # 2. Convert the input NumPy array into a Python list of integers.
    # (Conversion needed because numpy arrays don't have an insert method like lists)
    input_list = input_grid.tolist()

    # 3. Find the index of the first non-zero digit.
    insertion_index = find_first_non_zero_index(input_list)

    # 4. Create a new list by inserting 0 at the insertion_index.
    # Make a copy first if you need to preserve the original list for other operations
    # modified_list = input_list[:] # Use slicing for copying if needed
    # modified_list.insert(insertion_index, 0)
    # Or directly modify if the original list isn't needed afterwards:
    modified_list = input_list # Reassigning name, list is mutable
    modified_list.insert(insertion_index, 0)


    # 5. Take the first N elements from the modified list (truncate).
    output_list = modified_list[:original_length]

    # 6. Convert the final list of integers back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str
```
