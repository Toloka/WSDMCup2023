# Toloka Visual Question Answering Challenge at WSDM Cup 2023

We challenge you with a visual question answering task! **Given an image and a textual question, draw the bounding box around the object correctly responding to that question.**

| Question | Image and Answer |
| --- | --- |
| What do you use to hit the ball? | <img src="https://tlkfrontprod.azureedge.net/portal-production/static/uploaded/images/KUsGAc_eqdMcNxkBXzzl/KUsGAc_eqdMcNxkBXzzl_webp_1280_x2.webp" width="228" alt="What do you use to hit the ball?"> |
| What do people use for cutting? | <img src="https://tlkfrontprod.azureedge.net/portal-production/static/uploaded/images/brXEVYckNLfQKcfNu4DF/brXEVYckNLfQKcfNu4DF_webp_1280_x2.webp" width="228" alt="What do people use for cutting?"> |
| What do we use to support the immune system and get vitamin C? | <img src="https://tlkfrontprod.azureedge.net/portal-production/static/uploaded/images/HQ0A-ZvZCGCmYfTs83K7/HQ0A-ZvZCGCmYfTs83K7_webp_1280_x2.webp" width="228" alt="What do we use to support the immune system and get vitamin C?"> |

## Links

- **Competition:** <https://toloka.ai/challenges/wsdm2023>
- **CodaLab:** <https://codalab.lisn.upsaclay.fr/competitions/7434>
- **Dataset:** <https://doi.org/10.5281/zenodo.7057740>

## Citation

Please cite the challenge results or dataset description as follows.

- Ustalov D., Pavlichenko N., Likhobaba D., and Smirnova A. [WSDM Cup 2023 Challenge on Visual Question Answering](http://ceur-ws.org/Vol-3357/invited1.pdf). *Proceedings of the 4th Crowd Science Workshop on Collaboration of Humans and Learning Algorithms for Data Labeling.* Singapore, 2023, pp.&nbsp;1&ndash;7.

```bibtex
@inproceedings{TolokaWSDMCup2023,
  author    = {Ustalov, Dmitry and Pavlichenko, Nikita and Likhobaba, Daniil and Smirnova, Alisa},
  title     = {{WSDM~Cup 2023 Challenge on Visual Question Answering}},
  year      = {2023},
  booktitle = {Proceedings of the 4th Crowd Science Workshop on Collaboration of Humans and Learning Algorithms for Data Labeling},
  pages     = {1--7},
  address   = {Singapore},
  issn      = {1613-0073},
  url       = {http://ceur-ws.org/Vol-3357/invited1.pdf},
  language  = {english},
}
```

## Dataset

Our dataset consists of the images associated with textual questions. One entry (instance) in our dataset is a question-image pair labeled with the ground truth coordinates of a bounding box containing the visual answer to the given question. The images were obtained from a CC BY-licensed subset of the Microsoft Common Objects in Context dataset, [MS COCO](https://cocodataset.org/). All data labeling was performed on the Toloka crowdsourcing platform, <https://toloka.ai/>. We release the entire dataset under the CC BY license:

- Zenodo: <https://doi.org/10.5281/zenodo.7057740>
- Hugging Face Hub: <https://huggingface.co/datasets/toloka/WSDMCup2023>
- Kaggle: <https://www.kaggle.com/datasets/dustalov/toloka-wsdm-cup-2023-vqa>
- GitHub Packages: <https://github.com/Toloka/WSDMCup2023/pkgs/container/wsdmcup2023>

Licensed under the Creative Commons Attribution 4.0 License. See LICENSE-CC-BY.txt file for more details.

## Zero-Shot Baselines

We provide zero-shot baselines in `zeroshot_baselines` folder. All notebooks are made to run in Colab

#### YOLOR + CLIP

This baseline was provided to participants of WSDM Cup 2023 Challenge. First, it uses a detection model, YOLOR, to generate candidate rectangles. Then, it applies CLIP to measure the similarity between the question and a part of the image bounded by each candidate rectangle. To make a prediction, it uses the candidate with the highest similarity. This baseline method achieves **IoU = 0.21** on private test subset.

Licensed under the Apache License, Version 2.0. See LICENSE-APACHE.txt file for more details.

#### OVSeg + SAM

Another zero-shot baseline, called OVSeg, utilizes SAM as a proposal generator instead of MaskFormer in the original setup. This approach achieves **IoU = 0.35** on the private test subset.

#### OFA + SAM

Last one is primarily based on OFA, combined with bounding box correction using SAM. To solve the task, we followed a two-step zero-shot setup.

First, we address the Visual Question Answering, where the model is given a prompt `{question} Name an object in the picture` along with an image. The model provides the name of a clue object to the question.

In the second step, an object corresponding to the answer from the previous step is annotated using the prompt `which region does the text "{answer}" describe?`, resulting in IoU = 0.42.

Subsequently, with the obtained bounding boxes, SAM generates the corresponding masks for the annotated object, which are then transformed into bounding boxes. This enabled us to achieve **IoU = 0.45** with this baseline.


## Crowdsourcing Baseline

We evaluated how well non-expert human annotators can solve our task by running a dedicated round of crowdsourcing annotations on the [Toloka](https://toloka.ai/) crowdsourcing platform. We found them to tackle this task successfully without knowing the ground truth. On all three subsets of our data, the average IoU value was 0.87 &pm; 0.01, which we consider as a *strong human baseline* for our task. Krippendorff's &alpha; coefficients for the public test was 0.68 and for the private test was 0.66, showing the decent agreement between the responses; we used 1 &minus; IoU as the distance metric when calculating the &alpha; coefficient. We selected the bounding boxes which were the most similar to the ground truth data to indicate the upper bound of non-expert annotation quality; `*_crowd_baseline.csv` files contain these responses.

Licensed under the Creative Commons Attribution 4.0 License. See LICENSE-CC-BY.txt file for more details.

## Reproduction

The final score will be evaluated on the private test dataset during Reproduction phase. We kindly ask you to create a docker image and share it with us by December 19th 23:59 AoE in [this form](https://docs.google.com/forms/d/e/1FAIpQLSfWt-c2OvfXPcOQ-J7EmIh1AOAjiojH7RT33bRgchI4evtvLw/viewform?usp=sf_link). We put an instruction how to create a docker image in `reproduction` directory. 

We will run your solution on a machine with one Nvidia A100 80 GB GPU, 16 CPU cores, and 200 GB of RAM. Your Docker image must perform the inference in at most 3 hours on this machine. In other words, the docker run command must finish in 3 hours.

Don't hesitate to contact us at research@toloka.ai if you have any questions or suggestions.
