**Perception:**

The input and output for each task consist of a sequence of single-digit integers separated by spaces. The length of the sequence appears consistent within each example pair. Comparing the input and output sequences reveals a consistent pattern: the last element of the input sequence is moved to the beginning of the sequence, and all other elements are shifted one position to the right to accommodate the moved element. This operation is commonly known as a right circular shift or rotation.

**YAML Facts:**


```yaml
task_elements:
  - name: sequence
    type: list
    properties:
      - contains: integers
      - ordered: true
      - delimited_by: space
  - name: element
    type: integer
    properties:
      - single_digit: true # based on examples, might not be a strict rule

input_object:
  - name: input_sequence
    type: sequence

output_object:
  - name: output_sequence
    type: sequence

actions:
  - name: circular_shift_right
    description: Moves the last element of a sequence to the first position, shifting all other elements one position to the right.
    inputs:
      - input_sequence
    outputs:
      - output_sequence

relationships:
  - type: transformation
    from: input_sequence
    to: output_sequence
    rule: apply circular_shift_right
  - type: element_position
    description: The last element of the input_sequence becomes the first element of the output_sequence.
  - type: element_position
    description: Each element at index 'i' (where i > 0) in the input_sequence moves to index 'i+1' in the output_sequence.
```


**Natural Language Program:**

1.  Read the input sequence of numbers.
2.  Identify the last number in the sequence.
3.  Remove the last number from the sequence.
4.  Insert the removed number at the beginning of the sequence.
5.  Output the modified sequence.