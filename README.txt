## CSC 305 Assignment 3

## Introduction
This Python graphics program renders a scene of elipsoids using a simplified raytracing algorithm.

## Requirements
- Python 3.11 and up
- Numpy (required for mathematical operations)

## Installing Numpy
To install Numpy, run the following command:
```bash
pip install numpy
```

## Running the Program
All test files can be rendered using the main script:

```bash
python3 render.py
```
Individual files can be rendered by executing:

```bash
python3 RayTracer.py <path/to/test>.txt
```

## Implemented Test Cases
testImgPlane.txt: Fully implemented
testAmbient.txt: Fully implemented
testBackground.txt: Fully implemented
testBehind.txt: Fully implemented
testIntersection.txt: Fully implemented
testDiffuse.txt: Fully implemented
testShadow.txt: Fully implemented
testSpecular.txt: Fully implemented
testSample.txt: Fully implemented
testParsing.txt: Fully implemented
testReflection.txt: Fully implemented
testIllum.txt: Partially implemented (near plane slicing working, self shadowing not working)

## File Structure
render.py: Main script to render all test cases.
RayTracer.py: Core module implementing the ray tracing algorithm.
tests/: Directory containing various test cases in the form of text files.
