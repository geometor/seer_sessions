## Perception

The input and output are both sequences of numbers. In all provided examples, the input sequence consistently contains 12 numerical elements. The output sequence also contains 12 numerical elements. The core transformation appears to be a reordering of the elements within the sequence. By comparing the input and output sequences, a consistent pattern emerges: the last three elements of the input sequence are moved to the beginning of the output sequence, and the first nine elements of the input sequence follow them, maintaining their original relative order. This is equivalent to a right circular shift of the sequence by 3 positions.

## Facts


```yaml
Task: Sequence Transformation

Input:
  Type: Sequence
  Properties:
    - Contains numerical elements
    - Fixed length: 12 elements

Output:
  Type: Sequence
  Properties:
    - Contains numerical elements
    - Fixed length: 12 elements
    - Elements are the same as the input sequence but reordered

Transformation:
  Action: Circular Shift (Right Rotation)
  Description: The sequence is shifted circularly to the right.
  Details:
    - The last 3 elements of the input sequence become the first 3 elements of the output sequence.
    - The first 9 elements of the input sequence become the last 9 elements of the output sequence.
    - The relative order within the moved group (last 3) is maintained.
    - The relative order within the remaining group (first 9) is maintained.
    - Shift Amount: 3 positions

Examples_Consistent: Yes, all examples follow the same transformation rule.
```


## Natural Language Program

1.  Take the input sequence of 12 numbers.
2.  Identify the last 3 elements of the sequence.
3.  Identify the first 9 elements of the sequence.
4.  Construct the output sequence by concatenating the identified last 3 elements followed by the identified first 9 elements.