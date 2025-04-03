**Perception:**

The input and output are 1D arrays (or 1xN grids) of integers representing colors. The transformation appears to operate on a specific segment of the array containing non-zero values, leaving the surrounding zero values (white pixels) unchanged. Within the non-zero segment, there are always two distinct non-zero colors present: one color appears as a single pixel (the "singleton"), and the other appears as a contiguous block of multiple pixels (the "block"). The core transformation is the swapping of the relative positions of the singleton pixel and the block of pixels.

**Facts:**


```yaml
task_type: array_manipulation
grid_dimensionality: 1D # Effectively 1D arrays presented
background_color: 0 # white
objects:
  - name: singleton
    description: A single pixel of a non-zero color within the active segment.
    properties:
      - color: variable (5 in train_1, 1 in train_2, 4 in train_3)
      - count: 1
  - name: block
    description: A contiguous sequence of pixels of the same non-zero color within the active segment.
    properties:
      - color: variable (8 in train_1, 8 in train_2, 5 in train_3)
      - count: >1
      - contiguous: true
relationships:
  - type: adjacency
    objects: [singleton, block]
    description: The singleton and the block are always adjacent to each other in the input.
  - type: boundary
    objects: [singleton, block, background_color]
    description: The combined singleton and block form a contiguous segment surrounded by the background color (0).
actions:
  - name: identify_active_segment
    description: Find the contiguous subsequence of non-zero pixels.
  - name: identify_singleton_and_block
    description: Within the active segment, differentiate the pixel appearing once (singleton) from the pixel color appearing multiple times contiguously (block).
  - name: swap_position
    objects: [singleton, block]
    description: Reverse the order of the singleton and the block within the active segment.
  - name: reconstruct_output
    description: Place the modified active segment back into its original position relative to the surrounding background pixels.
```


**Natural Language Program:**

1.  Identify the start and end indices of the contiguous segment containing non-zero pixels in the input array.
2.  Extract this non-zero segment.
3.  Within the extracted segment, count the occurrences of each unique non-zero color.
4.  Identify the color that appears exactly once; this is the 'singleton' color.
5.  Identify the color that appears multiple times; this constitutes the 'block' color and its associated pixels.
6.  Create a new segment by placing the block pixels first, followed by the singleton pixel, if the singleton was originally first. Otherwise (if the block was originally first), place the singleton pixel first, followed by the block pixels. Essentially, swap their order.
7.  Construct the output array by replacing the original non-zero segment (between the identified start and end indices) with the newly created swapped segment. Keep all zero pixels outside this segment in their original positions.