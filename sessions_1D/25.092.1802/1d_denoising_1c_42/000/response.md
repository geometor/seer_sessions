**Perception:**

The task involves processing 4x8 grids containing a background color (white, 0) and one other primary color (red, azure, or green in the examples). The input grids feature one large, contiguous object composed of the primary color, along with one or more smaller, isolated pixels (or potentially small groups) of the same primary color located elsewhere in the grid. The transformation appears to isolate the largest contiguous object of the primary color. All other pixels of the primary color that are not part of this largest object are removed (changed to the background color). The background pixels and the pixels forming the largest object remain unchanged in their positions.

**Facts:**


```yaml
task_context:
  grid_size: Fixed (4x8 in examples)
  background_color: 0 (white)
  input_features:
    - Multiple objects of a single primary color (non-zero).
    - One object is significantly larger (in terms of pixel count) than others.
    - Smaller objects appear as isolated pixels or small groups.
  output_features:
    - Contains only the largest contiguous object from the input.
    - All other pixels of the primary color are replaced with the background color.
transformation_type: Object filtering based on size.

object_definitions:
  - object: A contiguous block of pixels of the same non-background color. Adjacency is defined by sharing an edge (not just diagonally).
  - background: Pixels with color 0 (white).
  - primary_color: The single non-background color present in each input grid (e.g., 2, 8, 3).
  - largest_object: The object (as defined above) with the greatest number of pixels.

actions:
  - Identify all objects of the primary color.
  - Calculate the size (pixel count) of each object.
  - Find the object with the maximum size.
  - Filter the grid to keep only the pixels belonging to the largest object.
  - Replace all other pixels of the primary color with the background color.

relationships:
  - Pixels belong to objects.
  - Objects have a size property.
  - The transformation selects based on the 'largest' size relationship among objects of the same color.
```


**Natural Language Program:**

1.  Identify the primary non-background color present in the input grid.
2.  Find all distinct contiguous objects composed of this primary color. Consider pixels connected horizontally or vertically (not diagonally) as part of the same object.
3.  Calculate the number of pixels (size) for each identified object.
4.  Determine the object with the largest size. Assume there is only one such largest object based on the examples.
5.  Create a new output grid of the same dimensions as the input grid, initially filled entirely with the background color (white, 0).
6.  Copy the pixels belonging to the identified largest object from their positions in the input grid to the corresponding positions in the new output grid.
7.  The resulting grid is the final output.