# 23b5c85d • 021 • example_4 • investigate_dreamer

---
Okay, let's analyze this input-output example.

**Perception of Elements:**

The input is a grid of colored pixels.  We see white (0), red (2), orange (7), and green (3).  The output is a smaller grid containing only orange (7) pixels. The input image appears to have distinct regions of red, orange, and green. The output image seems to correspond to the orange region in the input.

**YAML Block (Facts):**



```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      colors: [white, red, orange, green]
      dimensions: [13, 15]
  - name: orange_region
    type: object
    properties:
      color: orange
      shape: rectangle
    location:
      top_left: [4, 3]
      bottom_right: [6, 6]
  - name: output_grid
    type: grid
    properties:
      colors: [orange]
      dimensions: [3, 4]
relationships:
  - type: contains
    from: input_grid
    to: orange_region
  - type: corresponds_to
    from: output_grid
    to: orange_region

actions:
   - name: extract
     agent: unknown
     input_object: input_grid
     output: output_grid
     parameters:
        - type: color
          value: orange
```



**Natural Language Program:**

1.  **Identify** the rectangular region within the input grid that is entirely filled with orange (7) pixels.
2.  **Extract** this orange region.
3.  The extracted orange region becomes the output grid.

In essence, the transformation isolates and extracts the contiguous block of orange pixels from the input grid.

