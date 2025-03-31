*   **Perception:** The input grid contains a white background (0) and one or more distinct objects composed of azure pixels (8). The output grid maintains the white background and the exact shapes and positions of the input objects, but the objects are recolored. Each input azure object is replaced by an object of the same shape, colored either blue (1) or red (2). The core task is to determine the rule for assigning either blue or red to each distinct azure object from the input. Analysis suggests that exactly one object is colored red, and all others are colored blue. The object chosen to be red is the one with the smallest area (fewest pixels). If multiple objects share the smallest area, the tie is broken by choosing the object whose top-most pixel has the lowest row index. If there is still a tie, it's broken by choosing the object whose top-most, left-most pixel has the lowest column index.

*   **YAML:**
    
```yaml
    Observations:
      - Input and output grids have the same dimensions.
      - The background color (white, 0) remains unchanged.
      - Input contains distinct contiguous objects of azure color (8).
      - Output contains objects matching the shape and position of the input azure objects.
      - Output object colors are either blue (1) or red (2).
    Objects:
      - type: contiguous block of non-background pixels
      - color_input: azure (8)
      - color_output: blue (1) or red (2)
      - properties:
          - pixels: list of coordinates [(r1, c1), (r2, c2), ...]
          - size: count of pixels
          - top_left_pixel: the pixel (r, c) within the object with the minimum r, and minimum c for that r.
    Relationships:
      - Each azure object in the input maps directly to one blue or red object in the output.
      - Exactly one object in the output is red (2).
      - All other objects in the output are blue (1).
    Transformation:
      - Identify all distinct azure (8) objects in the input grid.
      - Calculate the size (pixel count) for each object.
      - Find the minimum size among all objects.
      - Identify all objects that have this minimum size.
      - If only one object has the minimum size:
          - This object is designated as the 'target' object.
      - If multiple objects share the minimum size:
          - Find the top-left pixel (minimum row, then minimum column) for each of these smallest objects.
          - Select the object whose top-left pixel has the minimum row index.
          - If there is still a tie (multiple smallest objects share the same minimum row index for their top-left pixel):
              - Select the object among the tied ones whose top-left pixel has the minimum column index.
          - This selected object is designated as the 'target' object.
      - Recolor the 'target' object to red (2).
      - Recolor all other azure objects to blue (1).
      - Preserve the white background pixels.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid template.
    2.  Identify all distinct contiguous objects composed of azure (8) pixels in the input grid. For each object, record its pixels, calculate its size (number of pixels), and determine its top-leftmost pixel (minimum row index, then minimum column index for that row).
    3.  Find the minimum size among all identified azure objects.
    4.  Filter the objects to find all candidates that have this minimum size.
    5.  Initialize the 'target' object reference to null.
    6.  If there is only one candidate object (unique minimum size), set the 'target' object reference to this object.
    7.  If there are multiple candidate objects (tie in minimum size):
        a.  Find the minimum row index among the top-leftmost pixels of the candidate objects.
        b.  Filter the candidates further to keep only those whose top-leftmost pixel has this minimum row index.
        c.  If only one candidate remains after filtering by row, set the 'target' object reference to this object.
        d.  If multiple candidates still remain (tie in minimum size and minimum row index):
            i.  Find the minimum column index among the top-leftmost pixels of the remaining candidates.
            ii. Set the 'target' object reference to the candidate whose top-leftmost pixel has this minimum column index (there should only be one).
    8.  Iterate through all identified azure objects from step 2.
    9.  For each object:
        a.  If the current object is the 'target' object identified in steps 5-7, change the color of all its corresponding pixels in the output grid template to red (2).
        b.  Otherwise (if the current object is not the 'target' object), change the color of all its corresponding pixels in the output grid template to blue (1).
    10. Return the modified output grid template.