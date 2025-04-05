## Perception of Task Elements

The input and output are both sequences of integers, separated by spaces. In all provided examples, the length of the input sequence is 12, and the length of the output sequence is also 12. The transformation rearranges the elements of the input sequence. Specifically, all the zero elements are moved to the beginning of the sequence, and all the non-zero elements are moved to the end of the sequence. Crucially, the relative order of the non-zero elements among themselves is preserved from the input to the output.

## YAML Facts


```yaml
objects:
  - name: input_sequence
    type: list of integers
  - name: output_sequence
    type: list of integers
  - name: zero_element
    type: integer
    value: 0
  - name: non_zero_element
    type: integer
    condition: value != 0
properties:
  - object: input_sequence
    property: length
    value: constant (12 in examples)
  - object: output_sequence
    property: length
    value: same as input_sequence length
  - object: non_zero_element
    property: relative_order
    description: The order of non-zero elements relative to each other.
relationships:
  - type: transformation
    source: input_sequence
    target: output_sequence
    description: Output is a rearrangement of the input.
  - type: preservation
    elements: non_zero_element
    property: relative_order
    description: The relative order of non-zero elements is preserved from input to output.
  - type: grouping
    target: output_sequence
    elements:
      - zero_element
      - non_zero_element
    description: All zero elements appear before all non-zero elements in the output sequence.
actions:
  - action: partition
    source: input_sequence
    criteria: element value (zero vs. non-zero)
    outputs:
      - list of zero elements
      - list of non-zero elements (maintaining relative order)
  - action: concatenate
    inputs:
      - list of zero elements
      - list of non-zero elements
    output: output_sequence
    order: zeros first, then non-zeros
```


## Natural Language Program

1.  Initialize two empty lists: `zeros` and `non_zeros`.
2.  Iterate through each number in the input sequence.
3.  If the number is 0, add it to the `zeros` list.
4.  If the number is not 0, add it to the `non_zeros` list.
5.  Create the output sequence by concatenating the `zeros` list followed by the `non_zeros` list.