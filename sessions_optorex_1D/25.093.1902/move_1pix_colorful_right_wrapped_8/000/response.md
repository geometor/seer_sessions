**Perception of Task Elements:**

The task involves transforming a sequence of numbers into another sequence of the same length. The input and output sequences appear to contain the same set of numbers, but their order is different. Observing the examples reveals a consistent pattern: the last number in the input sequence becomes the first number in the output sequence, and all preceding numbers are shifted one position to the right. This operation is commonly known as a right circular shift or rotation.

**Facts:**


```yaml
objects:
  - name: sequence
    type: list of integers
    properties:
      - ordered elements
      - fixed length (12 in examples)
actions:
  - name: rotate_right
    input: sequence
    output: sequence
    description: Moves the last element of the input sequence to the first position, shifting all other elements one position to the right.
relationships:
  - type: transformation
    input: input_sequence
    output: output_sequence
    rule: output_sequence is the result of applying the rotate_right action to the input_sequence.
```


**Natural Language Program:**

1.  Identify the input sequence of numbers.
2.  Take the last number from the input sequence.
3.  Take all numbers from the input sequence *except* the last one.
4.  Construct the output sequence by placing the number identified in step 2 at the beginning, followed by the numbers identified in step 3 in their original relative order.