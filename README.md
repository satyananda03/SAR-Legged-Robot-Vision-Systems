# SAR Legged Robot Vision System
Vision systems for SAR Legged Robot to detect victim in Indonesian SAR Legged Robot 2024 competition
- Train YOLOv5n model to detect victim target in robot arena
- Deploy on NVIDIA Jetson Nano 4GB that is already integrated with the Hexapod SAR legged robot
- Optimize model inference for NVDIA GPU using TensorRT (achieved 27 fps)

## Technology Used
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Ultralytics](https://img.shields.io/badge/Ultralytics-E4002B?style=for-the-badge&logo=ultralytics&logoColor=white)](https://ultralytics.com/)
[![NVIDIA](https://img.shields.io/badge/NVIDIA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://www.nvidia.com/)

## Victim Dataset
https://universe.roboflow.com/myworkspace-vi5mm/datacobanew

## Training Notebooks
https://colab.research.google.com/drive/1RFFaoFPvOF2Unn6aHxhcV3poeVyjak8h?usp=sharing

Training Result
- Precision : 0.989

- Recall : 0.988

- mAP50 : 0.99

- mAP950-95 : 0.962

# Results
Implementation on Hexapod SAR Legged Robot : https://drive.google.com/file/d/1aLB9E3pdhxQUv2Ye9aG545y4xIXn1qmp/view?usp=sharing
