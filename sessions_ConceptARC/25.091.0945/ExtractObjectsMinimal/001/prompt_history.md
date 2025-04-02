
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0
0 0 4 0 0 4 0 0
0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4
4 0 0 4
4 4 4 4
```


## train_2

**input:**
```
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0 0
0 0 0 4 0 0 0 4 0 0 0 0
0 0 4 0 0 0 0 0 4 0 0 0
0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 4 0 0 0
0 0 4 0 4 0 0
0 4 0 0 0 4 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 4 0 4 0 0
0 0 0 4 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6
6 6 6 6 6
6 6 6 6 6
6 6 6 6 6
6 6 6 6 6
```

**Perception:**

Each input grid contains a single, contiguous object composed of a non-white color (yellow in examples 1 and 2, magenta in example 3) set against a white background (color 0). The output grid consists solely of the non-white object extracted from the input, effectively removing all surrounding white pixels. The transformation crops the input grid to the minimal bounding box containing the non-white object.

**Facts:**


```yaml
- description: Input grid analysis
  elements:
    - type: grid
      properties:
        background_color: white (0)
        contains_object: true
    - type: object
      properties:
        color: non-white (e.g., yellow(4), magenta(6))
        contiguity: contiguous
        count: 1
        location: embedded within the white background
- description: Output grid analysis
  elements:
    - type: grid
      properties:
        size: minimal bounding box of the input object
        content: identical to the input object pixels
        background_color: none (or only pixels that were part of the object)
- description: Transformation rule
  action: crop
  input: input grid
  output: output grid
  steps:
    - Identify all pixels in the input grid that are not white (0).
    - Determine the minimum and maximum row indices (top, bottom) and column indices (left, right) containing these non-white pixels. This defines the bounding box.
    - Extract the subgrid defined by this bounding box from the input grid.
  result: The extracted subgrid is the output grid.
```


**Natural Language Program:**

1.  Scan the input grid to locate all pixels that have a color other than white (0).
2.  Find the coordinates (row and column indices) of the top-most, bottom-most, left-most, and right-most non-white pixels.
3.  Define a rectangular region (bounding box) using these minimum and maximum row and column indices.
4.  Create the output grid by extracting the pixels from the input grid that fall within this defined bounding box.
