
## train_1

**input:**
```
0 0 7 7 7 7 7 7 0 0 7 7 7 7 0 0 0 7 7 7 7 7 7 7 0 7 7 7 0
```


**output:**
```
0 0 7 7 7 7 7 7 0 0 7 7 7 7 0 0 0 9 9 9 9 9 9 9 0 7 7 7 0
```


## train_2

**input:**
```
0 0 7 0 0 7 7 7 7 7 0 0 7 7 7 7 7 0 0 0 7 7 0 0 0 7 7 7 7
```


**output:**
```
0 0 7 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 0 7 7 0 0 0 7 7 7 7
```


## train_3

**input:**
```
0 0 7 7 7 0 0 7 7 7 7 0 7 7 0 0 0 7 0 0 7 0 7 7 7 0 7 7 0
```


**output:**
```
0 0 7 7 7 0 0 9 9 9 9 0 7 7 0 0 0 7 0 0 7 0 7 7 7 0 7 7 0
```

## Perception

The input and output grids are composed primarily of white (0) and orange (7) pixels. The output grid introduces maroon (9) pixels.
The orange pixels in the input form several distinct horizontal rectangular blocks (objects), separated by white pixels.
Comparing the input and output grids, the transformation involves changing the color of *some* of the orange rectangles to maroon.
By examining the examples, it appears that the transformation targets the orange horizontal rectangle(s) with the greatest width (largest number of contiguous orange pixels in a row). If there are multiple rectangles tied for the maximum width, all of them change color. The rest of the grid remains unchanged.

## Facts


```yaml
elements:
  - type: grid
    colors_present: [white (0), orange (7)] # Input grid colors
    colors_present_output: [white (0), orange (7), maroon (9)] # Output grid colors
  - type: object
    identifier: horizontal orange rectangle
    description: A contiguous sequence of orange (7) pixels within a single row, bounded by white (0) pixels or grid edges.
    properties:
      - color: orange (7)
      - shape: horizontal rectangle (1 row high)
      - size: width (number of pixels)
actions:
  - name: identify_objects
    input: input grid
    output: list of horizontal orange rectangles with their locations and widths
  - name: find_max_width
    input: list of rectangle widths
    output: maximum width value
  - name: filter_largest_objects
    input: list of horizontal orange rectangles, maximum width
    output: list of rectangles with the maximum width
  - name: change_color
    target_objects: largest horizontal orange rectangle(s)
    from_color: orange (7)
    to_color: maroon (9)
    condition: The width of the rectangle equals the maximum width found among all horizontal orange rectangles in the input grid.
relationships:
  - type: comparison
    property: width
    description: The widths of all identified horizontal orange rectangles are compared to find the maximum width.
```


## Natural Language Program

1.  Scan the input grid row by row to identify all distinct horizontal rectangles composed solely of orange (7) pixels. A rectangle is defined as a contiguous block of orange pixels in a single row.
2.  For each identified orange rectangle, determine its width (the number of pixels it contains).
3.  Find the maximum width among all identified orange rectangles.
4.  Create the output grid by copying the input grid.
5.  Iterate through the identified orange rectangles again. If a rectangle's width matches the maximum width calculated in step 3, change the color of all pixels belonging to that rectangle in the output grid from orange (7) to maroon (9).
6.  Leave all other pixels in the output grid unchanged from their corresponding input grid values.
