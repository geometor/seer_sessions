## Perception

The input is a sequence of 12 single-digit numbers. The output is also a sequence of 12 single-digit numbers, containing the same digits as the input but in a different order. The transformation appears to be a structural rearrangement of the sequence. Specifically, the sequence is divided into two segments, and these segments are swapped in the output. The first segment consists of the first 8 numbers, and the second segment consists of the last 4 numbers.

## Facts


```yaml
task_description: Rearrange a sequence of 12 digits by swapping two segments.
objects:
  - name: input_sequence
    type: list of integers
    properties:
      - length: 12
  - name: output_sequence
    type: list of integers
    properties:
      - length: 12
  - name: segment_1
    type: sublist of input_sequence
    properties:
      - location: first 8 elements
      - length: 8
  - name: segment_2
    type: sublist of input_sequence
    properties:
      - location: last 4 elements
      - length: 4
actions:
  - name: split
    input: input_sequence
    parameters:
      - split_point: after the 8th element
    output:
      - segment_1
      - segment_2
  - name: concatenate
    input:
      - segment_2
      - segment_1
    output: output_sequence
relationships:
  - type: order_swap
    object_1: segment_1
    object_2: segment_2
    description: In the output sequence, segment_2 appears before segment_1.
```


## Natural Language Program

1.  Read the input sequence of 12 digits.
2.  Identify the first segment consisting of the first 8 digits.
3.  Identify the second segment consisting of the last 4 digits.
4.  Construct the output sequence by concatenating the second segment followed by the first segment.
5.  Output the resulting sequence.