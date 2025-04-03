*   **Perception of task elements:**
    *   The input and output data are presented as 1D sequences of integers (colors). The length of the sequence is consistent across inputs and outputs in the examples (31 elements).
    *   The sequence contains segments of non-white (non-zero) colors interspersed with white (zero) background pixels.
    *   Within the non-white segments, there can be multiple different colors present.
    *   The transformation modifies the colors *within* the non-white segments, leaving the white background pixels unchanged.

*   **YAML Fact Document:**
    
```yaml
    task_type: color_manipulation_1d
    components:
      - element: sequence
        attributes:
          - type: 1D array of integers (colors)
          - length: consistent between input and output (e.g., 31)
      - element: pixel
        attributes:
          - type: color (integer 0-9)
          - role: background (color 0 - white) or foreground (colors 1-9)
      - element: segment
        description: A contiguous subsequence of non-background (non-white) pixels bounded by background (white) pixels or the sequence ends.
        properties:
          - host_color: The dominant or defining color of the segment, specifically the color encountered when entering the segment from the background.
          - intruder_colors: Any non-background colors within the segment that are different from the host color.
    actions:
      - name: identify_segments
        input: input sequence
        output: list of segments with their start/end indices and host colors
      - name: homogenize_segment
        input: segment, host_color
        output: modified segment where all non-background pixels are replaced by the host_color
    relationships:
      - type: spatial
        description: Contiguity of pixels defines segments.
      - type: modification
        description: Intruder colors within a segment are replaced by the segment's host color. Background pixels remain unchanged.
    constraints:
      - Background color (0) acts as a delimiter and is never changed.
      - Only non-background colors within a segment are subject to modification.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty output sequence of the same length as the input sequence.
    2.  Initialize a variable `host_color` to `None` (or a sentinel value indicating not currently inside a non-background segment).
    3.  Iterate through each pixel of the input sequence at index `i` with color `c`:
        a.  If the current pixel color `c` is white (0):
            i.  Set the corresponding pixel in the output sequence to white (0).
            ii. Reset `host_color` to `None`, indicating the end of any current segment.
        b.  If the current pixel color `c` is not white (non-zero):
            i.  If `host_color` is `None` (meaning this is the first non-white pixel encountered after a white pixel or at the start of the sequence):
                - Set `host_color` to the current pixel's color `c`.
                - Set the corresponding pixel in the output sequence to `c`.
            ii. Else (if `host_color` is already set, meaning we are inside a non-white segment):
                - Set the corresponding pixel in the output sequence to the current `host_color`.
    4.  Return the completed output sequence.