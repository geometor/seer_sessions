**Perception:**

The input consists of two lines, each containing a sequence of the same number repeated multiple times, separated by spaces. The output also consists of two lines. The output lines are formed by interleaving the numbers from the two input lines. The first output line starts with the number from the first input line and alternates with the number from the second input line. The second output line starts with the number from the second input line and alternates with the number from the first input line. The length of the sequences in the output lines is the same as the length of the sequences in the input lines.

**Facts:**


```yaml
Input:
  type: text
  structure: two lines
  line_1:
    content: sequence of identical numbers (N1) separated by spaces
    length: L
  line_2:
    content: sequence of identical numbers (N2) separated by spaces
    length: L
Output:
  type: text
  structure: two lines
  line_1:
    content: alternating sequence of N1 and N2, starting with N1, separated by spaces
    length: L
  line_2:
    content: alternating sequence of N2 and N1, starting with N2, separated by spaces
    length: L
Relationships:
  - Output line 1 is generated by interleaving N1 and N2, starting with N1.
  - Output line 2 is generated by interleaving N2 and N1, starting with N2.
  - The length L of the sequences remains constant between input and output.
```


**Natural Language Program:**

1.  Read the first input line and identify the repeating number (N1) and the sequence length (L).
2.  Read the second input line and identify the repeating number (N2).
3.  Construct the first output line: For each position from 1 to L, if the position is odd, use N1; if the position is even, use N2. Join these numbers with spaces.
4.  Construct the second output line: For each position from 1 to L, if the position is odd, use N2; if the position is even, use N1. Join these numbers with spaces.
5.  Output the first constructed line followed by the second constructed line.