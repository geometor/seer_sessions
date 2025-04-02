*   **Perception:**
    *   The input and output are presented as 1D arrays (or sequences) of colored pixels.
    *   Each example features a distinct non-white color (blue=1, magenta=6, maroon=9).
    *   In each input, there is an initial horizontal sequence of three identical non-white pixels (`C C C`).
    *   Elsewhere in the input, there are single instances of the same color `C`, typically surrounded by white pixels (`0 C 0`).
    *   The transformation identifies the color `C` from the initial `C C C` pattern.
    *   It then finds all occurrences of the pattern `0 C 0` later in the sequence.
    *   For each `0 C 0` found, the two white pixels (0) are changed to the color `C`, resulting in `C C C`.
    *   Pixels not part of the initial `C C C` pattern or the modified `0 C 0` patterns remain unchanged.

*   **Facts:**
    
```yaml
    task_type: pattern_replication_1d
    
    elements:
      - element: pixel
        properties:
          - color: (0-9, represented by integers)
          - position: (index in the 1D array)
      - element: pattern
        properties:
          - type: initial_trigger
            value: sequence of three identical non-white pixels (C C C)
            role: defines the target color 'C'
          - type: target_isolated
            value: sequence (0 C 0), where C is the color from initial_trigger
            role: identifies locations for modification
          - type: replacement
            value: sequence (C C C)
            role: replaces target_isolated patterns
    
    transformation:
      - action: identify_color
        inputs: input_array
        steps:
          - Find the first sequence of three identical non-white pixels (C C C).
          - Store the color 'C'.
        outputs: color 'C'
    
      - action: find_and_replace
        inputs: 
          - input_array
          - color 'C'
        steps:
          - Create a copy of the input array for modification.
          - Iterate through the input array (indices i from 1 to length-2).
          - If input_array[i] == C AND input_array[i-1] == 0 AND input_array[i+1] == 0:
            - Mark indices i-1 and i+1 for modification.
          - After iterating, change all marked indices in the copied array to color 'C'.
        outputs: modified_array
    
    relationships:
      - The color 'C' of the isolated pixels ('0 C 0') must match the color of the initial trigger pattern ('C C C').
      - The modification happens by changing the immediate neighbors of the isolated 'C' pixel *if* they are white (0).
    
    constraints:
      - Input/Output are 1D arrays.
      - Assumes exactly one initial trigger pattern 'C C C' exists to define 'C'.
      - Assumes isolated pixels 'C' are always flanked by white pixels ('0 C 0') for the transformation to apply.
    ```


*   **Natural Language Program:**
    1.  Identify the primary non-white color (`C`) by finding the first sequence of three consecutive identical non-white pixels in the input array.
    2.  Create a copy of the input array to store the output.
    3.  Iterate through the input array, examining each triplet of pixels at indices `i-1`, `i`, `i+1` (where `i` ranges from 1 to length-2).
    4.  If a triplet matches the pattern `white, C, white` (i.e., `0, C, 0`), then in the output array, change the pixels at indices `i-1` and `i+1` to color `C`.
    5.  Return the modified output array.