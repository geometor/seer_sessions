
## train_1

**input:**
```
0 0 7 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 3 3 3 3 7 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 2 2 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 4 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 2 1 1 1 1 1 1 1 1 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 2 0 0 0
```

*   **Perception:**
    *   The input and output grids are single rows.
    *   Each input grid contains a contiguous sequence of non-white pixels surrounded by white pixels (color 0).
    *   Within this non-white sequence, the first pixel has a unique color, and the subsequent pixels all share a different, repeating color.
    *   The transformation modifies only the non-white sequence.
    *   The first pixel of the non-white sequence is moved to the end of that sequence. The rest of the sequence shifts one position to the left to fill the gap.
    *   Alternatively, the transformation can be seen as swapping the first and the last pixels within the contiguous non-white sequence.

*   **Facts:**
    
```yaml
    task_type: transformation
    grid_dimensionality: 1D (single row)
    objects:
      - type: background
        color: white (0)
        location: surrounds the non-white sequence
      - type: sequence
        color: non-white
        location: contiguous block within the row
        properties:
          - composition: contains exactly two distinct non-white colors
          - structure:
              - starts with a single pixel of one color (color_A)
              - followed by one or more pixels of a second color (color_B)
    actions:
      - action: modify_sequence
        target: non-white sequence
        effect: swap the first and last pixels of the sequence
    relationships:
      - The non-white sequence is always contiguous.
      - The position and color of the background (white pixels) remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous sequence of non-white pixels in the input row.
    2.  If no non-white sequence is found, return the input unchanged.
    3.  Within the identified non-white sequence, swap the color value of the first pixel with the color value of the last pixel.
    4.  Keep all other pixels (including the surrounding white pixels and the intermediate pixels within the non-white sequence) in their original relative positions.
    5.  Construct the output row using the modified sequence and the unchanged surrounding pixels.
