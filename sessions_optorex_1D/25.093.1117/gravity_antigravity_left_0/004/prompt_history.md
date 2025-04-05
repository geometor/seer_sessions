
## train_1

**input:**
```
2 1 2 0 2 1 2 1 2 0 2 0
```


**output:**
```
2 2 2 2 2 2 0 0 0 1 1 1
```


## train_2

**input:**
```
2 0 0 1 1 0 0 1 0 0 0 2
```


**output:**
```
2 2 0 0 0 0 0 0 0 1 1 1
```


## train_3

**input:**
```
1 1 0 0 1 0 2 0 0 0 0 1
```


**output:**
```
2 0 0 0 0 0 0 0 1 1 1 1
```


## train_4

**input:**
```
1 1 1 1 1 2 1 1 2 2 2 2
```


**output:**
```
2 2 2 2 2 1 1 1 1 1 1 1
```


## train_5

**input:**
```
1 1 2 0 2 0 0 1 0 2 2 0
```


**output:**
```
2 2 2 2 0 0 0 0 0 1 1 1
```


## train_6

**input:**
```
2 1 2 0 0 0 0 1 0 0 0 1
```


**output:**
```
2 2 0 0 0 0 0 0 0 1 1 1
```


## train_7

**input:**
```
0 1 1 0 0 0 0 0 0 0 2 1
```


**output:**
```
2 0 0 0 0 0 0 0 0 1 1 1
```

*   **Perception:** The task involves rearranging a sequence of twelve digits (0, 1, or 2). The output sequence contains the exact same digits as the input sequence, but sorted according to a specific custom order. The length of the sequence remains unchanged.

*   **Facts:**
    
```yaml
    task_type: rearrangement
    input_elements:
      type: sequence
      data_type: integer
      possible_values: [0, 1, 2]
      length: 12
    output_elements:
      type: sequence
      data_type: integer
      possible_values: [0, 1, 2]
      length: 12
    relationship:
      - The output sequence is a permutation of the input sequence.
      - The count of each distinct digit (0, 1, 2) is preserved between input and output.
      - The output sequence is sorted based on a custom key: 2 comes first, followed by 0, then 1.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of twelve digits.
    2.  Count the occurrences of the digit '2' in the input sequence.
    3.  Count the occurrences of the digit '0' in the input sequence.
    4.  Count the occurrences of the digit '1' in the input sequence.
    5.  Construct the output sequence by concatenating:
        *   The digit '2' repeated according to its count.
        *   The digit '0' repeated according to its count.
        *   The digit '1' repeated according to its count.
    6.  Return the resulting sequence.
```python
import collections

"""
Sorts a sequence of digits (0, 1, 2) according to a custom order: 2s first, then 0s, then 1s.
The input is a string of space-separated digits.
The output is a string of space-separated digits sorted according to the custom rule.
"""

# No external libraries needed beyond standard collections

def custom_sort_key(digit):
  """
  Defines the custom sorting order: 2 < 0 < 1.
  Maps digits to sortable values.
  """
  if digit == 2:
    return 0 # 2 comes first
  elif digit == 0:
    return 1 # 0 comes second
  elif digit == 1:
    return 2 # 1 comes last
  else:
    # Handle unexpected values if necessary, though the problem implies only 0, 1, 2
    return 3 

def transform(input_str):
    """
    Sorts the input sequence of digits based on the custom order 2 -> 0 -> 1.

    Args:
        input_str: A string containing space-separated digits (0, 1, or 2).

    Returns:
        A string containing the sorted digits, space-separated.
    """
    # 1. Receive the input sequence and parse it
    # Split the input string by spaces and convert each part to an integer
    input_digits = [int(d) for d in input_str.split()]

    # 2. Sort the digits using the custom key
    # The custom_sort_key function dictates that 2s are smallest, then 0s, then 1s
    sorted_digits = sorted(input_digits, key=custom_sort_key)

    # 3. Construct the output sequence string
    # Convert the sorted integers back to strings
    output_digits_str = [str(d) for d in sorted_digits]
    
    # Join the string digits with spaces
    output_str = " ".join(output_digits_str)

    # 4. Return the resulting sequence string
    return output_str

```
```python
"""
Sorts a NumPy array of digits (0, 1, 2) according to a custom order: 
elements with value 2 come first, followed by elements with value 0, 
followed by elements with value 1.
"""

import numpy as np

def custom_sort_key(digit):
  """
  Defines the custom sorting order: 2 < 0 < 1.
  Maps digits to sortable values for use with sorted().
  """
  if digit == 2:
    return 0 # 2 comes first
  elif digit == 0:
    return 1 # 0 comes second
  elif digit == 1:
    return 2 # 1 comes last
  else:
    # Assign a high value for unexpected inputs to place them last
    return 3 

def transform(input_array):
  """
  Sorts the input NumPy array based on the custom order 2 -> 0 -> 1.

  Args:
      input_array: A NumPy array containing integers (expected: 0, 1, or 2).

  Returns:
      A NumPy array containing the sorted integers according to the custom rule. 
      (Note: Returning a list might also be acceptable depending on the framework,
       but returning a NumPy array is generally safer if the input is NumPy).
  """
  # 1. Receive the input NumPy array (no parsing needed like before)
  # The input_array is already in a usable format (e.g., list or NumPy array)

  # 2. Sort the elements using the custom key
  # The sorted() function works on iterables like NumPy arrays and lists.
  # It returns a standard Python list.
  sorted_list = sorted(input_array, key=custom_sort_key)

  # 3. Convert the sorted list back to a NumPy array (optional but often preferred)
  # Ensure the output type matches the expected format (likely NumPy array).
  output_array = np.array(sorted_list, dtype=input_array.dtype) 

  # 4. Return the resulting sorted array
  return output_array

```
