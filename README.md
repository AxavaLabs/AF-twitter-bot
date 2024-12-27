# Twitter Bot

## Table of Contents

Jump to a specific section:

- [Twitter Bot](#twitter-bot)
  - [Table of Contents](#table-of-contents)
  - [Build docker](#build-docker)
    - [Requirements](#requirements)
    - [Build docker compose](#build-docker-compose)
  - [Quickstart](#quickstart)
    - [Environment](#environment)
    - [Run](#run)

## Build docker

### Requirements

- An **NVIDIA GPU**; tensor cores increase performance when available. All shown results come from an RTX 3090.
- A recent version of **[CUDA](https://developer.nvidia.com/cuda-toolkit)**. The following choices are recommended and have been tested:
  - **Linux:** CUDA 12.4 or higher

### Build docker compose

```
docker compose build
```

## Quickstart

### Environment

- Step 1: Install Pytorch

```
pip install torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 --index-url https://download.pytorch.org/whl/cu124
```

- Step 2: Install requirements

```
pip install -r requirements.txt
```

- Step 3: Rename `.example.env` to `.env` and modify env

### Run

```
python demo.py
```
