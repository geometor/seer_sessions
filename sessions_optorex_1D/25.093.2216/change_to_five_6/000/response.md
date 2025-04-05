*   **Perception of Task Elements:**
    *   The input and output are sequences of single digits, represented as space-separated strings.
    *   The length of the input sequence is preserved in the output sequence.
    *   The core transformation involves examining each digit in the input sequence individually.
    *   A distinction is made between the digit '0' and all other digits (1 through 9).
    *   The digit '0' remains unchanged in the output.
    *   All non-zero digits in the input are consistently replaced by the digit '5' in the output.
    *   The position of each digit is maintained throughout the transformation.

*   **YAML Facts:**
    
```yaml
    task_description: Replace non-zero digits with 5, keep zeros.
    input_format: Space-separated string of single digits.
    output_format: Space-separated string of single digits.
    objects:
      - name: digit
        properties:
          - value: integer (0-9)
          - is_zero: boolean
    actions:
      - name: map_digit
        inputs:
          - digit: Input digit
        outputs:
          - digit: Output digit
        logic: If the input digit's value is 0, the output digit's value is 0. Otherwise (if the input digit's value is 1-9), the output digit's value is 5.
      - name: process_sequence
        inputs:
          - sequence: Input string of digits
        outputs:
          - sequence: Output string of digits
        logic: Apply the 'map_digit' action to each digit in the input sequence, maintaining the original order and spacing.
    relationships:
      - type: position_correspondence
        description: The digit at index 'i' in the output sequence corresponds to the transformation of the digit at index 'i' in the input sequence.
      - type: value_mapping
        description: Input digits map to output digits based on whether they are zero or non-zero.
          - 0 maps to 0
          - 1-9 maps to 5
    constants:
      - name: replacement_value
        value: 5
      - name: zero_value
        value: 0
    ```


*   **Natural Language Program:**
    1.  Read the input string of space-separated digits.
    2.  Split the input string into a list of individual digit characters.
    3.  Create a new list to store the output digits.
    4.  Iterate through each digit character in the input list:
        a.  Convert the character to an integer.
        b.  Check if the integer value is equal to 0.
        c.  If the value is 0, append the character '0' to the output list.
        d.  If the value is not 0 (i.e., it is 1, 2, 3, 4, 5, 6, 7, 8, or 9), append the character '5' to the output list.
    5.  Join the characters in the output list back into a single string, separated by spaces.
    6.  Return the resulting string.