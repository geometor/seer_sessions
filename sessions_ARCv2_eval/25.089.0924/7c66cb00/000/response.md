Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
## Perception

The input and output grids are structured into distinct horizontal bands or segments. These bands are often characterized by a primary background color and sometimes a different "frame" color along the left and right edges.

The topmost band in the input grid contains one or more "patterns" - objects made of colors different from the top band's background color. These patterns can be simple shapes or more complex figures, sometimes composed of multiple colors.

The core transformation involves these patterns interacting with the bands located below the top band. The patterns essentially act as "stamps" or "templates".

The shape of each pattern from the top band is projected downwards onto each subsequent band. When a pattern's shape is projected onto a lower band, the pixels within that shape's area in the lower band are recolored. The color used for this "stamping" is determined by the frame color of the target band (the color on the far left and right edges of that band).

However, there's a specific exception: a pattern made of Green (3) will *not* be stamped onto a band whose background color is Azure (8). All other pattern color / target band background color combinations result in stamping.

Finally, after the stamping process affects the lower bands, the topmost band in the output grid is "cleared" – all its pixels are set to the original background color of that top band, effectively removing the original patterns from view.

## Facts


---
