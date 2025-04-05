## Perception

The input and output are both sequences of integers.
Comparing the input and output sequences, it appears that the first element of the input sequence is moved to the end of the sequence to form the output. The relative order of the remaining elements is preserved. This operation is equivalent to a single left rotation of the sequence.

## Facts


```yaml
objects:
  - type: sequence
    properties:
      - name: elements
        type: list[integer]
      - name: length
        value_description: The number of integers in the sequence.
actions:
  - name: left_rotate
    description: Moves the first element of the sequence to the end.
    input:
      - name: input_sequence
        type: sequence
    output:
      - name: output_sequence
        type: sequence
        description: The input sequence after moving the first element to the last position.
relationships:
  - type: transformation
    description: The output sequence is derived from the input sequence by performing a single left rotation.
    input: input_sequence
    output: output_sequence
    rule: Take the first element of the input sequence and append it to the end of the sequence formed by the remaining elements.
```


## Natural Language Program

1.  Receive the input sequence of integers.
2.  Identify the first integer in the sequence.
3.  Create a new sequence containing all integers from the input sequence *except* the first one, maintaining their original relative order.
4.  Append the first integer (identified in step 2) to the end of the new sequence created in step 3.
5.  Return the resulting sequence as the output.