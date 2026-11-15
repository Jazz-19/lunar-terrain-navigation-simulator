# Methodology

## 1. Image Input

The system takes lunar terrain images as input for visual analysis and navigation simulation.

## 2. Image Preprocessing

The input images are converted into grayscale to simplify processing. Gaussian blurring is applied to reduce noise and improve the consistency of subsequent image operations.

## 3. Terrain Roughness Analysis

Image-processing operations are used to identify variations in terrain appearance. Morphological operations and thresholding help distinguish relatively smooth regions from areas with greater visual irregularity.

## 4. Safe-Region Identification

The processed image is analyzed to identify candidate regions for navigation. Connected-component filtering helps remove smaller unwanted regions and retain relevant candidate areas.

## 5. Navigation Decision

The image is divided into navigation corridors. The detected candidate regions are analyzed to generate directional decisions:

- LEFT
- RIGHT
- STRAIGHT

## 6. Output Visualization

The system displays visual overlays to represent the detected regions and the selected navigation direction.

## 7. Scope and Limitations

This implementation is a vision-based navigation simulator. Its image-processing decisions are heuristic estimates of terrain suitability. They do not establish physical terrain safety or demonstrate autonomous movement of a lunar rover.
