**Perception of Elements:**

The core elements are sequences of integers. Each sequence represents a one-dimensional array or list of fixed length (12 in these examples). Within each input sequence, there are two distinct types of objects:
1.  **Background:** Represented by the integer `0`.
2.  **Foreground Object:** A contiguous block (run) of identical non-zero integers (e.g., `6 6 6`, `1 1 1 1`, `3 3 3`).

The transformation acts upon the entire sequence but specifically targets the foreground object. The output sequence retains the background and the foreground object, but the position of the foreground object changes relative to the background.

**Facts:**


```yaml
task_type: sequence_transformation
input_description: A list of 12 integers.
output_description: A list of 12 integers.
elements:
  - name: background_value
    value: 0
    role: fills the sequence outside the foreground object
  - name: foreground_object
    properties:
      - type: contiguous block of identical non-zero integers
      - value: the specific non-zero integer (e.g., 1, 3, 5, 6, 9)
      - length: number of elements in the block
      - start_index: position of the first element of the block in the input sequence
    role: the primary element being manipulated
relationships:
  - type: spatial
    description: The foreground_object is embedded within a sequence filled primarily with the background_value.
actions:
  - name: identify_foreground_object
    description: Locate the contiguous block of non-zero identical integers within the input sequence. Determine its value, start index, and length.
  - name: shift_object
    description: Move the identified foreground_object 4 positions to the left (decrease its start index by 4).
  - name: reconstruct_sequence
    description: Create the output sequence by placing the shifted foreground_object at its new position and filling all other positions with the background_value (0).
constants:
  - name: sequence_length
    value: 12
  - name: shift_amount
    value: -4 # (Shift left by 4 positions)
```


**Natural Language Program:**

1.  Initialize an output sequence of the same length as the input sequence, filled with zeros.
2.  Scan the input sequence to find the first non-zero integer. This marks the beginning of the foreground object.
3.  Identify the value and the full extent (start index and length) of this contiguous block of identical non-zero integers.
4.  Calculate the new start index for the foreground object in the output sequence by subtracting 4 from its start index in the input sequence.
5.  Place the identified foreground object (with its original value and length) into the output sequence starting at the calculated new start index.
6.  Return the modified output sequence.