
## example 1
*input:*
```
0 0 0 0 0 0
0 5 0 0 5 0
0 5 0 0 5 0
0 5 0 0 5 0
0 5 8 8 5 0
0 5 5 5 5 0
```
*expected output:*
```
8 8 8
0 0 0
0 0 0
```
*transformed output:*
```
5 0 0
5 8 8
5 5 5
```
size: True
palette: False
color count: False
pixels off: 9
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 5 0 0
0 0 5 0 0 0 5 0 0
0 0 5 0 0 0 5 0 0
0 0 5 0 0 0 5 0 0
0 0 5 8 8 8 5 0 0
0 0 5 8 8 8 5 0 0
0 0 5 8 8 8 5 0 0
0 0 5 5 5 5 5 0 0
```
*expected output:*
```
8 8 8
0 0 8
0 0 0
```
*transformed output:*
```
5 0 0
5 8 8
5 8 8
```
size: True
palette: False
color count: False
pixels off: 8
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 5 0
0 5 0 0 0 0 0 5 0
0 5 0 0 0 0 0 5 0
0 5 8 8 8 8 8 5 0
0 5 8 8 8 8 8 5 0
0 5 8 8 8 8 8 5 0
0 5 5 5 5 5 5 5 0
```
*expected output:*
```
8 8 8
0 0 0
0 0 0
```
*transformed output:*
```
5 0 0
5 8 8
5 8 8
```
size: True
palette: False
color count: False
pixels off: 9
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 5 0 0
0 0 5 0 0 0 5 0 0
0 0 5 8 8 8 5 0 0
0 0 5 8 8 8 5 0 0
0 0 5 8 8 8 5 0 0
0 0 5 8 8 8 5 0 0
0 0 5 5 5 5 5 0 0
```
*expected output:*
```
8 8 0
0 0 0
0 0 0
```
*transformed output:*
```
5 0 0
5 8 8
5 8 8
```
size: True
palette: False
color count: False
pixels off: 8
**FAILED!**

## example 5
*input:*
```
0 0 0 0 0 0
0 5 0 0 5 0
0 5 8 8 5 0
0 5 8 8 5 0
0 5 5 5 5 0
```
*expected output:*
```
8 0 0
0 0 0
0 0 0
```
*transformed output:*
```
5 0 0
5 8 8
5 8 8
```
size: True
palette: False
color count: False
pixels off: 7
**FAILED!**

## example 6
*input:*
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 5 0 0 0 5 0
0 5 0 0 0 5 0
0 5 8 8 8 5 0
0 5 8 8 8 5 0
0 5 5 5 5 5 0
```
*expected output:*
```
8 8 0
0 0 0
0 0 0
```
*transformed output:*
```
5 0 0
5 8 8
5 8 8
```
size: True
palette: False
color count: False
pixels off: 8
**FAILED!**
