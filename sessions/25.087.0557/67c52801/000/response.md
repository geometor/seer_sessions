**Perception:**

The task involves simulating a form of gravity acting on colored objects within a grid. Non-white objects (pixels with values 1-9) fall downwards until they encounter another non-white object directly below them or reach the bottom boundary of the grid. The white pixels (0) represent empty space through which objects can fall. Objects maintain their shape and color as they fall. The process continues iteratively until all objects have settled and no further downward movement is possible.

**Facts:**


```yaml
observations:
  - task_type: object_manipulation
  - mechanic: gravity
  - elements:
      - type: grid
        description: A 2D array of pixels with integer values 0-9.
      - type: pixel
        properties:
          - color: Represents different types (0=white/empty, 1-9=colored objects).
      - type: object
        description: A contiguous group of one or more pixels of the same non-white color.
        properties:
          - shape: The configuration of pixels forming the object.
          - color: The color value of the pixels in the object.
          - position: The coordinates of the pixels within the grid.
  - interactions:
      - gravity_effect:
          description: Non-white objects move downwards if the space below them is white (0).
          actor: non-white objects
          target: white space below
          condition: The entire space directly below the object's footprint must be white.
      - collision_stop:
          description: Downward movement stops when an object encounters another non-white pixel directly below any part of it.
          actor: falling object
          obstacle: non-white pixel below
      - boundary_stop:
          description: Downward movement stops when an object reaches the bottom row of the grid.
          actor: falling object
          obstacle: grid boundary (bottom row)
  - stability:
      description: The process repeats until no object can move further down, reaching a stable state.
      condition: No non-white object has only white pixels directly below it and is not already in the bottom row.
  - object_integrity:
      description: Objects maintain their shape and color during the falling process. They move as a single unit.
```


**Natural Language Program:**

1.  Identify all distinct, contiguous objects composed of non-white pixels (colors 1-9) in the input grid.
2.  Iteratively apply the following gravity rule until no object moves in a full iteration:
    a.  For each identified object, check the pixels directly below its lowest pixels.
    b.  If *all* pixels directly below the object's entire footprint are white (0) and the object is not already touching the bottom boundary of the grid, move the entire object down by one row.
    c.  If *any* pixel directly below the object's footprint is non-white (1-9) or the object is already at the bottom row, the object does not move in this step.
3.  Repeat step 2 until a full pass occurs where no object is moved downwards.
4.  The resulting grid configuration is the output.