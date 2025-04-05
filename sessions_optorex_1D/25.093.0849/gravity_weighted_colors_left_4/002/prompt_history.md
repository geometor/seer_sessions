
## train_1

**input:**
```
0 1 0 0 2 0 0 0 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 2 2 2
```


## train_2

**input:**
```
1 1 0 2 2 0 0 2 0 1 2 0
```


**output:**
```
0 0 0 0 0 1 1 1 2 2 2 2
```


## train_3

**input:**
```
2 0 2 0 0 0 2 2 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 2 2 2 2
```


## train_4

**input:**
```
2 2 0 0 0 0 1 1 0 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 2 2
```


## train_5

**input:**
```
1 0 0 0 0 2 0 0 2 1 1 2
```


**output:**
```
0 0 0 0 0 0 1 1 1 2 2 2
```


## train_6

**input:**
```
0 1 0 0 1 1 2 0 0 2 0 1
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 2 2
```


## train_7

**input:**
```
0 0 0 0 2 0 2 1 2 2 1 1
```


**output:**
```
0 0 0 0 0 1 1 1 2 2 2 2
```

*   **Perception:** The input is a string consisting of digits (0, 1, 2) separated by spaces. The output is also a string of space-separated digits. Observing the examples, the output string appears to contain the same digits as the input string, but rearranged. Specifically, the digits in the output string are always sorted in non-decreasing order (all 0s, then all 1s, then all 2s). The number of occurrences of each digit (0, 1, 2) seems to be preserved between the input and the output.

*   **Facts:**
    
```yaml
    task_type: transformation
    input_format: string
      components:
        - type: sequence
          element_type: digit
          valid_digits: [0, 1, 2]
          separator: space
          length: fixed (12 in examples)
    output_format: string
      components:
        - type: sequence
          element_type: digit
          valid_digits: [0, 1, 2]
          separator: space
          length: same as input
    transformation: rearrangement
      property: sorting
      order: non-decreasing (ascending)
      preserves_elements: true
      preserves_counts: true
    ```


*   **Natural Language Program:**
    1.  Read the input string containing space-separated digits.
    2.  Split the input string by spaces to get a list of digit characters.
    3.  Sort the list of digit characters numerically in non-decreasing (ascending) order.
    4.  Join the sorted list of digit characters back into a single string, using a space as the separator between digits.
    5.  Output the resulting string.
```python
"""
Transforms an input string of space-separated digits (0, 1, 2) by sorting the digits numerically in non-decreasing (ascending) order and returning the sorted digits as a space-separated string.
"""

import collections

def transform(input_str: str) -> str:
    """
    Sorts the digits in a space-separated string.

    Args:
        input_str: A string containing digits (0, 1, 2) separated by spaces.

    Returns:
        A string containing the same digits as the input, sorted numerically
        in non-decreasing order and separated by spaces.
    """
    # 1. Split the input string by spaces to get a list of digit characters.
    # Example: "0 1 0 0 2 0 0 0 2 2 0 0" -> ['0', '1', '0', '0', '2', '0', '0', '0', '2', '2', '0', '0']
    digits_str = input_str.split(' ')

    # 2. Convert the list of string digits to integers for numerical sorting (optional but cleaner).
    # Example: ['0', '1', '0', '0', '2', '0', '0', '0', '2', '2', '0', '0'] -> [0, 1, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0]
    # digits_int = [int(d) for d in digits_str] # Alternative if conversion is desired

    # 3. Sort the list of digit characters numerically (Python's sort works directly on strings here).
    # Example: ['0', '1', '0', '0', '2', '0', '0', '0', '2', '2', '0', '0'] -> ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2']
    digits_str.sort() # Sorting strings '0', '1', '2' works numerically

    # 4. Join the sorted list of digit characters back into a single string, using a space as the separator.
    # Example: ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2'] -> "0 0 0 0 0 0 0 0 1 2 2 2"
    output_str = ' '.join(digits_str)

    # 5. Return the resulting string.
    return output_str

```
