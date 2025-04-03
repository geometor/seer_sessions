**Perception of the Elements:**

The input and output are 1D arrays (or single rows/columns of a grid) represented by sequences of integers (colors). Each example contains a sequence of white pixels (0) surrounding a contiguous block of non-white pixels. This non-white block consistently consists of two distinct colors: one color appears as a single pixel, and the other color appears as a contiguous block of multiple pixels. The transformation involves swapping the positions of the single pixel and the block of pixels within this non-white sequence, leaving the surrounding white pixels unchanged.

**Facts:**


```yaml
task_type: array_transformation_1d
components:
  - type: background
    color: 0 # white
    role: static frame surrounding the active region
  - type: active_region
    description: A contiguous sequence of non-zero pixels within the input array.
    composition: Contains exactly two distinct non-zero colors.
    structure:
      - type: object
        description: A single pixel of one non-zero color.
        properties:
          - count: 1
      - type: object
        description: A contiguous block of pixels of a second non-zero color.
        properties:
          - count: >1
          - contiguous: true
    relationship: The two objects are adjacent within the active region.
transformation:
  action: swap_positions
  target: The two objects (single pixel and color block) within the active region.
  effect: The relative order of the single pixel and the color block is reversed in the output array.
  context: The background pixels remain unchanged and maintain their positions relative to the modified active region.
```


**Natural Language Program:**

1.  **Identify the Active Region:** Locate the contiguous sub-sequence within the input array that consists entirely of non-zero (non-white) pixels. Note the start and end indices of this region.
2.  **Identify Objects within the Active Region:** Within the active region, identify the single pixel of one color and the contiguous block of pixels of the other color.
3.  **Determine Order:** Observe the order in which the single pixel and the block appear within the input's active region.
4.  **Perform Swap:** Create the output's active region by placing the block of pixels first, followed by the single pixel, if the single pixel was first in the input, OR by placing the single pixel first, followed by the block of pixels, if the block was first in the input (i.e., reverse their order).
5.  **Construct Output Array:** Reconstruct the full output array by keeping the white pixels before the active region, inserting the swapped active region, and keeping the white pixels after the active region, maintaining the original array length.