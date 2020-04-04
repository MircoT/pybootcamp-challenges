# Soluzione 'The Maze Challenge' - Davide Pruscini (prushh)

Per questioni di comodità si è deciso di avviare l'engine direttamente da Python, motivo per cui bisogna specificare il *file_path* come mostrato di seguito:
```bash
python main.py mazeEngine.os.ext [--no_stats] [-c] [-d] [-h]
```

### Applicazione
Sono presenti due modalità:
 * **Classica**
 * **Controller** (disabilitare statistiche)

### Argparse
```
positional arguments:
  file_path         executable file to start engine

optional arguments:
  -h, --help        show this help message and exit
  -c, --controller  controller mode for interact with engine
  --no_stats        hide statistical information
  -d, --debug       print debug information and more
```