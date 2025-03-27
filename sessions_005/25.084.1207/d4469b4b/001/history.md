
## train_1

**input:**
```
1 0 1 0 0
1 0 0 1 1
1 1 0 1 0
0 1 0 1 0
1 0 0 0 1
```


**output:**
```
0 5 0
5 5 5
0 5 0
```


## train_2

**input:**
```
2 0 2 0 2
2 0 0 0 2
2 2 0 0 0
2 0 0 2 2
2 2 2 0 2
```


**output:**
```
5 5 5
0 5 0
0 5 0
```


## train_3

**input:**
```
0 3 0 3 0
3 3 0 0 0
0 3 0 0 0
0 0 3 0 0
3 3 3 0 0
```


**output:**
```
0 0 5
0 0 5
5 5 5
```


## train_4

**input:**
```
0 0 0 0 0
0 0 1 1 1
0 1 0 1 1
0 1 0 1 0
0 0 0 0 1
```


**output:**
```
0 5 0
5 5 5
0 5 0
```


## train_5

**input:**
```
3 0 0 0 0
0 0 0 3 3
0 3 3 0 0
0 3 0 3 0
3 0 3 3 0
```


**output:**
```
0 0 5
0 0 5
5 5 5
```


## train_6

**input:**
```
0 2 0 2 0
0 2 2 2 0
0 2 2 0 2
2 2 2 0 0
0 0 2 0 2
```


**output:**
```
5 5 5
0 5 0
0 5 0
```


## train_7

**input:**
```
2 0 0 0 0
0 2 0 0 2
2 0 0 2 0
0 0 0 2 2
0 0 2 2 0
```


**output:**
```
5 5 5
0 5 0
0 5 0
```

*   **Perception:**
    *   The input is always a 5x5 grid.
    *   The output is always a 3x3 grid.
    *   The input grid contains white (0) pixels and pixels of one other color (blue-1, red-2, or green-3).
    *   The output grid contains white (0) pixels and gray (5) pixels.
    *   The specific non-white color present in the input grid determines the pattern of gray pixels in the output grid.
    *   The arrangement of the colored pixels within the input grid does not influence the output pattern, only the *identity* of the color does.
    *   There's a fixed mapping between the input color and the output 3x3 pattern:
        *   Blue (1) in input maps to a '+' shape of gray pixels in the output.
        *   Red (2) in input maps to a 'T' shape of gray pixels in the output.
        *   Green (3) in input maps to a backward 'L' or 'corner' shape of gray pixels in the output.

*   **Facts:**
    
```yaml
    task_type: transformation
    input_grid:
      size: 5x5
      background_color: 0 (white)
      foreground_colors: [1 (blue), 2 (red), 3 (green)]
      property: Contains exactly one type of non-white color.
    output_grid:
      size: 3x3
      background_color: 0 (white)
      foreground_color: 5 (gray)
      property: Displays a specific pattern determined by the input's foreground color.
    transformation:
      type: mapping
      rule: The single non-white color present in the input grid dictates which predefined 3x3 pattern of gray pixels is generated as the output.
      color_map:
        1 (blue): pattern_plus  # [[0, 5, 0], [5, 5, 5], [0, 5, 0]]
        2 (red): pattern_t     # [[5, 5, 5], [0, 5, 0], [0, 5, 0]]
        3 (green): pattern_l     # [[0, 0, 5], [0, 0, 5], [5, 5, 5]]
    ```


*   **Natural Language Program:**
    1.  Identify the single non-white color present anywhere in the 5x5 input grid.
    2.  If the identified color is blue (1), create a 3x3 output grid with gray (5) pixels forming a plus shape (`[[0, 5, 0], [5, 5, 5], [0, 5, 0]]`) on a white (0) background.
    3.  If the identified color is red (2), create a 3x3 output grid with gray (5) pixels forming a 'T' shape (`[[5, 5, 5], [0, 5, 0], [0, 5, 0]]`) on a white (0) background.
    4.  If the identified color is green (3), create a 3x3 output grid with gray (5) pixels forming a backward 'L' shape (`[[0, 0, 5], [0, 0, 5], [5, 5, 5]]`) on a white (0) background.
    5.  Return the generated 3x3 grid.
