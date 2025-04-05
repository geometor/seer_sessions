*   **Perception of Task Elements:**
    *   The input and output are sequences of single digits, represented as space-separated strings.
    *   The length of the sequences appears fixed (12 digits in the examples).
    *   The core operation involves identifying the span of non-zero digits within the sequence.
    *   Digits outside this span (leading and trailing zeros) seem unchanged.
    *   Digits *within* the span, excluding the very first and very last non-zero digits, are changed to zero.
    *   The first non-zero digit and the last non-zero digit in the sequence retain their original positions and values.

*   **YAML Fact Document:**
    
```yaml
    task_description: Modifying a sequence of digits based on the positions of non-zero elements.
    input_data:
      type: string
      format: space-separated single digits (0-9)
      elements: sequence of numbers
      length: 12 (observed in examples)
    output_data:
      type: string
      format: space-separated single digits (0-9)
      elements: sequence of numbers, modified from input
      length: 12 (observed in examples)
    objects:
      - sequence: The list of digits.
      - digit: Individual element within the sequence.
      - non_zero_digit: A digit with a value > 0.
    properties:
      - index: Position of a digit within the sequence.
      - value: The numerical value of a digit (0-9).
      - first_non_zero: The non-zero digit with the lowest index.
      - last_non_zero: The non-zero digit with the highest index.
    actions:
      - identify: Find the indices of the first and last non-zero digits.
      - preserve: Keep the original value of certain digits (leading/trailing zeros, first/last non-zero).
      - replace: Change the value of digits between the first and last non-zero digits to 0.
    relationships:
      - between: The concept of digits located strictly between the index of the first non-zero digit and the index of the last non-zero digit.
      - boundary: The first and last non-zero digits define the boundaries for the replacement action.
    invariants:
      - Sequence length remains constant.
      - Digits outside the span from the first non-zero to the last non-zero digit are unchanged.
      - The values and positions of the first and last non-zero digits themselves are unchanged.
    special_cases:
      - If the sequence contains no non-zero digits, the output is identical to the input.
      - If the sequence contains only one non-zero digit, the output is identical to the input (as the first and last non-zero digit are the same).
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of digits.
    2.  Find the index of the first non-zero digit in the list. If no non-zero digit exists, proceed to step 6.
    3.  Find the index of the last non-zero digit in the list.
    4.  Create a copy of the input list to serve as the initial output list.
    5.  Iterate through the indices of the output list starting from the index *after* the first non-zero digit's index, up to (but *not including*) the last non-zero digit's index. For each index in this range, set the corresponding digit in the output list to 0.
    6.  Convert the final output list back into a space-separated string.