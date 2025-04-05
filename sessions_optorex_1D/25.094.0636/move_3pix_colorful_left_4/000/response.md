*   **Perception:** The task involves rearranging a sequence of single digits. Both input and output sequences consist of digits separated by spaces. The core operation appears to involve identifying a contiguous block of non-zero digits within the input and shifting this block to the left by a fixed amount (3 positions), padding the remaining spaces with zeros. The length of the sequence remains constant.

*   **Facts:**
    
```yaml
    task_elements:
      - item: sequence
        properties:
          - type: list of digits
          - separator: space
          - length: constant (12 in examples)
      - item: digit
        properties:
          - type: integer
          - range: 0-9
      - item: zero_digit
        properties:
          - value: 0
          - role: padding or placeholder
      - item: non_zero_digit
        properties:
          - value: 1-9
          - role: content to be shifted
      - item: non_zero_block
        properties:
          - type: contiguous subsequence
          - composition: consists only of non_zero_digits
          - location: bounded by zeros or sequence ends
      - item: transformation
        properties:
          - type: positional shift
          - target: the first contiguous non_zero_block
          - direction: left
          - magnitude: 3 positions
          - boundary_condition: shift stops at the beginning of the sequence (index 0)
          - padding: zeros fill vacated and remaining positions
    relationships:
      - The output sequence is derived from the input sequence by repositioning the first contiguous block of non-zero digits.
      - The relative order of digits within the non_zero_block is preserved.
      - The total number of each non-zero digit remains the same between input and output.
      - The number and position of zeros change based on the shift operation.
    ```


*   **Natural Language Program:**
    1.  Identify the input sequence of digits.
    2.  Locate the starting index of the first non-zero digit in the sequence. If no non-zero digits exist, the sequence remains unchanged.
    3.  Locate the ending index of the contiguous block of non-zero digits that starts at the identified starting index (i.e., find the index of the first zero that appears after the start of the block, or the end of the sequence if no zero follows).
    4.  Extract this contiguous block of non-zero digits.
    5.  Calculate the target starting index for this block in the output sequence by subtracting 3 from its original starting index. If the result is negative, use 0 as the target starting index.
    6.  Construct the output sequence, having the same total length as the input sequence:
        *   Initialize the output sequence with all zeros.
        *   Place the extracted non-zero block into the output sequence, starting at the calculated target starting index.
    7.  Format the resulting sequence of digits into a space-separated string.