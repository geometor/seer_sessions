
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 3 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 8 0 0 0 0 0 0 8 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 14
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 3 0 0 0 8 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 0 0 0 8 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 8 0 0 0 3 0 0
0 0 0 0 3 0 0 0 8 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 0 0 0 8 0 0
0 0 0 0 8 0 0 0 3 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 9
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0
0 8 3 3 3 3 3 3 3 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 3 0 0 0 0 0 0 0 3 0
0 8 0 0 0 0 0 0 0 8 0
0 3 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0
0 0 8 0 0 0 0 8 0 0 0
0 0 3 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 23
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 0 8 0 0 0
0 0 3 0 0 0
0 0 3 0 0 0
0 0 3 0 0 0
0 0 3 0 0 0
0 0 3 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
```
*transformed output:*
```
0 0 3 0 0 0
0 0 8 0 0 0
0 0 3 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 3 0 0 0
0 0 8 0 0 0
0 0 3 0 0 0
```
size: True
palette: True
color count: False
pixels off: 5
**FAILED!**

## example 5
*input:*
```
0 0 0
0 8 0
0 0 0
```
*expected output:*
```
0 0 0
0 8 0
0 0 0
```
*transformed output:*
```
0 3 0
0 8 0
0 3 0
```
size: True
palette: False
color count: False
pixels off: 2
**FAILED!**

## example 6
*input:*
```
0 0 0 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 8 0
0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 8 0
0 0 0 0 0 0
```
*transformed output:*
```
0 3 0 0 0 0
0 8 0 0 0 0
0 3 0 0 3 0
0 0 0 0 8 0
0 0 0 0 3 0
```
size: True
palette: False
color count: False
pixels off: 4
**FAILED!**

## example 7
*input:*
```
0 0 0 0 0 0
0 0 0 8 0 0
0 0 0 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 8 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 0 0 8 0 0
0 0 0 3 0 0
0 8 0 3 0 0
0 0 0 3 0 0
0 0 0 3 0 0
0 0 0 8 0 0
```
*transformed output:*
```
0 0 0 3 0 0
0 3 0 8 0 0
0 3 0 3 0 0
0 8 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
0 0 0 8 0 0
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**

## example 8
*input:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 8 3 3 3 8
0 8 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 3 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 3 0 0 3 0 0 0 3
0 3 0 0 0 0 3 0 0 0 3
0 3 0 0 0 0 8 0 0 0 8
0 8 0 0 0 0 3 0 0 0 3
0 3 0 0 0 0 3 0 0 0 3
0 3 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 22
**FAILED!**
