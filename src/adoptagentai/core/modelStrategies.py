import openai

def gpt_4o_strategy(model_name, prompt, credentials):
    """ GPT-4 OpenAI strategy. """
    openai.api_key = credentials.get("api_key")
    response = openai.responses.create(
        model=model_name,
        instructions="You are a helpful assistant that provides information about the topic.",
        input=prompt,
        temperature=0.7    )
    return response

def gpt_4o_mini_strategy(model_name, prompt, credentials):
    """ GPT-4 mini OpenAI strategy. """
    openai.api_key = credentials.get("api_key")
    response = openai.responses.create(
        model=model_name,
        instructions="You are a helpful assistant that provides information about the topic.",
        input=prompt,
        temperature=0.7    )
    return response