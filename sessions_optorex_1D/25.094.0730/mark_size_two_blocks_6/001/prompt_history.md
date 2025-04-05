
## train_1

**input:**
```
0 0 0 1 1 0 0 0 0 0 1 0
```


**output:**
```
0 0 3 1 1 3 0 0 0 0 1 0
```


## train_2

**input:**
```
1 1 0 0 0 0 0 0 0 1 0 0
```


**output:**
```
1 1 3 0 0 0 0 0 0 1 0 0
```


## train_3

**input:**
```
0 0 1 1 0 0 0 0 0 0 1 0
```


**output:**
```
0 3 1 1 3 0 0 0 0 0 1 0
```


## train_4

**input:**
```
1 0 0 0 0 0 0 0 0 0 1 0
```


**output:**
```
1 0 0 0 0 0 0 0 0 0 1 0
```


## train_5

**input:**
```
0 0 1 0 0 0 0 1 1 1 0 0
```


**output:**
```
0 0 1 0 0 0 0 1 1 1 0 0
```


## train_6

**input:**
```
1 0 0 0 0 0 1 0 0 0 0 0
```


**output:**
```
1 0 0 0 0 0 1 0 0 0 0 0
```


## train_7

**input:**
```
0 1 0 0 0 1 1 0 0 0 0 0
```


**output:**
```
0 1 0 0 3 1 1 3 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are both lists of single-digit integers.
    *   Input lists contain only 0s and 1s.
    *   Output lists can contain 0s, 1s, and 3s.
    *   The length of the input and output list is always the same for a given example.
    *   The transformation involves selectively changing some 0s in the input list to 3s in the output list.
    *   The change seems related to the presence of adjacent `1`s. Specifically, a pattern of exactly two consecutive `1`s (`1 1`) triggers the change.
    *   The 0s that change to 3s are those immediately preceding or immediately following such a `1 1` block.
    *   If a `1` is part of a longer sequence of `1`s (e.g., `1 1 1`), it does not trigger the change in adjacent 0s.
    *   If a `0` is adjacent to two separate `1 1` blocks, it doesn't seem to happen in the examples, but the rule implies it would still change to 3. (e.g., `1 1 0 1 1` -> `1 1 3 1 1`)

*   **YAML Facts:**
    
```yaml
    task_description: "Modify a sequence of 0s and 1s based on patterns of adjacent 1s."
    elements:
      - type: sequence
        name: input_list
        contains:
          - type: integer
            possible_values: [0, 1]
      - type: sequence
        name: output_list
        contains:
          - type: integer
            possible_values: [0, 1, 3]
        relationship: "Derived from input_list by conditional modification."
    objects:
      - name: digit_zero
        value: 0
        property: "Can be changed to 3 under specific conditions."
      - name: digit_one
        value: 1
        property: "Contributes to forming the trigger pattern."
      - name: digit_three
        value: 3
        property: "Result of transforming a specific digit_zero."
      - name: block_one_one
        value: "[1, 1]"
        property: "A sequence of exactly two consecutive 1s."
        relationship: "Triggers the transformation of adjacent 0s."
    actions:
      - name: identify_blocks
        input: input_list
        output: indices of all block_one_one instances
        condition: "The block must be exactly two 1s long (not preceded or followed by another 1)."
      - name: modify_neighbors
        input: input_list, indices of block_one_one
        output: modified_list (intermediate state)
        effect: "For each identified block_one_one at index i, i+1: if input_list[i-1] is 0, change it to 3 in the output; if input_list[i+2] is 0, change it to 3 in the output. Handle boundary conditions."
    relationships:
      - type: adjacency
        description: "A digit_zero is considered adjacent if it is immediately before the start or immediately after the end of a block_one_one."
      - type: transformation_trigger
        subject: block_one_one
        object: adjacent digit_zero
        action: change value to 3
    constraints:
      - "The length of the input and output sequences must be identical."
      - "Only 0s adjacent to a block of *exactly* two 1s are modified."
      - "1s and 0s not meeting the criteria remain unchanged."

    ```


*   **Natural Language Program:**
    1.  Initialize the output list as a copy of the input list.
    2.  Iterate through the input list from the first element up to the second-to-last element, examining each element and the one immediately following it. Let the current index be `i`.
    3.  Check if the element at index `i` is 1 and the element at index `i+1` is also 1.
    4.  If they are both 1, verify that this is a block of *exactly* two 1s:
        *   Check that the element *before* index `i` (if it exists, i.e., `i > 0`) is not 1.
        *   Check that the element *after* index `i+1` (if it exists, i.e., `i+1 < length - 1`) is not 1.
    5.  If both conditions in step 4 are met (it's exactly a `1 1` block):
        *   Check the element immediately *before* the block (at index `i-1`): If this element exists (`i > 0`) and its value in the *input* list is 0, change the corresponding element at index `i-1` in the *output* list to 3.
        *   Check the element immediately *after* the block (at index `i+2`): If this element exists (`i+1 < length - 1`) and its value in the *input* list is 0, change the corresponding element at index `i+2` in the *output* list to 3.
    6.  After iterating through all possible starting positions `i`, the final output list contains the transformed sequence.
