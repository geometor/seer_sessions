
## train_1

**input:**
```
0 0 0 0 0 0 3 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 6 0
```


## train_2

**input:**
```
0 0 0 8 2 2 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 2 2 1 0 0
```


## train_3

**input:**
```
9 9 1 3 6 3 7 0 0 8 3 2
```


**output:**
```
8 3 2 9 9 1 3 6 3 7 0 0
```


## train_4

**input:**
```
5 2 7 7 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 5 2 7 7 0 0 0 0 0
```


## train_5

**input:**
```
3 6 2 1 7 4 1 6 7 5 0 7
```


**output:**
```
5 0 7 3 6 2 1 7 4 1 6 7
```


## train_6

**input:**
```
1 8 4 4 0 0 0 0 0 6 1 7
```


**output:**
```
6 1 7 1 8 4 4 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 4 3 5 3 3 0
```


**output:**
```
3 3 0 0 0 0 0 0 0 4 3 5
```

## Perception of Task Elements

The task involves transforming a sequence of 12 single digits. Each input example consists of a string of 12 digits separated by spaces. The corresponding output is also a string of 12 digits separated by spaces. The core operation appears to be a rearrangement of the elements within the sequence. Specifically, the last three elements of the input sequence are moved to the beginning of the output sequence, while the first nine elements are shifted to the right to accommodate them. This is consistent across all examples, regardless of the specific digits or the presence of zeros. The transformation is a fixed-size circular shift (rotation) to the right.

## YAML Fact Document


```yaml
task_description: Rearrange elements within a sequence of digits.
input_structure:
  type: sequence
  element_type: digit (represented as strings, separated by spaces)
  length: 12
output_structure:
  type: sequence
  element_type: digit (represented as strings, separated by spaces)
  length: 12
transformation:
  type: circular_shift
  direction: right
  shift_amount: 3
  details: The last 3 elements of the input sequence become the first 3 elements of the output sequence. The first 9 elements of the input sequence become the last 9 elements of the output sequence, maintaining their relative order.
examples_consistency: All provided examples follow the same transformation rule.
```


## Natural Language Program

1.  Receive the input sequence of 12 digits.
2.  Identify the last 3 digits of the input sequence.
3.  Identify the first 9 digits of the input sequence.
4.  Construct the output sequence by first placing the identified last 3 digits, followed by the identified first 9 digits, maintaining the internal order within both subsequences.
5.  Format the resulting sequence as a string with digits separated by spaces.
```python
"""
Transforms a sequence of 12 digits by moving the last 3 digits to the beginning, 
effectively performing a circular right shift by 3 positions.
"""

import collections

def transform(input_str: str) -> str:
    """
    Applies a circular right shift of 3 positions to a sequence of 12 digits.

    Args:
        input_str: A string containing 12 digits separated by spaces.

    Returns:
        A string representing the transformed sequence, with digits separated by spaces.
    """
    # Split the input string into a list of digit strings
    digits = input_str.split(' ')

    # Ensure the input has the correct length (optional but good practice)
    if len(digits) != 12:
        raise ValueError("Input string must contain exactly 12 digits separated by spaces.")

    # Identify the last 3 digits
    last_three = digits[-3:]

    # Identify the first 9 digits
    first_nine = digits[:9]

    # Construct the output list by concatenating the last 3 and first 9 parts
    output_digits = last_three + first_nine

    # Join the transformed list back into a space-separated string
    output_str = ' '.join(output_digits)

    return output_str

```
```python
"""
Transforms a 1D numerical array of 12 elements by applying a circular right 
shift of 3 positions. The last 3 elements of the input array become the 
first 3 elements of the output array, and the first 9 elements of the input 
array follow them.
"""

import numpy as np

# Helper function to extract the last n elements
def extract_last_n(arr: np.ndarray, n: int) -> np.ndarray:
    """Extracts the last n elements from a numpy array."""
    return arr[-n:]

# Helper function to extract the first m elements
def extract_first_m(arr: np.ndarray, m: int) -> np.ndarray:
    """Extracts the first m elements from a numpy array."""
    return arr[:m]

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a circular right shift of 3 positions to the input array.

    Args:
        input_grid: A 1D NumPy array of shape (12,) containing integers.

    Returns:
        A 1D NumPy array of shape (12,) representing the transformed sequence.
    """
    # Define the shift amount
    shift_amount = 3
    array_length = len(input_grid)

    # Extract the subsequence containing the last 3 elements
    last_part = extract_last_n(input_grid, shift_amount)

    # Extract the subsequence containing the first 9 elements (length - shift_amount)
    first_part = extract_first_m(input_grid, array_length - shift_amount)

    # Concatenate the two parts in the new order: last part first, then first part
    output_grid = np.concatenate((last_part, first_part))

    # Return the resulting array
    return output_grid

```
