## Perception of Task Elements

The task operates on sequences of integers. Each input sequence contains exactly two identical non-zero integers, with all other elements being zero. The transformation rule involves filling the segment of the sequence between these two non-zero integers (inclusive) with the same non-zero integer value. Elements outside this segment remain unchanged (typically zero).

## Factual Documentation


```yaml
objects:
  - name: input_sequence
    type: list_of_integers
    description: The input data structure, primarily containing zeros and exactly two identical non-zero values.
  - name: output_sequence
    type: list_of_integers
    description: The transformed sequence, derived from the input sequence. It has the same length as the input.
  - name: non_zero_value
    type: integer
    description: The unique positive integer value present twice in the input sequence.
  - name: zero_value
    type: integer
    value: 0
    description: The background or placeholder value in the sequence.
  - name: start_index
    type: integer
    description: The index of the first occurrence of the non_zero_value in the input_sequence.
  - name: end_index
    type: integer
    description: The index of the second occurrence of the non_zero_value in the input_sequence.
  - name: fill_segment
    type: range_of_indices
    description: The continuous range of indices from start_index to end_index (inclusive).

actions:
  - name: identify_non_zero_value
    input: input_sequence
    output: non_zero_value
    description: Find the value that is not zero in the input sequence.
  - name: find_indices
    input: input_sequence, non_zero_value
    output: [start_index, end_index]
    description: Locate the first and second indices where the non_zero_value appears.
  - name: fill_segment_with_value
    input: output_sequence (initially a copy of input), fill_segment, non_zero_value
    output: modified_output_sequence
    description: Modify the output sequence by setting all elements within the fill_segment to the non_zero_value.

relationships:
  - type: definition
    from: fill_segment
    to: [start_index, end_index]
    description: The fill_segment is defined by the start_index and end_index of the non_zero_value.
  - type: determination
    from: non_zero_value
    to: fill_segment
    description: The value of the non_zero_value determines the value used to fill the segment in the output_sequence.
  - type: identity (initial)
    from: output_sequence
    to: input_sequence
    description: The output_sequence initially starts as a copy of the input_sequence before modification.
  - type: modification
    action: fill_segment_with_value
    target: output_sequence
    description: The fill action modifies the output_sequence within the defined segment.
```


## Natural Language Program

1.  Receive the input sequence of integers.
2.  Identify the unique non-zero integer value present in the input sequence.
3.  Find the index of the first occurrence of this non-zero value (`start_index`).
4.  Find the index of the second (and last) occurrence of this non-zero value (`end_index`).
5.  Create a new sequence which is initially an identical copy of the input sequence.
6.  Iterate through the indices from `start_index` to `end_index`, inclusive.
7.  For each index within this range, set the corresponding element in the new sequence to the identified non-zero value.
8.  Return the modified sequence as the output.