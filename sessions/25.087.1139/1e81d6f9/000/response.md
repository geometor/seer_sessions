*   **Perception:**
    *   The input and output are grids of pixels with various colors.
    *   The core transformation involves identifying and modifying pixels of a specific color: yellow (4).
    *   Comparing input and output grids across all examples reveals that only certain yellow pixels are changed to white (0). Other pixels remain untouched.
    *   The key factor determining whether a yellow pixel changes seems related to its context as part of a larger "object" (a contiguous block of the same color). Specifically, yellow pixels that form an object of size 1 (i.e., they have no adjacent yellow neighbours, including diagonals) are targeted for removal.

*   **Facts:**
    
```yaml
    task_elements:
      - element: grid
        description: A 2D array of pixels representing colors (0-9).
      - element: objects
        description: Contiguous blocks of pixels of the same color. Adjacency includes diagonals.
      - element: target_objects
        description: Objects composed entirely of yellow (4) pixels.
      - element: property_size
        description: The number of pixels constituting an object.
      - element: action
        description: Change the color of pixels.
    transformation:
      - select: target_objects
        where: property_size == 1
        action: Change the color of all pixels within the selected object(s) to white (0).
      - select: all_other_pixels
        action: Keep the color unchanged.

    ```


*   **Natural Language Program:**
    1.  Identify all distinct contiguous objects composed solely of yellow (4) pixels in the input grid. Consider pixels connected horizontally, vertically, or diagonally as part of the same object.
    2.  For each identified yellow object, determine its size (the count of pixels it contains).
    3.  If a yellow object has a size of exactly 1 pixel, change the color of that pixel in the output grid to white (0).
    4.  If a yellow object has a size greater than 1 pixel, keep its pixels unchanged in the output grid.
    5.  All pixels that are not part of a size-1 yellow object retain their original color in the output grid.