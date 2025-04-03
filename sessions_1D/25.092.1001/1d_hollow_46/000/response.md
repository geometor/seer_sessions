*   **Perception:**
    *   Each input is a 1D array (a single row) containing mostly white (0) pixels and a single contiguous block of non-white pixels (azure - 8 or red - 2).
    *   The non-white blocks vary in length and color across the examples.
    *   The output is also a 1D array of the same length as the input.
    *   In the output, the original contiguous block from the input is modified. Only the first and the last pixel of the original block retain their color. All pixels that were originally *between* the first and last pixel of the block are changed to white (0).
    *   If the block has only one pixel, that pixel remains unchanged in the output. (Although not explicitly shown, this is implied by keeping the 'first' and 'last', which are the same in this case).
    *   All pixels outside the original block remain white (0).

*   **YAML Facts:**
    
```yaml
    task_description: Retain only the endpoints of a single contiguous non-white horizontal segment.
    objects:
      - type: grid_row # Input and Output are 1D arrays representing a row
        properties:
          - length
          - pixels: list of color values (0-9)
      - type: segment # A contiguous block of non-white pixels within a row
        properties:
          - color: the single non-white color of the segment (e.g., azure, red)
          - start_index: the index of the first pixel in the segment
          - end_index: the index of the last pixel in the segment
          - length: number of pixels in the segment (end_index - start_index + 1)
    actions:
      - find: Locate the single contiguous segment of non-white pixels in the input row.
      - identify: Determine the start_index, end_index, and color of this segment.
      - create_output: Generate a new row of the same length as the input, initially filled with white (0).
      - preserve_endpoint: Copy the pixel color from the input row at the start_index of the segment to the output row at the same start_index.
      - preserve_endpoint: Copy the pixel color from the input row at the end_index of the segment to the output row at the same end_index. (Note: If length is 1, start_index equals end_index, and this step effectively does nothing extra).
    relationships:
      - input_output_dimensions: The output row has the same length as the input row.
      - modification_rule: The output row is identical to the input row except that all pixels within the identified segment, excluding the first and last pixels of that segment, are changed to white (0).
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block (segment) of non-white pixels in the input row.
    2.  Find the starting index and the ending index of this segment.
    3.  Create a new output row of the same length as the input row, filled entirely with white (0) pixels.
    4.  Copy the pixel value (color) from the input row at the starting index of the segment to the same index in the output row.
    5.  Copy the pixel value (color) from the input row at the ending index of the segment to the same index in the output row.
    6.  The resulting row is the final output.