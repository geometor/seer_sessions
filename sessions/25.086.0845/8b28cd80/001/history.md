
## train_1

**input:**
```
0 0 0
5 0 0
0 0 0
```


**output:**
```
5 5 5 5 5 0 5 0 5
0 0 0 0 5 0 5 0 5
5 5 5 0 5 0 5 0 5
5 0 5 0 5 0 5 0 5
5 0 5 0 5 0 5 0 5
0 0 5 0 5 0 5 0 5
5 5 5 0 5 0 5 0 5
0 0 0 0 5 0 5 0 5
5 5 5 5 5 0 5 0 5
```


## train_2

**input:**
```
0 0 0
0 0 8
0 0 0
```


**output:**
```
8 0 8 0 8 0 8 8 8
8 0 8 0 8 0 8 0 0
8 0 8 0 8 0 8 0 8
8 0 8 0 8 0 8 0 8
8 0 8 0 8 0 8 0 8
8 0 8 0 8 0 8 0 0
8 0 8 0 8 0 8 8 8
8 0 8 0 8 0 0 0 0
8 0 8 0 8 8 8 8 8
```


## train_3

**input:**
```
0 0 7
0 0 0
0 0 0
```


**output:**
```
7 0 7 0 7 0 7 0 7
7 0 7 0 7 0 7 0 0
7 0 7 0 7 0 7 7 7
7 0 7 0 7 0 0 0 0
7 0 7 0 7 7 7 7 7
7 0 7 0 0 0 0 0 0
7 0 7 7 7 7 7 7 7
7 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 7
```


## train_4

**input:**
```
0 3 0
0 0 0
0 0 0
```


**output:**
```
3 0 3 0 3 0 3 0 3
3 0 3 0 0 0 3 0 3
3 0 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3
```


## train_5

**input:**
```
0 0 0
0 4 0
0 0 0
```


**output:**
```
4 0 4 4 4 4 4 4 4
4 0 4 0 0 0 0 0 4
4 0 4 0 4 4 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 0 0 4 0 4
4 0 4 4 4 4 4 0 4
4 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4
```

*   **Perception:**
    *   The input grids are consistently 3x3, while the output grids are 9x9.
    *   Each input grid contains exactly one non-white pixel; the rest are white (0).
    *   The color of the single non-white pixel in the input grid varies across examples (gray, azure, orange, green, yellow).
    *   The output grid's pattern seems uniquely determined by the *color* of the non-white pixel in the input, not its position within the 3x3 input grid.
    *   Each specific non-white input color corresponds to a distinct, fixed 9x9 pattern in the output. The output pattern uses the same non-white color found in the input.
    *   The transformation appears to be a lookup process: the input color acts as a key to retrieve a predefined 9x9 grid pattern.

*   **Facts:**
    
```yaml
    task_type: lookup_pattern
    input_grid:
        size: 3x3
        content: Contains exactly one non-white pixel and white (0) pixels elsewhere.
        role: Acts as an index or key.
    output_grid:
        size: 9x9
        content: A specific pattern determined by the input's non-white color.
        role: The result of the lookup.
    transformation:
        action: Identify the non-white color in the input grid.
        rule: Map the identified color to a predefined 9x9 pattern associated with that color.
        output: Return the corresponding predefined 9x9 pattern.
    relationships:
        - Each unique non-white color seen in the inputs (3, 4, 5, 7, 8) maps to a unique, fixed 9x9 output pattern composed of that color and white (0).
        - The position of the non-white pixel within the 3x3 input grid does not affect the structure or content of the 9x9 output pattern.
    predefined_patterns:
        - color_3: green_pattern_9x9 (as seen in train_4 output)
        - color_4: yellow_pattern_9x9 (as seen in train_5 output)
        - color_5: gray_pattern_9x9 (as seen in train_1 output)
        - color_7: orange_pattern_9x9 (as seen in train_3 output)
        - color_8: azure_pattern_9x9 (as seen in train_2 output)
    ```


*   **Natural Language Program:**
    1.  Scan the input 3x3 grid to find the single pixel that is not white (color 0).
    2.  Identify the color of this non-white pixel.
    3.  Based on the identified color, select the corresponding predefined 9x9 output grid pattern. Use the patterns observed in the training examples as the definitions:
        *   If the color is gray (5), use the 9x9 pattern from train_1 output.
        *   If the color is azure (8), use the 9x9 pattern from train_2 output.
        *   If the color is orange (7), use the 9x9 pattern from train_3 output.
        *   If the color is green (3), use the 9x9 pattern from train_4 output.
        *   If the color is yellow (4), use the 9x9 pattern from train_5 output.
    4.  Return the selected 9x9 grid as the final output.
