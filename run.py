import json
import time
import llm


def construct_openai_messages(prompt):
    """
    This function takes in your prompt and converts it into an OpenAI API `messages` structure.
    You can also decide to prepend instructions in a system prompt here with "role": "system",
    and give only the user message with the role "user".
    """
    return [{"role": "user", "content": prompt}]


def construct_prompt(message, tags):
    """
    This function constructs a prompt for the LLM. The prompt should at a minimum
    - Contain both the user message as well a list of the tags available
    - Output a list of tags corresponding to the tag name

    :param message (str): The user's message
    :param tags (list[dict]): A list of tags associated with the message, format {"name": str, "description": str}
    :return: A string that can be used as a prompt for the language model
    """
    # Return your prompt here! Try to make the model output the data as JSON in the format
    # {"tags": list[str]}, where each tag is from the provided list of tags.
    prompt = f""""""
    return prompt


def parse_response(x):
    """
    This function should parse the LLM response and write {"tags": list[str]}.
    The list of tags should correspond to the `name` field in `tags_with_descriptions.jsonl`
    """
    # Models typically use markdown for JSON formatting so we 
    # need to preprocess here.
    return json.loads(x.replace("```json", "").replace("```", ""))


def process_messages(messages, tags):
    """
    Messages is the list of messages with fields {"tag", "message_eng"}
    """
    out = ""
    for idx, m in enumerate(messages):
        prompt = construct_openai_messages(
            construct_prompt(m["message_eng"], tags)
        )
        try:
            response = "".join(llm.respond(prompt))
            parsed = parse_response(response)
            
            assert parsed.get("tags") is not None and type(parsed["tags"]) == list,\
                "Parsed output should have a field `tags`"

            result = json.dumps({"row": idx, "tag_true": m["tag"], **parsed})
            print(result)
            out += result + "\n"
        except RuntimeError as e:
            print("Stopping due to unrecoverable error.")
            exit(1)
        except Exception as e:
            print(f"Error: {e}")
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