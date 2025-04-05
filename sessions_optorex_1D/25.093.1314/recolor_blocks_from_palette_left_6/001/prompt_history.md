
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
