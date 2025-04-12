
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

## Perception

The input grids contain various geometric shapes composed of different colors against a white background. Some shapes are "hollow" or incomplete squares (like the blue 'C' shapes in `train_1` and green 'C' shapes in `train_2`). There is also always one prominent solid, single-color square object present (green in `train_1`, magenta in `train_2`). The other shapes seem extraneous.

The output grid is consistently a smaller grid that exactly matches the solid square object identified in the input grid, preserving its color and dimensions. The task appears to involve identifying and isolating this specific solid square object from the rest of the input content. The key distinguishing feature of the target object is that it's a solid, single-color rectangle (specifically a square in these examples), and it seems to be the largest such object in the input.

## Facts


```yaml
task_type: object_extraction
input_features:
  grid_elements:
    - type: background
      color: white
    - type: shape
      properties:
        - color: varies (blue, green, magenta)
        - structure: can be solid or hollow
        - form: appears as rectangles, squares, or incomplete squares ('C' shapes)
  grid_properties:
    - multiple distinct objects can exist
    - one object is a solid, single-color rectangle (square in examples)
output_features:
  grid_elements:
    - type: background
      color: white (implicitly, if the extracted object doesn't fill the output grid, though not seen here)
    - type: shape
      properties:
        - color: matches the color of the extracted input object
        - structure: solid
        - form: rectangle (square in examples)
  grid_properties:
    - contains exactly one object
    - the object is a copy of a specific object from the input
transformation:
  action: identify_and_extract
  selection_criteria:
    - object_type: solid rectangle
    - color: non-white
    - size_metric: maximum area
  process:
    - find all contiguous, single-color, non-white objects
    - filter for objects that form solid rectangles
    - determine the area of each solid rectangle
    - select the solid rectangle with the largest area
    - create the output grid containing only this selected rectangle
relationship:
  - output grid is a subgrid or cropped version of the input grid, containing only the largest solid rectangular object.
```


## Natural Language Program

1.  Scan the input grid to identify all distinct contiguous blocks of non-white pixels.
2.  For each identified block, determine if it forms a solid rectangle (i.e., it has a rectangular bounding box, and all pixels within that bounding box share the same color as the block).
3.  Filter out any blocks that are not solid rectangles.
4.  Calculate the area (width * height) of each remaining solid rectangular block.
5.  Identify the solid rectangular block with the maximum area. If there's a tie, any of the largest ones might be chosen (though the examples don't show ties).
6.  Create a new output grid whose dimensions match the dimensions of the identified largest solid rectangle.
7.  Copy the pixels (colors) from the identified largest solid rectangle in the input grid to the corresponding positions in the new output grid.
