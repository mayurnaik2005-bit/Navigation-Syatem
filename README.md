# Navigation-Syatem

Store Navigator: indoor store navigation API and browser interface, with route optimization and graph demonstrations.

## Run the web app

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Open <http://127.0.0.1:8000/> for the interface or <http://127.0.0.1:8000/docs> for the API documentation.

## Optional demonstrations

Run `python main.py` to generate and display a sample store route graph. Run `python benchmark.py` to compare routing algorithms and generate a benchmark plot.