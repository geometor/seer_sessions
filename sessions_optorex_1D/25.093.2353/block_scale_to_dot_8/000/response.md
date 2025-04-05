*   **Perception of Task Elements:**
    *   The input and output are 1-dimensional sequences (arrays) of single-digit integers.
    *   The sequences contain three main types of elements:
        *   Zeros (`0`): Seemingly representing empty or background space.
        *   A single unique marker (`2`): Acts as a boundary or anchor point.
        *   Blocks of other identical digits (e.g., `4 4 4`, `8 8 8`, `1 1 1`): These are the 'fill numbers'.
    *   The core transformation involves the 'fill number' expanding to fill adjacent zeros (`0`).
    *   This expansion is directional and stops when it reaches the marker `2`.
    *   The expansion occurs in the space *between* the original block of the 'fill number' and the marker `2`.
    *   If the 'fill number' block is already directly adjacent to the marker `2`, no changes occur.
    *   Zeros outside the region between the 'fill number' block and the marker `2` remain unchanged.

*   **Facts:**
    
```yaml
    elements:
      - type: sequence
        description: A 1D array of single-digit integers.
      - type: integer
        value: 0
        role: background/empty_space
      - type: integer
        value: 2
        role: boundary_marker
        cardinality: exactly_one
      - type: integer
        value: non_zero_non_2_digit
        role: fill_number
        property: occurs_in_contiguous_blocks
    relationships:
      - type: spatial
        description: The fill_number block is separated from the boundary_marker (2) by zero or more background spaces (0).
    actions:
      - name: fill_gap
        input: sequence
        output: sequence
        condition: There are background spaces (0) between a fill_number block and the boundary_marker (2).
        steps:
          - Identify the index of the boundary_marker (2).
          - Identify the indices corresponding to the contiguous block of the fill_number closest to the boundary_marker (2).
          - Determine the range of indices strictly between the boundary_marker (2) and the edge of the fill_number block facing the marker.
          - Iterate through the elements within this determined range in the input sequence.
          - If an element in this range is a background space (0), change its value to the fill_number.
        effect: The background spaces (0) between the fill_number block and the boundary_marker (2) are replaced by the fill_number. If no such spaces exist, the sequence remains unchanged.

    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of digits.
    2.  Locate the unique boundary marker digit `2` in the sequence and note its index (`marker_index`).
    3.  Identify the non-zero, non-`2` digit (the `fill_number`) that forms a contiguous block closest to the `marker_index` (either immediately to its left or right, potentially separated only by zeros).
    4.  Find the index of the `fill_number` digit within its block that is nearest to `marker_index`. Let this be `fill_edge_index`.
    5.  Define the `start_index` as the minimum of `marker_index` and `fill_edge_index`, plus 1.
    6.  Define the `end_index` as the maximum of `marker_index` and `fill_edge_index`.
    7.  Iterate through the sequence from `start_index` up to (but not including) `end_index`.
    8.  For each element at the current index in this range, if the element's value is `0`, change its value to the `fill_number`.
    9.  Return the modified sequence.