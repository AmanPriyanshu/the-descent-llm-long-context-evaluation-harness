import json
from pathlib import Path

dataset_names = [
    "hotpotqa",
    "2wikimqa",
    "musique",
    "narrativeqa",
    "qasper",
    "gov_report",
    "qmsum",
    "triviaqa",
    "samsum",
    "multifieldqa_en",
    "passage_retrieval_en",
    "passage_count"
]

print("Loading all datasets from local files...")
print("Reading from structured directories.\n")

all_datasets = {}

for dataset_key in dataset_names:
    print(f"{'='*80}")
    print(f"Loading {dataset_key}...")
    print(f"{'='*80}")
    
    try:
        dataset_dir = Path(dataset_key)
        queries_file = dataset_dir / "queries.json"
        contexts_dir = dataset_dir / "contexts"
        
        with open(queries_file, 'r', encoding='utf-8') as f:
            queries = json.load(f)
        
        data = []
        for query in queries:
            context_id = query['context_id']
            context_file = contexts_dir / f"{context_id}.txt"
            
            with open(context_file, 'r', encoding='utf-8') as f:
                context = f.read()
            
            item = {
                'input': query['input'],
                'context': context,
                'answers': query['answers'],
                'length': query['length'],
                'dataset': query['dataset'],
                'language': query['language'],
                'all_classes': query['all_classes'],
                '_id': query['_id']
            }
            data.append(item)
        
        all_datasets[dataset_key] = data
        
        print(f"\nNumber of samples: {len(data)}")
        print(f"\nFirst sample:")
        print(f"{'-'*80}")
        for key, value in data[0].items():
            if isinstance(value, str) and len(value) > 200:
                print(f"{key}: {value[:200]}... (truncated)")
            else:
                print(f"{key}: {value}")
        print(f"{'-'*80}\n")
        
    except Exception as e:
        print(f"ERROR loading {dataset_key}: {e}\n")
        continue

print(f"\n{'='*80}")
print(f"Summary: Successfully loaded {len(all_datasets)}/{len(dataset_names)} datasets")
print(f"{'='*80}")
for name, dataset in all_datasets.items():
    print(f"{name}: {len(dataset)} samples")