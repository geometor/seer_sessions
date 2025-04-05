
## train_1

**input:**
```
0 2 0 1 1 2 0 0 1 0 1 1
```


**output:**
```
2 2 1 1 1 1 1 0 0 0 0 0
```


## train_2

**input:**
```
1 1 0 2 0 2 1 0 1 1 1 0
```


**output:**
```
2 2 1 1 1 1 1 1 0 0 0 0
```


## train_3

**input:**
```
0 1 2 1 2 0 0 0 1 0 2 1
```


**output:**
```
2 2 2 1 1 1 1 0 0 0 0 0
```


## train_4

**input:**
```
2 2 2 0 0 2 1 0 2 1 1 1
```


**output:**
```
2 2 2 2 2 1 1 1 1 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 1 1 0 1 1 2
```


**output:**
```
2 1 1 1 1 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 1 2 0 1 1 2 0 0 0 0 0
```


**output:**
```
2 2 1 1 1 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 2 0 0 0 0 1 2 0 1 0 2
```


**output:**
```
2 2 2 1 1 0 0 0 0 0 0 0
```

## Perception

The input and output are both sequences of integers, specifically containing only the digits 0, 1, and 2. Each sequence appears to have a fixed length of 12 elements. By comparing the input and output sequences across multiple examples, a consistent pattern emerges: the output sequence contains the same integers as the input sequence, but they are arranged in a different order. Specifically, the output sequence seems to be sorted in descending order (from largest to smallest value).

## Facts


```yaml
task_elements:
  - name: input_sequence
    type: List[int]
    description: A sequence of 12 integers, containing only values 0, 1, or 2.
    properties:
      length: 12
      elements: [0, 1, 2]
  - name: output_sequence
    type: List[int]
    description: A sequence of 12 integers derived from the input sequence.
    properties:
      length: 12
      elements: [0, 1, 2]
      relationship_to_input: Contains the same multiset of elements as the input sequence.

transformation:
  action: sort
  input: input_sequence
  output: output_sequence
  rule: The elements of the input sequence are rearranged to produce the output sequence.
  details: The rearrangement follows a descending order sort rule (largest values appear first).
```


## Natural Language Program

1.  Take the input sequence of 12 integers.
2.  Sort the integers within the sequence in descending order (from largest to smallest).
3.  Return the sorted sequence as the output.
```python
"""
Takes an input sequence of 12 integers (0, 1, or 2) and sorts them in descending order to produce the output sequence.
"""

import numpy as np

def transform(input_sequence_str: str) -> str:
    """
    Sorts a sequence of integers represented as a space-separated string in descending order.

    Args:
        input_sequence_str: A string containing space-separated integers (0, 1, or 2).

    Returns:
        A string containing the sorted integers, space-separated.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_sequence_str.split()]

    # Sort the list in descending order
    # The reverse=True argument sorts from largest to smallest
    output_list = sorted(input_list, reverse=True)

    # Format the output list back into a space-separated string
    output_sequence_str = " ".join(map(str, output_list))

    return output_sequence_str

```
```python
"""
Sorts the elements of an input sequence of 12 integers (composed of 0s, 1s, and 2s) in descending order.
"""

import numpy as np

def transform(input_sequence):
    """
    Sorts a sequence of integers in descending order.

    Args:
        input_sequence: A sequence (e.g., list or numpy array) of integers.

    Returns:
        A numpy array containing the sorted integers in descending order.
    """

    # The input might be a list or a numpy array.
    # Python's built-in sorted() function works on various sequence types
    # and returns a new list.
    # We specify reverse=True for descending order.
    sorted_list = sorted(input_sequence, reverse=True)

    # Convert the resulting sorted list to a numpy array for consistency
    # with the typical data structures used in such environments.
    output_sequence = np.array(sorted_list)

    return output_sequence
```
```python
"""
Takes an input sequence of integers represented as a space-separated string,
sorts the integers in descending order, and returns the sorted sequence
as a space-separated string.
"""

import numpy as np # Although numpy isn't strictly needed for this specific task,
                  # it's often available and can handle array/list operations.
                  # Standard Python lists and sorting are sufficient here.

def transform(input_sequence_str: str) -> str:
    """
    Sorts a sequence of integers represented as a space-separated string in descending order.

    Args:
        input_sequence_str: A string containing space-separated integers.

    Returns:
        A string containing the sorted integers, space-separated.
    """
    # 1. Parse the input string into a list of integers.
    # Split the string by spaces and convert each part to an integer.
    input_list = [int(x) for x in input_sequence_str.split()]

    # 2. Sort the list of integers in descending order.
    # The reverse=True argument ensures sorting from largest to smallest.
    sorted_list = sorted(input_list, reverse=True)

    # 3. Format the sorted list back into a space-separated string.
    # Convert each integer back to a string and join them with spaces.
    output_sequence_str = " ".join(map(str, sorted_list))

    # 4. Return the resulting string.
    return output_sequence_str

```
