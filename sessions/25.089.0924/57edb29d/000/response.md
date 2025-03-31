## Perception

1.  **Input Structure:** The input grids consist of a background color (Yellow, 4) and several distinct objects (contiguous regions of a single color). These objects often contain smaller patterns made of a *different*, single color (the "inner pattern color"). Within a single input grid, multiple objects of different colors might contain patterns made of the *same* inner pattern color.
2.  **Objects:** The main objects observed are Red(2), Blue(1), Green(3), and Azure(8).
3.  **Inner Patterns:** The inner patterns are made of Gray(5) in `train_1`, Orange(7) in `train_2`, and Magenta(6) in `train_3`. Notice that the inner pattern color is consistent across different host objects within the same input grid.
4.  **Output Structure:** The output grid is smaller than the input grid. It appears to be an extraction and recoloring of the pattern found *inside* one specific object from the input. The output grid uses the color of the selected host object as its "background" or "frame" color, and the inner pattern color for the pattern itself.
5.  **Transformation:** The core task involves identifying the correct "host" object from the input whose inner pattern should be extracted. The selection seems based on the *color* of the inner pattern common to multiple objects. Once the specific host object is identified using this rule, its bounding box is determined, and the pattern within that box is reproduced in the output, using the host color for the background and the inner pattern color for the pattern.

## Facts


```yaml
task_elements:
  - background_color: 4 # Yellow
  - objects:
      description: Contiguous regions of a single color, distinct from the background.
      properties:
        - color: The primary color of the object (e.g., Red, Blue, Green, Azure).
        - location: Position within the grid.
        - shape: General form.
        - bounding_box: The smallest rectangle enclosing the object.
        - contains_inner_pattern: Boolean, true if the object encloses pixels of the 'inner_pattern_color'.
  - inner_pattern_color:
      description: A single color (different from host object colors and background) found as pixels inside one or more host objects within a single input grid.
      examples:
        - train_1: 5 # Gray
        - train_2: 7 # Orange
        - train_3: 6 # Magenta
      identification: The unique color C that exists such that a pixel of color C is adjacent to a pixel of a host color H (where H is not background and H != C), and C appears within multiple different host colors.
  - selected_host_object:
      description: The specific object from the input whose inner pattern determines the output.
      selection_rule: Determined by a mapping based on the 'inner_pattern_color'.
      mapping:
        - if inner_pattern_color == 5 (Gray), selected_host_color = 3 (Green)
        - if inner_pattern_color == 7 (Orange), selected_host_color = 8 (Azure)
        - if inner_pattern_color == 6 (Magenta), selected_host_color = 1 (Blue)
      properties_used:
        - color: The color 'h_selected' corresponding to the mapping.
        - bounding_box: Used to define the output grid size and extract the pattern region.
        - content: Pixels within the bounding box, specifically those matching 'inner_pattern_color' and 'h_selected'.
  - output_grid:
      derivation: Extracted and recolored pattern from the 'selected_host_object'.
      size: Same dimensions as the bounding box of the 'selected_host_object'.
      content:
        - Pixels corresponding to the 'inner_pattern_color' in the host object's subgrid retain that color.
        - All other pixels (originally the host color 'h_selected') become 'h_selected'.
```


## Natural Language Program

1.  Identify the most common color in the input grid, assume this is the background color (e.g., Yellow 4). Ignore pixels of this color for object detection.
2.  Find the unique "inner pattern color" (`C_inner`) present in the grid. This is the color that appears as pixels located *inside* multiple distinct objects (contiguous regions of other non-background colors).
3.  Determine the "selected host color" (`h_selected`) based on the value of `C_inner` using the following fixed mapping:
    *   If `C_inner` is 5 (Gray), then `h_selected` is 3 (Green).
    *   If `C_inner` is 7 (Orange), then `h_selected` is 8 (Azure).
    *   If `C_inner` is 6 (Magenta), then `h_selected` is 1 (Blue).
4.  Locate the specific object (`O_selected`) in the input grid which consists of a contiguous region of the `h_selected` color and contains at least one pixel of the `C_inner` color.
5.  Calculate the bounding box of the `O_selected` object (the smallest rectangle enclosing all its pixels).
6.  Create a new output grid with the same height and width as the calculated bounding box.
7.  Iterate through each cell `(r, c)` within the bounding box relative to the top-left corner of the bounding box in the input grid:
    a.  Let the color of the input grid pixel at the absolute position corresponding to `(r, c)` within the bounding box be `input_color`.
    b.  If `input_color` is equal to `C_inner`, set the pixel at `(r, c)` in the output grid to `C_inner`.
    c.  Otherwise (if `input_color` is `h_selected` or any other color within the bounding box that isn't `C_inner`), set the pixel at `(r, c)` in the output grid to `h_selected`.
8.  Return the generated output grid.