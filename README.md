# AEPLA
In this work, we propose a general framework for constructing l∞-PLA with adaptive error bounds.
## Environment
* Install conda environment from .yml file  
`conda env create --file environment.yml`
## Running
* Running FSW under the new framework:  
`main.py --eps 0.1 --alpha 0.2 --alg p --method FSW`  
(Please find the instructions for hyperparameter settings in the main.py)
## Citation
If you find this repository useful, please cite: <br>
@article{zhou2023adaptive, <br>
  title={Adaptive error bounded piecewise linear approximation for time-series representation}, <br>
  author={Zhou, Zhou and Baratchi, Mitra and Si, Gangquan and Hoos, Holger H and Huang, Gang}, <br>
  journal={Engineering Applications of Artificial Intelligence}, <br>
  volume={126}, <br>
  pages={106892}, <br>
  year={2023}, <br>
  publisher={Elsevier}}
