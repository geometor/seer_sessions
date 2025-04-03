
## train_1

**input:**
```
0 0 0 5 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 4 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 3 1 1 1 1 1 1 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 3 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 8 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 8 0 0 0 0 0 0 0 0
```

**Perception of Elements:**

1.  **Grid Structure:** The examples primarily use 1D grids (or single rows within a potentially larger grid context, though presented flat).
2.  **Background:** The dominant color is white (0), acting as the background.
3.  **Objects:** Each input contains a single contiguous sequence of non-white pixels. This sequence appears to be the main object of interest.
4.  **Object Structure:** Within this non-white sequence, there are two distinct parts:
    *   A single "head" pixel at the beginning of the sequence (leftmost in the 1D representation).
    *   A contiguous "body" sequence of pixels immediately following the head, all having the same color, which is different from the head's color.
5.  **Transformation:** The core transformation involves rearranging the pixels within this non-white sequence. Specifically, the "head" pixel is moved from the start of the sequence to the end of the sequence. The "body" pixels shift one position to the left to occupy the space vacated by the head. The background pixels remain unchanged.

**YAML Facts:**


```yaml
task_description: Rearrange pixels within a specific sequence structure found in a 1D grid.

grid_properties:
  dimensionality: Primarily 1D (or single rows).
  background_color: white (0)

objects:
  - type: sequence
    description: A contiguous block of non-white pixels surrounded by white pixels.
    properties:
      - structure: Composed of a 'head' pixel and a 'body' sequence.
      - head:
          - count: 1
          - position: Start (leftmost) of the sequence.
          - color: Distinct from the body color.
      - body:
          - count: Variable (>= 1)
          - position: Immediately follows the head pixel.
          - color: Uniform color, different from the head color.
          - contiguity: Forms a single block.

actions:
  - name: identify_sequence
    description: Locate the contiguous block of non-white pixels.
  - name: identify_components
    description: Distinguish the 'head' pixel from the 'body' sequence within the non-white block.
  - name: relocate_head
    description: Move the 'head' pixel from the start to the end of the sequence space.
  - name: shift_body
    description: Move the 'body' sequence one position towards the original start (left) to fill the gap left by the head.

relationships:
  - type: adjacency
    description: The head pixel is initially adjacent to the start of the body sequence.
  - type: order_change
    description: The relative order of the head and body is reversed in the output compared to the input. Head moves from before the body to after the body.

constraints:
  - The transformation only applies if the identified non-white sequence has a single head pixel followed by a body sequence of uniform color different from the head.
  - The background remains unchanged.
```


**Natural Language Program:**

1.  Find the contiguous sequence of non-white pixels in the input grid.
2.  Identify the first pixel of this sequence (the 'head') and the subsequent pixels (the 'body').
3.  Check if the 'body' consists of one or more pixels, all having the same color, and if this color is different from the 'head' pixel's color.
4.  If these conditions are met, construct the output grid as follows:
    a.  Copy the portion of the input grid before the non-white sequence.
    b.  Append the 'body' sequence.
    c.  Append the 'head' pixel.
    d.  Copy the portion of the input grid after the non-white sequence.
5.  If the conditions in step 3 are not met, the output grid is identical to the input grid (although this case isn't explicitly shown in the examples, it's a reasonable default).
