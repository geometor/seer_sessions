
## train_1

**input:**
```
0 0 0 0 0 4 8 5 0 0 0 0
```


**output:**
```
0 0 0 0 4 8 5 0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 6 1 1 4 5 9 5 8 0
```


**output:**
```
0 4 6 1 1 4 5 9 5 8 0 0
```


## train_3

**input:**
```
0 0 5 9 7 0 0 0 0 0 0 0
```


**output:**
```
0 5 9 7 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
3 7 3 9 9 2 0 0 8 9 3 2
```


**output:**
```
7 3 9 9 2 0 0 8 9 3 2 3
```


## train_5

**input:**
```
0 0 0 0 0 3 7 3 0 0 0 0
```


**output:**
```
0 0 0 0 3 7 3 0 0 0 0 0
```


## train_6

**input:**
```
5 9 8 8 0 0 0 0 0 0 0 7
```


**output:**
```
9 8 8 0 0 0 0 0 0 0 7 5
```


## train_7

**input:**
```
2 0 0 0 0 6 2 6 7 2 4 7
```


**output:**
```
0 0 0 0 6 2 6 7 2 4 7 2
```

## Perception

The input and output are both sequences of integers.
Comparing the input and output sequences, it appears that the first element of the input sequence is moved to the end of the sequence to form the output. The relative order of the remaining elements is preserved. This operation is equivalent to a single left rotation of the sequence.

## Facts


```yaml
objects:
  - type: sequence
    properties:
      - name: elements
        type: list[integer]
      - name: length
        value_description: The number of integers in the sequence.
actions:
  - name: left_rotate
    description: Moves the first element of the sequence to the end.
    input:
      - name: input_sequence
        type: sequence
    output:
      - name: output_sequence
        type: sequence
        description: The input sequence after moving the first element to the last position.
relationships:
  - type: transformation
    description: The output sequence is derived from the input sequence by performing a single left rotation.
    input: input_sequence
    output: output_sequence
    rule: Take the first element of the input sequence and append it to the end of the sequence formed by the remaining elements.
```


## Natural Language Program

1.  Receive the input sequence of integers.
2.  Identify the first integer in the sequence.
3.  Create a new sequence containing all integers from the input sequence *except* the first one, maintaining their original relative order.
4.  Append the first integer (identified in step 2) to the end of the new sequence created in step 3.
5.  Return the resulting sequence as the output.
```python
import collections

"""
Takes an input sequence of integers (represented as a space-separated string), 
moves the first integer to the end of the sequence, and returns the modified 
sequence as a space-separated string. This is equivalent to a single left rotation.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    if not input_str.strip():
        return []
    return [int(x) for x in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def left_rotate_sequence(sequence: list[int]) -> list[int]:
    """Performs a single left rotation on the list."""
    # Handle empty or single-element lists (no change)
    if len(sequence) < 2:
        return sequence
    
    # Take the first element
    first_element = sequence[0]
    # Get the rest of the sequence
    remaining_sequence = sequence[1:]
    # Append the first element to the end
    rotated_sequence = remaining_sequence + [first_element]
    return rotated_sequence

def transform(input_str: str) -> str:
    """
    Transforms the input sequence string by performing a single left rotation.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the space-separated integers after left rotation.
    """
    # Parse the input string into a list of integers
    input_sequence = parse_input(input_str)

    # Perform the left rotation
    output_sequence = left_rotate_sequence(input_sequence)

    # Format the resulting list back into a space-separated string
    output_str = format_output(output_sequence)

    return output_str

```
```python
"""
Performs a single left rotation on the input 1D NumPy array. It takes the 
first element of the array and moves it to the end, preserving the relative 
order of the other elements.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a single left rotation to the input 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the input array after moving the first 
        element to the end.
    """

    # Get the size of the input array
    size = input_grid.shape[0]

    # Handle edge cases: empty or single-element arrays need no rotation
    if size < 2:
        return input_grid.copy() # Return a copy to avoid modifying the original if needed

    # Extract the first element
    first_element = input_grid[0]

    # Extract the remaining elements (from the second element to the end)
    remaining_elements = input_grid[1:]

    # Create the output array by appending the first element to the remaining elements
    # Note: np.append creates a new array
    output_grid = np.append(remaining_elements, first_element)

    return output_grid
```
```python
"""
Applies a single left rotation to the input 1D NumPy array. It takes the 
first element of the array and moves it to the end, preserving the relative 
order of the other elements.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Performs a single left rotation on the input 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the input array after moving the first 
        element to the end.
    """

    # Get the size of the input array
    size = input_grid.shape[0]

    # Handle edge cases: empty or single-element arrays need no rotation
    # Return a copy to avoid modifying the original if needed outside the function
    if size < 2:
        return input_grid.copy() 

    # Perform a left circular shift (rotation) by 1 position
    # np.roll shifts elements along the given axis. A shift of -1 moves 
    # elements to the left, wrapping the first element around to the end.
    output_grid = np.roll(input_grid, -1)

    # Return the rotated array
    return output_grid
```
