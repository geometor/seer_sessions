Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Elements:**

1.  **Input/Output Data Type:** Both input and output are sequences (lists) of single-digit integers. They are presented as space-separated strings but represent numerical lists.
2.  **Core Operation:** The transformation seems to involve identifying specific patterns within the input sequence and selectively preserving parts of that pattern while replacing others.
3.  **Key Feature:** The non-zero digits and their contiguous occurrences (runs) appear crucial. The lengths of these runs seem to determine what is kept in the output.
4.  **Filtering/Selection:** The process filters the input based on the longest contiguous sequence of a non-zero digit. Only the elements belonging to this longest sequence are retained in their original positions; all other elements become zero.
5.  **Zero Handling:** Zeros in the input act as separators between sequences of non-zero digits and are generally preserved in the output unless they are replaced by a digit from the selected longest sequence (which doesn't happen in the examples, as the longest sequence only replaces non-zeros or other parts of shorter sequences).
6.  **Tie-breaking (Implicit):** Although not explicitly shown with conflicting examples, if multiple non-zero digit sequences share the maximum length, a rule must exist. Common defaults would be to keep the first occurrence or the last. Based on the provided examples, it's consistent that *a* longest sequence is chosen, but the specific tie-breaker isn't definitively tested. Let's assume for now the *first* longest sequence encountered is kept.

**YAML Facts:**


```yaml
task_description: Identify and isolate the longest contiguous sequence of a single non-zero digit within a list of digits.
elements:
  - name: input_list
    type: list_of_integers
    description: The initial sequence of digits provided.
  - name: output_list
    type: list_of_integers
    description: The resulting sequence after applying the transformation.
    relationship: derived from input_list by isolating the longest run.
  - name: non_zero_digit
    type: integer
    properties:
      - value > 0
    description: Digits that can form sequences.
  - name: zero_digit
    type: integer
    properties:
      - value == 0
    description: Acts as a separator and default background value in the output.
  - name: contiguous_run
    type: object
    properties:
      - digit_value: integer (must be non-zero)
      - start_index: integer
      - end_index: integer
      - length: integer (end_index - start_index + 1)
    description: A sequence of identical, adjacent non-zero digits within the input_list.
    relationship: Found within input_list.
actions:
  - name: find_runs
    input: input_list
    output: list_of_contiguous_runs
    description: Scan the input_list to identify all contiguous_runs of non-zero digits.
  - name: find_longest_run
    input: list_of_contiguous_runs
    output: longest_run (a single contiguous_run object, or potentially null if no non-zero digits exist)
    description: Determine the run with the maximum length. If multiple runs share the maximum length, select the one with the smallest start_index.
  - name: generate_output
    input:
      - input_list_length
      - longest_run
    output: output_list
    description: Create a list of zeros with the same length as the input_list. If a longest_run was found, populate the corresponding indices (from start_index to end_index) in the output_list with the digit_value of the longest_run.
```


**Natural Language Program:**

1.  Receive the input list of digits.
2.  Initialize an empty list to store identified contiguous runs of non-zero digits.
3.  Iterate through the input list, identifying the start index, end index, digit value, and length of every contiguous sequence (run) of identical non-zero digits. Store these runs (e.g., as objects with digit, start, end, length).
4.  If no non-zero runs were found, return a list of zeros with the same length as the input list.
5.  If runs were found, determine the maximum length among all identified runs.
6.  Select the run(s) that have this maximum length.
7.  If there is only one run with the maximum length, choose it as the "target run".
8.  If there are multiple runs with the same maximum length, choose the one that appears earliest in the input list (i.e., the one with the minimum start index) as the "target run".
9.  Create an output list of the same length as the input list, initially filled entirely with zeros.
10. Iterate from the start index to the end index (inclusive) of the "target run". For each index in this range, set the value in the output list at that index to the digit value of the "target run".
11. Return the generated output list.