
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 1
0 0 2 0 0 0 0 2 0 0
0 0 2 0 0 1 0 2 0 0
0 0 2 0 0 0 0 2 0 0
0 0 2 0 0 0 0 2 0 0
0 0 2 2 2 2 2 2 0 0
1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
```


**output:**
```
0
0
0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 0 0 0
0 0 0 7 6 0 7 0 0 0
0 0 0 7 0 6 7 0 0 0
0 0 0 7 0 0 7 0 0 0
0 6 0 7 6 0 7 0 0 0
0 0 0 7 0 0 7 0 0 0
0 0 0 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
```


**output:**
```
0
0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 3 0 0
0 0 3 0 9 0 0 3 0 0
9 0 3 0 0 0 0 3 0 9
0 0 3 0 0 0 0 3 0 0
0 0 3 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
```


**output:**
```
0
0
0
```

*   **Perception:** The input grids contain a large rectangular frame of one color, potentially with some pixels missing from the frame itself. Inside and outside this frame, there are scattered pixels of another distinct color. The background is white (0). The output is a small vertical column of white pixels. The height of this output column seems related to the number of scattered pixels located *outside* the main frame.

*   **YAML Facts:**
    
```yaml
    background_color: white (0)
    elements:
      - type: frame
        description: A large, roughly rectangular object made of a single dominant color (red, orange, or green in examples). It defines an inner and outer region.
        properties:
          - color: Varies (red=2, orange=7, green=3)
          - shape: Rectangular frame (potentially incomplete)
          - role: Defines boundaries
      - type: scattered_pixels
        description: Single pixels of a color different from the background and the frame.
        properties:
          - color: Varies (blue=1, magenta=6, maroon=9), but consistent within a single example and different from the frame color.
          - quantity: Multiple instances occur both inside and outside the frame.
          - role: Items to be counted based on location relative to the frame.
    relationships:
      - type: spatial
        description: Scattered pixels can be inside or outside the bounding box of the frame.
    transformation:
      - action: identify
        target: frame object
        details: Find the largest connected component that is not the background color. Determine its bounding box.
      - action: identify
        target: scattered_pixels
        details: Find all pixels whose color is neither the background nor the frame color.
      - action: filter
        target: scattered_pixels
        condition: Pixels located outside the frame's bounding box.
      - action: count
        target: filtered scattered_pixels
        result: A number N.
      - action: generate_output
        details: Create an N x 1 grid filled entirely with the background color (white=0).
    output_characteristics:
      - shape: N x 1 grid (column vector)
      - content: Uniformly background color (white=0)
      - size_determinant: The count (N) of scattered pixels located outside the frame.

    ```


*   **Natural Language Program:**
    1.  Identify the background color (white, 0).
    2.  Find the largest connected object whose color is not the background color. This object is the 'frame'. Determine the minimum bounding box containing this frame.
    3.  Identify all pixels whose color is neither the background color nor the frame's color. These are the 'scattered pixels'. Note their color.
    4.  Count how many of these 'scattered pixels' lie strictly outside the bounding box of the frame. Let this count be N.
    5.  Generate the output grid as an N x 1 grid (a vertical column N pixels high and 1 pixel wide) filled entirely with the background color (white, 0).
