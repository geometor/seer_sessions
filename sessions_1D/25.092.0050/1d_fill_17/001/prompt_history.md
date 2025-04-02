
## train_1

**input:**
```
0 0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
```


**output:**
```
0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
```


## train_2

**input:**
```
0 0 0 2 0 0 0 0 0 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0
```


## train_3

**input:**
```
0 0 0 0 0 5 0 0 0 0 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 5 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The inputs and outputs are single rows (1D grids).
    *   Each input row contains exactly two pixels of the same non-white color (e.g., green, red, gray), separated by one or more white pixels. The rest of the row consists of white pixels.
    *   The output row is identical to the input row, except that the white pixels located *between* the two non-white pixels are changed to match the color of those non-white pixels.
    *   The non-white pixels act as boundary markers.
    *   The transformation fills the horizontal segment defined by these markers.

*   **YAML Facts:**
    
```yaml
    task_type: fill_segment
    grid_representation: 1D_array
    objects:
      - object: marker
        description: Two pixels of the same non-white color in the input row.
        properties:
          color: Identical non-white color (value > 0).
          count: 2
          position: Define the start and end points of a segment.
      - object: segment
        description: The pixels located strictly between the two marker pixels.
        properties_input:
          color: White (value = 0).
        properties_output:
          color: Same as the marker pixels.
      - object: background
        description: White pixels outside the segment defined by the markers.
        properties:
          color: White (value = 0).
          unchanged: True
    actions:
      - action: identify_markers
        description: Find the color and indices of the two non-white pixels.
      - action: fill_segment
        description: Change the color of the pixels between the identified marker indices to the marker color.
    relationships:
      - type: spatial
        description: The segment pixels lie horizontally between the marker pixels.
      - type: color_propagation
        description: The segment pixels adopt the color of the marker pixels in the output.
    ```


*   **Natural Language Program:**
    1.  Identify the non-white color present in the input row.
    2.  Find the index (position) of the first pixel with this non-white color.
    3.  Find the index (position) of the second (last) pixel with this non-white color.
    4.  Create the output row by copying the input row.
    5.  For every position between the first index (exclusive) and the second index (exclusive), change the pixel color in the output row to the identified non-white color.
    6.  Return the modified output row.
