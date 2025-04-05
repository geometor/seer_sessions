**Perception of Task Elements:**

The task involves transforming a sequence of integers into another sequence of the same length.
*   **Input:** A string containing space-separated integers. The length of the sequence appears constant across examples (12 integers). The integers themselves can range from 0 upwards.
*   **Output:** A string containing space-separated binary integers (0s and 1s). The length is the same as the input sequence.
*   **Transformation:** The output sequence seems to be determined by the count of non-zero elements in the input sequence. Specifically, the output sequence consists of a number of leading zeros followed by a number of trailing ones. The number of trailing ones corresponds exactly to the count of non-zero integers in the input sequence. The number of leading zeros is the total length of the sequence minus the count of non-zero integers.

**YAML Fact Documentation:**


```yaml
Task: Transform sequence of integers based on non-zero count.

Input:
  Type: List of integers (represented as space-separated string).
  Properties:
    - Length: L (appears fixed at 12 in examples).
    - Elements: Integers (non-negative).
    - Contains_Zeros: True/False based on presence of 0.
    - Non_Zero_Count: N (Count of elements > 0).

Output:
  Type: List of binary integers (0 or 1) (represented as space-separated string).
  Properties:
    - Length: L (same as input).
    - Structure: Consists of (L - N) zeros followed by N ones.

Relationship:
  - The number of '1's in the output list is equal to the 'Non_Zero_Count' (N) of the input list.
  - The number of '0's in the output list is equal to the 'Length' (L) of the input list minus the 'Non_Zero_Count' (N).
  - The '1's always appear at the end of the output list.
  - The '0's always appear at the beginning of the output list.

Action:
  1. Parse the input string into a list of integers.
  2. Count the number of non-zero integers (N) in the input list.
  3. Determine the total length (L) of the input list.
  4. Construct the output list by creating (L - N) zeros followed by N ones.
  5. Format the output list as a space-separated string.
```


**Natural Language Program:**

1.  Receive the input string of space-separated integers.
2.  Convert the input string into a list of integer values.
3.  Count how many integers in the list are not equal to zero; let this count be `N`.
4.  Determine the total number of integers in the list; let this length be `L`.
5.  Create a new list.
6.  Append `L - N` zeros to the new list.
7.  Append `N` ones to the new list.
8.  Convert the new list back into a string of space-separated integers to form the output.