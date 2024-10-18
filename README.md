# FinUA Workshop at Junction 2024
## Tagging messages using an autoregressive Large Language Model

### Introduction
One important task FinUA uses to streamline operations is *tagging* user messages. This helps in organizing,
prioritizing and distributing them to experts who can help with them. Currently, this is a manual process.
In this task, we will use a generative LLM (GPT-4o mini) to tag messages, by calling the model from Python code.
The goal is not to create a perfect tagging system, but to get a feel for how to develop with LLMs and
what kinds of limitations one might encounter.

If you use an on-device LLM, or have a subscription, you are also free to use those in this task.
Just mention the model name along with your results.

### The task on a high level
- Process input data one message at a time.
- Write a prompt for the LLM so that the LLM returns a list of predicted tags *for one input message*.
- Evaluate how good the results are.

## The evaluation measures
- Accuracy: what % of messages had the correct tag among the predicted tags
- False positive rate: what % of the predicted tags were *not* the correct tag

### The data
For this task, we have generated *synthetic data* using an LLM. No real user data is shared.
The following input files are provided:

| File Name          | Description                                                                 |
|--------------------|-------------------------------------------------------------------------------|
| `tags_with_descriptions.jsonl` | The list of tags to use. These should be given to the LLM as context.         |
| `input.jsonl`      | The complete set of input data in JSON lines format. Use this to calculate the final score. |
| `input_small.jsonl` | A smaller subset of `input.jsonl` for experimentation.

### Instructions
1. Fill provided API URL and API key to the file `config.template.json` and rename to `config.json`
2. Test the reference code by running `python run_reference.py input_small.jsonl`
3. Implement your solution in `run.py`, starting from the functions `construct_prompt` and `process_messages`. You can also modify the reference implementation in `run_reference.py`.
4. Run `python eval.py` when you have an output file.
5. When you have a solution, run `python run.py input.jsonl` to get the full set of results, and run evaluation again.
6. Finally, share your solution, output and metrics on Discord!
