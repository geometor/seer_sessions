**INSTRUCTIONS**

above is an example pair for a task

this is your opportunity to perceive the underlying logic that transforms the
input into the output

respond with the following deliverables:

- your perception of the elements of the task
- a YAML block documenting facts - Focus on identifying objects, their properties, actions performed on them, and the relationships between them
- a natural language program - Be as clear and concise as possible, providing a complete description of the transformation rule.


your responses should be considered as information in a report - not a conversation
**Perception of Elements:**

The input image consists of a grid containing pixels of different colors: black (background), blue, red, and green. The blue pixels form a large, solid, diagonally oriented rectangular shape. The red and green pixels appear as smaller, scattered groups or individual pixels, seemingly disconnected from the main blue shape and from each other.

The output image retains only the blue rectangular shape from the input, maintaining its exact position, size, shape, and color. All other pixels (red, green, and the original black background pixels not covered by the blue shape) are replaced with the black background color.

The core transformation appears to be an object isolation process. Specifically, it identifies the largest contiguous object (the blue rectangle in this case) and filters out all other smaller objects or "noise" pixels, preserving only the largest object against a clean background.

**YAML Facts:**


```yaml
Grid:
  - Type: Input
    Dimensions: 16x16 (rows x columns)
    Background_Color: Black (0)
    Objects:
      - Object_1:
          Type: Shape
          Shape_Type: Rectangle (diagonal)
          Color: Blue (1)
          Contiguous: True
          Pixel_Count: 36 (approximate visual estimate - requires precise count)
          Description: Largest contiguous object in the grid.
      - Object_2:
          Type: Pixels
          Color: Red (2)
          Contiguous: False (appears as scattered groups/individuals)
          Pixel_Count: 9 (approximate visual estimate)
          Description: Smaller noise elements.
      - Object_3:
          Type: Pixels
          Color: Green (3)
          Contiguous: False (appears as scattered groups/individuals)
          Pixel_Count: 1 (approximate visual estimate)
          Description: Smaller noise elements.
  - Type: Output
    Dimensions: 16x16 (rows x columns)
    Background_Color: Black (0)
    Objects:
      - Object_1:
          Type: Shape
          Shape_Type: Rectangle (diagonal)
          Color: Blue (1)
          Contiguous: True
          Pixel_Count: 36 (same as input Object_1)
          Description: The single remaining object, identical to the largest object from the input.
Transformation:
  Action: Object Isolation / Filtering
  Rule: Identify all contiguous groups of non-background pixels in the input. Determine the group with the largest number of pixels. Create an output grid of the same size, initially filled with the background color, and place only the pixels corresponding to the largest identified group from the input into the output grid at their original locations.
  Preserved_Properties:
    - Grid dimensions
    - Position of the largest object
    - Shape of the largest object
    - Color of the largest object
  Removed_Elements:
    - All non-background pixels not part of the largest contiguous object.
    - Original background pixels replaced by the largest object remain replaced.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (black).
2.  Identify all distinct contiguous groups (connected components) of non-background colored pixels in the input grid. Consider pixels connected if they share an edge or a corner (8-way connectivity).
3.  Calculate the size (number of pixels) of each identified contiguous group.
4.  Determine the group with the maximum size. This is the "largest object".
5.  Iterate through all pixel coordinates (row, column) of the input grid.
6.  If a pixel at a given coordinate belongs to the identified largest object, copy its color to the corresponding coordinate in the output grid.
7.  The final state of the output grid is the result.
**INSTRUCTIONS**

- generate a Python module to represent the natural language program 
- follow the template below
- all common math and science libraries are available
- create docstring only at top - but comment the workflow in the function
- use helper functions for common operations like finding objects, counting,
  measuring, moving, etc. 

remember - we are working iteratively - so this code will inform your future
self as we converge on the solution

*template:*

```python
"""
< natural language description of the transformation rule >
"""

< imports >

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # initialize output_grid

    # perform transformations

    return output_grid

``````python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Identifies all distinct contiguous groups (connected components) of non-background colored pixels 
in the input grid using 8-way connectivity. Calculates the size (number of pixels) of each group.
Determines the group with the maximum size (the "largest object"). Creates an output grid of the 
same dimensions as the input, filled with the background color (black, 0). Copies only the pixels 
belonging to the largest identified object from the input grid to the output grid at their 
original locations and with their original color.
"""

def find_largest_component(grid: np.ndarray, background_color: int = 0) -> tuple[np.ndarray | None, int | None]:
    """
    Finds the coordinates and color of the largest connected component of non-background pixels.

    Args:
        grid: The input grid as a numpy array.
        background_color: The integer value representing the background color.

    Returns:
        A tuple containing:
        - A boolean mask of the same shape as the grid, where True indicates a pixel
          belongs to the largest component. None if no non-background components exist.
        - The color of the largest component. None if no non-background components exist.
    """
    # Create a boolean mask where non-background pixels are True
    mask = grid != background_color

    # Define 8-way connectivity
    connectivity_structure = np.array([[1, 1, 1],
                                       [1, 1, 1],
                                       [1, 1, 1]], dtype=bool)

    # Label connected components
    # labeled_array contains integers identifying each component (0 for background)
    # num_features is the total number of components found (excluding background)
    labeled_array, num_features = label(mask, structure=connectivity_structure)

    # Handle the case where there are no non-background pixels
    if num_features == 0:
        return None, None

    # Find the size of each component (excluding background label 0)
    component_sizes = np.bincount(labeled_array.ravel())
    # Ignore the count for the background (label 0)
    component_sizes = component_sizes[1:]

    # Find the label of the largest component
    # Add 1 back because we sliced off the background count at index 0
    largest_component_label = np.argmax(component_sizes) + 1

    # Create a mask for the largest component
    largest_component_mask = (labeled_array == largest_component_label)

    # Find the coordinates of the first pixel in the largest component to get its color
    coords = np.argwhere(largest_component_mask)
    if len(coords) == 0: # Should not happen if num_features > 0, but good practice
         return None, None
    first_pixel_coords = tuple(coords[0])
    component_color = grid[first_pixel_coords]


    return largest_component_mask, component_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by isolating the largest connected component of
    non-background pixels and placing it on a background grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid with only the largest component.
    """
    # Convert input grid to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Define the background color (assuming 0 based on perception)
    background_color = 0

    # Initialize the output grid with the background color
    output_array = np.full((rows, cols), background_color, dtype=int)

    # Find the mask and color of the largest component
    largest_component_mask, component_color = find_largest_component(input_array, background_color)

    # If a largest component was found, draw it onto the output grid
    if largest_component_mask is not None and component_color is not None:
        # Apply the mask: where the mask is True, set the output array pixel
        # to the component's color
        output_array[largest_component_mask] = component_color

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
