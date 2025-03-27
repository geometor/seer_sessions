
## train_1

**input:**
```
7 7 7 6
6 6 7 6
7 7 6 7
7 6 7 7
7 6 7 6
6 6 6 7
```


**output:**
```
7 7 7 2
2 2 7 2
7 7 2 7
7 2 7 7
7 2 7 2
2 2 2 7
```


## train_2

**input:**
```
6 6 7 6
6 6 7 7
7 7 6 7
```


**output:**
```
2 2 7 2
2 2 7 7
7 7 2 7
```


## train_3

**input:**
```
7 7 6 6 6 6
6 7 6 7 7 7
7 6 7 7 6 7
```


**output:**
```
7 7 2 2 2 2
2 7 2 7 7 7
7 2 7 7 2 7
```

## Perception
The input grids consist of pixels colored magenta (6) and orange (7). The output grids consist of pixels colored red (2) and orange (7). Comparing the input and output grids for each example, it appears that every pixel that was magenta (6) in the input has been changed to red (2) in the output. All pixels that were orange (7) in the input remain orange (7) in the output. The dimensions (height and width) of the grids remain unchanged.

## Facts

```yaml
elements:
  - type: grid
    properties:
      colors_present_input: [magenta (6), orange (7)]
      colors_present_output: [red (2), orange (7)]
      dimensionality: constant (input and output grids have the same height and width)
transformation:
  - type: color_replacement
    description: All pixels with a specific color in the input are replaced by another specific color in the output.
    mapping:
      - input_color: magenta (6)
        output_color: red (2)
    unaffected_colors: [orange (7)] # Colors that remain unchanged
relationships:
  - type: pixel_correspondence
    description: Each pixel in the input grid corresponds directly to the pixel at the same row and column in the output grid.
```


## Natural Language Program
1.  Create a new output grid with the same dimensions as the input grid.
2.  For each pixel in the input grid:
    a.  Check the color of the pixel.
    b.  If the color is magenta (6), set the color of the corresponding pixel in the output grid to red (2).
    c.  If the color is not magenta (6) (i.e., it is orange (7) in these examples), set the color of the corresponding pixel in the output grid to the same color as the input pixel.
3.  Return the completed output grid.
