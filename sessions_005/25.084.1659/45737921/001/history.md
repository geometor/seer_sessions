
## train_1

**input:**
```
0 0 0 0 0 0 0
0 5 8 5 0 0 0
0 5 8 5 0 0 0
0 8 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 8 5 8 0 0 0
0 8 5 8 0 0 0
0 5 5 5 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 8 8 4 0 0 0 0 0 0
0 4 8 4 0 0 0 0 0 0
0 8 8 4 0 0 0 0 0 0
0 0 0 0 0 0 3 2 2 0
0 0 0 0 0 0 3 3 2 0
0 0 0 0 0 0 3 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 3 6 3 0 0 0 0 0
0 0 3 6 3 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 8 0 0 0 0 0 0
0 8 4 8 0 0 0 0 0 0
0 4 4 8 0 0 0 0 0 0
0 0 0 0 0 0 2 3 3 0
0 0 0 0 0 0 2 2 3 0
0 0 0 0 0 0 2 3 3 0
0 0 0 0 0 0 0 0 0 0
0 0 6 3 6 0 0 0 0 0
0 0 6 3 6 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0
0 8 1 8 0 0 0 3 2 3 0 0
0 8 8 8 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 1 1 0 0 0 0 0 0
0 0 0 1 6 6 0 0 0 0 0 0
0 0 0 1 6 6 0 0 4 4 5 0
0 0 0 0 0 0 0 0 4 5 5 0
0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 1 8 1 0 0 0 2 3 2 0 0
0 1 1 1 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 2 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 6 6 0 0 0 0 0 0
0 0 0 6 1 1 0 0 0 0 0 0
0 0 0 6 1 1 0 0 5 5 4 0
0 0 0 0 0 0 0 0 5 4 4 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The input grids contain several distinct objects composed of non-white pixels set against a white background. Each object appears to be constructed from exactly two different non-white colors. In the corresponding output grids, the shapes and positions of these objects remain identical, but the two colors comprising each object have swapped their positions. Pixels that are part of the white background remain unchanged.

**YAML Facts:**


```yaml
task_description: Swap the two constituent colors within each distinct multi-colored object.
background_color: white (0)
objects:
  - property: Composed of non-white pixels.
  - property: Contiguous blocks of pixels.
  - property: Each object in the examples consists of exactly two distinct non-white colors.
  - relationship: Objects are separated by the background color.
transformation:
  - action: Identify distinct objects.
  - condition: If an object is composed of exactly two different non-white colors (color A and color B).
  - action: Within that object, change all pixels of color A to color B, and all pixels of color B to color A.
  - condition: If a pixel is part of the background (white).
  - action: Leave the pixel unchanged.
  - condition: If an object is composed of only one non-white color (hypothetical, not seen in examples).
  - action: Leave the object unchanged (implied).
invariance:
  - The shape and position of each object remain the same.
  - The background pixels remain the same.
```


**Natural Language Program:**

1.  Identify all distinct connected components (objects) formed by non-white pixels in the input grid.
2.  For each identified object:
    a.  Determine the set of unique non-white colors present within that object.
    b.  If the object contains exactly two distinct non-white colors (let's call them Color1 and Color2):
        i.  Iterate through all pixels belonging to this object in the input grid.
        ii. If a pixel has Color1, change its color to Color2 in the output grid.
        iii. If a pixel has Color2, change its color to Color1 in the output grid.
    c.  If the object contains only one non-white color or more than two non-white colors, copy the object's pixels directly to the output grid without changing their colors.
3.  Copy all white background pixels from the input grid to the corresponding positions in the output grid.
4.  Return the resulting output grid.
