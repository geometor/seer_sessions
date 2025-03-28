
## train_1

**input:**
```
7 5 7 7 7 7 7 7 7
7 5 7 7 7 5 7 7 7
7 5 7 5 7 7 7 7 7
7 7 7 5 7 7 5 7 7
7 7 7 5 7 7 5 7 7
7 7 7 7 7 7 5 7 7
5 5 5 5 5 7 5 7 7
7 7 7 7 7 7 5 7 7
7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7
5 5 5 7 7 5 7 7 7
7 7 7 7 7 7 7 7 7
7 7 5 5 5 7 7 7 7
7 7 5 7 7 7 7 7 7
7 7 5 7 5 5 5 5 5
7 7 5 7 7 7 7 7 7
7 7 5 7 7 7 7 7 7
7 7 5 7 7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7 7
7 7 2 2 2 7 2 7 7
7 7 7 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 7 7 7
7 7 2 7 7 7 7 7 7
7 7 7 7 7 2 2 2 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 2 7 7 7 7 7
7 7 7 2 7 7 7 7 7
7 7 7 2 7 2 2 2 7
7 7 7 7 7 7 7 7 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 8 7 7 7 8 8 8 8 8 7
7 8 7 8 7 7 7 7 7 7 7
7 8 7 7 7 7 8 7 7 7 7
7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 8 7 7 7 7
7 7 7 7 7 7 8 7 7 7 7
8 8 8 8 8 7 8 7 7 7 7
7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 8 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
8 8 8 8 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 8 7
7 7 7 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 8 8 8 8 8 8 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
```

*   **Perception:**
    The task involves transforming an input grid into an output grid. The grids contain a background color (orange, 7) and one other "foreground" color (gray 5, red 2, or azure 8, depending on the example). The transformation appears to operate column by column. Within each column of the input grid, the foreground pixels define a vertical segment. The output grid is constructed by filling this vertical segment (from the highest foreground pixel to the lowest foreground pixel in that column) with the foreground color, while the rest of the column retains the background color. Columns in the input that contain only the background color remain unchanged in the output.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    components:
      - name: input_grid
        type: 2D_array
        properties:
          - background_color: dominant_color (e.g., orange)
          - foreground_pixels: non-background_color_pixels (e.g., gray, red, azure)
            properties:
              - color: specific_non_background_color
              - position: row, column
      - name: output_grid
        type: 2D_array
        properties:
          - background_color: same_as_input
          - foreground_segments: vertical_lines_of_foreground_color
            properties:
              - color: same_as_input_foreground
              - position: column, start_row, end_row
    transformation:
      scope: column-wise
      steps:
        - identify_background_color: most_frequent_color_in_input
        - identify_foreground_color: any_other_color_in_input
        - initialize_output_grid: copy_of_input_grid OR grid_of_background_color_with_same_dimensions
        - process_each_column:
            - find_foreground_pixels_indices: list_of_row_indices_containing_foreground_color_in_the_column
            - if_foreground_pixels_exist:
                - determine_min_row: minimum_index_from_list
                - determine_max_row: maximum_index_from_list
                - fill_output_column_segment: set_pixels_from_min_row_to_max_row_(inclusive)_to_foreground_color
            - else_if_no_foreground_pixels_exist:
                - fill_output_column: set_all_pixels_in_the_column_to_background_color (or leave as is if output initialized as background)
    relationships:
      - vertical_contiguity: output_foreground_pixels_form_continuous_vertical_lines_within_each_column
      - column_dependence: output_column_depends_only_on_the_corresponding_input_column
      - color_preservation: background_and_foreground_colors_are_preserved_from_input_to_output
    ```


*   **Natural Language Program:**
    1.  Determine the background color by finding the most frequent color in the input grid.
    2.  Identify the foreground color as the color present in the input grid that is not the background color.
    3.  Create an output grid of the same dimensions as the input grid, initially filled entirely with the background color.
    4.  For each column in the input grid (from left to right):
        a.  Find all the row indices where the foreground color appears in that column.
        b.  If any foreground pixels are found in the column:
            i.  Determine the smallest (topmost) row index (`min_row`).
            ii. Determine the largest (bottommost) row index (`max_row`).
            iii. In the corresponding column of the output grid, change the color of all pixels from `min_row` to `max_row` (inclusive) to the foreground color.
        c.  If no foreground pixels are found in the column, the corresponding column in the output grid remains entirely filled with the background color.
    5.  The resulting grid is the final output.
