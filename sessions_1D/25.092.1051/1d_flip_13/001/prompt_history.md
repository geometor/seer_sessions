
## train_1

**input:**
```
0 0 0 0 0 7 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 7 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 7 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 1 0 0 0 0 0 0 0 0 0
```

**Perception:**

The task operates on 1-dimensional grids (or single rows). Each input grid contains a single contiguous segment of non-white pixels, surrounded by white pixels (0). Within this non-white segment, there is always exactly one pixel of a unique color, while the rest of the pixels in the segment share another, different non-white color. The transformation involves swapping the position of the unique-colored pixel with the pixel at the opposite end of the non-white segment. The surrounding white pixels remain unchanged.

**Facts:**


```yaml
task_type: transformation
grid_dimensionality: 1D # Effectively 1xN grids
background_color: white (0)
objects:
  - type: contiguous_segment
    description: A sequence of non-white pixels bounded by white pixels.
    properties:
      - contains exactly one instance of a unique non-white color (the 'unique_pixel').
      - contains multiple instances of another non-white color (the 'repeating_pixel').
      - location: defined by start and end indices within the 1D grid.
pixels:
  - type: unique_pixel
    description: The pixel within the segment whose color appears only once.
    properties:
      - color: variable (e.g., orange(7) in train_1/2, blue(1) in train_3)
      - count_in_segment: 1
  - type: repeating_pixel
    description: The pixels within the segment whose color appears multiple times.
    properties:
      - color: variable (e.g., azure(8) in train_1, blue(1) in train_2, orange(7) in train_3)
      - count_in_segment: >1
  - type: boundary_pixel
    description: The pixel at the opposite end of the segment from the unique_pixel.
    properties:
      - color: initially the color of the repeating_pixel.
      - location: either the start or end index of the segment.
actions:
  - type: identify_segment
    description: Find the start and end indices of the contiguous non-white segment.
  - type: identify_unique_pixel
    description: Find the pixel within the segment whose color count is 1. Note its index and color.
  - type: identify_boundary_pixel
    description: Determine the index of the pixel at the opposite end of the segment relative to the unique_pixel. Note its index and color.
  - type: swap_pixels
    description: Exchange the colors of the unique_pixel and the boundary_pixel.
relationships:
  - The unique_pixel is always located at one of the ends (start or end) of the non-white segment.
  - The boundary_pixel is located at the other end of the segment.
invariance:
  - The white background pixels (0) remain unchanged.
  - The colors and count of the repeating_pixels (other than the one swapped) remain unchanged, only their relative position might shift slightly if the unique pixel was not originally adjacent to them.
  - The length of the non-white segment remains the same.
  - The overall grid dimensions remain the same.
```


**Natural Language Program:**

1.  Identify the contiguous sequence of non-white pixels in the input grid. Determine the start and end indices of this sequence (segment).
2.  Analyze the colors within this segment to find the color that appears only once. Record the index and color of this unique pixel.
3.  Identify the index of the pixel at the opposite end of the segment from the unique pixel. Record the index and color of this boundary pixel. (If the unique pixel is at the start index, the boundary pixel is at the end index, and vice-versa).
4.  Create the output grid as a copy of the input grid.
5.  In the output grid, place the color of the original boundary pixel at the index of the original unique pixel.
6.  In the output grid, place the color of the original unique pixel at the index of the original boundary pixel.
7.  Return the modified grid.
