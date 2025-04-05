Okay, let's break down the transformation.

**Perception of Elements:**

*   The input and output are sequences of single digits.
*   The length of the sequence remains constant between input and output.
*   The core transformation involves reversing a part of the sequence.
*   Leading and trailing zeros in the input sequence appear to maintain their positions relative to the start and end of the sequence.
*   The segment of the sequence that lies *between* the contiguous block of leading zeros and the contiguous block of trailing zeros is reversed. If there are no leading or trailing zeros, the entire sequence (or the relevant part determined by the first/last non-zero element) is reversed.

**YAML Facts:**


```yaml
task_elements:
  - object: sequence
    properties:
      - type: list_of_integers
      - length: fixed (12 in examples)
      - contains: single digits (0-9)
  - object: leading_zeros
    properties:
      - type: sub-sequence
      - location: start_of_sequence
      - content: only_zeros
      - relationship: precedes the core_segment
  - object: trailing_zeros
    properties:
      - type: sub-sequence
      - location: end_of_sequence
      - content: only_zeros
      - relationship: follows the core_segment
  - object: core_segment
    properties:
      - type: sub-sequence
      - location: between leading_zeros and trailing_zeros
      - content: contains all non-zero digits and any zeros interspersed within them
      - bounds: starts at the first non-zero digit, ends at the last non-zero digit
      - relationship: is acted upon by the primary transformation
actions:
  - action: identify_boundaries
    inputs: input_sequence
    outputs:
      - index_first_non_zero
      - index_last_non_zero
    description: Find the start and end indices of the core_segment. Handle cases where the sequence might be all zeros.
  - action: segment_sequence
    inputs:
      - input_sequence
      - index_first_non_zero
      - index_last_non_zero
    outputs:
      - leading_zeros_segment
      - core_segment
      - trailing_zeros_segment
    description: Split the input sequence into three parts based on the identified boundaries.
  - action: reverse_segment
    inputs: core_segment
    outputs: reversed_core_segment
    description: Reverse the order of elements within the core_segment.
  - action: concatenate_segments
    inputs:
      - leading_zeros_segment
      - reversed_core_segment
      - trailing_zeros_segment
    outputs: output_sequence
    description: Combine the segments in order (leading, reversed core, trailing) to form the final output sequence.
relationships:
  - type: positional_invariance
    elements: [leading_zeros, trailing_zeros]
    description: The leading and trailing zero segments maintain their position and content in the output relative to the sequence boundaries.
  - type: transformation
    elements: [core_segment]
    action: reverse_segment
    description: The core_segment is the target of the reversal operation.
```


**Natural Language Program:**

1.  Receive the input sequence of digits.
2.  Identify the index of the first non-zero digit (`start_index`). If no non-zero digits exist, the sequence remains unchanged; return the original sequence.
3.  Identify the index of the last non-zero digit (`end_index`).
4.  Extract the sub-sequence from the beginning of the input up to (but not including) `start_index`. This is the `prefix` (leading zeros).
5.  Extract the sub-sequence from `start_index` up to and including `end_index`. This is the `middle` segment.
6.  Extract the sub-sequence from the element after `end_index` to the end of the input. This is the `suffix` (trailing zeros).
7.  Reverse the order of the elements within the `middle` segment.
8.  Construct the output sequence by concatenating the `prefix`, the reversed `middle` segment, and the `suffix` in that order.
9.  Return the constructed output sequence.