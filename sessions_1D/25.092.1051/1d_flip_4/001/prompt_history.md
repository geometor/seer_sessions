
## train_1

**input:**
```
0 0 0 0 6 4 4 0 0 0
```


**output:**
```
0 0 0 0 4 4 6 0 0 0
```


## train_2

**input:**
```
0 0 0 7 8 8 8 8 0 0
```


**output:**
```
0 0 0 8 8 8 8 7 0 0
```


## train_3

**input:**
```
0 0 3 4 4 0 0 0 0 0
```


**output:**
```
0 0 4 4 3 0 0 0 0 0
```

*   **Perception**:
    *   The input and output are single rows of pixels.
    *   Each row contains a segment of non-white pixels surrounded by white pixels (color 0).
    *   Within the non-white segment, there are exactly two distinct colors present.
    *   One of these colors appears as a single pixel.
    *   The other color appears as a contiguous block of two or more pixels.
    *   The transformation involves swapping the position of the single pixel with the contiguous block of pixels within the non-white segment.
    *   The surrounding white pixels remain unchanged.

*   **Facts**:
    
```yaml
    task_type: object_manipulation
    input_dimensionality: 1D (single row)
    output_dimensionality: 1D (single row)
    background_color: white (0)
    objects:
      - type: contiguous_segment
        description: A sequence of non-white pixels within the row.
        properties:
          - contains_exactly_two_distinct_non_white_colors
      - type: single_pixel
        description: A pixel of one non-white color that appears exactly once within the non-white segment.
        relationship: adjacent_to the contiguous_block
      - type: contiguous_block
        description: A sequence of two or more identical non-white pixels within the non-white segment.
        relationship: adjacent_to the single_pixel
    actions:
      - action: identify
        target: non_white_segment
        details: Find the start and end indices of the contiguous block of non-white pixels.
      - action: identify
        target: single_pixel
        within: non_white_segment
        details: Find the unique pixel color and its position within the segment.
      - action: identify
        target: contiguous_block
        within: non_white_segment
        details: Find the repeating pixel color, its start position, and its end position within the segment.
      - action: swap
        target1: single_pixel
        target2: contiguous_block
        details: Exchange the positions of the single pixel and the contiguous block within the bounds of the original non_white_segment.
    constraints:
      - The relative order of the single_pixel and contiguous_block is reversed in the output compared to the input.
      - The surrounding white pixels (color 0) remain fixed.
      - The length of the row remains unchanged.
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous sequence of non-white pixels in the input row. Determine its start and end indices.
    2.  Within this non-white sequence, identify the two distinct objects: a single pixel of one color and a contiguous block of pixels of another color.
    3.  Create a new row identical to the input row.
    4.  Place the contiguous block object into the position previously occupied by the single pixel object within the identified sequence range in the new row.
    5.  Place the single pixel object into the position previously occupied by the contiguous block object within the identified sequence range in the new row.
    6.  Ensure all other pixels (the surrounding white pixels) remain in their original positions.
    7.  The resulting row is the output.
