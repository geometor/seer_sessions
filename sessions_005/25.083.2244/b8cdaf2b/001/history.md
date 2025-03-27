
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```


**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


## train_4

**input:**
```
0 0 0
0 2 0
2 4 2
```


**output:**
```
4 0 4
0 2 0
2 4 2
```

Okay, I'm ready to analyze the provided input-output examples and discern the underlying transformation logic. Here's my breakdown of the task:

**Perception of Elements:**

The task involves 2D grids of single-digit integers (0-9), representing different colors. The transformation seems to focus on modifying a specific object in the input grid, specifically the object defined by contiguous pixels of the largest-valued color, and copying its border one row/column up, mirroring the pixels on the border. The copied pixels take the colors of the border pixels. Other parts of the grid seem to stay the same. The examples seem to use different colors to represent the border.

**YAML Block - Facts:**


```yaml
facts:
  - observation: "Input and output grids have the same dimensions."
  - object: "Largest contiguous color block"
    properties:
      - "Defined by the highest single-digit value present in the grid (excluding 0)."
      - "Consists of one or more adjacent pixels of the same color."
    actions:
      - "Identified as the primary target for transformation."
  - object: "Top Border Pixels"
    properties:
      - The set of colors that build up the border of the "Largest contiguous color block"
    actions:
      - Copy values from the "Top Border Pixels" one row/column above the position, when possible. If the border extends to row 0, copy to the bottom if available, otherwise it stops.
  - relationship: "The rest of the grid (pixels not involved by the top border copy) remains unchanged."
```


**Natural Language Program:**

1.  **Identify the Target Object:** Find the contiguous block of pixels with the highest non-zero value in the input grid. This is the "target object."
2.  **Locate Top Border** Find the pixels that comprise the top border of the shape.
3.  **Copy Top Border:** Copy the colors to the row/column above the current location. If we are already in the top row (index 0), do not make a copy.
4.  **Preserve Other Pixels:** All other pixels in the grid that are not part of the border copying retain their original values.
5. **Output:** generate the output grid.


