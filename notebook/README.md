## Conda MacOS and matplotlib (work in progress)

```
conda create -n mango python=3.12
conda activate mango
pip install -r requirements.txt
pip install -U ipykernel 
pip install -U notebook
pip install -U ipympl
python -m ipykernel install --user --name mango --display-name "pyvo 1.8 (mango)"
python -m jupyterlab
```
and select the appropriate kernel....
