
## train_1

**input:**
```
2 3 2 3 2 2 0 0 0 0 0 0 0 0
2 3 2 3 2 2 0 0 0 0 0 0 0 0
2 3 2 3 2 2 0 2 2 2 2 2 2 0
2 3 2 3 2 2 0 2 2 2 2 2 2 0
2 3 2 3 2 2 0 3 3 3 3 3 3 0
2 3 2 3 2 2 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 2 3 2 3 2 0 2 2 2 2 2 2 0
0 2 3 2 3 2 0 0 0 0 0 0 0 0
0 2 3 2 3 2 0 0 0 0 0 0 0 0
0 2 3 2 3 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 8 8 8 8 8 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 8 8 8 8 8 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 8 8 8 8 8 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception**

1.  **Input Grid Structure:** Both input examples contain two distinct, separated rectangular patterns composed of non-white pixels. These patterns are set against a white background. A single column of white pixels consistently separates the two main patterns.
2.  **Pattern Types:** In each input grid, one pattern exhibits colors arranged in horizontal stripes (rows are predominantly one color or alternate colors row by row), while the other pattern shows colors arranged in vertical stripes (columns are predominantly one color or alternate colors column by column).
    *   In `train_1`, the left pattern has vertical stripes (alternating red/green columns), and the right pattern has horizontal stripes (alternating red/green rows).
    *   In `train_2`, the left pattern has horizontal stripes (alternating yellow/azure rows), and the right pattern has vertical stripes (alternating blue/magenta columns).
3.  **Transformation:** The transformation involves selecting one of the two patterns and discarding the other. The separating white column is also discarded (effectively becoming part of the white background).
4.  **Selection Criterion:** The pattern that is *kept* in the output grid is always the one exhibiting horizontal stripes. The pattern with vertical stripes is removed.
5.  **Output Grid Structure:** The output grid has the same dimensions as the input grid. It contains only the selected horizontal stripe pattern, placed in its original position. All other pixels, including the area previously occupied by the vertical stripe pattern and the separating column, are white.

**Facts**


```yaml
task_description: Isolate the pattern with horizontal stripes from two separated patterns in the input grid.

examples:
  train_1:
    input:
      grid_dimensions: [11, 14]
      objects:
        - id: pattern_left
          pixels:
            - color: red (2)
            - color: green (3)
          structure: vertical_stripes
          location: columns 0-5
          bounding_box: [[0, 0], [10, 5]] # Approx
        - id: pattern_right
          pixels:
            - color: red (2)
            - color: green (3)
          structure: horizontal_stripes
          location: columns 7-12
          bounding_box: [[2, 7], [7, 12]] # Approx
      relationships:
        - type: separation
          object_ids: [pattern_left, pattern_right]
          details: Separated by a single vertical column of white (0) pixels at column index 6.
    output:
      grid_dimensions: [11, 14]
      objects:
        - id: pattern_right_preserved
          pixels:
            - color: red (2)
            - color: green (3)
          structure: horizontal_stripes
          location: columns 7-12 # Same as input
          bounding_box: [[2, 7], [7, 12]] # Same as input
      background: white (0)
      action_summary: pattern_left and the separator column were removed (replaced with white). pattern_right was kept.

  train_2:
    input:
      grid_dimensions: [12, 12]
      objects:
        - id: pattern_left
          pixels:
            - color: yellow (4)
            - color: azure (8)
          structure: horizontal_stripes
          location: columns 1-5
          bounding_box: [[1, 1], [9, 5]] # Approx
        - id: pattern_right
          pixels:
            - color: blue (1)
            - color: magenta (6)
          structure: vertical_stripes
          location: columns 7-11
          bounding_box: [[2, 7], [9, 11]] # Approx
      relationships:
        - type: separation
          object_ids: [pattern_left, pattern_right]
          details: Separated by a single vertical column of white (0) pixels at column index 6.
    output:
      grid_dimensions: [12, 12]
      objects:
        - id: pattern_left_preserved
          pixels:
            - color: yellow (4)
            - color: azure (8)
          structure: horizontal_stripes
          location: columns 1-5 # Same as input
          bounding_box: [[1, 1], [9, 5]] # Same as input
      background: white (0)
      action_summary: pattern_right and the separator column were removed (replaced with white). pattern_left was kept.

general_rule:
  input_contains: Two distinct non-white objects (patterns).
  object_properties:
    - One object has a horizontal stripe structure.
    - The other object has a vertical stripe structure.
  relationship: The objects are separated spatially, typically by white pixels.
  transformation: Identify the object with the horizontal stripe structure.
  output_generation: Create a new grid of the same size as the input, filled with the background color (white). Copy the identified horizontal stripe object into the output grid at its original coordinates. Discard the vertical stripe object and any separator pixels.
```


**Natural Language Program**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Identify all distinct connected components (objects) of non-white pixels in the input grid.
3.  Filter these objects to find the two main patterns, likely the largest ones or those clearly separated. Assume there will be exactly two such patterns relevant to the task.
4.  For each of the two identified patterns:
    a.  Determine its primary stripe orientation (horizontal or vertical). This can be done by analyzing color changes within the object's bounding box:
        i.  Count the number of adjacent pixel pairs within the object where the colors differ horizontally (left-right neighbors).
        ii. Count the number of adjacent pixel pairs within the object where the colors differ vertically (up-down neighbors).
        iii. If the vertical color change count is significantly greater than the horizontal count, classify the pattern as having horizontal stripes.
        iv. If the horizontal color change count is significantly greater than the vertical count, classify the pattern as having vertical stripes.
5.  Select the pattern identified as having horizontal stripes.
6.  Iterate through all the pixels belonging to the selected horizontal stripe pattern in the input grid.
7.  For each pixel of the selected pattern, copy its color and coordinates to the corresponding position in the output grid.
8.  Return the final output grid.
