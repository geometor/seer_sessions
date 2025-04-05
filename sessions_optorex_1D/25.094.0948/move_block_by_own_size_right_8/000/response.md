## Perception of Task Elements

The task involves transforming a sequence of 12 digits. Each input sequence contains a single contiguous block of identical non-zero digits, surrounded by zeros. The output sequence consists of the same block of non-zero digits, shifted to the right within the sequence, with the remaining positions filled with zeros. The amount of the rightward shift is equal to the length of the non-zero block.

## Task Facts


```yaml
task_elements:
  - type: sequence
    description: Input is a sequence of 12 digits.
    properties:
      length: 12
      composition: Contains zeros and a single contiguous block of identical non-zero digits.
  - type: block
    description: A contiguous sub-sequence of identical non-zero digits within the input sequence.
    properties:
      - digit_value: The non-zero digit repeated in the block (e.g., 1, 9, 4, 7, 3).
      - length: The number of digits in the block.
      - start_index: The position (0-based index) where the block begins in the input sequence.
  - type: transformation
    description: The process applied to the input sequence to produce the output sequence.
    action:
      - identify: Locate the non-zero block in the input sequence.
      - measure: Determine the length of the identified block.
      - shift: Move the block to the right within the sequence.
      - fill: Place zeros in all positions not occupied by the shifted block.
    relationship:
      - The shift distance is equal to the length of the non-zero block.
  - type: sequence
    description: Output is a sequence of 12 digits.
    properties:
      length: 12
      composition: Contains zeros and the same non-zero block from the input, shifted rightward.
      - shifted_start_index: The new starting position of the block (original start_index + block length).
```


## Natural Language Program

1.  Receive the input sequence of 12 digits.
2.  Initialize an output sequence of 12 zeros.
3.  Iterate through the input sequence to find the first non-zero digit. Record its value (`digit_value`) and its index (`start_index`).
4.  Continue iterating from `start_index` to find the end of the contiguous block of `digit_value`. Calculate the length of this block (`block_length`).
5.  Calculate the new starting index for the block in the output sequence: `new_start_index = start_index + block_length`.
6.  Place the block of `digit_value` with length `block_length` into the output sequence, starting at `new_start_index`.
7.  Return the modified output sequence.