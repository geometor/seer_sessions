
## train_1

**input:**
```
0 0 2 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 4 2 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 4 7 7 7 0 0
```


**output:**
```
0 0 0 0 0 0 7 7 7 4 0 0
```


## train_3

**input:**
```
0 0 0 5 7 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 7 7 7 7 5 0 0 0 0
```

Okay, let's break down the perception, facts, and the natural language program for this task.

**Perception of the Elements:**

*   The input and output are single rows (1D grids).
*   Each row contains mostly white (0) pixels.
*   Crucially, each input row contains exactly two distinct non-white elements:
    1.  A single pixel of one color (e.g., red in example 1, yellow in example 2, gray in example 3).
    2.  A contiguous horizontal block of pixels of *another* color (e.g., yellow block in example 1, orange block in examples 2 and 3).
*   These two non-white elements are always directly adjacent to each other.
*   The single pixel is always immediately to the left of the block of pixels.
*   The transformation appears to swap the positions of the single pixel and the adjacent block. The single pixel moves to occupy the position immediately to the right of where the block was, and the block shifts left to occupy the original position of the single pixel. The surrounding white pixels remain unchanged.

**YAML Facts:**


```yaml
task_description: Swap the positions of an adjacent single pixel and a contiguous block of pixels.
elements:
  - type: grid
    dimensionality: 1D (single row)
  - type: background_pixel
    color: white (0)
    role: Fills space around active elements.
  - type: active_element_1
    description: A single non-white pixel.
    properties:
      - count: 1 per input grid
      - color: variable (red, yellow, gray in examples)
  - type: active_element_2
    description: A contiguous horizontal block of non-white pixels.
    properties:
      - count: 1 per input grid
      - color: variable, different from active_element_1 (yellow, orange in examples)
      - length: variable (5 in example 1, 3 in example 2, 4 in example 3)
relationships:
  - type: adjacency
    element1: active_element_1
    element2: active_element_2
    details: Element 1 is immediately to the left of Element 2.
transformation:
  action: swap_position
  elements: [active_element_1, active_element_2]
  details:
    - Locate the single pixel (Element 1) and the adjacent block (Element 2).
    - Determine the color and index of Element 1.
    - Determine the color, starting index, and length of Element 2.
    - In the output grid, place the block (Element 2) starting at the original index of Element 1.
    - Place the single pixel (Element 1) immediately to the right of where the block (Element 2) was originally placed.
    - Maintain the position of all background (white) pixels.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through the input grid from left to right to find the first non-white pixel. Let its color be `color_A` and its index be `index_A`.
3.  Continue iterating from `index_A + 1` to find the start of the contiguous block of a different non-white color. Let this color be `color_B` and the starting index be `index_B` (which will always be `index_A + 1`).
4.  Determine the length (`length_B`) of the contiguous block of `color_B` starting at `index_B`.
5.  Modify the output grid:
    a.  Place `length_B` pixels of `color_B` starting at `index_A`.
    b.  Place a single pixel of `color_A` at index `index_A + length_B`.
6.  Return the modified output grid.
