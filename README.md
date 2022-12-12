# Toloka Visual Question Answering Challenge at WSDM Cup 2023

We challenge you with a visual question answering task! **Given an image and a textual question, draw the bounding box around the object correctly responding to that question.**

| Question | Image and Answer |
| --- | --- |
| What do you use to hit the ball? | <img src="https://tlk-infra-front.azureedge.net/portal-static/images/wsdm2023/tennis/x2/image.webp" width="228" alt="What do you use to hit the ball?"> |
| What do people use for cutting? | <img src="https://tlk-infra-front.azureedge.net/portal-static/images/wsdm2023/scissors/x2/image.webp" width="228" alt="What do people use for cutting?"> |
| What do we use to support the immune system and get vitamin C? | <img src="https://tlk-infra-front.azureedge.net/portal-static/images/wsdm2023/juice/x2/image.webp" width="228" alt="What do we use to support the immune system and get vitamin C?"> |

- **Competition:** <https://toloka.ai/challenges/wsdm2023>
- **CodaLab:** <https://codalab.lisn.upsaclay.fr/competitions/7434>
- **Dataset:** <https://doi.org/10.5281/zenodo.7057740>

## Dataset

Our dataset consists of the images associated with textual questions. One entry (instance) in our dataset is a question-image pair labeled with the ground truth coordinates of a bounding box containing the visual answer to the given question. The images were obtained from a CC BY-licensed subset of the Microsoft Common Objects in Context dataset, [MS COCO](https://cocodataset.org/). All data labeling was performed on the Toloka crowdsourcing platform, <https://toloka.ai/>. The entire dataset can be downloaded at <https://doi.org/10.5281/zenodo.7057740>.

Licensed under the Creative Commons Attribution 4.0 License. See LICENSE-CC-BY.txt file for more details.

## Baseline

We offer a zero-shot baseline in `Baseline.ipynb`. First, it uses a detection model, YOLOR, to generate candidate rectangles. Then, it applies CLIP to measure the similarity between the question and a part of the image bounded by each candidate rectangle. To make a prediction, it uses the candidate with the highest similarity. This baseline method achieves IoU = 0.20 on both public and private test subsets.

Licensed under the Apache License, Version 2.0. See LICENSE-APACHE.txt file for more details.

## Reproduction

The final score will be evaluated on the private test dataset during Reproduction phase. We kindly ask you to create a docker image and share it with us by December 19th 23:59 AoE in [this form](https://docs.google.com/forms/d/e/1FAIpQLSfWt-c2OvfXPcOQ-J7EmIh1AOAjiojH7RT33bRgchI4evtvLw/viewform?usp=sf_link). We put an instruction how to create a docker image in `reproduction` directory. 

We will run your solution on a machine with one Nvidia A100 80 GB GPU, 16 CPU cores, and 200 GB of RAM. Your Docker image must perform the inference in at most 3 hours on this machine. In other words, the docker run command must finish in 3 hours.

Don't hesitate to contact us at research@toloka.ai if you have any questions or suggestions.
