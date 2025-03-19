
## example 1
*input:*
```
3 0 0
0 0 0
0 0 4
```
*expected output:*
```
0 0 0
0 3 0
0 0 4
```
*transformed output:*
```
0 0 0
0 0 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 2
*input:*
```
0 0 0
3 0 4
0 0 0
0 0 0
0 0 0
```
*expected output:*
```
0 0 0
0 3 4
0 0 0
0 0 0
0 0 0
```
*transformed output:*
```
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0
0 0 0 0 0
0 3 0 0 4
0 0 0 0 0
0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0
0 0 0 0 0
0 0 3 0 4
0 0 0 0 0
0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0
0 0 0 0 0
0 4 0 0 0
0 0 0 0 0
0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 3
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0 0
0 3 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 4 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 3 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 4 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 5
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 6
*input:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 7
*input:*
```
0 0 3
0 0 0
4 0 0
```
*expected output:*
```
0 0 0
0 3 0
4 0 0
```
*transformed output:*
```
0 0 0
0 0 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**
