
## train_1

**input:**
```
0 0 0 0 3 3 3 3 3 0 0 0 0
0 2 2 2 3 2 2 2 3 2 2 2 0
0 2 0 2 3 2 0 2 3 2 0 2 0
0 2 2 2 3 2 2 2 3 2 2 2 0
0 0 0 0 3 3 3 3 3 0 0 0 0
0 2 2 2 0 2 2 2 0 2 2 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 2 2 0 2 2 2 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 2 2 2 0 2 2 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 2 2 0 2 2 2 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3
3 0 0 0 3
3 0 0 0 3
3 0 0 0 3
3 3 3 3 3
```


## train_2

**input:**
```
6 6 6 6 6 0 0 0 0 0 0
6 3 3 3 6 0 3 3 3 3 0
6 3 0 0 6 0 3 0 0 3 0
6 3 0 0 6 0 3 0 0 3 0
6 6 6 6 6 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 3 3 3 3
0 0 3 0 0 3 0 3 0 0 3
0 0 3 0 0 3 0 3 0 0 3
0 0 3 3 3 3 0 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6
6 0 0 0 6
6 0 0 0 6
6 0 0 0 6
6 6 6 6 6
```

## Perception of Elements

The input grids contain multiple distinct objects composed of non-white pixels, separated by a white background. These objects can have different colors and shapes. The output grid is always a 5x5 hollow square (a square with a 1-pixel thick border and a white interior). The color of the output square is determined by one specific object in the input.

In both examples provided:
1.  **train_1**: The input has a green cross-shaped object and three red U-shaped objects. The green object's bounding box is 5x5. The red objects have smaller bounding boxes. The output is a 5x5 hollow green square.
2.  **train_2**: The input has a magenta hollow square object and three green objects of varying shapes. The magenta object's bounding box is 5x5. The green objects have smaller bounding boxes. The output is a 5x5 hollow magenta square.

The core logic appears to involve:
1.  Identifying all distinct contiguous non-white objects in the input.
2.  Calculating the bounding box for each object.
3.  Finding the unique object whose bounding box dimensions are exactly 5x5.
4.  Determining the color of this unique 5x5 object.
5.  Constructing the output grid as a 5x5 hollow square using the identified color for the border and white for the 3x3 interior.

## YAML Facts


```yaml
task_description: Construct a 5x5 hollow square based on the color of a uniquely sized object in the input grid.

input_features:
  - grid: 2D array of integers (colors).
  - background_color: white (0).
  - objects: Multiple distinct contiguous regions of non-white pixels.
    - properties:
      - color: The single color composing the object.
      - shape: Variable.
      - size: Variable.
      - bounding_box: The smallest rectangle enclosing the object.

identification_rule:
  - Identify all distinct non-white objects.
  - Calculate the bounding box (height x width) for each object.
  - Filter objects to find the one with a bounding box size of exactly 5x5.
  - Assumption: There will be exactly one such object in the input.
  - Extract the color of this unique 5x5-bounded object.

output_features:
  - grid: A new 5x5 2D array.
  - structure: Hollow square.
    - border: 1-pixel thick border using the color identified from the input object.
    - interior: 3x3 center area filled with white (0).
```


## Natural Language Program

1.  Parse the input grid to identify all distinct contiguous objects composed of non-white pixels. Treat adjacent pixels (including diagonals) of the same non-white color as part of the same object.
2.  For each identified object:
    a.  Determine its color (the single non-white color it is composed of).
    b.  Calculate its bounding box (the minimum and maximum row and column indices it occupies).
    c.  Calculate the height and width of the bounding box.
3.  Search through the identified objects to find the single object whose bounding box dimensions are exactly 5 rows high and 5 columns wide.
4.  Record the color of this unique object.
5.  Create a new 5x5 output grid, initialized with white (0) pixels.
6.  Set the color of the pixels forming the outer border of the 5x5 output grid (row 0, row 4, column 0, column 4) to the recorded color from step 4.
7.  The resulting 5x5 grid with the colored border and white interior is the final output.
