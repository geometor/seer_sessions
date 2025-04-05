## Perception of Task Elements

The task involves transforming a 1D sequence of numbers. The input sequences consist of blocks of identical numbers, often separated or surrounded by zeros. The transformation primarily affects contiguous blocks of identical *non-zero* numbers. Zeros seem to act as delimiters or background elements that remain unchanged unless they are part of the modification applied to the non-zero blocks. The core operation targets the *interior* elements of these non-zero blocks, specifically when the block's length exceeds two.

## Facts


```yaml
objects:
  - name: sequence
    type: list_of_integers
    description: Represents both the input and output data structure.
  - name: element
    type: integer
    description: Individual number within the sequence. Can be 0 or non-zero.
  - name: block
    type: contiguous_subsequence
    description: A run of identical, consecutive non-zero elements within the sequence.
properties:
  - object: block
    name: value
    type: integer
    description: The non-zero integer value repeated within the block.
  - object: block
    name: length
    type: integer
    description: The number of elements in the block.
  - object: block
    name: start_index
    type: integer
    description: The index of the first element of the block in the main sequence.
  - object: block
    name: end_index
    type: integer
    description: The index of the last element of the block in the main sequence.
actions:
  - name: identify_blocks
    description: Scan the input sequence to find all contiguous blocks of identical non-zero numbers.
  - name: modify_block
    description: Change elements within an identified block based on its length.
  - name: preserve_element
    description: Keep an element unchanged if it is 0 or part of a block not meeting modification criteria.
relationships:
  - type: condition
    description: The modification applied to a block depends on its length.
    condition: block.length > 2
    action: Replace elements between the first and last element of the block with 0.
  - type: condition
    description: If a block's length is 2 or less, it remains unchanged.
    condition: block.length <= 2
    action: Preserve all elements of the block.
  - type: context
    description: Elements equal to 0 that are not part of a modified block remain unchanged.
```


## Natural Language Program

1.  Initialize an output sequence identical to the input sequence.
2.  Iterate through the input sequence to identify contiguous blocks of identical non-zero numbers. For each block, record its value, start index, and end index.
3.  For each identified block:
    a.  Calculate the length of the block (end index - start index + 1).
    b.  If the length of the block is greater than 2:
        i.  Iterate from the element *after* the first element (index: start index + 1) up to the element *before* the last element (index: end index - 1).
        ii. Set the value of each element within this range in the *output* sequence to 0.
4.  Return the modified output sequence. Elements not part of a block longer than 2 (i.e., zeros or elements in blocks of length 1 or 2) remain unchanged from the input.