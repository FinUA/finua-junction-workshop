"""
Given the list of tags, print the expected accuracy if were randomly picking the
labels. This can be used as a baseline to assess how good the performance is.
"""
import json

with open('tags_with_descriptions.jsonl', 'r') as f:
    tags = f.readlines()
    tags = [json.loads(tag.strip()) for tag in tags]

def calc_random_baseline_accuracy(input_lists):
    tag_count = len(tags)
    # for each row, the expected correct count
    num_correct = [len(x)/tag_count for x in input_lists]
    return sum(num_correct)/len(input_lists)

def calc_random_baseline_fpr(input_lists):
    tag_count = len(tags)
    num_incorrect = [(1-len(x)/tag_count)*len(x) for x in input_lists]
    return sum(num_incorrect)/sum(len(x) for x in input_lists)
