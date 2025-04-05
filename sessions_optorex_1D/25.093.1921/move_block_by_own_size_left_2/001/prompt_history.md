
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 5 5 5
```


**output:**
```
0 0 0 0 0 0 5 5 5 0 0 0
```


## train_2

**input:**
```
0 0 7 7 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 4 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 6 6 6 6 0 0 0 0
```


**output:**
```
6 6 6 6 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 2 2 2
```


**output:**
```
0 0 0 0 0 0 2 2 2 0 0 0
```


## train_6

**input:**
```
0 0 0 1 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 1 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 2 2 2 0 0 0
```


**output:**
```
0 0 0 2 2 2 0 0 0 0 0 0
```

*   **Perception:** The task involves processing a one-dimensional sequence of 12 digits. Each input sequence contains a single contiguous block of identical non-zero digits, surrounded by zeros ('0'). The transformation shifts this block of non-zero digits to the left. The amount of the shift appears to be determined by the length of the non-zero block itself. The rest of the sequence remains filled with zeros.

*   **Facts:**
    
```yaml
    task_type: sequence transformation
    input_format: list of 12 integers (space-separated string)
    output_format: list of 12 integers (space-separated string)
    background_element: 0
    objects:
      - name: sequence
        properties:
          - length: 12
          - elements: integers (0-9)
      - name: non_zero_block
        properties:
          - contiguity: true
          - elements: identical non-zero integers
          - length: variable (depends on input)
          - start_index: variable (depends on input)
    action:
      - name: identify_block
        inputs: input_sequence
        outputs: non_zero_block, start_index, length
      - name: calculate_shift
        inputs: length
        outputs: shift_amount (equals length)
      - name: calculate_new_index
        inputs: start_index, shift_amount
        outputs: new_start_index (start_index - shift_amount)
      - name: construct_output
        inputs: non_zero_block, new_start_index, sequence_length, background_element
        outputs: output_sequence
    relationships:
      - The shift amount is equal to the length of the non_zero_block.
      - The non_zero_block is moved leftwards by the shift amount.
      - Positions not occupied by the shifted block in the output are filled with the background_element (0).
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of 12 integers.
    2.  Identify the contiguous block of non-zero integers within the input list. Determine its starting index and its length.
    3.  Calculate the new starting index for the block by subtracting the block's length from its original starting index.
    4.  Create a new list of 12 integers, initialized with zeros.
    5.  Place the identified non-zero block into the new list, starting at the calculated new starting index.
    6.  Format the new list back into a space-separated string for the output.
