
## train_1

**input:**
```
0 0 1 0 1 1 1 1 0 1 1 1 1 0 0 1 1 1 1 0 0 0 1 1 1 0 0 0
```


**output:**
```
0 0 1 0 7 7 7 7 0 7 7 7 7 0 0 7 7 7 7 0 0 0 1 1 1 0 0 0
```


## train_2

**input:**
```
0 0 0 1 1 1 1 1 0 0 1 1 1 1 0 0 0 1 1 1 1 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 7 7 7 7 7 0 0 1 1 1 1 0 0 0 1 1 1 1 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 1 1 0 1 1 1 1 1 1 1 0 1 1 1 0 0 1 1 1 1 1 0 0 0 0 0
```


**output:**
```
0 0 1 1 0 7 7 7 7 7 7 7 0 1 1 1 0 0 1 1 1 1 1 0 0 0 0 0
```

*   **Perception:** The task involves processing a single-row grid. The input grid contains sequences of white (0) and blue (1) pixels. The output grid shows that some sequences of blue pixels have been changed to orange (7), while others remain blue. White pixels are unchanged. Specifically, contiguous horizontal sequences of exactly four blue pixels are transformed into sequences of four orange pixels. Blue sequences of other lengths (like the single blue pixel and the sequence of three blue pixels) are left untouched.

*   **Facts:**
    
```yaml
    task_type: color_change_conditional
    grid_dimensionality: 1D # Effectively 1D as it's a single row
    objects:
      - type: sequence
        color: blue (1)
        attributes:
          - length
    actions:
      - type: color_change
        source_color: blue (1)
        target_color: orange (7)
        condition: Applies only to blue sequences with a length of exactly 4.
    background: white (0) pixels remain unchanged.
    unchanged_elements:
      - blue (1) sequences with lengths other than 4.
    ```


*   **Natural Language Program:**
    1.  Iterate through the input grid to identify contiguous horizontal sequences of blue (1) pixels.
    2.  For each identified blue sequence, determine its length.
    3.  If the length of a blue sequence is exactly 4, change the color of all pixels within that specific sequence to orange (7) in the output grid.
    4.  If the length of a blue sequence is not 4, keep the pixels as blue (1) in the output grid.
    5.  Copy all other pixels (white pixels) directly from the input to the output grid without modification.
