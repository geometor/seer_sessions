
## train_1

**input:**
```
0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 1 7 0 0 2 0 0 0 0 8 0
0 0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 5 4 0 0 0 0 6 0 0 0 0
0 0 0 4 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 9 6 0 0
0 0 0 0 0 0 0 0 0 9 0 0 0
3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 8 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 1 7 0 0 2 0 3 3 3 3 0
0 0 0 7 0 0 0 0 0 0 8 3 0
0 0 0 0 0 0 0 0 0 0 0 3 0
0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 5 4 0 0 0 0 9 9 0 0 0
0 0 0 4 0 0 0 0 9 6 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 6 7 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 9 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
0 0 6 7 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 9 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception**

1.  **Input/Output Structure:** Both input and output are grids of pixels with different colors. The background is white (0).
2.  **Objects:** The grids contain distinct objects:
    *   Some objects are single pixels of a specific color (e.g., the Red pixel in `train_1`, the lone Orange pixel in `train_2`).
    *   Other objects are composite shapes made of multiple pixels, sometimes involving more than one color in close proximity (e.g., the Green 'L' with an adjacent Azure pixel in `train_1`, the Magenta 'L' with an internal Orange pixel in `train_2`).
3.  **Transformation:** The core transformation appears to be the movement of one specific composite object pattern. Other objects remain in their original positions.
4.  **Trigger:** The movement seems to be triggered by the presence of a specific single, isolated pixel. The color of this trigger pixel determines *which* composite object pattern moves.
    *   In `train_1`, the single Red (2) pixel seems to trigger the movement of the Green/Azure pattern.
    *   In `train_2`, the single Orange (7) pixel seems to trigger the movement of the Magenta/Orange pattern.
5.  **Movement Rule:**
    *   The original instance of the moving pattern is erased (set to white 0).
    *   The pattern is then redrawn (stamped) at a new location.
    *   The new location seems related to the trigger pixel's location.
    *   In `train_2`, the Magenta/Orange pattern's top-left corner moves exactly to the location of the Orange trigger pixel (offset 0, 0).
    *   In `train_1`, the Green/Azure pattern's top-left corner moves to a location that is offset by (0 rows, +2 columns) relative to the Red trigger pixel's location.
6.  **Hypothesis:** There's a mapping between trigger pixel colors and specific object patterns + placement offsets. When a trigger pixel is found, its corresponding pattern is located, erased from its original position, and redrawn relative to the trigger pixel using the associated offset.

**Facts**


```yaml
Task: Move a specific object pattern based on a trigger pixel.

Input_Grid:
  - Contains a background (white, 0).
  - Contains multiple distinct colored objects.
  - Objects_Types:
      - Single_Pixels: Act as triggers. Color determines action. (e.g., Red(2), Orange(7))
      - Composite_Patterns: Specific arrangements of pixels, potentially multi-colored. Some are mobile, others static. (e.g., Green-L+Azure, Magenta-L+Orange, Orange-L, Yellow-L+Gray, etc.)
  - Key_Features:
      - Presence of a unique, single trigger pixel.
      - Presence of a unique instance of the 'mover' pattern corresponding to the trigger.

Output_Grid:
  - Mostly identical to Input_Grid.
  - Differences:
      - The 'mover' pattern is absent from its original location (replaced by white 0).
      - The 'mover' pattern is drawn at a new location.

Transformation:
  - Action: Move (erase and redraw) a specific composite object pattern.
  - Trigger: A single pixel of a specific color.
  - Target_Object: The composite pattern associated with the trigger color.
  - Destination: Determined by the trigger pixel's location plus a color-specific offset.
  - Overwrite: The redrawn pattern overwrites existing pixels at the destination.

Relationships:
  - Trigger_Color -> Mover_Pattern_Type:
      - Red(2) -> Green-L+Azure Pattern
      - Orange(7) -> Magenta-L+Orange Pattern
  - Trigger_Color -> Placement_Offset (relative to trigger pixel location):
      - Red(2) -> (Row_Offset=0, Col_Offset=2)
      - Orange(7) -> (Row_Offset=0, Col_Offset=0)
  - Rule: New_Pattern_TopLeft = Trigger_Location + Placement_Offset
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to find a single pixel that is isolated (not connected horizontally, vertically, or diagonally to another pixel of the same color). This is the "trigger pixel". Record its color, `C_trigger`, and location, `(R_trigger, C_trigger)`.
3.  Determine the corresponding "mover shape pattern", `P_mover`, and the "placement offset", `(dR, dC)`, based on `C_trigger`:
    *   If `C_trigger` is Red (2), `P_mover` is the pattern consisting of a Green (3) 'L' shape with an adjacent Azure (8) pixel, and the offset `(dR, dC)` is (0, 2).
    *   If `C_trigger` is Orange (7), `P_mover` is the pattern consisting of a Magenta (6) 'L' shape with an internal Orange (7) pixel, and the offset `(dR, dC)` is (0, 0).
    *   *(Assumption: The task definition implies these are the only relevant trigger/pattern mappings needed based on the examples).*
4.  Locate the occurrence of `P_mover` in the input grid. Identify its bounding box and specifically its top-left corner coordinates, `(R_original, C_original)`.
5.  Erase `P_mover` from the output grid by changing all pixels within its original bounding box that belong to the pattern back to the background color (white, 0).
6.  Calculate the destination top-left corner for redrawing the pattern: `(R_new, C_new) = (R_trigger + dR, C_trigger + dC)`.
7.  Draw the `P_mover` pattern onto the output grid, starting at `(R_new, C_new)`. For each pixel in `P_mover` at a relative position `(r, c)` from its own top-left corner, set the pixel at `(R_new + r, C_new + c)` in the output grid to the corresponding color from the pattern, overwriting any previous value at that location.
8.  Return the final output grid.
