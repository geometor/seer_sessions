
## train_1

**input:**
```
5 5 6 6 6
6 5 5 6 6
6 6 5 5 6
6 6 6 5 5
5 6 6 6 5
```


**output:**
```
6 6 0 0 0
0 6 6 0 0
0 0 6 6 0
0 0 0 6 6
6 0 0 0 6
```


## train_2

**input:**
```
4 5 4
5 5 5
4 5 4
```


**output:**
```
0 4 0
4 4 4
0 4 0
```


## train_3

**input:**
```
9 5 9 9 9
9 9 5 5 9
9 5 9 9 9
9 9 5 9 9
9 9 9 5 5
```


**output:**
```
0 9 0 0 0
0 0 9 9 0
0 9 0 0 0
0 0 9 0 0
0 0 0 9 9
```

## Perception

The input grids contain two distinct colors. One of these colors is always gray (value 5). The other color varies across the examples (magenta/6 in train_1, yellow/4 in train_2, maroon/9 in train_3). The output grids have the same dimensions as their corresponding input grids. In the output grids, the pixels that were gray (5) in the input are now white (0). All other pixels retain their original color from the input.

## Facts


```yaml
task: color_replacement
examples:
  - name: train_1
    input_grid_size: [5, 5]
    input_colors: [gray, magenta]
    output_grid_size: [5, 5]
    output_colors: [white, magenta]
    transformation:
      - color: gray
        becomes: white
      - color: magenta
        remains: magenta
  - name: train_2
    input_grid_size: [3, 3]
    input_colors: [yellow, gray]
    output_grid_size: [3, 3]
    output_colors: [white, yellow]
    transformation:
      - color: gray
        becomes: white
      - color: yellow
        remains: yellow
  - name: train_3
    input_grid_size: [5, 5]
    input_colors: [maroon, gray]
    output_grid_size: [5, 5]
    output_colors: [white, maroon]
    transformation:
      - color: gray
        becomes: white
      - color: maroon
        remains: maroon
general_rule:
  - identify_color: gray (value 5)
  - action: replace gray pixels with white pixels (value 0)
  - other_colors: remain unchanged in their positions
```


## Natural Language Program

1.  Create an output grid with the same dimensions as the input grid.
2.  Iterate through each pixel in the input grid.
3.  If the pixel's color is gray (value 5), set the corresponding pixel in the output grid to white (value 0).
4.  If the pixel's color is not gray, copy its color to the corresponding pixel in the output grid.
5.  Return the completed output grid.
