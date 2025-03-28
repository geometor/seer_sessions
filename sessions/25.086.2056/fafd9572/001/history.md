
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0 1 1 0 0
0 0 0 0 0 1 0 0 1 0 0 0
0 2 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 4 4 0 0
0 0 0 0 0 2 0 0 4 0 0 0
0 2 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
1 1 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
1 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 1 1 0 0 0 0 0 0 0 2 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0
1 1 0 0 0 0 0 0 1 1 0 0 0 0 0 3 2 0
1 0 1 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 1 0 1 0 1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 3 0 3 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 3 3 0 0 0 0 0 0 0 2 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0
3 3 0 0 0 0 0 0 3 3 0 0 0 0 0 3 2 0
3 0 3 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 2 0 2 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves identifying objects of a specific color (blue, value 1) and recoloring them based on a set of "palette" colors present elsewhere in the input grid. The non-blue, non-white background elements remain unchanged. The transformation preserves the shapes of the blue objects but alters their color according to a rule based on the order of the blue objects and the order of the available palette colors. The order for both blue objects and palette colors seems to be determined by a top-to-bottom, left-to-right scan of the grid. Specifically, the first blue object identified takes the color of the first palette color identified, the last blue object takes the color of the last palette color, and any blue objects in between take the color of the second palette color identified.

*   **Facts:**
    
```yaml
    elements:
      - type: background
        color: white (0)
        description: The predominant color, typically filling empty space. Remains unchanged.
      - type: target_object
        color: blue (1)
        description: Contiguous blocks of blue pixels. These are the objects acted upon.
        properties:
          - shape: The spatial arrangement of pixels within the object. Preserved in the output.
          - position: Location within the grid, defined by constituent pixels.
          - order: Determined by the top-leftmost pixel during a top-to-bottom, left-to-right scan relative to other blue objects.
      - type: palette_color
        color: any color except white (0) and blue (1)
        description: Pixels or objects whose colors define the replacement colors for target_objects.
        properties:
          - color_value: The specific color (e.g., red, green, yellow).
          - order: Determined by the first pixel of this color encountered during a top-to-bottom, left-to-right scan relative to other unique palette colors.
        relationship: Provides the source colors for the transformation. Palette colors themselves and their locations remain unchanged in the output.

    actions:
      - action: identify_palette
        description: Find all unique colors present in the input grid, excluding white (0) and blue (1).
      - action: order_palette
        description: Order the identified palette colors based on the row and column index of their first occurrence (top-to-bottom, left-to-right scan).
      - action: identify_targets
        description: Find all contiguous objects composed solely of blue (1) pixels.
      - action: order_targets
        description: Order the identified blue objects based on the row and column index of their top-leftmost pixel (top-to-bottom, left-to-right scan).
      - action: recolor_targets
        description: Change the color of all pixels within each blue object based on a specific mapping rule using the ordered targets and ordered palette.
        rule:
          - The first target object takes the first palette color.
          - If there is more than one target object and more than one palette color:
            - The last target object takes the last palette color.
            - All intermediate target objects take the second palette color.
          - If there is more than one target object but only one palette color, all target objects take that single palette color.

    output_grid:
      description: A grid of the same dimensions as the input, containing the original non-blue objects/pixels and the recolored target objects.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the basis for the output grid.
    2.  Identify the set of unique "palette colors" present in the input grid by finding all colors other than white (0) and blue (1).
    3.  Determine the order of these palette colors by scanning the input grid row-by-row from top to bottom, and left-to-right within each row, recording the order in which each unique palette color is first encountered.
    4.  Identify all distinct contiguous objects composed entirely of blue (1) pixels.
    5.  Determine the order of these blue objects by finding the top-leftmost pixel of each object and ordering the objects based on these pixels' positions using a top-to-bottom, left-to-right scan.
    6.  If no blue objects were found or no palette colors were found, the process is complete, and the copied grid is the final output.
    7.  Let the ordered blue objects be `B1, B2, ..., Bn` and the ordered palette colors be `P1, P2, ..., Pm`.
    8.  Recolor all pixels belonging to the first blue object (`B1`) with the first palette color (`P1`) in the output grid.
    9.  If there is more than one blue object (`n > 1`):
        a.  If there is only one palette color (`m == 1`), recolor all remaining blue objects (`B2` through `Bn`) with that single palette color (`P1`).
        b.  If there is more than one palette color (`m > 1`), then:
            i.  Recolor the last blue object (`Bn`) with the last palette color (`Pm`).
            ii. Recolor all intermediate blue objects (`B2` through `Bn-1`, if any exist) with the second palette color (`P2`).
    10. Return the modified output grid.
