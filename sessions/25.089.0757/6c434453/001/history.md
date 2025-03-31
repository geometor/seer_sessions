
## train_1

**input:**
```
0 0 0 0 1 1 1 0 0 0
1 1 0 0 1 0 1 0 0 0
1 1 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 1 1 1
0 1 1 1 0 0 0 0 1 0
0 1 0 1 0 0 0 0 0 0
0 1 1 1 0 0 1 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 0 0 0 0
1 1 0 0 2 2 2 0 0 0
1 1 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 1 1 1
0 0 2 0 0 0 0 0 1 0
0 2 2 2 0 0 0 0 0 0
0 0 2 0 0 0 1 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
1 1 1 0 0 0 0 0 0 0
1 0 1 0 0 0 0 1 0 0
1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
0 1 0 1 1 1 0 0 0 0
0 0 0 1 0 1 0 0 1 1
0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 1 0 0
0 2 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
0 1 0 0 2 0 0 0 0 0
0 0 0 2 2 2 0 0 1 1
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception of the Elements:**

1.  **Input Grids:** The input grids consist of a white (0) background with several distinct shapes made of blue (1) pixels. These shapes vary in form. Some specific shapes appear multiple times across the examples, notably a 3x3 hollow square (`[[1,1,1],[1,0,1],[1,1,1]]`).
2.  **Output Grids:** The output grids are modifications of the input grids. The background remains white (0). Most of the blue (1) shapes from the input remain unchanged in the output. However, specific blue shapes are transformed.
3.  **Transformation:** The core transformation seems to involve identifying a particular 3x3 pattern in the input and replacing it with another 3x3 pattern in the output. Specifically, the 3x3 hollow blue square pattern is replaced by a red (2) plus sign pattern (`[[0,2,0],[2,2,2],[0,2,0]]`). Pixels not part of this specific pattern matching and replacement remain identical to the input.
4.  **Object Identification:** The key object to identify is the 3x3 hollow blue square. Other blue shapes act as distractors or context but are not directly involved in the transformation.
5.  **Color Change:** The transformation involves changing blue (1) pixels to red (2) pixels within the matched pattern, and also changing the central white (0) pixel of the hollow square to red (2). Some blue pixels from the original pattern (the corners) become white (0) in the output.

**Facts:**


```yaml
Grid:
  background_color: 0 (white)
  relevant_colors: [1 (blue), 2 (red)]

Objects:
  - type: Pattern
    name: Target Pattern
    description: A 3x3 subgrid consisting of a blue (1) border around a white (0) center.
    representation:
      [[1, 1, 1],
       [1, 0, 1],
       [1, 1, 1]]
  - type: Pattern
    name: Replacement Pattern
    description: A 3x3 subgrid representing a red (2) plus sign on a white (0) background.
    representation:
      [[0, 2, 0],
       [2, 2, 2],
       [0, 2, 0]]
  - type: Shapes
    name: Other Blue Shapes
    description: Various contiguous blocks of blue (1) pixels that do not match the Target Pattern.
    properties:
      color: 1 (blue)

Actions:
  - action: Find
    target: All occurrences of the Target Pattern within the input grid.
  - action: Replace
    target: Each found Target Pattern occurrence.
    replacement: The Replacement Pattern.
    location: The replacement occurs at the exact same 3x3 coordinates as the found Target Pattern.

Relationships:
  - The transformation is local to the 3x3 areas matching the Target Pattern.
  - Pixels outside these matched 3x3 areas (including Other Blue Shapes and background pixels) remain unchanged between the input and output grids.
  - The transformation rule is consistent across all provided examples.
```


**Natural Language Program:**

1.  Initialize the output grid as an identical copy of the input grid.
2.  Define the target 3x3 pattern as a blue border with a white center: `[[1,1,1],[1,0,1],[1,1,1]]`.
3.  Define the replacement 3x3 pattern as a red plus sign: `[[0,2,0],[2,2,2],[0,2,0]]`.
4.  Scan the input grid by examining every possible 3x3 subgrid. Iterate through rows `r` from 0 to `height-3` and columns `c` from 0 to `width-3`.
5.  For each top-left coordinate (`r`, `c`), compare the 3x3 subgrid extracted from the input grid starting at (`r`, `c`) with the defined target pattern.
6.  If the extracted subgrid exactly matches the target pattern, modify the *output* grid by replacing the 3x3 area starting at (`r`, `c`) with the defined replacement pattern.
7.  Continue scanning until all possible 3x3 subgrids in the input have been checked.
8.  The final state of the output grid is the result of the transformation.
