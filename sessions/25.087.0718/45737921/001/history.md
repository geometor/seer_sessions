
## train_1

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


## train_2

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

Okay, let's analyze the transformation.

## Perception

1.  **Grid Structure:** The task operates on grids containing pixels of different colors. The background is consistently white (0).
2.  **Objects:** The non-white pixels form distinct, separate objects within the grid. Each object is composed of pixels of exactly two different non-white colors.
3.  **Transformation:** The core transformation happens *within* each distinct object. The two non-white colors that constitute an object appear to swap their positions. If an object is made of Color A and Color B, every pixel that was Color A becomes Color B, and every pixel that was Color B becomes Color A.
4.  **Invariance:** The white background pixels remain unchanged. The overall shape, size, and position of each object remain unchanged. Only the colors *within* the object are modified.
5.  **Isolation:** The transformation applied to one object does not affect any other object or the background.

## Facts


```yaml
version: 1.0
facts:
  - name: Grid Structure
    description: Input and output are 2D grids of pixels with integer values 0-9 representing colors.
    properties:
      background_color: white (0)
      dimensionality: 2D
      cell_values: integers 0-9

  - name: Objects
    description: Contiguous areas of non-white pixels form distinct objects.
    properties:
      composition: Each object consists of pixels of exactly two different non-white colors.
      separation: Objects are separated by white pixels.
      structure: Contiguous blocks of non-white pixels.

  - name: Transformation Action
    description: Within each object, the two constituent non-white colors swap places.
    type: Color Swap
    scope: Intra-object
    effect: For an object made of Color A and Color B, all Color A pixels become Color B, and all Color B pixels become Color A.

  - name: Invariant Elements
    description: Elements that remain unchanged during the transformation.
    elements:
      - White background pixels
      - Object shape
      - Object size
      - Object position
      - Number of objects
```


## Natural Language Program

1.  Identify all distinct contiguous objects in the input grid that are composed of non-white pixels.
2.  For each identified object:
    a.  Determine the two unique non-white colors present within that object (let's call them Color A and Color B).
    b.  Create a corresponding object in the output grid at the same location and with the same shape.
    c.  For every pixel position within the boundary of the object:
        i.  If the input pixel at that position was Color A, set the output pixel at the corresponding position to Color B.
        ii. If the input pixel at that position was Color B, set the output pixel at the corresponding position to Color A.
3.  Ensure all pixels in the output grid that are not part of any identified object retain their original color (which will be white, based on the examples).
