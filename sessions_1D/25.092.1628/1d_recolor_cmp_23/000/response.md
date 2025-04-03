*   **Perception:** The task operates on 1D sequences (or single rows) of pixels. The input sequences contain white (0) and azure (8) pixels. The output sequences contain white (0), azure (8), and orange (7) pixels. The transformation involves changing the color of certain azure blocks to orange based on their properties and context. Specifically, the length of the azure block and its immediate neighbors (being white pixels) determine if a color change occurs.

*   **Facts:**
    
```yaml
    task_type: color_transformation
    grid_dimensionality: 1D # or single row within 2D
    colors_involved:
      - white (0)
      - azure (8)
      - orange (7)
    objects:
      - pixel: Basic unit with a color value.
      - block: A contiguous horizontal sequence of pixels of the same color.
        properties:
          - color: The color of the pixels in the block (azure in this focus).
          - length: The number of pixels in the block.
          - position: Start and end indices within the sequence.
          - context: Pixels immediately preceding and succeeding the block.
    actions:
      - identify_azure_blocks: Find all contiguous blocks of azure (8) pixels.
      - check_surroundings: For each azure block, determine if it is immediately preceded by white (0) and immediately followed by white (0). Handle boundary conditions as if they are not white (0).
      - find_max_length: Among the azure blocks surrounded by white (0), find the maximum length.
      - change_color: Change the color of all azure blocks that are surrounded by white (0) AND have the maximum length found in the previous step to orange (7).
    relationships:
      - adjacency: Pixels are adjacent horizontally.
      - grouping: Pixels of the same color form blocks.
      - conditionality: Color change depends on block length and adjacency to white pixels.
    invariants:
      - White (0) pixels always remain white (0).
      - Azure (8) pixels that are part of blocks not meeting the criteria (not surrounded by white OR not of maximum length among surrounded blocks) remain azure (8).
      - The length of the sequence remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize the output sequence as a copy of the input sequence.
    2.  Scan the input sequence to identify all contiguous horizontal blocks composed solely of azure (8) pixels. Record their start index, end index, and length.
    3.  Create a list of "candidate" blocks: Filter the identified azure blocks, keeping only those that are immediately preceded by a white (0) pixel AND immediately followed by a white (0) pixel. (A block at the very beginning or end of the sequence cannot be surrounded by white pixels).
    4.  If the list of candidate blocks is empty, the transformation is complete, and the initial copy of the input is the final output.
    5.  If there are candidate blocks, determine the maximum length among them.
    6.  Iterate through the list of candidate blocks again. For each candidate block whose length equals the determined maximum length, change the color of all pixels within that block's range (from its start index to its end index) in the output sequence to orange (7).
    7.  Return the modified output sequence.