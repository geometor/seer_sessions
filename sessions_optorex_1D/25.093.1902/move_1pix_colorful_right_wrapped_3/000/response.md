## Perception of Task Elements

The input consists of a sequence of 12 single-digit integers, separated by spaces. The output is also a sequence of 12 single-digit integers, separated by spaces. Comparing the input and output sequences across all examples reveals that the numbers present in the input are exactly the same as the numbers in the output, and they maintain their relative order, but their positions within the sequence have changed. Specifically, the entire sequence appears to be shifted one position to the right, with the last element wrapping around to become the first element.

## Documented Facts


```yaml
Data:
  - type: sequence
    format: list of integers
    length: 12
    elements: single digits (0-9)
Transformation:
  action: rotate_right
  target: entire input sequence
  amount: 1 position
Relationships:
  - Output sequence is a right circular shift of the input sequence by one position.
  - The last element of the input sequence becomes the first element of the output sequence.
  - All other elements from the input sequence are shifted one position to the right in the output sequence.
```


## Natural Language Program

1.  Take the input sequence of 12 integers.
2.  Identify the last element of the sequence.
3.  Create a new sequence starting with the last element identified in step 2.
4.  Append all elements from the input sequence, *except* the last one, to the new sequence, maintaining their original relative order.
5.  The resulting sequence is the output.