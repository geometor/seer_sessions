
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 2 0 3 5 0 2 0 0 0 0
0 0 0 0 2 0 6 8 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0
0 0 0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 2
2 3 3 5 5 2
2 3 3 5 5 2
2 6 6 8 8 2
2 6 6 8 8 2
2 2 2 2 2 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 0 0
0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 2 0 3 3 4 4 0 0 0 2 0 0
0 0 2 0 3 3 4 4 0 0 0 2 0 0
0 0 2 0 1 1 8 8 0 0 0 2 0 0
0 0 2 0 1 1 8 8 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 2 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 2 2 2 2 2
2 3 3 3 3 4 4 4 4 2
2 3 3 3 3 4 4 4 4 2
2 3 3 3 3 4 4 4 4 2
2 3 3 3 3 4 4 4 4 2
2 1 1 1 1 8 8 8 8 2
2 1 1 1 1 8 8 8 8 2
2 1 1 1 1 8 8 8 8 2
2 1 1 1 1 8 8 8 8 2
2 2 2 2 2 2 2 2 2 2
```

Okay, let's analyze the provided examples.

## Perception

1.  **Input Grid Structure:** Both input examples feature a large grid (14x14) primarily filled with the background color white (0). Within this background, there is a hollow rectangle constructed from red (2) pixels. Inside this red rectangle, there are various other colored pixels arranged in small blocks or individually.
2.  **Output Grid Structure:** The output grids are smaller than the input grids. They consist of a central area containing colored pixels, surrounded by a 1-pixel thick border of red (2) pixels.
3.  **Color Mapping:** The colors inside the red rectangle in the input (excluding white and red itself) appear in the central area of the output grid. The background white (0) pixels from the input's inner region do not seem to map directly to the output's central area, except possibly influencing spacing or scaling. The red (2) pixels forming the rectangle in the input correspond to the border color in the output.
4.  **Transformation:** The core transformation appears to involve:
    *   **Identifying Content:** Locating the pixels *inside* the red rectangle in the input grid that are *not* white (0) and *not* red (2).
    *   **Extraction:** Determining the smallest rectangular region (bounding box) that contains all these identified "content" pixels. Extracting this subgrid.
    *   **Scaling:** Enlarging this extracted subgrid. In `train_1`, a 2x2 content area becomes a 4x4 area in the output (before the border). In `train_2`, a 4x4 content area becomes an 8x8 area. This suggests each pixel in the extracted content subgrid is scaled up to a 2x2 block in the output's central area.
    *   **Framing:** Adding a 1-pixel thick border of red (2) pixels around the scaled-up content area to form the final output grid.

## Facts


```yaml
- task_description: "Extract a pattern of specific 'content' colors from the input, scale it up by 2x2, and add a red border."
- elements:
    - input_grid:
        - properties:
            - contains_background: True
              color: white (0)
            - contains_frame: True
              color: red (2)
              shape: rectangle (hollow)
            - contains_content_pixels: True
              colors: [blue (1), green (3), yellow (4), gray (5), magenta (6), azure (8)] # Colors other than background and frame
              location: inside the red frame
    - output_grid:
        - properties:
            - contains_border: True
              color: red (2)
              thickness: 1 pixel
            - contains_scaled_content: True
              source: content_pixels from input
              scale_factor: 2x2
- relationships:
    - relationship: "Input content pixels define the source pattern."
      source: input_grid.content_pixels
      target: source_pattern (intermediate)
    - relationship: "Source pattern is scaled to form the output's inner area."
      source: source_pattern
      target: output_grid.scaled_content
      transformation: scale each pixel to a 2x2 block
    - relationship: "Output border color matches the input frame color."
      source: input_grid.frame.color
      target: output_grid.border.color
    - relationship: "The minimal bounding box of input content pixels determines the source pattern."
      source: input_grid.content_pixels
      target: source_pattern
      transformation: find minimal bounding box, extract subgrid
- actions:
    - action: find_content_pixels
      input: input_grid
      output: coordinates of pixels not white (0) and not red (2)
    - action: determine_bounding_box
      input: coordinates of content_pixels
      output: top-left and bottom-right coordinates of the minimal bounding box
    - action: extract_source_pattern
      input: input_grid, bounding_box
      output: subgrid (source_pattern)
    - action: scale_pattern
      input: source_pattern
      parameter: scale_factor (2x2)
      output: scaled_grid (inner area of output)
    - action: add_border
      input: scaled_grid
      parameter: border_color (red, 2), border_thickness (1)
      output: final output_grid
```


## Natural Language Program

1.  Identify all pixels in the input grid that are *not* the background color white (0) and *not* the frame color red (2). These are the "content pixels".
2.  Find the minimum bounding box (smallest rectangle) that encloses all identified content pixels.
3.  Extract the subgrid from the input grid defined by this bounding box. This is the "source pattern".
4.  Create a new, larger grid ("scaled grid") whose height is twice the height of the source pattern and whose width is twice the width of the source pattern.
5.  Populate the scaled grid: For each pixel at `(row, col)` with color `C` in the source pattern, fill a 2x2 block of pixels in the scaled grid starting at `(row * 2, col * 2)` with the color `C`.
6.  Create the final output grid by adding a 1-pixel thick border of red (2) color around the entire scaled grid. The final output grid's dimensions will be `(scaled_grid_height + 2)` by `(scaled_grid_width + 2)`.
