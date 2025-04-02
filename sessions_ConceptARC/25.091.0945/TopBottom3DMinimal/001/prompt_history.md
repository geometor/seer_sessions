
## train_1

**input:**
```
2 2 2 2 2 0 0 0
2 0 3 3 2 3 3 0
2 0 3 3 2 3 3 0
2 0 3 3 2 3 3 0
2 2 2 2 2 3 3 0
0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 0 0 0
2 0 3 3 3 3 3 0
2 0 3 3 3 3 3 0
2 0 3 3 3 3 3 0
2 2 3 3 3 3 3 0
0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 6 6 6 6
0 0 7 7 7 7 7 6
0 0 7 0 6 6 7 6
0 0 7 7 7 7 7 6
0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 6 6 6
0 0 7 7 6 6 6 6
0 0 7 0 6 6 6 6
0 0 7 7 6 6 6 6
0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

### Perception

1.  **Grid Structure:** Both examples operate on 8x8 grids. The background color is consistently white (0).
2.  **Key Objects:** In both inputs, there are two primary non-background objects:
    *   A larger object that forms a kind of 'U' shape or frame, open on one side (left in example 1, top in example 2). Let's call this the "Frame Object".
    *   One or more other distinct objects located partially inside or adjacent to the opening/cavity of the Frame Object. Let's call these "Inner Objects".
3.  **Interaction:** The transformation clearly involves an interaction between the Frame Object and the Inner Object(s) where they are adjacent or nearly adjacent. The output grid shows modifications primarily at the boundary between these objects.
4.  **Color Dependency:** The nature of the modification seems to depend crucially on the color of the Inner Object.
    *   In `train_1`, the Frame is Red(2) and the Inner Object is Green(3). The output shows some pixels of the *Frame* changing color to match the *Inner* object (Red -> Green).
    *   In `train_2`, the Frame is Magenta(6) and the Inner Object is Orange(7). The output shows some pixels of the *Inner* object changing color to match the *Frame* (Orange -> Magenta).
5.  **Specific Rule Trigger:** The presence of Green(3) as the Inner Object color in `train_1` appears to trigger a different rule ("Frame pixels change") compared to `train_2` where the Inner Object color is Orange(7) ("Inner pixels change"). The specific color Green(3) seems to be the deciding factor.
6.  **Adjacency:** The changes occur only where pixels of the Frame Object and Inner Object(s) are adjacent (sharing a side, i.e., 4-connectivity).

### Facts


```yaml
task_context:
  grid_size: ثابت (8x8 in examples)
  background_color: white (0)
  num_examples: 2

identified_objects:
  - object_type: Frame
    description: A large, often U-shaped or enclosing object.
    properties:
      - color: (Red(2) in ex1, Magenta(6) in ex2)
      - forms_boundary: True
  - object_type: InnerObject
    description: An object adjacent to the Frame, often partially within its concave area.
    properties:
      - color: (Green(3) in ex1, Orange(7) in ex2)
      - position: Adjacent to Frame object
      - count: Can be one or more parts (ex1 has two green parts, ex2 has one orange part)

relationships:
  - type: Adjacency
    description: Pixels of the Frame object are adjacent (4-connectivity) to pixels of the InnerObject. This adjacency is the site of interaction.

transformation_properties:
  - type: Conditional Color Change
    description: The color change rule depends on the color of the InnerObject.
    condition: InnerObject color == Green(3)
    rule_if_true: Certain Frame pixels adjacent to the InnerObject change color to Green(3).
    rule_if_false: Certain InnerObject pixels adjacent to the Frame change color to the Frame's color.
  - type: Locality
    description: Changes only occur at or near the boundary pixels involved in the adjacency relationship.
  - type: Frame Integrity (Partial)
    description: The Frame object mostly retains its shape and color, except when the InnerObject is Green(3).
  - type: Inner Object Integrity (Partial)
    description: The InnerObject mostly retains its shape and color, except when it's not Green(3) and adjacent to the Frame.

example_specific_details:
  - example: train_1
    frame_color: Red(2)
    inner_color: Green(3)
    action: Change adjacent Frame pixels (Red 2) to Inner color (Green 3).
    affected_pixels: Specific pixels on the 'bottom' edge of the U-frame change.
  - example: train_2
    frame_color: Magenta(6)
    inner_color: Orange(7)
    action: Change adjacent Inner pixels (Orange 7) to Frame color (Magenta 6).
    affected_pixels: Specific Orange pixels touching the Magenta frame change.

```


### Natural Language Program

1.  Identify the background color (assume white 0).
2.  Identify all contiguous non-background objects.
3.  Designate the object that forms a partial enclosure or 'U' shape as the "Frame Object". Record its color (`C_frame`).
4.  Identify any other distinct non-background object(s) adjacent (sharing a side, 4-connectivity) to the Frame Object as "Inner Objects". Determine the set of colors (`S_inner`) present in these Inner Objects.
5.  Check if the color Green(3) is present in `S_inner`.
6.  **If Green(3) is in `S_inner`:**
    *   Iterate through each pixel `P_frame` belonging to the Frame Object.
    *   Check if `P_frame` is adjacent (4-connectivity) to *any* pixel `P_inner` belonging to an Inner Object whose color is Green(3).
    *   If such adjacency exists, change the color of `P_frame` in the output grid to Green(3).
    *   Keep all other pixels (non-adjacent frame pixels, inner object pixels, background pixels) unchanged from the input grid.
7.  **If Green(3) is NOT in `S_inner`:**
    *   Iterate through each pixel `P_inner` belonging to any Inner Object.
    *   Check if `P_inner` is adjacent (4-connectivity) to *any* pixel `P_frame` belonging to the Frame Object.
    *   If such adjacency exists, change the color of `P_inner` in the output grid to `C_frame` (the color of the Frame Object).
    *   Keep all other pixels (non-adjacent inner object pixels, frame object pixels
