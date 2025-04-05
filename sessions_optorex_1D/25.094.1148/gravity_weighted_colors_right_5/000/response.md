**Perception of Task Elements:**

The task involves transforming an input sequence of 12 integers into an output sequence of the same length. The integers in the sequence are limited to the values 0, 1, and 2. Comparing the input and output sequences across multiple examples reveals that the output sequence consistently contains the same counts of each integer (0, 1, 2) as the input sequence, but arranged in a specific order. The output sequence always appears sorted in descending order, with all the 2s appearing first, followed by all the 1s, and finally all the 0s.

**Facts:**


```yaml
task_elements:
  - object: input_sequence
    properties:
      - type: sequence
      - element_type: integer
      - allowed_values: [0, 1, 2]
      - length: 12
  - object: output_sequence
    properties:
      - type: sequence
      - element_type: integer
      - allowed_values: [0, 1, 2]
      - length: 12
action:
  - name: sort
    parameters:
      - order: descending
    input: input_sequence
    output: output_sequence
relationship:
  - type: transformation
    from: input_sequence
    to: output_sequence
    rule: The output_sequence is the result of sorting the input_sequence in descending order.
```


**Natural Language Program:**

1.  Receive the input sequence of 12 integers.
2.  Rearrange the elements of the input sequence such that they are sorted in descending order (from largest to smallest).
3.  Produce the rearranged sequence as the output.