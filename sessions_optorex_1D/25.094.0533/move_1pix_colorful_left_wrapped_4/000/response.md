**Perception**

The input is a sequence of single-digit integers, presented as space-separated values. The output is also a sequence of single-digit integers, of the same length as the input. Upon comparing the input and output sequences across all examples, a consistent pattern emerges: the first element of the input sequence is relocated to the end of the sequence to form the output. All other elements retain their relative order but shift one position to the left. This operation is equivalent to a left rotation of the sequence by one position.

**Facts**


```yaml
objects:
  - name: input_sequence
    type: list
    properties:
      - contains: single_digit_integers
      - order: significant
  - name: output_sequence
    type: list
    properties:
      - contains: single_digit_integers
      - order: significant
      - length: same as input_sequence
  - name: first_element
    type: integer
    properties:
      - value: the integer at the first position (index 0) of the input_sequence
  - name: remaining_elements
    type: list
    properties:
      - contains: all elements of the input_sequence except the first_element
      - order: preserved from input_sequence

actions:
  - name: identify_first_element
    input: input_sequence
    output: first_element
  - name: identify_remaining_elements
    input: input_sequence
    output: remaining_elements
  - name: construct_output
    inputs:
      - remaining_elements
      - first_element
    output: output_sequence
    description: Concatenate the remaining_elements list with the first_element appended to the end.

relationships:
  - output_sequence is derived from input_sequence by moving the first_element to the end.
  - The order of remaining_elements in the output_sequence is the same as their relative order in the input_sequence.
  - The output_sequence represents a single left rotation of the input_sequence.
```


**Natural Language Program**

1.  Read the input sequence of integers.
2.  Identify and store the first integer in the sequence.
3.  Create a new sequence containing all integers from the input sequence starting from the second integer up to the last one, maintaining their original relative order.
4.  Append the stored first integer to the end of this new sequence.
5.  The resulting sequence is the output.