# Learning Python for Signal Analysis (P4SA)
Learning and experimenting with PySDR, SciPy, and SigMF for a synthetic burst detector / annotator project... Primarily notes and exercise records. Folders separate topics in order of coverage.

## Quickstart

This repository uses a local virtual environment in the project root.

1. Clone the repo in your desired directory:

```bash
git clone https://github.com/christopher-leese/learning_P4SA.git
cd learning_P4SA
```

2. Create the environment:

```bash
python3 -m venv .venv
```

3. Install the needed dependencies (using pip in my case):

```bash
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install numpy matplotlib scipy SigMF
```

Now, any of the project sections can be ran in our virtual environment. Below is an example of the `complex_baseband_and_sampling` folder:

```bash
cd complex_baseband_and_sampling
../.venv/bin/python main.py
```
