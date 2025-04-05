
## train_1

**input:**
```
0 0 5 5 0 5 5 0 0 0 8 6
```


**output:**
```
0 0 8 8 0 6 6 0 0 0 8 6
```


## train_2

**input:**
```
0 5 5 5 0 5 5 5 0 0 3 4
```


**output:**
```
0 3 3 3 0 4 4 4 0 0 3 4
```


## train_3

**input:**
```
5 5 5 0 5 5 5 0 0 0 5 9
```


**output:**
```
5 5 5 0 9 9 9 0 0 0 5 9
```


## train_4

**input:**
```
5 5 5 0 0 5 5 5 0 0 8 7
```


**output:**
```
8 8 8 0 0 7 7 7 0 0 8 7
```


## train_5

**input:**
```
0 5 5 0 5 5 0 0 0 0 9 6
```


**output:**
```
0 9 9 0 6 6 0 0 0 0 9 6
```


## train_6

**input:**
```
5 5 5 0 0 5 5 5 0 0 8 4
```


**output:**
```
8 8 8 0 0 4 4 4 0 0 8 4
```


## train_7

**input:**
```
5 5 5 5 0 0 0 0 0 0 0 5
```


**output:**
```
5 5 5 5 0 0 0 0 0 0 0 5
```

*   **Perception of Task Elements:**
    *   The input and output are sequences of 12 single-digit integers, represented as space-separated strings.
    *   The core task involves selectively replacing occurrences of the digit `5` within the first 10 positions of the sequence.
    *   The digits `0` act as a background or neutral value, remaining unchanged in the output.
    *   The last two digits of the input sequence (at indices 10 and 11) serve as parameters that determine the replacement values. Let's call them `param1` and `param2`, respectively. These parameters are also copied directly to the last two positions of the output.
    *   The replacement logic depends on how the `5`s are grouped or clustered within the first 10 positions. Specifically, it depends on identifying connected components (or "blobs") of adjacent `5`s.
    *   If there are exactly two distinct components of `5`s, the `5`s in the first component (based on starting index) are replaced by `param1`, and the `5`s in the second component are replaced by `param2`.
    *   If there is only one component of `5`s, or no `5`s at all, no replacement occurs in the first 10 positions; the original digits (including the `5`s) are retained.

*   **YAML Facts:**
    
```yaml
    task_description: Replace specific digits in a sequence based on parameters and spatial grouping.
    input_format: A string of 12 space-separated single-digit integers.
    output_format: A string of 12 space-separated single-digit integers.
    objects:
      - name: sequence
        type: list of 12 integers
        description: Represents both input and output data structure.
      - name: data_segment
        type: list of 10 integers
        description: The first 10 elements of the sequence (indices 0-9) where transformations occur.
      - name: parameters
        type: list of 2 integers
        description: The last 2 elements of the input sequence (indices 10, 11).
        properties:
          - param1: integer at index 10
          - param2: integer at index 11
      - name: target_value
        type: integer
        value: 5
        description: The specific digit within the data_segment that is subject to replacement.
      - name: background_value
        type: integer
        value: 0
        description: A digit that is ignored during replacement and copied directly to the output.
      - name: component
        type: set of indices
        description: A set of adjacent indices in the data_segment where the value is the target_value (5). Adjacency is defined horizontally (index i and i+1).
    actions:
      - name: parse_input
        description: Convert input string to a list of integers.
      - name: identify_parameters
        description: Extract param1 and param2 from the input list.
      - name: identify_components
        description: Find all connected components of target_value (5) within the data_segment (first 10 elements).
      - name: count_components
        description: Determine the number of identified components.
      - name: replace_values
        description: Modify a copy of the input sequence based on the number of components and parameter values.
      - name: format_output
        description: Convert the final list of integers back to a space-separated string.
    relationships:
      - The output sequence is derived from the input sequence.
      - The values used for replacement (param1, param2) come from the input sequence.
      - The replacement action is conditional on the number of components identified (must be exactly 2 for replacement to occur).
      - If replacement occurs, param1 replaces the first component's values, and param2 replaces the second component's values.
      - background_value (0) and parameter values are always preserved in their respective output positions.
      - If only one component exists, its values (target_value 5) are preserved.
    ```


*   **Natural Language Program:**
    1.  Read the input string and convert it into a list of 12 integers.
    2.  Identify the first parameter (`param1`) as the integer at index 10 and the second parameter (`param2`) as the integer at index 11.
    3.  Create a working copy of the input list to serve as the initial output list.
    4.  Examine the first 10 elements (indices 0 through 9) of the list. Find all groups of connected `5`s, where connection means being horizontally adjacent (e.g., `5` at index `i` is connected to `5` at index `i+1`). Each such group is a "component".
    5.  Count how many distinct components of `5`s were found.
    6.  If exactly two components were found:
        a.  Identify the component that starts at the lower index (the "first" component).
        b.  Identify the component that starts at the higher index (the "second" component).
        c.  For each index within the first component, change the value in the output list at that index to `param1`.
        d.  For each index within the second component, change the value in the output list at that index to `param2`.
    7.  If the number of components found was not exactly two (i.e., zero or one), do not make any changes to the first 10 elements of the output list (they remain as they were in the input).
    8.  Ensure the last two elements (indices 10 and 11) of the output list are `param1` and `param2` (they should already be, due to copying the input initially).
    9.  Convert the final output list back into a string of space-separated integers.
```python
import re
from typing import List, Tuple

"""
Transforms a sequence of 12 integers based on the following rules:
1.  Parses the input string into a list of 12 integers.
2.  Identifies the last two integers as parameters: param1 (at index 10) and param2 (at index 11).
3.  Examines the first 10 integers (indices 0-9) to find connected components (adjacent sequences) of the digit 5.
4.  If exactly two such components of 5s are found:
    a.  Replace all 5s in the first component (the one starting at the lower index) with param1.
    b.  Replace all 5s in the second component with param2.
5.  If the number of components of 5s is not exactly two (i.e., zero or one), the first 10 integers remain unchanged.
6.  The last two integers in the output are always param1 and param2.
7.  Formats the resulting list of integers back into a space-separated string.
"""

def _parse_input(input_str: str) -> List[int]:
    """Converts the input string to a list of integers."""
    return [int(x) for x in input_str.split()]

def _find_components(data_segment: List[int], target_value: int) -> List[List[int]]:
    """Finds connected components of target_value in the data segment."""
    components = []
    current_component = []
    for i, val in enumerate(data_segment):
        if val == target_value:
            # If the current value is the target, add its index to the current component
            current_component.append(i)
        else:
            # If the current value is not the target and we were building a component, finalize it
            if current_component:
                components.append(current_component)
                current_component = []
    # Add the last component if the sequence ended with the target value
    if current_component:
        components.append(current_component)
    return components

def _format_output(output_list: List[int]) -> str:
    """Converts the output list back to a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string of 12 space-separated single-digit integers.

    Returns:
        A string of 12 space-separated single-digit integers after applying the transformation.
    """
    # 1. Parse the input string into a list of 12 integers.
    input_list = _parse_input(input_str)
    if len(input_list) != 12:
        raise ValueError("Input must contain exactly 12 integers.")

    # 2. Identify the parameters (last two elements).
    param1 = input_list[10]
    param2 = input_list[11]

    # Create a working copy for the output
    output_list = list(input_list)

    # 3. Examine the first 10 elements (data segment) to find components of 5s.
    data_segment = input_list[:10]
    target_value = 5
    components = _find_components(data_segment, target_value)

    # 4. Count components and apply replacement logic if exactly two are found.
    if len(components) == 2:
        # 4.a. Identify the first and second components (already sorted by starting index)
        first_component_indices = components[0]
        second_component_indices = components[1]

        # 4.b. Replace 5s in the first component with param1
        for index in first_component_indices:
            output_list[index] = param1

        # 4.c. Replace 5s in the second component with param2
        for index in second_component_indices:
            output_list[index] = param2

    # 5. If not exactly two components, the first 10 elements remain unchanged (already copied).

    # 6. Ensure the last two elements are param1 and param2 (already copied).
    #    output_list[10] = param1
    #    output_list[11] = param2
    #    (This step is implicitly handled by copying the input initially)

    # 7. Format the resulting list back into a space-separated string.
    return _format_output(output_list)

```
```python
import copy
from typing import List, Union
import numpy as np # Assuming input might be numpy array based on previous error

"""
Transforms a sequence of 12 integers based on the following rules:
1.  Accepts the input as a list or array of 12 integers.
2.  Identifies the last two integers as parameters: param1 (at index 10) and param2 (at index 11).
3.  Examines the first 10 integers (indices 0-9, the "data segment") to find connected components (adjacent sequences) of the digit 5.
4.  If exactly two such components of 5s are found:
    a.  Replace all 5s in the first component (the one starting at the lower index) with param1.
    b.  Replace all 5s in the second component with param2.
5.  If the number of components of 5s is not exactly two (i.e., zero or one), the first 10 integers remain unchanged.
6.  The last two integers in the output are always param1 and param2.
7.  Returns the resulting sequence as a list or array of 12 integers.
"""


def _find_components(data_segment: List[int], target_value: int) -> List[List[int]]:
    """
    Finds connected components (sequences of adjacent indices) where the value
    matches target_value within the data segment.

    Args:
        data_segment: The list of integers to search within (first 10 elements).
        target_value: The integer value defining the components (e.g., 5).

    Returns:
        A list of components, where each component is a list of indices.
        Returns an empty list if no components are found.
    """
    components = []
    current_component = []
    for i, val in enumerate(data_segment):
        if val == target_value:
            # If the current value is the target, add its index to the current component
            current_component.append(i)
        else:
            # If the current value is not the target and we were building a component, finalize it
            if current_component:
                components.append(current_component)
                current_component = []
    # Add the last component if the sequence ended with the target value
    if current_component:
        components.append(current_component)
    return components

def transform(input_sequence: Union[List[int], np.ndarray]) -> Union[List[int], np.ndarray]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of 12 integers.

    Returns:
        A list or NumPy array (matching input type) of 12 integers after
        applying the transformation.
    """
    # Ensure input is a list for consistent processing
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
        is_numpy = True
    else:
        input_list = list(input_sequence) # Make a copy if it's already a list
        is_numpy = False

    if len(input_list) != 12:
        raise ValueError("Input sequence must contain exactly 12 integers.")

    # 1. Identify the parameters (last two elements).
    param1 = input_list[10]
    param2 = input_list[11]

    # 2. Create a working copy for the output.
    # Use deepcopy if elements could be mutable, though ints are not. Simple list copy is fine here.
    output_list = list(input_list)

    # 3. Examine the first 10 elements (data segment) to find components of 5s.
    data_segment = input_list[:10]
    target_value = 5
    components = _find_components(data_segment, target_value)

    # 4. Count components and apply replacement logic if exactly two are found.
    if len(components) == 2:
        # 4.a. Identify the first and second components (sorted by starting index by _find_components).
        first_component_indices = components[0]
        second_component_indices = components[1]

        # 4.b. Replace 5s in the first component with param1.
        for index in first_component_indices:
            output_list[index] = param1

        # 4.c. Replace 5s in the second component with param2.
        for index in second_component_indices:
            output_list[index] = param2

    # 5. If not exactly two components, the first 10 elements remain unchanged (already copied).

    # 6. The last two elements remain param1 and param2 (already copied).

    # 7. Return the final sequence, converting back to numpy array if necessary.
    if is_numpy:
        return np.array(output_list, dtype=input_sequence.dtype) # Preserve original dtype
    else:
        return output_list
```
