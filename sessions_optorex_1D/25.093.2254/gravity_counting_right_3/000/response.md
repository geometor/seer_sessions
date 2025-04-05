*   **Perception of Task Elements:**
    *   The input is a sequence of space-separated integers.
    *   The output is also a sequence of space-separated integers, specifically consisting only of 0s and 1s.
    *   The length of the input sequence is preserved in the output sequence.
    *   The output sequence always starts with a block of 1s, followed by a block of 0s (or potentially only 1s or only 0s, though not seen in examples).
    *   The key transformation seems related to the count of non-zero elements in the input.

*   **YAML Documentation:**
    
```yaml
    task_description: "Transforms a sequence of integers into a binary sequence of the same length, where the number of 1s corresponds to the count of non-zero elements in the input."
    input_elements:
      - name: input_sequence
        type: list[int]
        description: "A sequence of integers."
        properties:
          - length: L
          - contains_zeros: boolean
          - contains_non_zeros: boolean
    output_elements:
      - name: output_sequence
        type: list[int]
        description: "A sequence of 1s followed by 0s."
        properties:
          - length: L (same as input_sequence)
          - values: subset of {0, 1}
    transformation:
      actions:
        - name: count_non_zeros
          input: input_sequence
          output: non_zero_count (N)
          description: "Counts the number of elements in the input sequence that are not equal to 0."
        - name: construct_output
          inputs:
            - non_zero_count (N)
            - input_length (L)
          output: output_sequence
          description: "Creates a new sequence containing N ones followed by (L - N) zeros."
      relationships:
        - The length of the output_sequence is equal to the length of the input_sequence.
        - The number of '1's in the output_sequence is equal to the non_zero_count (N) derived from the input_sequence.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of integers.
    2.  Count how many numbers in the input sequence are not zero. Let this count be `N`.
    3.  Determine the total length of the input sequence. Let this length be `L`.
    4.  Generate an output sequence consisting of `N` ones followed by `L - N` zeros.
    5.  Format the generated sequence as a space-separated string for the final output.