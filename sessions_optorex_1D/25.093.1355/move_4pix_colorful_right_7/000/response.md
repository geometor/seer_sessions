*   **Perception:** The task operates on fixed-length sequences of 12 integers. Each input sequence contains a single contiguous block of non-zero integers, surrounded by zeros. The transformation involves relocating this non-zero block within the sequence while preserving the block itself and the surrounding zeros. The core action is a rightward shift of the non-zero block by a fixed amount.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input_type: list_of_integers
    output_type: list_of_integers
    sequence_length: 12
    elements:
      - type: zero
        role: padding/background
      - type: non_zero_block
        description: A contiguous subsequence of non-zero integers.
        properties:
          - content: the sequence of non-zero integers
          - start_index_input: the index where the block begins in the input
          - length: the number of elements in the block
    action:
      type: shift
      direction: right
      amount: 4
      target: non_zero_block
    relationship: The output sequence is constructed by taking the input sequence, identifying the non_zero_block, and placing it in a new sequence (initially all zeros) starting at `start_index_input + 4`. The relative order of elements within the non_zero_block is preserved.
    constraints: Assumes only one contiguous non-zero block exists in the input. Assumes the shifted block fits within the sequence length of 12.
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of length 12 with all zeros.
    2.  Scan the input sequence to find the first non-zero integer. Record its index as `start_index`.
    3.  Continue scanning from `start_index` to find the end of the contiguous block of non-zero integers. Record this block of numbers as the `payload`.
    4.  Calculate the `target_start_index` by adding 4 to the `start_index`.
    5.  Place the `payload` into the output sequence, starting at the `target_start_index`.
    6.  Return the output sequence.