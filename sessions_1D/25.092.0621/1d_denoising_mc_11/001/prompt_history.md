
## train_1

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 8 7 7 7 7 7 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 1 1 1 8 1 1 1 1 1 1 1 7 5 1 1 1 1 2 1 1 1 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
```


## train_3

**input:**
```
5 5 5 5 5 5 5 5 3 5 5 8 8 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0
```

*   **Perception:**
    The input and output are single rows (1D grids). Each row consists of three parts: leading white pixels (color 0), a central segment of non-white pixels, and trailing white pixels. The central segment contains primarily one color, which acts as a background or dominant color for that segment. Scattered within this dominant color sequence are a small number of pixels of different colors ("noise" pixels). The transformation modifies only the central, non-white segment. Specifically, it identifies the dominant color within this segment and replaces all other non-white pixels ("noise" pixels) with this dominant color, effectively smoothing the segment to a single color. The leading and trailing white pixels remain unchanged.

*   **Facts:**
    
```yaml
    task_type: noise_reduction_1d
    elements:
      - role: border
        properties:
          color: white (0)
          location: flanking the central segment (leading and trailing)
      - role: segment
        properties:
          location: central part of the row, between borders
          composition: contains non-white pixels
      - role: dominant_color_pixel
        properties:
          color: the most frequent non-white color within the segment
          location: within the central segment
      - role: noise_pixel
        properties:
          color: any non-white color within the segment that is not the dominant color
          location: within the central segment, interspersed among dominant color pixels
    actions:
      - name: identify_segment
        inputs: input_row
        outputs: central non-white segment
        description: Isolate the contiguous sequence of non-white pixels, ignoring leading/trailing white pixels.
      - name: determine_dominant_color
        inputs: central_segment
        outputs: dominant_color
        description: Find the color that appears most frequently within the identified segment.
      - name: replace_noise
        inputs:
          - input_row
          - central_segment
          - dominant_color
        outputs: output_row
        description: Iterate through the central segment in the input row. Replace any pixel whose color is not white (0) and not the dominant color with the dominant color. Leave dominant color pixels and border pixels unchanged.
    relationships:
      - type: frequency
        description: The dominant color is determined by its frequency within the non-white segment.
      - type: containment
        description: Noise pixels are contained within the sequence of dominant color pixels in the central segment.
      - type: adjacency
        description: Noise pixels are often adjacent to dominant color pixels.
      - type: transformation_target
        description: Only noise pixels within the central segment are targeted for replacement.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous central segment of non-white pixels in the input row, ignoring any leading or trailing white (0) pixels.
    2.  Determine the dominant color within this central segment by finding the non-white color that occurs most frequently.
    3.  Create the output row by copying the input row.
    4.  Iterate through the pixels of the identified central segment in the output row.
    5.  For each pixel in the segment, if its color is not white (0) and not the dominant color, change its color to the dominant color.
    6.  Leave all white pixels and pixels already matching the dominant color unchanged.
