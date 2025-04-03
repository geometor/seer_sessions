
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 4 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 8 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 8 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 8 9 9 9 9 9 9 9 9 9 9 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 9 9 9 9 9 9 9 9 9 9 8 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output are single rows (1D grids) of pixels.
    *   Each example contains a single contiguous block of non-white (non-zero) pixels surrounded by white (zero) pixels.
    *   This non-white block consists of two distinct colors: a single pixel of one color at the beginning, followed by a sequence of one or more pixels of a second color.
    *   The transformation moves the initial single pixel to the end of the sequence of the second color.
    *   The surrounding white pixels remain unchanged in their positions.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    components:
      - name: background
        type: pixels
        properties:
          color: white (0)
          location: surrounding the active sequence
      - name: active_sequence
        type: object (contiguous non-white pixels)
        properties:
          location: embedded within the background
          composition: consists of two parts:
            - marker_pixel: the first pixel in the sequence (unique color within sequence)
            - body_pixels: the remaining pixels in the sequence (all of the same color)
    transformation:
      action: rearrangement
      target: active_sequence
      rule: move the marker_pixel to the position immediately following the last body_pixel
      constraints: the background pixels remain unchanged
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous sequence of non-white pixels in the input row. Define this as the "active sequence". Note its start and end indices.
    2.  Isolate the first pixel of the "active sequence". This is the "marker pixel".
    3.  Isolate the remaining pixels of the "active sequence" (from the second pixel to the end). This is the "body sequence".
    4.  Create a new sequence by concatenating the "body sequence" followed by the "marker pixel". This is the "transformed sequence".
    5.  Construct the output row by taking the portion of the input row before the "active sequence", appending the "transformed sequence", and then appending the portion of the input row after the "active sequence".
