**Perception of Task Elements:**

The task involves identifying a single, contiguous object of a non-white color within a larger input grid filled mostly with white pixels. The transformation then isolates this object, determines its minimal bounding box, and creates a new output grid by duplicating the object's shape side-by-side, separated by a single column of white pixels.

**Facts:**


```yaml
- task: object_duplication_with_spacer
  examples:
    - id: train_1
      input:
        grid_size: [8, 8]
        objects:
          - color: red
            pixels: [[5, 3], [6, 2], [6, 3], [6, 4], [7, 2], [7, 3]]
            bounding_box: # rows 5-7, cols 2-4 (3x3)
              pixels: [[., 2, .], [2, 2, 2], [2, 2, .]]
              shape: L-shape variant
              size: [3, 3]
        background_color: white
      output:
        grid_size: [3, 6]
        content:
          - pattern: bounding_box_content
            position: [0, 0]
          - pattern: vertical_white_line
            position: [0, 3]
            size: [3, 1]
          - pattern: bounding_box_content # Duplication
            position: [0, 4]
        background_color: white

    - id: train_2
      input:
        grid_size: [8, 8]
        objects:
          - color: azure
            pixels: [[1, 1], [1, 2], [2, 2], [3, 1], [3, 2], [3, 3]]
            bounding_box: # rows 1-3, cols 1-3 (3x3)
              pixels: [[8, 8, .], [. , 8, .], [8, 8, 8]]
              shape: custom
              size: [3, 3]
        background_color: white
      output:
        grid_size: [3, 6]
        content:
          - pattern: bounding_box_content
            position: [0, 0]
          - pattern: vertical_white_line
            position: [0, 3]
            size: [3, 1]
          - pattern: bounding_box_content # Duplication
            position: [0, 4]
        background_color: white

    - id: train_3
      input:
        grid_size: [8, 8]
        objects:
          - color: blue
            pixels: [[1, 5], [1, 6], [2, 4], [3, 5]]
            bounding_box: # rows 1-3, cols 4-6 (3x3)
              pixels: [[., 1, 1], [1, ., .], [., 1, .]]
              shape: custom
              size: [3, 3]
        background_color: white
      output:
        grid_size: [3, 6]
        content:
          - pattern: bounding_box_content
            position: [0, 0]
          - pattern: vertical_white_line
            position: [0, 3]
            size: [3, 1]
          - pattern: bounding_box_content # Duplication
            position: [0, 4]
        background_color: white

  common_properties:
    - input_grid_contains_single_non_white_object
    - output_grid_size_depends_on_input_object_bounding_box
    - transformation_involves_extracting_bounding_box
    - transformation_duplicates_bounding_box_content
    - transformation_inserts_white_separator_column

```


**Natural Language Program:**

1.  Identify the contiguous group of non-white pixels in the input grid; this is the "object".
2.  Determine the minimal bounding box that tightly encloses the object. Let the height of this box be `H` and the width be `W`.
3.  Extract the subgrid defined by the bounding box coordinates. Call this the `ObjectPattern`.
4.  Create a new output grid with height `H` and width `(2 * W) + 1`, initially filled with white pixels (color 0).
5.  Place the `ObjectPattern` into the output grid starting at the top-left corner (row 0, column 0).
6.  Place the `ObjectPattern` again into the output grid starting at row 0 and column `W + 1`.
7.  The resulting grid is the final output.