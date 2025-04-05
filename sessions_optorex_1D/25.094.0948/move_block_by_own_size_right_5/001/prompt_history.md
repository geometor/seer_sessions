
## train_1

**input:**
```
0 0 9 9 9 9 9 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 9 9 9 9
```


## train_2

**input:**
```
0 7 7 7 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 8 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 0
```


## train_4

**input:**
```
9 9 9 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 9 9 9 9 0 0 0 0
```


## train_5

**input:**
```
1 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 1 0 0 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 4 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 0 0 0 0 0 0
```


## train_7

**input:**
```
2 2 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 2 2 0 0 0 0 0 0 0 0
```

*   **Perception:** The input and output are sequences of digits, represented as space-separated strings. Each input sequence contains exactly one contiguous block of identical non-zero digits, surrounded by zeros. The output sequence also contains the same block of non-zero digits, shifted to the right, and surrounded by zeros. The amount of the rightward shift appears to be equal to the length of the non-zero block itself. The overall length of the sequence remains constant.

*   **Facts:**
    
```yaml
    task_elements:
      - object: sequence
        description: A sequence of digits of fixed length (12 in examples).
        properties:
          - length: Integer (e.g., 12)
          - elements: Digits (0-9)
      - object: block
        description: A contiguous sub-sequence within the main sequence.
        properties:
          - type: non_zero_block
            description: Consists of identical digits greater than 0.
            constraints: Exactly one such block exists in the input.
            attributes:
              - value: The non-zero digit (e.g., 9, 7, 8, 1, 4, 2)
              - length: The number of digits in the block (Integer > 0)
              - start_index: The 0-based index where the block begins in the input sequence.
          - type: zero_block
            description: Consists of the digit 0. Fills the space around the non_zero_block.
      - object: input_sequence
        description: The initial sequence containing one non_zero_block.
      - object: output_sequence
        description: The resulting sequence after transformation.
        properties:
          - same length as input_sequence
          - contains the identical non_zero_block from the input, but shifted.
          - filled with zeros elsewhere.
    actions:
      - action: identify_block
        description: Locate the non_zero_block in the input_sequence.
        inputs: input_sequence
        outputs:
          - block_value
          - block_length
          - block_start_index
      - action: calculate_shift
        description: Determine the number of positions to shift the block.
        inputs: block_length
        outputs: shift_amount (equal to block_length)
      - action: calculate_new_position
        description: Determine the new starting index for the block in the output sequence.
        inputs:
          - block_start_index
          - shift_amount
        outputs: new_start_index (block_start_index + shift_amount)
      - action: construct_output
        description: Create the output_sequence.
        steps:
          - Initialize a sequence of the same length as the input with all zeros.
          - Place the identified non_zero_block (using block_value and block_length) starting at the calculated new_start_index.
    relationships:
      - relationship: shift_equals_length
        description: The amount the non_zero_block is shifted to the right is equal to its own length.
      - relationship: block_preservation
        description: The value and length of the non_zero_block remain unchanged from input to output.
      - relationship: length_preservation
        description: The total length of the sequence remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a sequence of digits.
    2.  Identify the contiguous block of identical non-zero digits within the input sequence. Determine its value, its length, and its starting index.
    3.  Calculate the target starting index for this block in the output sequence by adding the block's length to its original starting index.
    4.  Create a new sequence of the same length as the input, initially filled entirely with zeros.
    5.  Place the identified block of non-zero digits into the new sequence, starting at the calculated target starting index.
    6.  Format the resulting sequence back into a space-separated string for the output.
