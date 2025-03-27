**Perception:**

The task involves transforming an input grid containing an object made of azure (8) pixels into an output grid. The background is consistently white (0). In each example, the azure object shifts vertically downwards by one position while maintaining its original shape. Concurrently, the color of the object changes from azure (8) to red (2). The rest of the grid remains unchanged (white).

**Facts:**


```yaml
Task: Grid Transformation
Input_Components:
  - Grid: 2D array of integers (0-9) representing colors.
  - Background: Predominantly white (0) pixels.
  - Objects:
    - Type: Contiguous blocks of non-background pixels.
    - Color: Azure (8) in all examples.
    - Shape: Varies (single pixel, 2x2 square, 1x3 rectangle).
Output_Components:
  - Grid: Same dimensions as the input grid.
  - Background: White (0) pixels, same as input where no object is placed.
  - Transformed_Objects:
    - Source: Derived from the azure objects in the input.
    - Color: Red (2).
    - Shape: Same as the corresponding input object.
    - Position: Shifted one row down compared to the input object's position.
Transformation:
  - Action_1: Identify all pixels with the color azure (8).
  - Action_2: Group connected azure pixels into objects.
  - Action_3: For each identified azure object:
    - Translate: Move the entire object one cell down vertically.
    - Recolor: Change the color of all pixels within the object from azure (8) to red (2).
  - Action_4: Preserve the background color (white, 0) in all other locations.
Relationships:
  - Input azure object maps directly to the output red object.
  - The shape of the object is preserved during the transformation.
  - The position changes predictably (down by 1 row).
  - The color changes predictably (azure to red).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, but replace all azure (8) pixels with white (0) pixels.
2.  Identify all pixels in the input grid that have the color azure (8).
3.  For each identified azure pixel at coordinates (row, column):
    a.  Calculate the new row coordinate by adding 1 to the original row coordinate (row + 1).
    b.  Ensure the new row coordinate is within the bounds of the grid height.
    c.  If the new position (row + 1, column) is within the grid bounds, change the color of the pixel at this position in the output grid to red (2).