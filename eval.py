import json
import sys
import glob
from utils.calc_random_baseline import calc_random_baseline_accuracy, calc_random_baseline_fpr

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    try:
        files = sorted(glob.glob("output_*.jsonl"))
        file = files[-1]
    except Exception:
        print("No output file found")
        exit(1)

with open(file, "r") as f:
    # Load the data into a Python list of dictionaries
    results = [json.loads(line) for line in f.readlines()]

correct_count = sum(x['tag_true'] in x['tags'] for x in results)
row_count = len(results)

incorrect_count = sum(len(x["tags"])-1*(x['tag_true'] in x['tags']) for x in results)
prediction_count = sum(len(x["tags"]) for x in results)

# Accuracy: in how many examples did we give the correct tag?
accuracy = correct_count / row_count
# False positive rate: what percentage of all predictions were incorrect?
FPR = incorrect_count / prediction_count
# Random baseline for accuracy: assuming that we have the same amount of
# predictions for each input, but randomly selected from the available tasks
random_baseline_acc = calc_random_baseline_accuracy([x["tags"] for x in results])
random_baseline_fpr = calc_random_baseline_fpr([x["tags"] for x in results])


print(f"Accuracy: {100*accuracy:.2f}%")
print(f"False positive rate: {100*FPR:.2f}%")
print("---")
print(f"Random baseline for accuracy: {100*random_baseline_acc:.2f}%")
print(f"Random baseline for false positive rate: {100*random_baseline_fpr:.2f}%")