*   **Perception**:
    *   The input and output grids are single rows.
    *   Each input row contains a single contiguous horizontal segment (object) of a non-white color, surrounded by white pixels (color 0).
    *   The non-white colors observed are azure (8), green (3), and orange (7).
    *   The output is identical to the input, except the colored segment is shifted one position to the right.
    *   The length of the colored segment and the overall row length remain unchanged.

*   **Facts**:
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D (single row)
    background_color: white (0)
    objects:
      - type: segment
        count: 1
        description: A contiguous horizontal block of a single non-white color.
        properties:
          color: varies (azure, green, orange observed)
          length: varies
    actions:
      - name: shift
        target: the non-white segment
        direction: right
        distance: 1 position
    relationships:
      - The non-white segment is surrounded by the background color.
      - The transformation preserves the segment's color and length.
      - The transformation preserves the grid's overall dimensions.

    ```


*   **Natural Language Program**:
    1.  Identify the contiguous segment of non-white pixels within the input row.
    2.  Determine the starting position (index) of this segment.
    3.  Create a new row of the same length as the input, initially filled with the background color (white, 0).
    4.  Copy the identified non-white segment into the new row, starting at an index one greater than its original starting index.