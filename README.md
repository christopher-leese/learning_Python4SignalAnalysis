# learning_PySDR
Learning and experimenting with PySDR for a synthetic burst detector / SigMF annotator project... Primarily notes and exercise records.

## Quickstart

This repository uses a local virtual environment in the project root.

1. Clone the repo in your desired directory:

```bash
git clone https://github.com/christopher-leese/learning_PySDR.git
cd learning_PySDR
```

2. Create the environment:

```bash
python3 -m venv .venv
```

3. Install the needed dependencies:

```bash
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install numpy matplotlib
```

Now, any of the project sections can be ran in your virtual environment. Below is an example of the `complex_baseband_and_sampling` folder:

```bash
cd complex_baseband_and_sampling
../.venv/bin/python main.py
```