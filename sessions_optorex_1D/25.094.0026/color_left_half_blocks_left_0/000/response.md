*   **Perception:** The task involves transforming a sequence of integers containing only 0s and 2s into a sequence containing 0s, 2s, and 8s. The length of the sequence remains the same. The transformation rule specifically targets the number '2'. A '2' can potentially change into an '8' based on its position within a contiguous block (run) of '2's and the element immediately following that block. Zeros remain unchanged. The core logic involves identifying runs of '2's that terminate either just before a '0' or at the very end of the sequence. For such runs, a specific number of '2's at the end of the run are converted to '8's. The number of '2's converted depends on the total length of the run.

*   **Facts:**
    
```yaml
    objects:
      - name: input_sequence
        type: List[int]
        description: The initial sequence of integers (0s and 2s).
      - name: output_sequence
        type: List[int]
        description: The transformed sequence of integers (0s, 2s, and 8s).
      - name: element
        type: int
        description: An individual integer within the sequence (0, 2, or 8).
      - name: run_of_twos
        type: List[Tuple[int, int]] # List of (start_index, end_index)
        description: A contiguous subsequence composed entirely of the integer 2.
    properties:
      - name: value
        applies_to: element
        description: The integer value (0, 2, or 8).
      - name: index
        applies_to: element
        description: The position of the element within the sequence (0-based).
      - name: length
        applies_to: run_of_twos
        description: The number of elements in the run.
      - name: start_index
        applies_to: run_of_twos
        description: The index of the first element in the run.
      - name: end_index
        applies_to: run_of_twos
        description: The index of the last element in the run.
    relationships:
      - type: position
        description: An element exists at a specific index in the sequence.
      - type: adjacency
        description: An element is immediately followed by another element or the end of the sequence.
      - type: membership
        description: An element is part of a specific run_of_twos.
    actions:
      - name: identify_runs
        actor: system
        input: input_sequence
        output: List[run_of_twos]
        description: Scan the input sequence to find all contiguous runs of the integer 2.
      - name: check_termination
        actor: system
        input: run_of_twos, input_sequence
        output: boolean
        description: Check if the element immediately following the run is 0 or if the run extends to the end of the sequence.
      - name: calculate_changes
        actor: system
        input: run_of_twos
        output: int
        description: Calculate the number of elements to change (floor of run length divided by 2).
      - name: apply_transformation
        actor: system
        input: input_sequence, List[indices_to_change]
        output: output_sequence
        description: Create the output sequence by copying the input and changing the specified '2's at the calculated indices to '8's.

    ```


*   **Natural Language Program:**
    1.  Initialize the output sequence as a copy of the input sequence.
    2.  Iterate through the input sequence to identify all contiguous runs of the number '2'. For each run, record its starting index, ending index, and length.
    3.  For each identified run of '2's (with length `L`, starting at index `start`, ending at index `end`):
        a.  Check the element immediately following the run (at index `end + 1`).
        b.  Determine if the run terminates correctly: it terminates correctly if either the run ends at the last index of the sequence OR the element at index `end + 1` is '0'.
        c.  If the run terminates correctly:
            i.  Calculate the number of elements to change: `num_changes = floor(L / 2)`.
            ii. If `num_changes` is greater than 0, iterate from index `end - num_changes + 1` up to `end` (inclusive). For each index in this range, change the value in the *output* sequence at that index from '2' to '8'.
    4.  Return the modified output sequence.