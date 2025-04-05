## Perception of Elements

The task involves transforming a sequence of single digits (represented as space-separated integers) into another sequence of the same length. The core transformation appears to involve identifying contiguous blocks of non-zero digits within the input sequence and rearranging these blocks in the output sequence based on specific criteria, padding with zeroes to maintain the original length.

1.  **Input/Output Format:** Both input and output are sequences of integers of a fixed length (12 in all examples).
2.  **Zeroes and Non-Zeroes:** The digit '0' acts as a separator or background, while non-zero digits form meaningful blocks.
3.  **Block Identification:** Contiguous sequences of non-zero digits in the input seem to be treated as distinct units or "blocks".
4.  **Rearrangement:** These blocks are rearranged in the output. The original relative order of digits *within* a block is preserved.
5.  **Sorting Criterion:** The rearrangement of blocks appears to follow a sorting rule. Observing the examples suggests blocks are sorted primarily by their length in descending order. Ties in length seem to be broken by the original starting index of the block in ascending order.
6.  **Output Construction:** The output sequence starts with a number of leading zeroes, followed by the sorted blocks. Each block is separated from the next by a single zero. The total length of the sequence remains constant.
7.  **Padding:** The number of leading zeroes is determined by the total length of the sequence minus the sum of the lengths of all blocks and the number of separating zeroes required between blocks.

## Facts


```yaml
task_type: sequence_transformation
input_type: sequence
  element_type: integer
  separator: space
  length: fixed (e.g., 12)
output_type: sequence
  element_type: integer
  separator: space
  length: fixed (same as input)

components:
  - object: input_sequence
    properties:
      - elements: list of integers
      - length: integer
  - object: output_sequence
    properties:
      - elements: list of integers
      - length: integer (equals input_sequence length)
  - object: block
    properties:
      - elements: list of non-zero integers (contiguous in input)
      - length: integer (number of elements)
      - start_index: integer (position of the first element in the input_sequence)

actions:
  - name: identify_blocks
    input: input_sequence
    output: list of blocks (each with elements, length, start_index)
    description: Scan the input sequence to find all contiguous sub-sequences composed entirely of non-zero digits.
  - name: sort_blocks
    input: list of blocks
    output: sorted list of blocks
    description: Sort the identified blocks first by length in descending order, then by their original start_index in ascending order to break ties.
  - name: construct_output
    input:
      - sorted list of blocks
      - original_sequence_length
    output: output_sequence
    description: >
      Calculate the required number of leading zeroes based on the total length,
      the sum of block lengths, and the number of blocks (to account for separators).
      Create the output sequence by starting with the leading zeroes, then appending
      the sorted blocks, placing a single zero separator between consecutive blocks.

relationships:
  - The output sequence length must equal the input sequence length.
  - The non-zero elements in the output sequence are exactly the non-zero elements from the input sequence, potentially rearranged.
  - The order of blocks in the output depends on the sorting criteria (length desc, index asc).
  - The number of leading zeroes depends on the total length and the space occupied by the sorted blocks and their separators.
```


## Natural Language Program

1.  Parse the input string into a list of integers (the `input_sequence`). Record its `length`.
2.  Initialize an empty list called `blocks`. Iterate through the `input_sequence` to identify contiguous blocks of non-zero numbers. For each block found, store its sequence of digits, its length, and its starting index in the `input_sequence`. Add this block information to the `blocks` list.
3.  Sort the `blocks` list. The primary sorting key is the block length (descending order). The secondary sorting key (for tie-breaking) is the block's original starting index (ascending order). Store the result as `sorted_blocks`.
4.  Calculate the total number of non-zero elements (`N`) by summing the lengths of all blocks in `sorted_blocks`.
5.  Calculate the number of blocks (`k`) which is the count of blocks in `sorted_blocks`.
6.  Calculate the number of separating zeroes required between blocks (`num_separators`). This is `k - 1` if `k > 0`, otherwise it is `0`.
7.  Calculate the number of leading zeroes (`num_leading_zeros`) needed for the output sequence. This is `length - N - num_separators`.
8.  Initialize the `output_sequence` as a list containing `num_leading_zeros` zeroes.
9.  Iterate through the `sorted_blocks`. For each `block`:
    a.  Append the elements of the `block` to the `output_sequence`.
    b.  If this is not the last block in `sorted_blocks`, append a single zero to the `output_sequence` as a separator.
10. Convert the `output_sequence` (list of integers) back into a space-separated string.