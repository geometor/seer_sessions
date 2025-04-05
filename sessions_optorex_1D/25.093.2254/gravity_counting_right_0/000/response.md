## Perception of Task Elements

1.  **Input Data:** The input consists of a sequence of integers, separated by spaces. In all provided examples, the sequence has a fixed length of 12 elements. The elements themselves are single digits ranging from 0 to 9.
2.  **Output Data:** The output is also a sequence of integers, separated by spaces, and has the same length (12) as the input sequence. The output sequence consists only of 0s and 1s.
3.  **Transformation:** The transformation appears to involve counting certain elements in the input and using that count to construct the output sequence. Specifically, the number of non-zero elements in the input determines the number of `1`s at the beginning of the output sequence. The remaining positions in the output sequence are filled with `0`s. The original values and positions of the non-zero elements in the input do not seem to influence the output, only their count does.

## Documented Facts


```yaml
task_type: sequence_transformation
input_data:
  type: sequence
  element_type: integer
  separator: space
  length: fixed (12 in examples)
  element_range: 0-9
output_data:
  type: sequence
  element_type: integer
  separator: space
  length: same as input (12 in examples)
  element_range: 0-1
transformation:
  - action: count
    target: non-zero elements in the input sequence
    result: a number (let's call it N)
  - action: construct_output
    details:
      - Create a sequence of N ones.
      - Create a sequence of (L - N) zeros, where L is the length of the input sequence.
      - Concatenate the sequence of ones and the sequence of zeros.
    output_structure: N ones followed by (L - N) zeros.
relationship:
  - The number of '1's in the output sequence is equal to the count of non-zero elements in the input sequence.
  - The number of '0's in the output sequence is equal to the count of zero elements in the input sequence.
  - The total length of the output sequence is equal to the total length of the input sequence.
```


## Natural Language Program

1.  Receive the input sequence of numbers.
2.  Count the total number of elements in the input sequence (`L`).
3.  Count the number of elements in the input sequence that are not equal to zero (`N`).
4.  Generate an output sequence consisting of `N` elements with the value `1`.
5.  Append `L - N` elements with the value `0` to the end of the generated sequence.
6.  Return the resulting sequence.