
## train_1

**input:**
```
0 1 2 1 1 1 0 2 0 0 0 0
```


**output:**
```
2 2 0 0 0 0 0 0 1 1 1 1
```


## train_2

**input:**
```
2 0 2 0 1 0 0 0 2 0 2 2
```


**output:**
```
2 2 2 2 2 0 0 0 0 0 0 1
```


## train_3

**input:**
```
0 0 2 1 1 1 1 1 2 2 2 0
```


**output:**
```
2 2 2 2 0 0 0 1 1 1 1 1
```


## train_4

**input:**
```
2 0 2 0 0 0 1 2 0 0 0 0
```


**output:**
```
2 2 2 0 0 0 0 0 0 0 0 1
```


## train_5

**input:**
```
0 0 0 0 2 1 2 1 2 0 0 2
```


**output:**
```
2 2 2 2 0 0 0 0 0 0 1 1
```


## train_6

**input:**
```
0 0 1 0 2 2 1 2 0 1 1 2
```


**output:**
```
2 2 2 2 0 0 0 0 1 1 1 1
```


## train_7

**input:**
```
0 1 2 2 0 0 1 1 2 1 2 0
```


**output:**
```
2 2 2 2 0 0 0 0 1 1 1 1
```

## Perception

The input and output are both sequences of integers, specifically containing only the digits 0, 1, and 2. Each input sequence has a corresponding output sequence of the same length (12 elements in all provided examples).

Comparing the input and output sequences, the key observation is that the *counts* of each digit (0, 1, 2) are generally preserved between the input and output. For example, in `train_1`, the input has six 0s, four 1s, and two 2s, and the output also has six 0s, four 1s, and two 2s. This holds true for all examples except `train_2`, which might be an anomaly or error in the data (input has 5 zeros, 1 one, 6 twos; output has 6 zeros, 1 one, 5 twos). Assuming count preservation is the general rule, the transformation appears to be a rearrangement or sorting of the input elements.

Looking at the structure of the output sequences, a consistent pattern emerges:
1.  All the '2's appear first.
2.  All the '0's appear next.
3.  All the '1's appear last.

This suggests a custom sorting order: 2 > 0 > 1.

## Facts


```yaml
task_elements:
  - item: sequence
    properties:
      - type: list of integers
      - allowed_values: [0, 1, 2]
      - length: fixed (12 in examples)
relationship:
  - input sequence: contains elements [0, 1, 2]
  - output sequence: contains the same elements as the input sequence, but rearranged
transformation:
  - type: sorting
  - rule: rearrange elements based on a custom order
  - order:
      1. All '2's
      2. All '0's
      3. All '1's
preservation:
  - counts of each distinct element (0, 1, 2) are preserved from input to output (with potential exception noted in train_2).
  - sequence length is preserved.
```


## Natural Language Program

1.  Receive the input sequence of numbers.
2.  Count the occurrences of the number '2' in the input sequence.
3.  Count the occurrences of the number '0' in the input sequence.
4.  Count the occurrences of the number '1' in the input sequence.
5.  Construct the output sequence by first concatenating '2' repeated by its count, followed by '0' repeated by its count, and finally followed by '1' repeated by its count.
6.  Return the newly constructed sequence.
```python
import collections

"""
Transforms an input sequence of integers (0, 1, 2) by rearranging its elements according to a specific custom order: all '2's first, followed by all '0's, and finally all '1's. The counts of each digit (0, 1, 2) from the input sequence are preserved in the output sequence.
"""

def transform(input_str: str) -> list[int]:
    """
    Sorts a sequence of digits (0, 1, 2) based on the custom order 2 > 0 > 1.

    Args:
        input_str: A string containing space-separated integers (0, 1, or 2).

    Returns:
        A list of integers sorted according to the rule: 2s, then 0s, then 1s.
    """
    # Parse the input string into a list of integers
    # Handle potential errors if input is not as expected, though examples are clean.
    try:
        input_list = [int(x) for x in input_str.split()]
    except ValueError:
        print("Error: Input string contains non-integer values.")
        return [] # Or raise an exception

    # Count the occurrences of each number (2, 0, 1)
    counts = collections.Counter(input_list)
    count2 = counts.get(2, 0)
    count0 = counts.get(0, 0)
    count1 = counts.get(1, 0)

    # Construct the output list based on the counts and the desired order (2, 0, 1)
    output_list = []
    output_list.extend([2] * count2) # Add all the '2's
    output_list.extend([0] * count0) # Add all the '0's
    output_list.extend([1] * count1) # Add all the '1's

    return output_list

# Example usage (optional, for testing)
# train_1_input = "0 1 2 1 1 1 0 2 0 0 0 0"
# train_1_output = transform(train_1_input)
# print(f"Input: {train_1_input}")
# print(f"Output: {train_1_output}") # Expected: [2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]

# train_2_input = "2 0 2 0 1 0 0 0 2 0 2 2"
# train_2_output = transform(train_2_input)
# print(f"Input: {train_2_input}")
# print(f"Output: {train_2_output}") # Expected: [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1]
                                     # Actual:   [2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1] (follows derived rule)
```
```python
import collections
import numpy as np
from typing import List, Union

"""
Transforms an input sequence of integers (0, 1, 2) by rearranging its elements according to a specific custom sorting order: all occurrences of '2' first, followed by all occurrences of '0', and finally all occurrences of '1'. The counts of each digit (0, 1, 2) from the input sequence are strictly preserved in the output sequence.
"""

def count_elements(sequence: Union[List[int], np.ndarray]) -> collections.Counter:
    """Counts the occurrences of each element in the sequence."""
    return collections.Counter(sequence)

def construct_sorted_sequence(counts: collections.Counter) -> List[int]:
    """Constructs the output sequence based on counts and the custom sort order (2, 0, 1)."""
    # Get counts for each element, defaulting to 0 if not present
    count2 = counts.get(2, 0)
    count0 = counts.get(0, 0)
    count1 = counts.get(1, 0)

    # Build the output list by appending elements in the desired order
    output_sequence = []
    output_sequence.extend([2] * count2) # Add all the '2's
    output_sequence.extend([0] * count0) # Add all the '0's
    output_sequence.extend([1] * count1) # Add all the '1's
    return output_sequence

def transform(input_sequence: Union[List[int], np.ndarray]) -> List[int]:
    """
    Sorts a sequence containing digits 0, 1, and 2 based on the custom order 2 > 0 > 1.

    Args:
        input_sequence: A list or numpy array containing integers (0, 1, or 2).

    Returns:
        A new list containing the same elements as the input, but sorted
        according to the rule: 2s first, then 0s, then 1s.
    """
    # Ensure input is treated as a standard list if it's a numpy array
    # This allows consistent use of collections.Counter
    if isinstance(input_sequence, np.ndarray):
        # Assuming a 1D array based on examples
        input_list = input_sequence.tolist() 
    else:
        input_list = input_sequence

    # Count the occurrences of each number (0, 1, 2)
    element_counts = count_elements(input_list)

    # Construct the output sequence using the counts and the custom order
    output_sequence = construct_sorted_sequence(element_counts)

    return output_sequence
```
