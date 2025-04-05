
## train_1

**input:**
```
0 8 2 0 5 7 0 0 9 0 6 0
```


**output:**
```
0 0 0 0 0 0 8 2 5 7 9 6
```


## train_2

**input:**
```
1 0 6 0 0 9 0 0 0 7 0 7
```


**output:**
```
0 0 0 0 0 0 0 1 6 9 7 7
```


## train_3

**input:**
```
0 7 0 0 0 9 0 0 3 7 2 0
```


**output:**
```
0 0 0 0 0 0 0 7 9 3 7 2
```


## train_4

**input:**
```
0 0 0 2 0 6 8 0 2 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 2 6 8 2 4
```


## train_5

**input:**
```
9 0 7 0 0 0 6 8 0 2 7 0
```


**output:**
```
0 0 0 0 0 0 9 7 6 8 2 7
```


## train_6

**input:**
```
0 0 4 0 0 7 7 0 0 8 0 8
```


**output:**
```
0 0 0 0 0 0 0 4 7 7 8 8
```


## train_7

**input:**
```
0 0 0 0 0 5 0 5 3 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 5 5 3 1
```

*   **Perception of Elements:**
    *   The input and output are sequences of single-digit integers represented as strings separated by spaces.
    *   The sequences contain two types of numbers: zero (0) and non-zero (1-9).
    *   The length of the output sequence is the same as the length of the input sequence.
    *   The multiset of numbers in the output is identical to the multiset of numbers in the input. The transformation is a reordering (permutation) of the input elements.

*   **YAML Facts:**
    
```yaml
    task_description: "Reorder a sequence of single-digit integers."
    input_elements:
      - type: sequence
        description: "A sequence of single-digit integers separated by spaces."
        item_type: integer (0-9)
    output_elements:
      - type: sequence
        description: "A reordered sequence of the input integers, separated by spaces."
        item_type: integer (0-9)
    objects:
      - name: input_sequence
        properties:
          - elements: list of integers
          - length: integer
      - name: output_sequence
        properties:
          - elements: list of integers
          - length: integer (same as input)
      - name: zero_elements
        properties:
          - subset_of: input_sequence
          - value: 0
      - name: non_zero_elements
        properties:
          - subset_of: input_sequence
          - value: range(1, 10)
          - relative_order: maintained from input
    relationships:
      - type: identity
        description: "The multiset of numbers in the output is identical to the input."
      - type: ordering
        description: "All zero elements from the input appear first in the output."
      - type: ordering
        description: "All non-zero elements from the input appear after the zeros in the output."
      - type: relative_ordering
        description: "The relative order of the non-zero elements in the output is the same as their relative order in the input."
    actions:
      - name: parse_input
        description: "Convert the input string into a list of integers."
      - name: partition
        description: "Separate the input list into two lists: one containing only zeros and one containing non-zeros while preserving the relative order of non-zeros."
      - name: concatenate
        description: "Combine the list of zeros followed by the list of non-zeros."
      - name: format_output
        description: "Convert the resulting list of integers back into a space-separated string."

    ```


*   **Natural Language Program:**
    1.  Read the input string representing a sequence of space-separated integers.
    2.  Parse the input string into a list of integers.
    3.  Create two new empty lists: one for zeros (`zeros_list`) and one for non-zeros (`non_zeros_list`).
    4.  Iterate through the parsed list of integers from the input:
        *   If the integer is 0, append it to the `zeros_list`.
        *   If the integer is not 0, append it to the `non_zeros_list`.
    5.  Concatenate the `zeros_list` and the `non_zeros_list` to form the final result list.
    6.  Convert the integers in the result list back to strings.
    7.  Join the string representations of the integers in the result list with spaces to form the output string.
    8.  Output the resulting string.
```python
import math # math is available
import numpy as np # numpy is available
import collections # collections is available
import re # regular expressions is available


"""
Reorders a sequence of space-separated single-digit integers such that all zero 
elements appear first, followed by all non-zero elements. The relative order of 
the non-zero elements is preserved from the original input sequence.
"""

def transform(input_str: str) -> str:
    """
    Transforms a string of space-separated integers by moving all zeros 
    to the beginning while maintaining the relative order of non-zero elements.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing the reordered space-separated integers.
    """

    # 1. Parse the input string into a list of integers.
    # Split the input string by spaces and convert each part to an integer.
    try:
        numbers_int = [int(n) for n in input_str.split()]
    except ValueError:
        # Handle cases where input might not be valid integers
        print(f"Error: Input string '{input_str}' contains non-integer values.")
        return "" # Or raise an error, depending on desired behavior

    # 2. Create two new empty lists: one for zeros and one for non-zeros.
    zeros_list = []
    non_zeros_list = []

    # 3. Iterate through the parsed list of integers.
    # Populate the lists based on whether the number is zero or non-zero.
    for num in numbers_int:
        if num == 0:
            # If the integer is 0, append it to the zeros_list.
            zeros_list.append(num)
        else:
            # If the integer is not 0, append it to the non_zeros_list.
            # This preserves the relative order of non-zeros.
            non_zeros_list.append(num)

    # 4. Concatenate the zeros_list and the non_zeros_list.
    # This forms the final ordered list of integers.
    result_list_int = zeros_list + non_zeros_list

    # 5. Convert the integers in the result list back to strings.
    result_list_str = [str(num) for num in result_list_int]

    # 6. Join the string representations with spaces.
    # Format the final list as a space-separated string for output.
    output_str = " ".join(result_list_str)

    # 7. Return the resulting string.
    return output_str

```
```python
import numpy as np # numpy is available for array operations
import math # math is available
import collections # collections is available
import re # regular expressions is available

"""
Reorders elements of an integer NumPy array such that all zeros precede non-zeros, 
preserving the relative order of non-zeros, and formats the result as a space-separated string.
"""

def transform(input_arr: np.ndarray) -> str:
    """
    Transforms a NumPy array of integers by moving all zeros to the beginning 
    while maintaining the relative order of non-zero elements, and returns 
    the result as a space-separated string.

    Args:
        input_arr: A 1-dimensional NumPy array containing integers.

    Returns:
        A string containing the reordered space-separated integers.
    """

    # 1. Create two new empty lists to store zero and non-zero elements.
    zeros_list = []
    non_zeros_list = []

    # 2. Iterate through each element in the input NumPy array.
    for element in input_arr:
        # 3. Check if the element is zero.
        if element == 0:
            # If it is 0, append it to the zeros_list.
            zeros_list.append(element)
        else:
            # If it is not 0, append it to the non_zeros_list.
            # This preserves the relative order of non-zero elements.
            non_zeros_list.append(element)

    # 4. Concatenate the lists: zeros first, then non-zeros.
    # This creates the final ordered sequence of numbers.
    ordered_list = zeros_list + non_zeros_list

    # 5. Convert each integer in the ordered list to its string representation.
    # We use a list comprehension for conciseness.
    string_list = [str(num) for num in ordered_list]

    # 6. Join the string representations with a single space.
    # This formats the output according to the required specification.
    output_str = " ".join(string_list)

    # 7. Return the resulting space-separated string.
    return output_str

```
```python
import numpy as np # numpy is available for array operations
import math # math is available
import collections # collections is available
import re # regular expressions is available

"""
Reorders the elements of an input integer NumPy array such that all zeros 
precede non-zeros, preserving the relative order of the non-zero elements, 
and formats the result as a space-separated string.
"""

def transform(input_arr: np.ndarray) -> str:
    """
    Transforms a NumPy array of integers by moving all zeros to the beginning 
    while maintaining the relative order of non-zero elements, and returns 
    the result as a space-separated string.

    Args:
        input_arr: A NumPy array containing integers (potentially multi-dimensional).

    Returns:
        A string containing the reordered space-separated integers.
    """

    # 1. Flatten the input NumPy array into a 1D sequence.
    # This handles potential multi-dimensional inputs consistently.
    flattened_sequence = input_arr.flatten()

    # 2. Create two new empty lists to store zero and non-zero elements.
    zeros_list = []
    non_zeros_list = []

    # 3. Iterate through each element in the flattened sequence.
    for element in flattened_sequence:
        # 4. Check if the element is zero.
        if element == 0:
            # If it is 0, append it to the zeros_list.
            zeros_list.append(element)
        else:
            # If it is not 0, append it to the non_zeros_list.
            # This preserves the relative order of non-zero elements from the flattened sequence.
            non_zeros_list.append(element)

    # 5. Concatenate the lists: zeros first, then non-zeros.
    # This creates the final ordered sequence of numbers.
    ordered_list = zeros_list + non_zeros_list

    # 6. Convert each integer in the ordered list to its string representation.
    # We use a list comprehension for conciseness.
    string_list = [str(num) for num in ordered_list]

    # 7. Join the string representations with a single space.
    # This formats the output according to the required specification.
    output_str = " ".join(string_list)

    # 8. Return the resulting space-separated string.
    return output_str
```
