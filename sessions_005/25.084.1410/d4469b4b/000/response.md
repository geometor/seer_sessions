## Perception

1.  **Input/Output Sizes**: All input grids are 5x5. All output grids are 3x3.
2.  **Color Palette**:
    *   Input grids contain white (0) and one other color: blue (1), red (2), or green (3).
    *   Output grids contain white (0) and gray (5).
3.  **Core Transformation**: The transformation appears to identify the *type* of non-white color present in the input grid and maps it to a specific, fixed 3x3 pattern made of gray pixels in the output grid. The arrangement or quantity of the non-white pixels in the input does not seem to influence the output pattern, only their color identity.
4.  **Color-Pattern Mapping**:
    *   If the input contains blue (1), the output is a gray '+' shape.
    *   If the input contains red (2), the output is a gray 'T' shape.
    *   If the input contains green (3), the output is a gray 'L' shape (mirrored and rotated).
5.  **Consistency**: This color-to-pattern mapping holds true across all provided training examples. Examples with the same non-white input color produce the same output pattern, regardless of the specific placement of the colored pixels within the 5x5 input grid.

## Facts


```yaml
task_type: pattern_mapping
input_grid:
  size: 5x5
  colors:
    - white (0)
    - one_of: [blue (1), red (2), green (3)]
output_grid:
  size: 3x3
  colors:
    - white (0)
    - gray (5)
transformation:
  type: color_identification_and_pattern_lookup
  steps:
    - Identify the unique non-white color present in the input grid.
    - Map the identified color to a predefined 3x3 pattern.
color_pattern_map:
  blue (1):
    pattern_name: plus_sign
    grid:
      - [0, 5, 0]
      - [5, 5, 5]
      - [0, 5, 0]
  red (2):
    pattern_name: T_shape
    grid:
      - [5, 5, 5]
      - [0, 5, 0]
      - [0, 5, 0]
  green (3):
    pattern_name: L_shape
    grid:
      - [0, 0, 5]
      - [0, 0, 5]
      - [5, 5, 5]
notes: The specific arrangement or count of the non-white input pixels is irrelevant; only the color identity matters for determining the output.
```


## Natural Language Program

1.  Examine the input 5x5 grid to find any pixel that is not white (color 0).
2.  Identify the color code of this non-white pixel (it will be 1, 2, or 3).
3.  Based on the identified color code, construct the corresponding 3x3 output grid:
    *   If the color is blue (1), create a 3x3 grid with a gray (5) plus sign shape centered:
        
```
        0 5 0
        5 5 5
        0 5 0
        ```

    *   If the color is red (2), create a 3x3 grid with a gray (5) 'T' shape:
        
```
        5 5 5
        0 5 0
        0 5 0
        ```

    *   If the color is green (3), create a 3x3 grid with a gray (5) 'L' shape in the bottom-right:
        
```
        0 0 5
        0 0 5
        5 5 5
        ```

4.  Return the constructed 3x3 grid as the output.