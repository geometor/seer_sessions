**Perception:**

The input is a sequence of 12 integers. The output is also a sequence of 12 integers, which appears to be a rearrangement of the input sequence. By comparing the input and output sequences across the examples, a consistent pattern emerges. The input sequence seems to be divided into two subsequences. The first subsequence consists of the first 4 integers, and the second subsequence consists of the remaining 8 integers. The output sequence is formed by placing the second subsequence first, followed by the first subsequence.

**Facts:**


```yaml
task_description: Rearrange a sequence of 12 integers by swapping two fixed-length blocks.
elements:
  - type: sequence
    role: input
    subtype: integer
    length: 12
    representation: space-separated string
  - type: sequence
    role: output
    subtype: integer
    length: 12
    representation: space-separated string
transformation:
  action: split
  input: input sequence
  parameters:
    split_index: 4 # Split after the 4th element (index 3)
  outputs:
    - name: part1
      elements: input[0:4]
    - name: part2
      elements: input[4:12]
  action: concatenate
  inputs:
    - part2
    - part1
  output: output sequence
relationship:
  output_sequence = concatenate(part2, part1) where part1 = input[0:4] and part2 = input[4:12]
```


**Natural Language Program:**

1.  Take the input sequence of 12 integers.
2.  Divide the input sequence into two parts:
    *   The first part consists of the first 4 integers.
    *   The second part consists of the remaining 8 integers (from the 5th to the 12th integer).
3.  Construct the output sequence by concatenating the second part followed by the first part.