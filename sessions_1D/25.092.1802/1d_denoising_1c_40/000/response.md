## Perception

1.  **Input/Output Format:** The examples present input and output data as flattened 1D sequences of integers (0-9, representing colors). To understand the spatial relationships, these sequences must be reshaped into 2D grids.
2.  **Grid Dimensions:** The dimensions are not explicit. By analyzing the lengths of the sequences and the structure suggested by the transformations, the dimensions can be inferred:
    *   Examples 1 & 2: Input length 34, Output length 34. Likely dimensions are 2x17 (or 17x2). The transformation preserves dimensions.
    *   Example 3: Input length 31, Output length 31. Likely dimensions are 31x1 (or 1x31). The transformation preserves dimensions.
3.  **Colors:** The primary colors are white (0), which acts as the background, and one other non-background color per example (orange/7 in Ex 1 & 2, magenta/6 in Ex 3).
4.  **Core Transformation:** The transformation involves identifying structures within the non-background pixels. Specifically, it focuses on contiguous blocks of the non-background color. Connectivity is defined by horizontal and vertical adjacency. The key operation is to isolate the *largest* such contiguous block (by pixel count) and remove all other non-background pixels, changing them to the background color (white/0).
5.  **Objects:** The main objects of interest are these contiguous blocks of non-background pixels. Their key property is their size (number of pixels).
6.  **Consistency:** The rule "identify the largest contiguous block of non-background color and keep only that block in the output grid (of the same dimensions), setting all other pixels to background" consistently explains all three examples after correctly inferring the grid shapes and output sizes.

## Facts


```yaml
task_description: Isolate the largest contiguous block of non-background pixels.

grid_properties:
  dimensionality: 2D
  background_color: 0 (white)
  shape_inference: Required based on sequence length and factors. Dimensions are preserved from input to output.

objects:
  - name: background_pixels
    color: 0 (white)
    role: Fills the grid initially and replaces removed pixels.
  - name: foreground_pixels
    color: Any color other than 0 (e.g., 7/orange, 6/magenta).
    role: Form structures within the grid.
  - name: contiguous_block
    definition: A group of connected foreground_pixels of the same color, where connectivity is defined by horizontal and vertical adjacency.
    properties:
      - color: The color of the pixels in the block.
      - size: The number of pixels in the block.
      - location: The set of coordinates occupied by the block's pixels.

actions:
  - name: identify_blocks
    input: input_grid
    output: list_of_contiguous_blocks
    description: Find all distinct contiguous blocks of non-background pixels in the input grid.
  - name: calculate_block_sizes
    input: list_of_contiguous_blocks
    output: list_of_block_sizes
    description: Determine the number of pixels (size) for each identified block.
  - name: find_largest_block
    input: list_of_contiguous_blocks, list_of_block_sizes
    output: largest_block
    description: Identify the contiguous block with the maximum size. Assumes a unique largest block based on examples.
  - name: generate_output_grid
    input: input_grid_dimensions, largest_block
    output: output_grid
    description: Create a new grid with the same dimensions as the input, filled with the background color (0). Then, copy the pixels belonging to the largest_block from their original input positions to the corresponding positions in the new grid.

relationships:
  - The output grid's dimensions are identical to the input grid's dimensions.
  - The output grid contains only the background color (0) and the pixels corresponding to the single largest contiguous block of non-background color found in the input grid. All other pixels from the input grid (including smaller non-background blocks) are represented as the background color in the output.
```


## Natural Language Program

1.  Determine the dimensions (height H, width W) of the input grid by reshaping the input sequence appropriately (e.g., for a sequence of length L, find factors H, W such that H * W = L, considering context from examples if ambiguous).
2.  Identify all pixels in the input grid that are *not* the background color (white, 0).
3.  Group these non-background pixels into distinct contiguous blocks. A block consists of pixels of the same color that are connected horizontally or vertically.
4.  Calculate the size (number of pixels) of each contiguous block found in step 3.
5.  Identify the contiguous block that has the largest size. (Assume there is only one such largest block).
6.  Create a new output grid with the same dimensions (H x W) as the input grid.
7.  Initialize all pixels in the output grid to the background color (white, 0).
8.  For each pixel belonging to the largest contiguous block identified in step 5, copy its color and position from the input grid to the corresponding position in the output grid.
9.  The resulting grid is the final output.