*   **Perception of task elements:**
    *   The input and output are sequences of numerical digits, presented as space-separated strings.
    *   The length of the sequence is consistently 12 digits in all provided examples.
    *   The digits present in the input are the same as the digits in the output, indicating a rearrangement or permutation rather than addition, subtraction, or replacement of digits.
    *   Comparing input and output sequences, a specific pattern of rearrangement emerges: the last four digits of the input sequence are moved to the beginning of the output sequence, while the remaining preceding digits follow in their original relative order.

*   **YAML Facts:**
    
```yaml
    task_description: Rearrange a sequence of digits by moving the last segment to the front.
    input_data:
      type: string
      format: space-separated digits
      length: 12
      elements: digits (0-9)
    output_data:
      type: string
      format: space-separated digits
      length: 12
      elements: digits (0-9)
      relationship_to_input: rearrangement
    transformation:
      action: block_move
      source_block:
        location: end_of_sequence
        length: 4 elements
      destination_block_location: start_of_sequence
      preserved_properties:
        - element_identity
        - total_length
        - relative_order_within_moved_block
        - relative_order_within_remaining_block
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 space-separated digits.
    2.  Split the input sequence into two parts: the first 8 digits (Part A) and the last 4 digits (Part B).
    3.  Construct the output sequence by placing Part B at the beginning, followed immediately by Part A.
    4.  Format the resulting sequence as a space-separated string.