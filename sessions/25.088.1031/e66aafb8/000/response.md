*   **Perception**:
    *   Each input grid contains various colored pixels.
    *   A key feature across all examples is the presence of a contiguous block of white pixels (color 0). In some examples, this block is roughly centered, while in others, it's near an edge.
    *   The output grid appears to be a direct copy (extraction) of a subgrid from the input grid.
    *   The location and size of the output grid seem related to the location and size of the white block.
    *   Comparing the output grid to the regions immediately surrounding the white block (above, below, left, right), the output consistently matches one of these adjacent regions in terms of both dimensions and pixel content.
    *   The specific adjacent region chosen (above, below, left, or right) varies between examples, but in each case, only one of the four directly adjacent regions matches the output.

*   **Facts**:
    
```yaml
    Task: ExtractSubgridAdjacentToWhiteBlock
    
    Input:
      - name: InputGrid
        type: Grid
        description: A 2D array of pixels with colors 0-9.
        contains:
          - name: WhiteBlock
            type: Object
            properties:
              color: white (0)
              shape: contiguous block (often rectangular, but can be irregular)
              location: variable within the InputGrid
              size: variable
            identification: Find the largest contiguous block of 'white' pixels. Determine its bounding box (min_row, max_row, min_col, max_col).
          - name: PotentialOutputRegions
            type: Set of Objects
            description: Four rectangular regions directly adjacent to the WhiteBlock's bounding box.
            relationship: Share a full edge with the WhiteBlock.
            definition:
              - Above: InputGrid[0:min_row, min_col:max_col+1]
              - Below: InputGrid[max_row+1:H, min_col:max_col+1] (where H is input height)
              - Left: InputGrid[min_row:max_row+1, 0:min_col]
              - Right: InputGrid[min_row:max_row+1, max_col+1:W] (where W is input width)
              
            Note: The actual extracted region shares the full edge, so its dimensions depend on the white block's bounding box dimensions along that edge.
              - Region Above: rows = min_row, cols = max_col - min_col + 1. Located at [0:min_row, min_col:max_col+1]
              - Region Below: rows = H - (max_row + 1), cols = max_col - min_col + 1. Located at [max_row+1:H, min_col:max_col+1]
              - Region Left: rows = max_row - min_row + 1, cols = min_col. Located at [min_row:max_row+1, 0:min_col]
              - Region Right: rows = max_row - min_row + 1, cols = W - (max_col + 1). Located at [min_row:max_row+1, max_col+1:W]
              
              Simplified Definition based on observation:
              - Above: InputGrid[white_block.min_row - output.height : white_block.min_row, white_block.min_col : white_block.max_col + 1]
              - Below: InputGrid[white_block.max_row + 1 : white_block.max_row + 1 + output.height, white_block.min_col : white_block.max_col + 1]
              - Left: InputGrid[white_block.min_row : white_block.max_row + 1, white_block.min_col - output.width : white_block.min_col]
              - Right: InputGrid[white_block.min_row : white_block.max_row + 1, white_block.max_col + 1 : white_block.max_col + 1 + output.width]


    Output:
      - name: OutputGrid
        type: Grid
        description: A subgrid extracted from the InputGrid.
        properties:
          content: Pixel data identical to one of the PotentialOutputRegions.
          dimensions: Matches the dimensions of one of the PotentialOutputRegions.
    
    Transformation:
      - action: FindWhiteBlock
        description: Locate the largest contiguous block of white pixels (0) in the InputGrid and determine its bounding box.
      - action: IdentifyAdjacentRegions
        description: Define the four rectangular regions immediately adjacent (above, below, left, right) to the WhiteBlock's bounding box, sharing a full edge.
      - action: MatchAndExtract
        description: Compare the dimensions and content of the expected OutputGrid (from the training example) with the four identified AdjacentRegions. The region that exactly matches the OutputGrid is the one to be extracted. For the test case, implicitly assume there is only one region adjacent to the white block whose dimensions match the pattern seen in training (i.e., dimensions derived from the white block's edge length and the perpendicular distance to the grid edge/another object). Alternatively, identify the non-white region adjacent to the white block.
    
    Refined Transformation based on examples:
      - Find the largest contiguous block of white pixels (color 0). Determine its bounding box [min_r, max_r, min_c, max_c].
      - Consider the four regions directly adjacent to this bounding box:
        - Region Above: InputGrid[0:min_r, min_c:max_c+1]
        - Region Below: InputGrid[max_r+1:H, min_c:max_c+1]
        - Region Left: InputGrid[min_r:max_r+1, 0:min_c]
        - Region Right: InputGrid[min_r:max_r+1, max_c+1:W]
      - Identify which of these four regions matches the dimensions and content of the example output grid.
      - The output is the content of that specific adjacent region.
    ```


*   **Natural Language Program**:
    1.  Identify the largest contiguous area consisting solely of white pixels (color 0) within the input grid.
    2.  Determine the bounding box coordinates (minimum row, maximum row, minimum column, maximum column) of this white area.
    3.  Define four potential source regions in the input grid, located immediately adjacent to the white area's bounding box:
        *   The region directly *above* the white area, extending from the top edge of the grid (row 0) down to the row just before the white area's minimum row, and spanning the same columns as the white area's bounding box.
        *   The region directly *below* the white area, extending from the row immediately after the white area's maximum row down to the bottom edge of the grid, and spanning the same columns as the white area's bounding box.
        *   The region directly to the *left* of the white area, extending from the left edge of the grid (column 0) to the column just before the white area's minimum column, and spanning the same rows as the white area's bounding box.
        *   The region directly to the *right* of the white area, extending from the column immediately after the white area's maximum column to the right edge of the grid, and spanning the same rows as the white area's bounding box.
    4.  Determine which one of these four adjacent regions exactly matches the provided output grid example in terms of both its dimensions (height and width) and its pixel content.
    5.  The final output is a copy of this matching adjacent region.