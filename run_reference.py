"""
This is the "reference implementation" for the workshop task.
"""
import json
import time
import llm

def construct_openai_messages(prompt):
    # you can prepend a system prompt here with "role": "system"
    return [{"role": "user", "content": prompt}]

def construct_prompt(message, tags):
    # write tags as "Tag name: Tag description"
    tags_rendered = "\n".join([x["name"]+": "+x["description"] for x in tags])

    return f"""
Your task is to *label a message with tags*. You will get the list of tags and the message below.

The ALLOWED TAGS (description after colon):
{tags_rendered}

---
Instructions:
- You MUST output a list of UP TO ONE tags relevant to the message; do NOT output any irrelevant tags
- You MUST NOT output more than ONE tags
- Each tag you write MUST be from the below list; do NOT invent any new tags.
- If there are no matching tags, you MAY output an empty list.

---
The message:
{message}

All the tags in your answer MUST BE ALLOWED TAGS.
Write your answer in the JSON format
{{"tags": list[str]}}
Write NOTHING ELSE than the JSON.
"""

def parse_response(x):
    return json.loads(x.replace("```json", "").replace("```", ""))


def process_messages(messages, tags):
    out = ""
    for idx, m in enumerate(messages):
        prompt = construct_openai_messages(
            construct_prompt(m["message_eng"], tags)
        )
        try:
            response = "".join(llm.respond(prompt))
            parsed = parse_response(response)
            result = json.dumps({"row": idx, "tag_true": m["tag"], **parsed})
            print(result)
            out += result + "\n"
        except RuntimeError as e:
            print("Stopping due to unrecoverable error.")
            exit(1)
        except Exception as e:
            print(e)
    return out


if __name__ == "__main__":
    import sys
    messages = None
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "input.jsonl"

    with open(input_file, 'r') as f:
        messages = f.readlines()
        messages = [json.loads(x) for x in messages]

    tags = None
    with open('tags_with_descriptions.jsonl', 'r') as f:
        tags = f.readlines()
        tags = [json.loads(x) for x in tags]
    
    out = process_messages(messages, tags)
    timestamp = int(time.time())
    with open(f"output_{timestamp}.jsonl", "w+") as f:
        f.write(out)