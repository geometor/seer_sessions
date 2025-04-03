## Perception

The input and output are presented as 1D arrays (or 1xN grids) of colored pixels.
Each input array consists of three distinct parts:
1.  A leading sequence of zero pixels (white).
2.  A central sequence of non-zero pixels.
3.  A trailing sequence of zero pixels (white).

Within the central sequence of non-zero pixels, one color appears most frequently (the "dominant" color), while one or more other colors appear less frequently (the "impurity" colors).

The transformation rule involves identifying the dominant color within the central non-zero sequence and replacing all impurity colors within that same sequence with the dominant color. The leading and trailing zero sequences remain unchanged.

## Facts


```yaml
Task: Replace minority colors with the majority color within a central segment.

Input:
  - Structure: 1D array (or 1xN grid).
  - Segments:
    - LeadingBorder: Sequence of zero pixels (white) at the beginning. Can be empty.
    - CentralSegment: Contiguous sequence of non-zero pixels following the LeadingBorder.
    - TrailingBorder: Sequence of zero pixels (white) at the end, following the CentralSegment. Can be empty.
  - Objects within CentralSegment:
    - Pixels: Each element in the sequence.
    - Properties:
      - Color: An integer from 1 to 9.
      - Frequency: Count of occurrences within the CentralSegment.
    - Categories:
      - DominantColorPixel: Pixel whose color is the most frequent non-zero color in the CentralSegment.
      - ImpurityColorPixel: Pixel whose color is non-zero but not the DominantColor.

Output:
  - Structure: Same dimensions and segment structure as the input.
  - Transformation:
    - Action: Replace color.
    - Target: ImpurityColorPixels within the CentralSegment.
    - Source: DominantColor.
    - Result: All pixels within the CentralSegment now have the DominantColor.
    - Invariance: LeadingBorder and TrailingBorder pixels remain unchanged.

Relationships:
  - The transformation is localized to the CentralSegment.
  - The replacement color (DominantColor) is determined by the most frequent color *within* the CentralSegment of the input.
```


## Natural Language Program

1.  Identify the boundaries of the central contiguous segment of non-zero pixels in the input array. Ignore any leading or trailing zero pixels.
2.  Within this central segment, count the frequency of each distinct non-zero color.
3.  Determine the color with the highest frequency; this is the "dominant color".
4.  Create the output array as a copy of the input array.
5.  Iterate through the pixels within the identified central segment of the output array.
6.  For each pixel in this segment, if its color is not the dominant color, change its color to the dominant color.
7.  Leave all pixels outside the central segment (the leading and trailing zero pixels) unchanged.
8.  The resulting array is the final output.