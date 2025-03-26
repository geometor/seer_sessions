
## train_1

**input:**
```
5 5 5
0 0 5
0 0 0
```


**output:**
```
0 0 0
4 4 0
4 4 4
```


## train_2

**input:**
```
0 8 0
0 8 0
8 0 0
```


**output:**
```
2 0 2
2 0 2
0 2 2
```


## train_3

**input:**
```
8 0 8
0 8 0
0 8 0
```


**output:**
```
0 2 0
2 0 2
2 0 2
```


## train_4

**input:**
```
0 0 3
0 3 0
3 0 0
```


**output:**
```
1 1 0
1 0 1
0 1 1
```


## train_5

**input:**
```
5 0 0
5 5 0
5 0 0
```


**output:**
```
0 4 4
0 0 4
0 4 4
```


## train_6

**input:**
```
8 0 0
0 8 0
0 0 0
```


**output:**
```
0 2 2
2 0 2
2 2 2
```

Okay, I will analyze the provided examples and derive the transformation logic.

**Perception of Elements:**

*   **Grid Structure:** All examples use 3x3 grids for both input and output.
*   **Color Palette:** Each input grid contains exactly two colors: white (0) and one other specific color (gray-5, azure-8, or green-3). Each output grid also contains exactly two colors: white (0) and one other specific color (yellow-4, red-2, or blue-1).
*   **Objects:** The non-white pixels in the input grids form various simple shapes or patterns. The non-white pixels in the output grids also form shapes, which appear to be the negative image or inverse of the input shapes within the grid boundaries.
*   **Transformation:** The core transformation seems to involve swapping the roles of the two colors present in the input. Pixels that were non-white in the input become white in the output. Pixels that were white in the input become a new non-white color in the output.
*   **Color Mapping:** There's a specific mapping rule between the non-white input color and the non-white output color:
    *   Gray (5) in input maps to Yellow (4) in output.
    *   Azure (8) in input maps to Red (2) in output.
    *   Green (3) in input maps to Blue (1) in output.

**Facts (YAML):**


```yaml
task_description: Apply a color swap and specific color mapping based on the non-white input color.
grid_properties:
  - size: All examples use 3x3 grids.
colors:
  - input_has_two_colors: white (0) and one other color (input_color).
  - output_has_two_colors: white (0) and one other color (output_color).
color_mapping:
  - rule: { gray: yellow, azure: red, green: blue }
  - mapping_codes: { 5: 4, 8: 2, 3: 1 }
transformation_steps:
  - identify_input_color: Find the single non-white color present in the input grid.
  - determine_output_color: Use the color_mapping rule to find the corresponding output color based on the identified input color.
  - pixel_wise_operation:
      - For each pixel in the input grid:
          - If the pixel color is the input_color, change it to white (0) in the output grid.
          - If the pixel color is white (0), change it to the output_color in the output grid.
shapes:
  - The pattern of non-white pixels in the output is the inverse (negative image) of the pattern of non-white pixels in the input.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid.
2.  Identify the unique non-white color present in the input grid; let this be `input_color`.
3.  Determine the corresponding `output_color` based on the following rules:
    *   If `input_color` is gray (5), set `output_color` to yellow (4).
    *   If `input_color` is azure (8), set `output_color` to red (2).
    *   If `input_color` is green (3), set `output_color` to blue (1).
4.  Iterate through each cell (`pixel`) of the input grid at coordinates (row, column).
5.  For each `pixel`:
    *   If the color of the `pixel` is equal to `input_color`, set the color of the cell at (row, column) in the output grid to white (0).
    *   If the color of the `pixel` is white (0), set the color of the cell at (row, column) in the output grid to `output_color`.
6.  Return the completed output grid.
