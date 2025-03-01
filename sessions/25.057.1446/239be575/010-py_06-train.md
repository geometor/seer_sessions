
## example 1
*input:*
```
0 0 8 0 8
2 2 8 0 0
2 2 0 0 8
0 0 0 2 2
8 8 0 2 2
```
*expected output:*
```
0
```
*transformed output:*
```
0 0 8 0 8
2 0 8 0 0
0 8 8 0 8
0 0 0 2 0
8 0 0 0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 8 0 0 0 0 0
2 2 0 8 8 8 0
2 2 8 8 0 2 2
0 0 8 0 0 2 2
0 8 0 0 8 0 0
```
*expected output:*
```
8
```
*transformed output:*
```
0 8 0 0 0 0 0
2 0 0 0 0 0 0
0 0 0 8 0 2 0
0 0 8 8 0 0 0
0 8 0 0 8 0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
8 2 2 8 8 0 0
0 2 2 0 0 0 8
0 8 8 0 0 8 0
0 0 8 0 0 0 8
8 0 8 8 8 2 2
8 0 0 0 0 2 2
```
*expected output:*
```
8
```
*transformed output:*
```
8 2 0 8 0 0 0
0 0 0 0 0 0 8
0 8 8 0 0 8 0
0 0 8 0 0 0 8
8 0 0 0 0 2 0
0 0 0 0 0 0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 4
*input:*
```
8 8 0 0 2 2 0
0 8 8 0 2 2 8
0 0 0 8 0 8 0
8 0 0 0 0 0 0
0 2 2 0 8 0 8
0 2 2 8 8 0 8
```
*expected output:*
```
0
```
*transformed output:*
```
8 8 0 0 2 0 0
0 0 0 0 0 0 8
0 0 8 8 8 8 0
8 0 0 8 0 0 0
0 2 0 0 0 0 8
0 0 0 0 0 0 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 5
*input:*
```
8 0 0 0 0 8 0
0 0 2 2 0 8 0
8 0 2 2 0 0 0
0 0 8 0 0 8 0
0 0 8 2 2 0 8
8 0 0 2 2 8 0
```
*expected output:*
```
8
```
*transformed output:*
```
8 0 0 0 0 8 0
0 2 2 2 0 0 0
8 2 2 2 0 0 0
0 0 8 0 0 8 0
0 0 0 2 0 0 8
8 0 0 0 0 8 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 6
*input:*
```
8 0 0 2 2 8
8 0 8 2 2 0
0 0 0 0 8 0
2 2 8 0 8 0
2 2 0 0 0 8
0 8 8 0 8 0
```
*expected output:*
```
0
```
*transformed output:*
```
8 0 0 2 0 8
0 8 8 0 0 0
0 8 8 0 8 0
2 0 8 0 0 0
0 0 0 0 0 8
0 8 0 0 8 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**
