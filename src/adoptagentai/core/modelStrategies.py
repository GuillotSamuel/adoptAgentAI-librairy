import openai

def gpt_4o_base_strategy(model_name,
                         prompt,
                         credentials,
                         instructions="You are a helpful assistant that provides information about the topic.",
                         temperature=0.7,
                         max_completion_tokens=None,
                         n=1, 
                         stop=None,
                         presence_penalty=0,
                         frequency_penalty=0,
                         top_p=1.0,
                         logprobs=None,
                         user=None,
                         reasoning_effort="medium",
                         response_format=None,
                         tool_choice="auto", 
                         service_tier="auto",
                         seed=None,
                         stream=False,
                         store=False,
                         logit_bias=None, 
                         parallel_tool_calls=True):
    """ GPT-4 OpenAI base strategy. """
    openai.api_key = credentials.get("api_key")
    response = openai.responses.create(
        model=model_name,
        instructions=instructions,
        input=prompt,
        temperature=temperature,
        # max_completion_tokens=max_completion_tokens,
        # n=n,
        # stop=stop,
        # presence_penalty=presence_penalty,
        # frequency_penalty=frequency_penalty,
        # top_p=top_p,
        # logprobs=logprobs,
        # user=user,
        # reasoning_effort=reasoning_effort,
        # response_format=response_format,
        # tool_choice=tool_choice,
        # service_tier=service_tier,
        # seed=seed,
        # stream=stream,
        # store=store,
        # logit_bias=logit_bias,
        # parallel_tool_calls=parallel_tool_calls
    )
    return response

def gpt_4o_strategy(model_name, prompt, credentials, **kwargs):
    """ GPT-4 OpenAI strategy. """
    return gpt_4o_base_strategy(
        model_name=model_name,
        prompt=prompt,
        credentials=credentials,
        instructions="You are a helpful assistant that provides information about the topic.",
        **kwargs
    )

def gpt_4o_mini_strategy(model_name, prompt, credentials, **kwargs):
    """ GPT-4 mini OpenAI strategy. """
    return gpt_4o_base_strategy(
        model_name=model_name,
        prompt=prompt,
        credentials=credentials,
        instructions="You are a helpful assistant that provides concise and accurate information.",
        temperature=0.5,
        max_completion_tokens=500,
        **kwargs
    )

