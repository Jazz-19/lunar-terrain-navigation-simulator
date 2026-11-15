# Autonomous Lunar Terrain Navigation Simulator

A vision-based lunar terrain navigation simulator that explores safe-path identification and autonomous navigation decisions using classical image processing and machine learning.

## Project Overview

This project investigates how a lunar rover navigation system can identify potentially safe and hazardous terrain from images and generate navigation decisions.

The system explores three approaches:
- Classical image processing
- Support Vector Machine (SVM)
- Convolutional Neural Network (CNN)

## Key Features

- Lunar terrain image preprocessing using OpenCV
- Safe and unsafe terrain classification
- Comparison of classical vision and machine learning approaches
- Navigation decisions: LEFT, RIGHT and STRAIGHT
- Raspberry Pi-based embedded validation

## System Workflow

1. Input lunar terrain images
2. Image preprocessing
3. Terrain feature extraction and classification
4. Safe-region identification
5. Navigation decision generation
6. Visualization of the selected path

## Technologies Used

- Python
- OpenCV
- TensorFlow / Keras
- Scikit-learn
- Raspberry Pi

## Dataset

The project evaluates a sequence of 9,766 generated or rendered lunar terrain frames. Refer to the dataset documentation for details about data organization and availability.

## Repository Structure

The source code, documentation, results and hardware setup instructions are organized into separate directories.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/lunar-terrain-navigation-simulator.git
cd lunar-terrain-navigation-simulator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project using the entry point and instructions documented for the available implementation.

## Results

Add verified evaluation results, sample classification outputs and navigation visualizations here.

## Hardware Validation

The project includes Raspberry Pi integration for embedded validation of the navigation pipeline. This should not be interpreted as testing an operational lunar rover.

## Author

- Jiya Modak

## Acknowledgements

Guided by Prof. Shwetha Shetty and Prof. Sahil Nikam.

## Future Scope

- Testing with more diverse lunar terrain datasets
- Improving classification robustness
- Optimizing the pipeline for embedded deployment
- Exploring integration with physical rover platforms

## License

Specify the license under which this repository is distributed.

