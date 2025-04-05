## Perception

The input and output are both sequences (lists) of single-digit integers. The length of the output sequence is identical to the length of the input sequence in all examples. Comparing the input and output sequences reveals a consistent pattern: the first element of the input sequence is moved to the end of the sequence to form the output. All other elements retain their original relative order but shift one position to the left. This operation is equivalent to a left circular shift or rotation of the sequence by one position.

## Facts


```yaml
objects:
  - name: input_sequence
    type: list
    properties:
      - elements: single-digit integers
      - order: significant
  - name: output_sequence
    type: list
    properties:
      - elements: single-digit integers
      - order: significant
  - name: first_element
    type: integer
    source: first position of input_sequence
  - name: remaining_elements
    type: list
    source: elements of input_sequence starting from the second position
relationships:
  - type: transformation
    from: input_sequence
    to: output_sequence
    action: circular_shift_left_by_one
  - type: derivation
    input: input_sequence
    output: first_element
    action: extract_first
  - type: derivation
    input: input_sequence
    output: remaining_elements
    action: slice_from_second
  - type: composition
    components:
      - remaining_elements
      - first_element
    output: output_sequence
    action: concatenate_in_order
```


## Natural Language Program

1.  Identify the input sequence of integers.
2.  Take the first element from the input sequence.
3.  Create a new sequence containing all elements from the input sequence *except* the first element, maintaining their relative order.
4.  Append the element identified in step 2 to the end of the new sequence created in step 3.
5.  The resulting sequence is the output.