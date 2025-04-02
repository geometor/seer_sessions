
## train_1

**input:**
```
0 0 0 0 0 0 8 8 8 8 0 0 0 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 8 8 8 8 8 8 9 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 9
```


**output:**
```
0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 9
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0 0 0 0 0 0 9 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 9 0 0
```

*   **Perception**:
    *   The inputs and outputs are single rows (1D grids).
    *   The background color is white (0).
    *   Each input contains exactly one contiguous segment (or block) of a non-white color (azure-8, green-3, orange-7).
    *   Each input also contains exactly one maroon (9) pixel.
    *   The colored segment and the maroon pixel are separated by one or more white (0) pixels.
    *   In the output, the space between the colored segment and the maroon pixel is filled with the color of the segment. The segment effectively "grows" or "extends" towards the maroon pixel until it reaches it.

*   **YAML Facts**:
    
```yaml
    task_elements:
      grid_dimensionality: 1D
      background_color: 0
      objects:
        - object_type: segment
          description: A contiguous block of a single color C, where C is not white (0) and not maroon (9).
          properties:
            color: C
            location: indices of the pixels in the segment
        - object_type: target_pixel
          description: A single pixel with maroon color (9).
          properties:
            color: 9
            location: index of the pixel
      relationships:
        - type: spatial
          description: The segment and the target_pixel are located on the same row, separated by one or more background (0) pixels.
      actions:
        - action_type: fill
          description: >
            Replace the background (0) pixels located between the end of the
            segment (the end closest to the target_pixel) and the target_pixel
            with the color C of the segment.
    ```


*   **Natural Language Program**:
    1.  Identify the background color, which is white (0).
    2.  Identify the target pixel color, which is maroon (9). Locate the single instance of the target pixel.
    3.  Identify the contiguous segment of a single color (let's call this color C) that is not the background color (0) and not the target color (9). Determine its start and end indices.
    4.  Find the indices of all background pixels that lie *between* the segment and the target pixel.
    5.  Change the color of these intermediate background pixels to the color C of the segment.
