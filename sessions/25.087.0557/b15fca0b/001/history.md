
## train_1

**input:**
```
2 1 1 1 2
0 1 0 1 0
0 1 0 1 0
0 1 0 1 0
0 0 0 0 0
```


**output:**
```
2 1 1 1 2
4 1 0 1 4
4 1 0 1 4
4 1 0 1 4
4 4 4 4 4
```


## train_2

**input:**
```
0 0 0 1 2
0 0 0 1 0
0 1 0 1 0
0 1 0 0 0
2 1 0 0 0
```


**output:**
```
0 0 0 1 2
4 4 4 1 4
4 1 4 1 4
4 1 4 4 4
2 1 0 0 0
```


## train_3

**input:**
```
2 0 0 0 0 0
1 1 1 1 0 0
0 0 0 0 0 0
0 0 0 1 1 1
0 0 0 0 0 2
0 0 0 0 0 0
```


**output:**
```
2 4 4 4 4 0
1 1 1 1 4 0
0 0 4 4 4 0
0 0 4 1 1 1
0 0 4 4 4 2
0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 2
0 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 0
2 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
4 4 4 4 4 2
4 1 1 1 1 1
4 4 4 4 4 4
1 1 1 1 1 4
2 4 4 4 4 4
0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 1 0 1 1 0 1 0 1 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
```


**output:**
```
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 4
0 0 0 1 1 0 0 0 1 4
4 4 4 1 1 4 4 4 1 4
4 1 4 1 1 4 1 4 1 4
4 1 4 4 4 4 1 4 4 4
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
```

*   **Perception:**
    *   The input and output grids have the same dimensions for each example.
    *   The primary colors involved in the input are white (0), blue (1), and red (2).
    *   The output grids introduce a new color, yellow (4), while retaining the blue (1) and red (2) pixels in their original positions.
    *   The transformation involves changing some white (0) pixels in the input to yellow (4) in the output.
    *   Observing the patterns, the white pixels that change to yellow are always adjacent (horizontally, vertically, or diagonally) to at least one blue (1) pixel in the input grid.
    *   Pixels that are not white (0) in the input remain unchanged in the output.
    *   White pixels that are not adjacent to any blue pixels remain white.
    *   The red (2) pixels do not seem to influence the transformation; they simply persist in their locations.

*   **Facts:**
    
```yaml
    elements:
      - type: grid
        properties:
          - colors: white (0), blue (1), red (2) present in input
          - colors: white (0), blue (1), red (2), yellow (4) present in output
          - dimensions: input and output grids have identical dimensions per example
    transformation:
      - type: color_change
        input_color: white (0)
        output_color: yellow (4)
        condition:
          - type: adjacency
            target_color: blue (1)
            adjacency_type: [horizontal, vertical, diagonal] # 8 neighbours
            notes: A white pixel changes to yellow if at least one of its 8 neighbors is blue.
      - type: color_preservation
        colors: [blue (1), red (2)]
        notes: Blue and red pixels retain their color and position.
      - type: color_preservation
        color: white (0)
        condition:
          - type: adjacency
            target_color: blue (1)
            adjacency_type: [horizontal, vertical, diagonal]
            negation: true # No blue neighbors
        notes: White pixels not adjacent to any blue pixels remain white.
    ```


*   **Natural Language Program:**
    1.  Create an output grid with the same dimensions as the input grid.
    2.  Iterate through each pixel of the input grid using its row and column index.
    3.  For the current pixel:
        a.  Check the color of the pixel in the input grid.
        b.  If the input pixel's color is white (0):
            i.  Examine all 8 neighboring pixels (horizontal, vertical, and diagonal neighbors).
            ii. If any of these neighbors in the input grid have the color blue (1), set the corresponding pixel in the output grid to yellow (4).
            iii. If none of the neighbors are blue (1), set the corresponding pixel in the output grid to white (0).
        c.  If the input pixel's color is not white (0) (i.e., it's blue (1) or red (2) or any other color), copy its color directly to the corresponding pixel in the output grid.
    4.  Return the completed output grid.
