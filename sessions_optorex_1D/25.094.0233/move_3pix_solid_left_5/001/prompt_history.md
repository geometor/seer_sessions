
## train_1

**input:**
```
0 0 0 0 0 0 9 9 9 9 0 0
```


**output:**
```
0 0 0 9 9 9 9 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 9 9 9 9 9 9 9
```


**output:**
```
0 0 9 9 9 9 9 9 9 0 0 0
```


## train_3

**input:**
```
0 0 0 4 4 4 4 4 4 4 4 0
```


**output:**
```
4 4 4 4 4 4 4 4 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 9 9 9 9
```


**output:**
```
0 0 0 0 0 9 9 9 9 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 9 9 9 9 9 0
```


**output:**
```
0 0 0 9 9 9 9 9 0 0 0 0
```


## train_6

**input:**
```
0 0 0 6 6 6 6 0 0 0 0 0
```


**output:**
```
6 6 6 6 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 4 4 4 4 4 4 4 0
```


**output:**
```
0 4 4 4 4 4 4 4 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are sequences (lists or arrays) of single digits.
    *   Each sequence contains primarily zeros ('0') and a single contiguous block of identical non-zero digits (e.g., '9', '4', '6').
    *   The length of the input sequence is preserved in the output sequence.
    *   The specific non-zero digit and the count of its occurrences (length of the block) remain unchanged between input and output.
    *   The core transformation involves changing the position of the non-zero block within the sequence.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: sequence
        description: A list of single digits.
        properties:
          - length: Fixed for input and output in each pair.
          - elements: Consist of '0' and one type of non-zero digit.
      - object: non_zero_block
        description: A contiguous subsequence of identical non-zero digits within the main sequence.
        properties:
          - digit_value: The specific non-zero digit (e.g., 9, 4, 6).
          - length: The number of times the non-zero digit repeats consecutively.
          - start_index_input: The starting position (0-based index) of the block in the input sequence.
          - start_index_output: The starting position (0-based index) of the block in the output sequence.
        relationships:
          - contained_within: sequence
    actions:
      - action: shift_left
        actor: non_zero_block
        details: The block's position is moved 3 indices towards the beginning of the sequence.
        constraints:
          - The shift amount is constant (3 positions).
          - The sequence composition (digit value, block length, number of zeros) is preserved.
          - If the calculated start index is less than 0, it defaults to 0.
    relationships:
      - type: transformation
        input: input_sequence
        output: output_sequence
        rule: The non_zero_block found in the input_sequence is shifted 3 positions to the left to produce the output_sequence.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of integers.
    2.  Identify the contiguous block of non-zero digits. Determine its value, its length, and its starting index in the input list.
    3.  Calculate the target starting index for the block in the output list by subtracting 3 from the input starting index. If the result is negative, use 0 as the target starting index.
    4.  Create a new list of the same length as the input list, initialized with zeros.
    5.  Place the identified block of non-zero digits into the new list, starting at the calculated target starting index.
    6.  Format the resulting list back into a space-separated string of digits for the output.
