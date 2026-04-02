<h1 align="center">The Superposition of Diffusion Models Using the Itô Density Estimator</h1>

<p align="center">
<a href="https://arxiv.org/abs/2412.17762"><img src="https://img.shields.io/badge/arXiv-b31b1b?style=for-the-badge&logo=arxiv" alt="arXiv"/></a>
<a href="https://colab.research.google.com/drive/1iCEiQUMXmQREjT6pUYQ6QOw1_0EAqa82"><img src="https://img.shields.io/badge/Colab-e37e3d.svg?style=for-the-badge&logo=googlecolab&logoColor=white" alt="Jupyter"/></a>
  <a href="https://huggingface.co/superdiff/"><img src="https://img.shields.io/badge/HuggingFace-1f27ca.svg?style=for-the-badge&logo=HuggingFace&logoColor=yellow" alt="HF"/></a>
</p>

The principled method for efficiently combining multiple pre-trained diffusion models solely during inference! We provide a new approach for estimating density without touching the divergence. This gives us the control to easily interpolate concepts (logical AND) or mix densities (logical OR), allowing us to create one-of-a-kind generations!

<p align="center">
<img src="assets/SD_examples.gif" alt="Animation of the examples of SuperDiff for StableDiffusion"/>
</p>

</details>

## Install dependencies

For Stable Diffusion examples, see [Installing Dependencies for CIFAR and SD](/applications/images/README.md)

For Protein examples, see [Installing Dependencies for Protein Models](/applications/proteins/README.md)

## Using Code & Examples

We outline the high-level organization of the repo in the **_project tree_** and provide links to specific examples, notebooks, and experiments in the **_introduction_**, **_CIFAR_**, **_Stable Diffusion (SD)_**, and **_Proteins_** sections. 

#### Project Tree

```
├── applications
│   ├── images
│           - directory for reproducing SD experiments
│   └── proteins
│           - directory for reproducing protein experiments
├── assets
│       - folder with images
├── cifar
│       - directory for reproducing CIFAR experiments
├── LICENSE
├── notebooks
│       - educational examples and notebooks for SD
└── README.md
```

#### Introduction and Educational Notebooks

**Diffusion ([diffusion_edu.ipynb](/notebooks/diffusion_edu.ipynb)):** for an introduction to diffusion models and a basic example of training and sampling.

**Superposition ([superposition_edu.ipynb](/notebooks/superposition_edu.ipynb)):** for an introduction to combining diffusion models and reproducing  Figure 2.


#### CIFAR

**Train:** example for training a single model on CIFAR-10
```
python cifar/main.py --config cifar/configs/sm/cifar/vpsde.py --workdir $PWD/cifar/chkpt/ --mode 'train'
```

**Eval:** example for evaluating a single model on CIFAR-10
```
python cifar/main.py --config cifar/configs/sm/cifar/vpsde.py --workdir $PWD/cifar/chkpt/ --mode 'eval_fid'
```

#### Stable Diffusion (SD)

**Superposition AND ([superposition_AND.ipynb](/notebooks/superposition_AND.ipynb)):** notebook consisting of examples for generating images and interpolating concepts using SuperDiff (AND) with SD.

**Superposition OR ([superposition_OR.ipynb](/notebooks/superposition_OR.ipynb)):** notebook consisting of examples for of generating images using SuperDiff (OR) with SD.

**[SD Experiments](/applications/images/README.md):** for an example of how to generate images using SuperDiff with SD and reproducing the SD experiments.

#### Proteins

**[Protein Experiments](/applications/proteins/README.md):** for an example of how to generate proteins with SuperDiff and reproducing the protein experiments.


## Citation

<div align="left">
  
If you find this code useful in your research, please cite the following paper (expand for BibTeX):

<details>
<summary>
M. Skreta*, L. Atanackovic*, A.J. Bose, A. Tong, K. Neklyudov. The Superposition of Diffusion Models Using the Itô Density Estimator, 2024.
</summary>

```bibtex
@article{skreta2024superposition,
  title={The Superposition of Diffusion Models Using the It$\backslash$\^{} o Density Estimator},
  author={Skreta, Marta and Atanackovic, Lazar and Bose, Avishek Joey and Tong, Alexander and Neklyudov, Kirill},
  journal={arXiv preprint arXiv:2412.17762},
  year={2024}
}
```
