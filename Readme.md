## An Empirical Study of Parameter-Efficient Fine-Tuning in Code Change Learning and Beyond

### Datasets
- Datasets are Available Here: [JIT-DP](https://github.com/jacknichao/JIT-Fine), [CMG](https://zenodo.org/records/7196966#.Y0juJHZBxmM), [TYP](https://github.com/giganticode/probes).
- For the CCM and LTP datasets, please refer to the [datasets/probing](https://github.com/ishuoliu/PeftCC/tree/main/datasets/probing) folder.



### Quick Start
- Just-In-Time Defect Prediction:

Finetune / Adapter / LoRA:
```commandline
  cd ./just-in-time
  source run.sh
```

Prompt / Prefix:
```commandline
  cd ./just-in-time
  source run_peft.sh
```

Probing tasks:
```commandline
  cd ./just-in-time
  python probe_extractor.py
  python probe_classifier.py
```

- Commit Message Generation:

Finetune / Adapter / LoRA:
```commandline
  cd ./commit-generation
  source run.sh
```

Prompt / Prefix / Pasta:
```commandline
  cd ./commit-generation
  source run_peft.sh
```

Probing tasks:
```commandline
  cd ./commit-generation
  python probe_extractor.py
  python probe_classifier.py
```