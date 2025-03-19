
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 8 8 0
0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
8 0 0 0
0 8 0 0
0 0 8 0
0 0 0 8
```
*transformed output:*
```
8 0 0
8 8 0
8 8 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
8 0 0
0 8 0
0 0 8
```
*transformed output:*
```
8 8 0
0 8 8
8 8 0
```
size: True
palette: True
color count: False
pixels off: 5
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 8 0 0 0
0 0 0 8 8 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
8 0
0 8
```
*transformed output:*
```
8 8 8
8 8 8
0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
