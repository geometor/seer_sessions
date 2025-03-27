
## train_1

**input:**
```
0 0 0 1
0 0 0 0
2 2 2 0
0 0 0 0
0 3 3 0
0 0 0 0
8 8 8 8
```


**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
0 0 3 3
0 2 2 2
8 8 8 8
```


## train_2

**input:**
```
0 2 2 0 0 0 0
0 0 0 0 3 0 0
1 1 1 0 0 0 0
0 0 0 0 0 0 0
0 5 5 5 5 5 5
0 0 0 0 0 0 0
6 6 6 6 6 0 0
0 0 0 4 4 4 4
0 0 0 0 0 0 0
8 8 8 8 8 8 8
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 3
0 0 0 0 0 2 2
0 0 0 0 1 1 1
0 0 0 4 4 4 4
0 0 6 6 6 6 6
0 5 5 5 5 5 5
8 8 8 8 8 8 8
```


## train_3

**input:**
```
2 2 0
0 4 0
8 8 8
```


**output:**
```
0 0 4
0 2 2
8 8 8
```

*   **Perception:**
    *   The input grids contain several distinct objects composed of non-white pixels against a white background.
    *   Each grid consistently features a solid horizontal line of `azure` (8) pixels at the bottom row. This line acts as a stable base or "ground".
    *   The other objects (blue, red, green, yellow, gray, magenta) appear to be positioned above this azure line.
    *   In the output grids, the azure line remains unchanged in its position.
    *   The other objects are rearranged. They appear to have moved downwards and rightwards.
    *   The objects seem to undergo a "gravity" effect, falling downwards until they encounter either the azure line or another object that has already settled.
    *   There's also a consistent rightward shift. The entire collection of non-azure, non-white objects seems to shift as a group so that the rightmost pixel among them aligns with the right edge of the grid *before* the gravity effect takes place.
    *   Objects stack vertically upon each other or the azure line, maintaining their relative horizontal positions after the initial rightward shift.

*   **Facts:**
    
```yaml
    Examples:
      - Input:
          Grid_Size: [7, 4]
          Objects:
            - ID: 1
              Color: blue
              Pixels: [[0, 3]]
            - ID: 2
              Color: red
              Pixels: [[2, 0], [2, 1], [2, 2]]
            - ID: 3
              Color: green
              Pixels: [[4, 1], [4, 2]]
            - ID: 4
              Color: azure
              Pixels: [[6, 0], [6, 1], [6, 2], [6, 3]] # Ground
          Background: white (0)
        Output:
          Grid_Size: [7, 4]
          Objects:
            - ID: 1 # Originally blue
              Pixels: [[3, 3]]
            - ID: 3 # Originally green
              Pixels: [[4, 2], [4, 3]]
            - ID: 2 # Originally red
              Pixels: [[5, 1], [5, 2], [5, 3]]
            - ID: 4 # Ground
              Pixels: [[6, 0], [6, 1], [6, 2], [6, 3]]
          Action:
            - Collective right-shift of objects 1, 2, 3 until rightmost pixel (originally at col 3) hits grid edge (col 3).
            - Object 2 falls onto Object 4 (ground).
            - Object 3 falls onto Object 2.
            - Object 1 falls onto Object 3.
      - Input:
          Grid_Size: [10, 7]
          Objects:
            - ID: 1
              Color: red
              Pixels: [[0, 1], [0, 2]]
            - ID: 2
              Color: green
              Pixels: [[1, 4]]
            - ID: 3
              Color: blue
              Pixels: [[2, 0], [2, 1], [2, 2]]
            - ID: 4
              Color: gray
              Pixels: [[4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6]]
            - ID: 5
              Color: magenta
              Pixels: [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4]]
            - ID: 6
              Color: yellow
              Pixels: [[7, 3], [7, 4], [7, 5], [7, 6]]
            - ID: 7
              Color: azure
              Pixels: [[9, 0], [9, 1], [9, 2], [9, 3], [9, 4], [9, 5], [9, 6], [9, 7]] # Ground (width 8, but grid width 7) -> check this - yes width 7, cols 0-6
          Background: white (0)
        Output:
          Grid_Size: [10, 7]
          Objects:
             - ID: 2 # Originally green
               Pixels: [[3, 6]]
             - ID: 1 # Originally red
               Pixels: [[4, 5], [4, 6]]
             - ID: 3 # Originally blue
               Pixels: [[5, 4], [5, 5], [5, 6]]
             - ID: 6 # Originally yellow
               Pixels: [[6, 3], [6, 4], [6, 5], [6, 6]]
             - ID: 5 # Originally magenta
               Pixels: [[7, 2], [7, 3], [7, 4], [7, 5], [7, 6]]
             - ID: 4 # Originally gray
               Pixels: [[8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [8, 6]]
             - ID: 7 # Ground
               Pixels: [[9, 0], [9, 1], [9, 2], [9, 3], [9, 4], [9, 5], [9, 6]] # Note: Example 2 input/output width is 7
          Action:
            - Collective right-shift of objects 1-6 until rightmost pixel (originally col 6) hits grid edge (col 6).
            - Gravity simulation: Objects fall and stack on ground (Object 7) or other settled objects.
      - Input:
          Grid_Size: [3, 3]
          Objects:
            - ID: 1
              Color: red
              Pixels: [[0, 0], [0, 1]]
            - ID: 2
              Color: yellow
              Pixels: [[1, 1]]
            - ID: 3
              Color: azure
              Pixels: [[2, 0], [2, 1], [2, 2]] # Ground
          Background: white (0)
        Output:
          Grid_Size: [3, 3]
          Objects:
            - ID: 2 # Originally yellow
              Pixels: [[0, 2]]
            - ID: 1 # Originally red
              Pixels: [[1, 1], [1, 2]]
            - ID: 3 # Ground
              Pixels: [[2, 0], [2, 1], [2, 2]]
          Action:
            - Collective right-shift of objects 1, 2 until rightmost pixel (col 1) hits grid edge (col 2). Object 1 moves 1 right, Object 2 moves 1 right.
            - Gravity simulation: Objects fall and stack. Object 1 falls onto Object 3. Object 2 falls onto Object 1 (specifically the part at [1, 2]).

    Properties:
      - Objects are contiguous blocks of non-white pixels.
      - An azure line at the bottom acts as a non-moving ground.
      - Other objects are subject to movement.
    Relationships:
      - Objects can be stacked vertically.
      - Objects rest upon the ground or other objects below them.
    Actions:
      - Identify: Separate the ground (azure line) from movable objects.
      - Group: Treat all movable objects initially as a single composite shape for horizontal alignment.
      - Align Right: Calculate the rightmost column occupied by any movable object pixel. Shift the entire group horizontally so this rightmost column aligns with the grid's rightmost column.
      - Simulate Gravity: Starting from the bottom-most movable objects, move each object straight down until it hits the ground or another already settled object. Maintain relative horizontal positions established after the alignment step.
      - Render: Create the output grid with the ground and settled objects in their final positions.

    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, filled with the background color (white).
    2.  Identify the horizontal line of `azure` (8) pixels at the bottom row. This is the "ground". Copy the ground to its same position in the output grid.
    3.  Identify all other distinct, contiguous objects (pixels with colors 1-7, 9) in the input grid. These are the "movable objects".
    4.  Determine the maximum column index (`max_col_movable`) occupied by any pixel of any movable object in the input grid.
    5.  Determine the maximum column index of the grid (`grid_max_col`).
    6.  Calculate the horizontal shift required: `shift = grid_max_col - max_col_movable`.
    7.  Create a temporary representation of the movable objects, shifting each object's horizontal coordinates by `shift` columns to the right.
    8.  Simulate gravity vertically for the shifted movable objects:
        *   Process the objects row by row from bottom to top (or process objects based on their lowest initial row).
        *   For each object, determine its target resting row by finding the highest occupied row below its lowest pixel (either the ground row or the top row of an already placed object in the same columns).
        *   Move the object straight down so its lowest pixels are just above the determined resting row. Place the object's pixels onto the output grid. Mark these positions as occupied for subsequent object placement.
    9.  Ensure that objects maintain their shape and relative horizontal positions (as determined after the initial rightward shift) during the downward movement.
    10. The final output grid contains the unchanged ground and the movable objects settled in their new positions after the right-alignment and gravity simulation.
