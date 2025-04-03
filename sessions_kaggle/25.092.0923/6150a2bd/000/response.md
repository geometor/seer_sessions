## Perception

The task presents pairs of input and output grids. Both input and output grids in the provided examples are 3x3. The colors present in the input grid are the same as the colors present in the corresponding output grid, suggesting that no colors are added or removed, only rearranged. Comparing the pixel positions between the input and output grids reveals a consistent pattern across both examples: the output grid is a 180-degree rotation of the input grid.

For example 1:
Input:

```
5 5 2
1 0 0
0 0 0
```

If rotated 180 degrees, pixel at (0,0) moves to (2,2), (0,1) to (2,1), (0,2) to (2,0), (1,0) to (1,2), (1,1) to (1,1), (1,2) to (1,0), (2,0) to (0,2), (2,1) to (0,1), (2,2) to (0,0). Applying this:

```
0 0 0
0 0 1
2 5 5
```

This matches the output.

For example 2:
Input:

```
3 3 8
3 7 0
5 0 0
```

Rotating 180 degrees:

```
0 0 5
0 7 3
8 3 3
```

This also matches the output.

The transformation is a simple geometric rotation.

## Facts


```yaml
task_type: grid_transformation
transformation_category: geometric
input_output_properties:
  - relationship: input grid is transformed into the output grid
  - dimension_preservation: input and output grids have the same dimensions (e.g., 3x3 in examples)
  - color_preservation: all colors from the input grid are present in the output grid, and no new colors are introduced.
grid_elements:
  - type: pixels
  - properties: color (integer 0-9)
transformation_details:
  - name: rotation
  - angle: 180 degrees
  - origin: center of the grid
  - scope: applies to the entire input grid structure uniformly
```


## Natural Language Program

1.  Identify the input grid.
2.  Rotate the input grid by 180 degrees. Treat the grid as a single object and rotate it around its central point.
3.  The grid resulting from the 180-degree rotation is the final output grid.