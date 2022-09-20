# Toloka Visual Question Answering Challenge at WSDM Cup 2023

## Dataset

Our dataset consists of the images associated with textual questions. One entry (instance) in our dataset is a question-image pair labeled with the ground truth coordinates of a bounding box containing the visual answer to the given question. The images were obtained from a CC BY-licensed subset of the Microsoft Common Objects in Context dataset, [MS COCO](https://cocodataset.org/). All data labeling was performed on the Toloka crowdsourcing platform, <https://toloka.ai/>. The entire dataset can be downloaded at <https://doi.org/10.5281/zenodo.7057740>.

Licensed under the Creative Commons Attribution 4.0 License. See LICENSE-CC-BY.txt file for more details.

## Baseline

We offer a zero-shot baseline in `Baseline.ipynb`. First, it uses a detection model, YOLOR, to generate candidate rectangles. Then, it applies CLIP to measure the similarity between the question and a part of the image bounded by each candidate rectangle. To make a prediction, it uses the candidate with the highest similarity. This baseline method achieves IoU = 0.20 on both public and private test subsets.

Licensed under the Apache License, Version 2.0. See LICENSE-APACHE.txt file for more details.
