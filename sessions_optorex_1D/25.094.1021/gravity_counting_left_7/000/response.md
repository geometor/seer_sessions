## Perception of Elements

The task involves transforming a sequence of single-digit integers into a binary sequence (0s and 1s) of the same length. The key observation is that the output sequence consists of a block of zeros followed by a block of ones. The position where the sequence switches from 0 to 1 seems determined by a property of the input sequence, specifically related to the count of the digit '0'.

## Facts


```yaml
objects:
  - name: input_sequence
    type: List[int]
    description: A sequence of single-digit integers.
  - name: output_sequence
    type: List[int]
    description: A sequence of binary digits (0 or 1) with the same length as the input sequence.
  - name: zero_digit
    type: int
    value: 0
    description: The specific digit whose occurrences are counted.
properties:
  - object: input_sequence
    name: length
    type: int
  - object: output_sequence
    name: length
    type: int
  - object: input_sequence
    name: zero_count
    type: int
    description: The total number of times the digit 0 appears in the input sequence.
relationships:
  - type: equality
    between: [input_sequence.length, output_sequence.length]
    description: The input and output sequences have the same number of elements.
  - type: dependency
    description: The value of each element in the output_sequence depends on its index and the zero_count from the input_sequence.
actions:
  - name: count_zeros
    input: input_sequence
    output: zero_count
    description: Iterate through the input sequence and count occurrences of the digit 0.
  - name: generate_output
    input: [input_sequence.length, zero_count]
    output: output_sequence
    description: Create the output sequence where elements with index less than zero_count are 0, and elements with index greater than or equal to zero_count are 1.
```


## Natural Language Program

1.  Receive the input sequence of digits.
2.  Count the total number of times the digit '0' appears in the input sequence. Store this count (let's call it `zero_count`).
3.  Determine the length of the input sequence (let's call it `length`).
4.  Create a new output sequence of the same `length`.
5.  Iterate through the indices of the output sequence, from 0 up to `length - 1`.
6.  For each index `i`:
    *   If `i` is less than `zero_count`, set the element at index `i` in the output sequence to '0'.
    *   Otherwise (if `i` is greater than or equal to `zero_count`), set the element at index `i` in the output sequence to '1'.
7.  Format the output sequence as a space-separated string of digits.