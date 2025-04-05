Okay, I will analyze the provided input-output examples to understand the transformation rule.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are sequences (lists) of 12 integers.
2.  **Key Positions:** The last two integers in the input sequence (`index 10` and `index 11`) appear to act as parameters or control values for the transformation.
3.  **Target Sequence:** The first 10 integers (`index 0` to `index 9`) constitute the primary sequence being modified.
4.  **Target Value:** The integer `5` seems to be the specific value targeted for replacement within the first 10 positions. Other values (specifically `0`) remain unchanged in their positions.
5.  **Replacement Values:** The values from index 10 and index 11 of the input are used to replace the target value (`5`).
6.  **Grouping:** The replacement seems sensitive to contiguous groups (or "runs") of the target value `5`.
7.  **Conditional Replacement Logic:**
    *   If there's only one contiguous group of `5`s in the first 10 positions, the replacement value used depends on the input values at index 10 (`val1`) and index 11 (`val2`). If `val1` is non-zero, it's used; otherwise, `val2` is used.
    *   If there are two contiguous groups of `5`s, the first group is replaced by `val1`, and the second group is replaced by `val2`.
8.  **Preservation:** The values `0` in the first 10 positions and the values at index 10 and 11 are preserved in the output in their original positions.

**Facts:**


```yaml
objects:
  - name: input_sequence
    type: list
    properties:
      length: 12
      elements: integer
  - name: output_sequence
    type: list
    properties:
      length: 12
      elements: integer
  - name: target_subsequence
    type: list slice
    source: input_sequence
    indices: 0-9
  - name: control_values
    type: list slice
    source: input_sequence
    indices: 10-11
    elements:
      - name: val1
        index: 10 (relative to input_sequence)
      - name: val2
        index: 11 (relative to input_sequence)
  - name: target_value
    type: integer
    value: 5
  - name: ignored_value
    type: integer
    value: 0
  - name: groups_of_target
    type: list of list slices
    description: Contiguous sequences of target_value within target_subsequence.

actions:
  - name: identify_groups
    input: target_subsequence, target_value
    output: groups_of_target
    description: Find all contiguous blocks of the target_value.
  - name: generate_output_prefix
    input: target_subsequence, groups_of_target, val1, val2
    output: list (length 10)
    description: >
      Create the first 10 elements of the output by copying the target_subsequence
      and then replacing values within the identified groups based on the number of groups
      and the values of val1 and val2.
      If one group exists: replace with val1 if val1 != 0, else replace with val2.
      If two groups exist: replace first group with val1, second group with val2.
      Leave ignored_value (0) unchanged.
  - name: construct_output
    input: generated_output_prefix, val1, val2
    output: output_sequence
    description: Concatenate the generated_output_prefix with val1 and val2.

relationships:
  - The output_sequence depends on the input_sequence.
  - The transformation primarily affects elements in the target_subsequence that match the target_value.
  - The specific replacement values are determined by control_values (val1, val2).
  - The application logic of control_values depends on the number and position of groups_of_target.
  - Elements equal to ignored_value in the target_subsequence remain unchanged.
  - control_values (val1, val2) are preserved in the last two positions of the output_sequence.

```


**Natural Language Program:**

1.  Accept the input sequence of 12 integers.
2.  Identify the two control values: `val1` is the element at index 10, and `val2` is the element at index 11.
3.  Create a working copy of the first 10 elements of the input sequence.
4.  Scan the working copy to identify the start and end indices of all contiguous groups of the integer `5`. Store these groups.
5.  Count the number of identified groups of `5`s.
6.  If exactly one group was found:
    *   Determine the replacement value: if `val1` is not equal to `0`, use `val1`; otherwise, use `val2`.
    *   Replace all `5`s within that single group in the working copy with the determined replacement value.
7.  If two or more groups were found (examples show only up to two):
    *   Replace all `5`s within the first identified group in the working copy with `val1`.
    *   Replace all `5`s within the second identified group in the working copy with `val2`.
8.  Construct the final output sequence by taking the modified working copy (the first 10 elements) and appending the original `val1` and `val2` to its end.
9.  Return the final output sequence.