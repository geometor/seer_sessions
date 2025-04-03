*   **Perception:** The input and output are grids of pixels, likely 3x10 based on the 30 elements provided and visual coherence of the patterns across examples. The grids contain a background color (white - 0) and one other primary color (azure - 8, gray - 5, or red - 2). The input grid features several distinct contiguous groups (objects) of the primary color, separated by the background color. The output grid retains only one of these objects – specifically, the largest one in terms of pixel count. All other pixels in the output grid, including those that were part of smaller primary-colored objects in the input, are set to the background color (white - 0). Connectivity for defining objects appears to be based on orthogonal adjacency (sharing a side), not diagonal.

*   **Facts:**
    
```yaml
    task_context:
      grid_representation: 2D array of integers (pixels)
      colors:
        - 0: white (background)
        - non-zero: primary object color (varies per example: 8, 5, 2)
      grid_dimensions: Assumed 3x10 based on consistent pattern analysis across examples.
    
    elements:
      - element: background
        pixels: color 0 (white)
      - element: primary_objects
        pixels: non-zero color (e.g., 8, 5, 2)
        properties:
          - form contiguous groups (objects)
          - defined by orthogonal adjacency
          - vary in size (pixel count)
    
    transformation:
      input_grid: Contains background and multiple primary_objects of varying sizes.
      output_grid: Contains only the single largest primary_object from the input; all other pixels are background.
      steps:
        1: Identify the primary non-background color.
        2: Find all distinct contiguous objects of this color using orthogonal adjacency.
        3: Determine the size (pixel count) of each object.
        4: Select the object with the maximum size. (Assume unique largest for now).
        5: Create a new grid filled with the background color.
        6: Place the pixels corresponding to the largest object onto the new grid, preserving their color.
    
    relationships:
      - size_comparison: Objects are compared based on their pixel count to find the largest.
      - preservation: The pixels of the largest object retain their position and color.
      - removal: Pixels of smaller objects and original background pixels (not part of the largest object) are replaced by the background color in the output.
    ```


*   **Natural Language Program:**
    1.  Identify the primary color present in the input grid (any color other than white-0).
    2.  Scan the input grid to find all separate contiguous blocks (objects) composed of this primary color, considering pixels connected only horizontally or vertically (not diagonally) as part of the same object.
    3.  Count the number of pixels in each identified object.
    4.  Determine which object has the largest pixel count.
    5.  Generate the output grid, initially filled entirely with the background color (white-0).
    6.  For every pixel location that belongs to the largest object identified in step 4, set the corresponding pixel in the output grid to the primary color found in step 1. Leave all other pixels in the output grid as the background color.