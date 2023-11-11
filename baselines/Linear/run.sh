#!/bin/bash
python experiments/train.py -c baselines/Linear/ETTh1.py --gpus '0'
python experiments/train.py -c baselines/Linear/ETTh2.py --gpus '0'
python experiments/train.py -c baselines/Linear/ETTm1.py --gpus '0'
python experiments/train.py -c baselines/Linear/ETTm2.py --gpus '0'
python experiments/train.py -c baselines/Linear/Electricity.py --gpus '0'
python experiments/train.py -c baselines/Linear/ExchangeRate.py --gpus '0'
python experiments/train.py -c baselines/Linear/Weather.py --gpus '0'
python experiments/train.py -c baselines/Linear/PEMS04.py --gpus '0'
python experiments/train.py -c baselines/Linear/PEMS08.py --gpus '0'