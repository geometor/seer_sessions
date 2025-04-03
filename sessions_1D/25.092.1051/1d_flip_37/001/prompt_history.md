
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 8 7 7 7 7 7 7 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 8 0 0 0
```


## train_2

**input:**
```
8 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6 6 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 4 6 6 6 6 6 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 6 6 6 4 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

## Perception

1.  **Input Structure:** The inputs are single-row grids (1D arrays).
2.  **Content:** Each input primarily consists of white pixels (0). There is a single contiguous segment of non-white pixels within each row.
3.  **Non-White Segment:** This segment is composed of two distinct non-white colors. One color appears only once (let's call it the 'head'), and the other color appears multiple times consecutively (let's call it the 'body'). The head pixel is always located at one end of the body segment.
4.  **Transformation:** The core transformation involves repositioning the 'head' pixel. In the output, the head pixel is moved to the opposite end of the 'body' segment.
5.  **Preservation:** The colors themselves, the length of the body segment, and the surrounding white pixels remain unchanged. The overall position of the non-white segment within the row is also preserved.

## Facts


```yaml
task_type: object_manipulation
grid_dimensionality: 1D (row)
background_color: white (0)
objects:
  - name: colored_segment
    description: A single contiguous block of non-white pixels.
    properties:
      colors: Exactly two distinct non-white colors.
      structure: Consists of two parts:
        - name: head
          description: A single pixel of one color.
          location: At one end of the segment.
        - name: body
          description: Multiple contiguous pixels of the second color.
          location: Adjacent to the head.
    count_per_example: 1
actions:
  - name: move_head
    object: colored_segment
    description: The head pixel is moved from its original end of the body segment to the opposite end.
    details:
      - The sequence of body pixels remains unchanged relative to each other.
      - The head pixel retains its color.
      - The body pixels retain their color.
      - The overall start and end position of the reconstructed segment within the row remains the same as the original segment.
relationships:
  - type: adjacency
    between: head, body
    description: The head pixel is directly adjacent to the body segment in the input.
  - type: order_reversal
    target: head position relative to body
    description: The position of the head relative to the body segment is reversed (e.g., from leading to trailing, or vice-versa).
invariants:
  - Background pixels (white) remain unchanged.
  - The colors used for the head and body remain the same.
  - The number of body pixels remains the same.
  - The total length of the colored segment remains the same.
  - The position of the segment within the row (start and end indices) remains the same.
```


## Natural Language Program

1.  Identify the contiguous segment of non-white pixels in the input row.
2.  Within this segment, identify the unique 'head' pixel (the color that appears only once) and the repeated 'body' pixels (the color that appears multiple times). Note the color and count of the body pixels.
3.  Determine the position (start and end indices) of the non-white segment in the original row.
4.  Construct the output row:
    a.  Keep all white pixels outside the segment's original position unchanged.
    b.  Reconstruct the segment at its original position by placing the sequence of 'body' pixels first, followed immediately by the single 'head' pixel. Ensure the total length and position match the original segment. If the head was originally at the beginning of the segment, place it at the end in the output. If it was originally at the end, place it at the beginning in the output.
