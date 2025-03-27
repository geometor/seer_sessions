*   **Perception:** The task involves transforming an input grid into an output grid. In all provided examples, the input and output grids have the same dimensions. The content of the individual rows remains the same, but their order is reversed. The first row of the input becomes the last row of the output, the second row of the input becomes the second-to-last row of the output, and so on. This constitutes a vertical reflection or flip of the entire grid.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    transformation: geometric
    operation: reflection
    axis: horizontal # The reflection happens across the horizontal center line
    dimensionality: 2D
    input_entity: grid
    output_entity: grid
    properties:
      - input and output grids have the same dimensions.
      - pixel values within rows remain unchanged.
      - the order of rows is reversed vertically.
      - row i of the input becomes row (height - 1 - i) of the output.
    ```


*   **Natural Language Program:**
    1.  Take the input grid.
    2.  Reverse the order of the rows. The first row becomes the last, the second becomes the second-to-last, and so on, until the last row becomes the first.
    3.  The resulting grid is the output.