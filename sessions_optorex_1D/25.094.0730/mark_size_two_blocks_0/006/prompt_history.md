
## train_1

**input:**
```
0 1 1 0 0 0 1 0 0 0 1 0
```


**output:**
```
3 1 1 3 0 0 1 0 0 0 1 0
```


## train_2

**input:**
```
0 1 0 0 0 0 0 1 1 1 0 0
```


**output:**
```
0 1 0 0 0 0 0 1 1 1 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 0 0 0 1 0 0
```


**output:**
```
0 0 0 1 1 1 0 0 0 1 0 0
```


## train_4

**input:**
```
1 1 1 0 0 0 0 0 1 0 0 0
```


**output:**
```
1 1 1 0 0 0 0 0 1 0 0 0
```


## train_5

**input:**
```
1 0 0 0 0 0 0 1 1 1 0 0
```


**output:**
```
1 0 0 0 0 0 0 1 1 1 0 0
```


## train_6

**input:**
```
1 1 0 0 0 1 0 0 0 1 0 0
```


**output:**
```
1 1 3 0 0 1 0 0 0 1 0 0
```


## train_7

**input:**
```
1 0 0 0 1 1 1 0 0 0 0 0
```


**output:**
```
1 0 0 0 1 1 1 0 0 0 0 0
```

**Perception of the Elements:**

The task involves transforming a sequence of single digits (0s and 1s) into another sequence of the same length. The core transformation appears to target specific `0`s based on their neighboring elements. In some examples (`train_1`, `train_6`), certain `0`s are changed to `3`s, while in others (`train_2`, `train_3`, `train_4`, `train_5`, `train_7`), the input sequence remains unchanged in the output. The change from `0` to `3` seems conditional on the immediate context of the `0` within the sequence, specifically its relationship with adjacent `1`s. Sequences of `1`s of length other than two (e.g., single `1` or `1 1 1`) do not trigger this change.

**Facts:**


```yaml
objects:
  - name: sequence_element
    properties:
      - value: integer (0, 1 initially; can become 3 in output)
      - position: index within the sequence (0-based)
  - name: sequence
    properties:
      - elements: list of sequence_element
      - length: integer

relationships:
  - type: adjacency
    description: Describes the positional relationship between sequence elements.
    properties:
      - preceding_element: The element immediately before the current element.
      - succeeding_element: The element immediately after the current element.
      - preceding_pair: The two elements immediately before the current element.
      - succeeding_pair: The two elements immediately after the current element.

actions:
  - name: check_adjacency
    description: Examine the values of elements adjacent to a specific element.
    inputs:
      - sequence_element (specifically, one with value 0)
      - sequence
    outputs:
      - boolean (true if adjacent context meets criteria, false otherwise)
  - name: replace_value
    description: Change the value of a sequence element.
    inputs:
      - sequence_element (the one to change)
      - new_value: integer (specifically, 3)
    outputs:
      - modified_sequence_element

conditions_for_change:
  - element_value_is_zero: The sequence element's value must be 0.
  - adjacent_to_exactly_two_ones:
      - The element must be immediately preceded by the sequence `1 1`.
      - OR The element must be immediately succeeded by the sequence `1 1`.

transformation_goal:
  - Create an output sequence by applying the replacement rule to all qualifying 0s in the input sequence, while keeping all other elements unchanged.
```


**Natural Language Program:**

1.  Initialize an output sequence as a copy of the input sequence.
2.  Iterate through each element of the input sequence using its index, from the beginning to the end.
3.  For the element at the current index:
    *   Check if the element's value is `0`.
    *   If it is `0`, check its neighbors:
        *   Check if the two elements *preceding* the current index (i.e., at index-2 and index-1) both exist and have the value `1`.
        *   Check if the two elements *succeeding* the current index (i.e., at index+1 and index+2) both exist and have the value `1`.
    *   If *either* the preceding pair is `1 1` *or* the succeeding pair is `1 1`, change the value of the element at the current index in the *output* sequence to `3`.
4.  After iterating through all elements, return the modified output sequence.
```python
import re
from typing import List

"""
Transforms a sequence of 0s and 1s based on adjacency rules.
Specifically, a 0 is changed to a 3 if it is immediately preceded
by '1 1' OR immediately succeeded by '1 1'. Otherwise, the
sequence remains unchanged. The input and output are space-separated
strings of digits.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A space-separated string of 0s and 1s.

    Returns:
        A space-separated string representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # Iterate through each element of the input sequence
    for i in range(n):
        # Check if the current element is 0
        if input_list[i] == 0:
            # Check the preceding pair condition
            precedes_11 = False
            if i >= 2 and input_list[i-2] == 1 and input_list[i-1] == 1:
                precedes_11 = True

            # Check the succeeding pair condition
            succeeds_11 = False
            if i <= n - 3 and input_list[i+1] == 1 and input_list[i+2] == 1:
                succeeds_11 = True

            # If either condition is met, change the corresponding output element to 3
            if precedes_11 or succeeds_11:
                output_list[i] = 3

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str

```
```python
import numpy as np
from typing import List, Union

"""
Transforms a sequence of 0s and 1s based on adjacency rules.
A 0 in the sequence is changed to a 3 if it is immediately preceded
by the sub-sequence [1, 1] OR immediately succeeded by the sub-sequence [1, 1].
All other elements remain unchanged. The input is expected to be a 
list or NumPy array of integers, and the output will be a NumPy array.
"""

def transform(input_sequence: Union[List[int], np.ndarray]) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of 0s and 1s.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_sequence, dtype=int)
    
    # Initialize the output array as a copy of the input
    output_array = np.copy(input_array)
    n = len(input_array)

    # Iterate through each element of the input sequence by index
    for i in range(n):
        # Check if the current element is 0
        if input_array[i] == 0:
            # Check condition 1: Preceded by [1, 1]
            # Ensure index i is at least 2 to check i-1 and i-2
            precedes_11 = False
            if i >= 2 and input_array[i-2] == 1 and input_array[i-1] == 1:
                precedes_11 = True

            # Check condition 2: Succeeded by [1, 1]
            # Ensure index i is at most n-3 to check i+1 and i+2
            succeeds_11 = False
            if i <= n - 3 and input_array[i+1] == 1 and input_array[i+2] == 1:
                succeeds_11 = True

            # If either condition is met, change the corresponding output element to 3
            if precedes_11 or succeeds_11:
                output_array[i] = 3

    # Return the modified output array
    return output_array
```
```python
import numpy as np
from typing import List, Union

"""
Transforms a sequence of 0s and 1s based on adjacency rules.
A 0 in the sequence is changed to a 3 if it is immediately preceded
by the exact sub-sequence [1, 1] (meaning the element before [1, 1] is not 1, or it's the start of the sequence) 
OR immediately succeeded by the exact sub-sequence [1, 1] (meaning the element after [1, 1] is not 1, or it's the end of the sequence).
All other elements remain unchanged.
"""

def check_preceding_pattern(arr: np.ndarray, index: int) -> bool:
    """Checks if the element at index is preceded by exactly [1, 1]."""
    # Check if there are enough preceding elements for the pattern [1, 1]
    if index < 2:
        return False
    # Check if the immediate preceding elements form the pattern [1, 1]
    if arr[index-2] == 1 and arr[index-1] == 1:
        # Check if the pattern is *exactly* [1, 1]
        # This means either we are at index 2 (no element at index-3)
        # or the element at index-3 is not 1.
        if index == 2 or arr[index-3] != 1:
            return True
    return False

def check_succeeding_pattern(arr: np.ndarray, index: int) -> bool:
    """Checks if the element at index is succeeded by exactly [1, 1]."""
    n = len(arr)
    # Check if there are enough succeeding elements for the pattern [1, 1]
    if index > n - 3:
        return False
    # Check if the immediate succeeding elements form the pattern [1, 1]
    if arr[index+1] == 1 and arr[index+2] == 1:
        # Check if the pattern is *exactly* [1, 1]
        # This means either we are at index n-3 (no element at index+3)
        # or the element at index+3 is not 1.
        if index == n - 3 or arr[index+3] != 1:
            return True
    return False

def transform(input_grid: Union[List[int], np.ndarray]) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (grid).

    Args:
        input_grid: A list or NumPy array of 0s and 1s.

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output array as a copy of the input
    output_grid = np.copy(input_array)
    n = len(input_array)

    # Iterate through each element of the input sequence by index
    for i in range(n):
        # Check if the current element is 0
        if input_array[i] == 0:
            # Check if it meets the preceding condition
            preceded = check_preceding_pattern(input_array, i)
            # Check if it meets the succeeding condition
            succeeded = check_succeeding_pattern(input_array, i)
            
            # If either condition is met, change the corresponding output element to 3
            if preceded or succeeded:
                output_grid[i] = 3

    # Return the modified output array
    return output_grid

```
