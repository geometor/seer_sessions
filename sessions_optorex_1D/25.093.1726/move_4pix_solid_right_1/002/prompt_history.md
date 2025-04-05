
## train_1

**input:**
```
0 0 0 0 0 0 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 8 0
```


## train_2

**input:**
```
0 0 9 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 9 0 0 0 0 0
```


## train_3

**input:**
```
2 2 2 2 2 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 0 0
```


## train_4

**input:**
```
0 0 0 0 2 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 3 0
```


## train_6

**input:**
```
0 0 0 0 0 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 7 0 0
```


## train_7

**input:**
```
0 0 3 3 3 3 3 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 3 3 3 3 3
```

**Perception of Task Elements:**

The task operates on one-dimensional sequences (arrays or lists) of integers. The key elements are:

1.  **Sequence:** A fixed-length list of integers (length 12 in all examples).
2.  **Objects:** Non-zero integer values within the sequence. These can be single elements or contiguous blocks of the same non-zero value.
3.  **Empty Space:** Zero values within the sequence, representing unoccupied positions.
4.  **Transformation:** A spatial shift applied to the objects within the sequence.

The core operation is the displacement of all non-zero elements (objects) within the sequence by a fixed amount, while maintaining their relative order and values. The vacated positions are filled with zeros.

**YAML Facts:**


```yaml
task_elements:
  - type: sequence
    properties:
      - name: structure
        value: 1D array/list of integers
      - name: length
        value: 12 (constant across examples)
      - name: element_types
        values: [integer]
  - type: object
    properties:
      - name: representation
        value: non-zero integer values
      - name: characteristic
        value: can be single or contiguous blocks
      - name: state
        value: position (index) within the sequence
  - type: empty_space
    properties:
      - name: representation
        value: zero integer value
      - name: state
        value: position (index) within the sequence
relationships:
  - type: relative_position
    between: [object, object]
    characteristic: maintained during transformation
actions:
  - type: shift
    target: object(s)
    properties:
      - name: direction
        value: right (increasing index)
      - name: distance
        value: 4 positions
      - name: effect
        value: changes position state of objects, fills original positions with empty_space
```


**Natural Language Program:**

1.  Identify all non-zero elements (objects) and their indices in the input sequence.
2.  Create a new output sequence of the same length as the input sequence, initially filled with zeros (empty space).
3.  For each identified object in the input sequence at index `i`, place that object's value into the output sequence at index `i + 4`.
4.  Ensure that the relative order of the objects is preserved in the output sequence.
5.  The resulting sequence is the final output.
```python
"""
Identifies all non-zero elements (objects) in the input sequence.
Creates a new output sequence of the same length, initially filled with zeros.
For each non-zero element found at index `i` in the input, places that element's 
value into the output sequence at index `i + 4`, provided the new index is 
within the bounds of the sequence. The relative order of non-zero elements is preserved.
"""

import numpy as np # Although not strictly necessary for this list-based approach,
                   # numpy could be useful for more complex grid manipulations.

# No specific helper functions needed for this simple shift,
# but could be added for modularity (e.g., find_objects, shift_object).

def transform(input_grid: list[int]) -> list[int]:
    """
    Shifts all non-zero elements in the input list 4 positions to the right.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A new list of integers with non-zero elements shifted 4 positions right.
    """
    # Get the length of the input grid
    grid_length = len(input_grid)

    # Initialize the output grid with zeros, having the same length as the input
    output_grid = [0] * grid_length

    # Iterate through the input grid with index and value
    for i, val in enumerate(input_grid):
        # Check if the current element is non-zero (an object)
        if val != 0:
            # Calculate the new index by adding the shift amount (4)
            new_index = i + 4
            # Check if the new index is within the bounds of the grid
            if 0 <= new_index < grid_length:
                # Place the non-zero value at the new position in the output grid
                output_grid[new_index] = val

    # Return the transformed grid
    return output_grid

```
