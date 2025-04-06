## Perception of Elements

The input consists of two lines, each containing a sequence of identical numbers separated by spaces. The length of the sequence is consistent within each example. The output also consists of two lines. Each output line is formed by alternating the numbers found in the two input lines. The first output line starts with the number from the first input line, and the second output line starts with the number from the second input line. The length of the output sequences matches the length of the input sequences.

## Facts


```yaml
task_description: Generate two output sequences by alternating elements from two input sequences.
input_structure:
  type: text
  lines: 2
  elements_per_line: multiple, space-separated
  element_type: integer
  line_1_property: Contains repetitions of a single number (num1).
  line_2_property: Contains repetitions of a different single number (num2).
  shared_property: Both lines have the same number of elements (length).
output_structure:
  type: text
  lines: 2
  elements_per_line: multiple, space-separated, same length as input
  element_type: integer
transformation:
  line_1_output:
    pattern: Alternating sequence of num1 and num2.
    start_element: num1
    length: Matches input length.
  line_2_output:
    pattern: Alternating sequence of num2 and num1.
    start_element: num2
    length: Matches input length.
relationships:
  - Output elements are derived solely from the two unique numbers in the input.
  - Output sequence length is determined by input sequence length.
  - The starting element of each output line corresponds to the number on the respective input line.
```


## Natural Language Program

1.  Read the first line of the input and identify the repeating number (`num1`) and the count of numbers (`length`).
2.  Read the second line of the input and identify the repeating number (`num2`).
3.  Create the first output line:
    *   Initialize an empty sequence.
    *   For `i` from 0 to `length - 1`:
        *   If `i` is even, append `num1` to the sequence.
        *   If `i` is odd, append `num2` to the sequence.
    *   Format the sequence as a space-separated string.
4.  Create the second output line:
    *   Initialize an empty sequence.
    *   For `i` from 0 to `length - 1`:
        *   If `i` is even, append `num2` to the sequence.
        *   If `i` is odd, append `num1` to the sequence.
    *   Format the sequence as a space-separated string.
5.  Output the first formatted string, followed by a newline, followed by the second formatted string.