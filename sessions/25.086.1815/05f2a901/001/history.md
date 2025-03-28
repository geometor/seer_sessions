
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 8 8 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 0 2 2 8 8 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
2 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
2 2 0 2 0 0 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids contain pixels of white (0), red (2), and azure (8).
    *   Each grid features exactly one contiguous object composed of red pixels and one contiguous object composed of azure pixels, set against a white background.
    *   Comparing input and output grids reveals that the red object changes position while the azure object and the white background remain stationary.
    *   The movement of the red object appears directed towards the azure object.
    *   The movement occurs along a single axis (either horizontal or vertical) per example.
    *   The axis of movement seems to be the one where the initial separation between the objects is largest.
    *   The distance moved seems calculated to leave a one-pixel gap between the objects along the axis of movement.

*   **Facts:**
    
```yaml
    elements:
      - object_type: grid
        properties:
          - background_color: white (0)
      - object_type: shape
        identifier: red_object
        properties:
          - color: red (2)
          - count: 1
      - object_type: shape
        identifier: azure_object
        properties:
          - color: azure (8)
          - count: 1
          - static: true # Does not move between input and output

    relationships:
      - type: spatial
        object1: red_object
        object2: azure_object
        details: Objects are spatially separated. Their relative positions vary across examples.

    actions:
      - action_type: move
        target: red_object
        details:
          - The red object is translated (moved without rotation or scaling).
          - The azure object serves as a reference point or target for the movement.
          - The direction of movement (horizontal or vertical) depends on the axis of greatest separation between the red and azure objects' bounding boxes.
          - The distance of movement is determined by the initial gap between the objects along the chosen axis, such that the final gap along that axis is 1 pixel.
          - If the horizontal gap is strictly greater than the vertical gap, move horizontally. Otherwise (vertical gap >= horizontal gap), move vertically.
          - The movement distance equals the initial gap along the chosen axis.
          - Gap definition: The number of background pixels strictly between the closest edges of the two objects' bounding boxes along a given axis. `gap = max(0, min_coord_obj2 - max_coord_obj1 - 1)` or `gap = max(0, min_coord_obj1 - max_coord_obj2 - 1)`.

    state_changes:
      - object: red_object
        change: position
      - object: azure_object
        change: none
      - object: background (white pixels)
        change: none (except where overwritten by the moved red object or vacated by its original position)
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous red object and the contiguous azure object within the input grid. Determine their respective bounding boxes.
    2.  Calculate the horizontal gap between the bounding boxes (the number of columns strictly between the rightmost column of one object and the leftmost column of the other). If the objects overlap horizontally or are adjacent, the horizontal gap is 0.
    3.  Calculate the vertical gap between the bounding boxes (the number of rows strictly between the bottommost row of one object and the topmost row of the other). If the objects overlap vertically or are adjacent, the vertical gap is 0.
    4.  Compare the horizontal gap and the vertical gap.
    5.  If the horizontal gap is strictly greater than the vertical gap:
        *   Determine the horizontal direction from the red object towards the azure object (left or right).
        *   Translate the entire red object horizontally in that direction by a distance equal to the calculated horizontal gap.
    6.  Otherwise (if the vertical gap is greater than or equal to the horizontal gap):
        *   Determine the vertical direction from the red object towards the azure object (up or down).
        *   Translate the entire red object vertically in that direction by a distance equal to the calculated vertical gap.
    7.  Construct the output grid by placing the translated red object and the original azure object onto a white background of the same dimensions as the input grid.
