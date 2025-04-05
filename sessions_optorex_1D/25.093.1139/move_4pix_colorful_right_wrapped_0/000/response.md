*   **Perception of Task Elements:**
    *   The input and output are both sequences of 12 numerical digits.
    *   The digits themselves within the sequence are preserved from input to output.
    *   The order of the digits is changed following a consistent pattern across all examples.
    *   The transformation appears to operate on fixed-size blocks or segments of the input sequence.
    *   Observing the examples, particularly how blocks of zeros and non-zeros shift, suggests a rearrangement of segments of length 4. The input sequence of 12 digits can be divided into three consecutive segments of 4 digits each.

*   **YAML Facts:**
    
```yaml
    task_description: Rearrange blocks of digits within a sequence.
    input_object:
      type: sequence
      subtype: digits
      properties:
        length: 12
        elements: numerical digits (0-9)
    output_object:
      type: sequence
      subtype: digits
      properties:
        length: 12
        elements: numerical digits (0-9), same multiset as input
    actions:
      - name: split
        target: input_sequence
        parameters:
          segment_length: 4
        resulting_objects:
          - segment_1: first 4 digits
          - segment_2: middle 4 digits
          - segment_3: last 4 digits
      - name: rearrange
        source_objects: [segment_1, segment_2, segment_3]
        target: output_sequence
        rule: Concatenate segments in the order [segment_3, segment_1, segment_2]
    relationships:
      - The output sequence is a permutation of the input sequence based on segment rearrangement.
      - The segments maintain their internal order of digits.
    ```


*   **Natural Language Program:**
    1.  Divide the input sequence of 12 digits into three consecutive segments, each containing 4 digits. Let these segments be S1 (digits 1-4), S2 (digits 5-8), and S3 (digits 9-12).
    2.  Construct the output sequence by concatenating these segments in the following order: S3, then S1, then S2.