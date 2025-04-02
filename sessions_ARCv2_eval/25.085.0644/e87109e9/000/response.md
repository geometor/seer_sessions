*   **Perception**:
    *   The input grid is visually divided into two main sections: an upper 'key' section (rows 0-5) and a lower 'data' section (rows 6-24).
    *   The key section is bordered by gray (5) pixels and contains four smaller blocks, also bordered by gray (5). Each inner block contains mostly white (0) pixels and a single column of a distinct color (blue-1, magenta-6, yellow-4, red-2).
    *   The column index of the non-white color within each key block seems significant. These columns are 1, 7, 13, and 19.
    *   The data section contains larger regions of various colors (green-3, blue-1, yellow-4, red-2) and a small 2x2 azure (8) square.
    *   The output grid corresponds exactly in size to the data section of the input grid (19x24). The key section is discarded.
    *   The transformation involves changing the color of specific pixels within the data section. Comparing the input's data section to the output grid, many green (3) pixels have become azure (8).
    *   The change from green (3) to azure (8) occurs *only* in the columns identified from the key section (columns 1, 7, 13, 19). However, the change only applies if the original pixel was green (3). Other colors in these columns (like blue-1 in col 1, yellow-4 in col 19, and the original azure-8 in col 13) remain unchanged. Pixels outside these specific columns also remain unchanged.

*   **Facts**:
    
```yaml
    InputGrid:
      Properties:
        - Size: 25x24
        - Contains two distinct sections vertically.
    KeySection:
      ObjectType: Region
      Location: Top rows of InputGrid (e.g., rows 0-5)
      Properties:
        - Bounded by gray (5) pixels.
        - Contains smaller KeyBlocks.
    KeyBlocks:
      ObjectType: SubRegion
      Location: Within KeySection
      Properties:
        - Four distinct blocks.
        - Bounded by gray (5) pixels.
        - Each contains mostly white (0) pixels and one column of a unique non-white color (1, 6, 4, 2).
      Relationship:
        - The column index of the non-white color within each block defines a TargetColumn.
    TargetColumns:
      ObjectType: Set of Indices
      Derivation: Extracted from the location of non-white colors in KeyBlocks.
      Value: [1, 7, 13, 19] in the example.
    DataSection:
      ObjectType: Region
      Location: Bottom rows of InputGrid (e.g., rows 6-24)
      Properties:
        - Contains various colored regions/pixels (3, 1, 4, 2, 8).
    OutputGrid:
      Properties:
        - Size: 19x24 (matches DataSection size)
      Derivation: Based on DataSection with modifications.
    Transformation:
      Action: Modify pixels within DataSection based on TargetColumns.
      Rule:
        - For each pixel in the DataSection:
          - If its column index is in TargetColumns AND its color is green (3):
            - Change its color to azure (8) in the OutputGrid.
          - Otherwise:
            - Keep its original color in the OutputGrid.
      Discard: KeySection is not present in the OutputGrid.

    ```


*   **Natural Language Program**:
    1.  Identify the upper 'key' section of the input grid, characterized by gray (5) borders enclosing blocks with single colored columns.
    2.  Identify the lower 'data' section of the input grid, located below the key section.
    3.  From the key section, determine the column indices where the non-white colors (blue-1, magenta-6, yellow-4, red-2) appear within their respective blocks. These are the 'target columns'.
    4.  Create the output grid by making a copy of the data section.
    5.  Iterate through each pixel in the output grid (which corresponds to the data section).
    6.  If a pixel's column index matches one of the target columns identified in step 3, *and* that pixel's color in the original data section was green (3), change its color in the output grid to azure (8).
    7.  Leave all other pixels in the output grid unchanged from their color in the data section.
    8.  The final modified copy of the data section is the result.