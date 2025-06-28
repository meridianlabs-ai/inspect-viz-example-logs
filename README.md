# inspect-viz-sandbox

This repo includes prototypes of higher level functions and example code for [Inspect Viz](https://meridianlabs-ai.github.io/inspect_viz/).

## Getting Started

To use this repo begin by ensuring that you have GitLFS installed (used for log files in `/logs/` dir):

<https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage>

Then, clone the repo and create a virtual environment:

```bash
git clone git@github.com:meridianlabs-ai/inspect-viz-sandbox.git
cd inspect-viz-sandbox
python3 -m venv .venv
source .venv/bin/activate
```

> [!IMPORTANT]
> Next, be sure that you install the _very latest_ GitHub versions the `inspect_ai` and `inspect_viz` packages:
>  ```bash
>  pip install git+https://github.com/UKGovernmentBEIS/inspect_ai
>  pip install git+https://github.com/meridianlabs-ai/inspect_viz
>  ```
>
> You should update these packages frequently as we will be adding capabilities to both packages frequently to facilliate work in this repo.

## Development

Notebooks are an excellent interactive environment for workign on higher level plotting code (see the [demo.ipynb](demo.ipynb) notebook for a simple example).

Inspect Viz is built on top of the [Moasic](https://idl.uw.edu/mosaic/) data visualization system which is in turn built on [Observable Plot](https://observablehq.com/plot/). The Inspect Viz Python wrapper functions typically map quite closely to Observable Plot, so if you are using Google or an LLM to help with development, asking how to do things in Observable Plot will typically yield actionable advice.

