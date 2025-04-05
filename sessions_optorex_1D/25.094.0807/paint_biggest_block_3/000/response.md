*   **Perception of task elements:**
    *   The input and output are sequences of single-digit integers, separated by spaces.
    *   The transformation involves identifying a specific contiguous subsequence within the input and modifying it.
    *   The modification consists of replacing the digits in the identified subsequence with the digit `1`.
    *   The subsequence targeted for modification appears to be the *longest* contiguous run of identical non-zero digits.
    *   If multiple runs share the same maximum length, the *first* one encountered (from left to right) is the one modified.
    *   Digits equal to `0` act as separators for these runs and are never modified.
    *   Other runs of non-zero digits that are not the longest (or the first of the longest) remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_description: Modify a sequence of digits by replacing the first occurring longest contiguous run of identical non-zero digits with 1s.
    input_type: Sequence of single-digit integers.
    output_type: Sequence of single-digit integers.
    elements:
      - name: DigitSequence
        type: List[int]
        description: Represents the input and output data.
      - name: NonZeroRun
        type: Object
        description: A contiguous subsequence of identical non-zero digits within the DigitSequence.
        properties:
          - name: value
            type: int
            description: The digit value (1-9) repeated in the run.
          - name: start_index
            type: int
            description: The starting position (0-based index) of the run in the DigitSequence.
          - name: length
            type: int
            description: The number of digits in the run.
      - name: TargetRun
        type: NonZeroRun
        description: The specific NonZeroRun selected for modification based on length and position.
    actions:
      - name: find_non_zero_runs
        input: DigitSequence
        output: List[NonZeroRun]
        description: Identifies all NonZeroRuns in the input sequence.
      - name: select_target_run
        input: List[NonZeroRun]
        output: TargetRun | None
        description: Selects the run with the maximum length. If multiple runs have the maximum length, selects the one with the minimum start_index. Returns None if no NonZeroRuns exist.
      - name: replace_run_with_ones
        input:
          - DigitSequence
          - TargetRun
        output: DigitSequence
        description: Creates a new sequence where the digits corresponding to the TargetRun in the input sequence are replaced by the digit 1.
    relationships:
      - The TargetRun is the NonZeroRun with the maximum 'length' property.
      - In case of ties in 'length', the TargetRun is the one with the minimum 'start_index' property.
    constants:
      - name: replacement_digit
        value: 1
        description: The digit used to replace the elements of the TargetRun.
      - name: zero_digit
        value: 0
        description: Acts as a separator and is never part of a NonZeroRun.

    ```


*   **Natural Language Program:**
    1.  Initialize an empty list to store information about runs of identical non-zero digits found in the input sequence.
    2.  Iterate through the input sequence, identifying each contiguous run of identical non-zero digits. For each run found, record its starting index, its length, and the digit it consists of. Add this information to the list of runs.
    3.  If no non-zero runs were found, return the original input sequence unchanged.
    4.  Examine the recorded runs to find the maximum length among them.
    5.  Filter the list of runs to keep only those that have this maximum length.
    6.  From the filtered list (runs of maximum length), select the run that has the smallest starting index. This is the target run.
    7.  Create a copy of the input sequence to serve as the output sequence.
    8.  Iterate from the starting index of the target run up to (starting index + length - 1). For each position within this range in the output sequence, change the digit to `1`.
    9.  Return the modified output sequence.