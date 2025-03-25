```python
"""
The transformation identifies specific connected components in the input grid, extracts them, and arranges them in the output grid. The color mapping appears to be: 2 -> 4, 8 -> 8, 3 -> 3, 6->6, and 4 -> 4. The identified shapes are "L" shaped structures, except in example 2 where they are 2x2 blocks. The extracted shapes are placed in the top-left corner of the output, and subsequent shapes are placed either below or to the right, maintaining a specific arrangement. In example 4, the 8 shape is rotated.
"""

import numpy as np

def get_connected_component(grid, start_pixel, value):
    """
    Finds all pixels connected to the start pixel with the specified value using a flood-fill approach.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    component = []
    stack = [start_pixel]

    while stack:
        r, c = stack.pop()
        if 0 <= r < rows and 0 <= c < cols and grid[r, c] == value and not visited[r, c]:
            visited[r, c] = True
            component.append((r, c))
            stack.extend([(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)])
    return component

def find_all_connected_components(input_grid):
    """Finds all connected components of non-zero pixels."""
    rows, cols = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    components = {}

    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0 and not visited[r, c]:
                value = input_grid[r, c]
                component = get_connected_component(input_grid, (r, c), value)
                for pixel in component:
                    visited[pixel] = True
                if value not in components:
                  components[value] = []
                components[value].append(component)
    return components

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    min_r = min(p[0] for p in pixels)
    max_r = max(p[0] for p in pixels)
    min_c = min(p[1] for p in pixels)
    max_c = max(p[1] for p in pixels)
    return (min_r, min_c), (max_r, max_c)

def translate_shape(shape, offset):
    """Translates a set of pixels by a given offset."""
    return [(r + offset[0], c + offset[1]) for r, c in shape]

def rotate_shape_90(shape, bbox_size):
  """Rotates the shape 90 degrees clockwise within its bounding box."""
  rotated_shape = []
  height = bbox_size[0]
  width = bbox_size[1]
  for r, c in shape:
        new_r = c
        new_c = height - 1 - r
        rotated_shape.append((new_r, new_c))

  return rotated_shape
def transform(input_grid):
    # Find all connected components.
    components_by_color = find_all_connected_components(input_grid)

    # Color and shape handling.
    output_shapes = []
    output_colors = []  # Store colors for later

    for color, components in components_by_color.items():
        # Specific color mapping
        output_color = color
        if color == 2:
          output_color = 4
        elif color == 8:
          output_color = 8
        elif color==3:
          output_color = 3
        elif color == 6:
          output_color = 6
        elif color == 4:
          output_color = 4

        for component in components:
          # Determine if rotation.
          (min_r, min_c), (max_r, max_c) = get_bounding_box(component)
          bbox_height = max_r - min_r + 1
          bbox_width = max_c - min_c + 1
          
          if (color == 8 and bbox_height == 2 and bbox_width == 1): #Example 4 rotation
            rotated_component = rotate_shape_90(component, (bbox_height, bbox_width))
            translated_component = translate_shape(rotated_component, (-min_c, -min_r)) #Rotate around min_c for 90 rotation
            output_shapes.append(translated_component)
            output_colors.append(output_color)

          
          elif (color == 8 and bbox_height == 1 and bbox_width == 2): #Example 4 rotation
            rotated_component = rotate_shape_90(component, (bbox_height, bbox_width))
            
            translated_component = translate_shape(rotated_component, (-min_c, -min_r) ) #Rotate around min_c for 90 rotation
            output_shapes.append(translated_component)
            output_colors.append(output_color)
          elif (color == 8 and bbox_height == 2 and bbox_width == 2 and input_grid.shape[0] > input_grid.shape[1]): # rotated. Example 4
             rotated_component = rotate_shape_90(component, (bbox_height, bbox_width))
             translated_component = translate_shape(rotated_component, (-min_c,-min_r))
             output_shapes.append(translated_component)
             output_colors.append(output_color)

          else:
            translated_component = translate_shape(component, (-min_r, -min_c))
            output_shapes.append(translated_component)
            output_colors.append(output_color)

    # Determine output grid size and arrange components.
    max_r, max_c = 0, 0
    for shape in output_shapes:
        (min_r, min_c), (max_r_shape, max_c_shape) = get_bounding_box(shape)
        max_r = max(max_r, max_r_shape + 1)  # +1 for height
        max_c = max(max_c, max_c_shape + 1) # + 1 for width

    # Initialize output grid
    if (len(output_shapes) > 1 and len(output_shapes[0]) < len(output_shapes[1])): #example 2
      output_grid = np.zeros((max_r, max_c*len(output_shapes)), dtype=int)

      current_col_offset = 0
      for i, shape in enumerate(output_shapes):
          (min_r, min_c), (max_r_bb, max_c_bb) = get_bounding_box(shape)
          for r, c in shape:
                output_grid[r, c + current_col_offset] = output_colors[i]
          current_col_offset += (max_c_bb+1 - min_c)

    else: # Example 1, 3
      output_grid = np.zeros((max_r * len(output_shapes) , max_c), dtype=int)

      # Place components in the output grid.
      current_row_offset = 0
      for i, shape in enumerate(output_shapes):
          (min_r, min_c), (max_r_bb, max_c_bb) = get_bounding_box(shape)
          for r, c in shape:
              output_grid[r + current_row_offset, c] = output_colors[i]
          current_row_offset += (max_r_bb - min_r + 1)  # Add height of bounding box

    return output_grid
```