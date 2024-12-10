import openai
import os
import time
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

azure_deployment_model=os.environ['AZURE_DEPLOYMENT_MODEL']

azure_client = AzureOpenAI(
    azure_deployment = azure_deployment_model,
    api_key = os.environ['AZURE_OPENAI_API_KEY'],
    azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT'],
    api_version = os.environ['AZURE_OPENAI_API_VERSION'],
   )

# OpenAI or AzureOpenAI completion client
Completion_Obj = azure_client.chat.completions if os.environ['AZURE_OPENAI_ENDPOINT'] else openai.ChatCompletion


os.environ["OPENAI_API_KEY"] = os.environ["YUFEI_OPENAI_API_KEY"] # put your api key here
def query(system, user_contents, assistant_contents, model='gpt-4', save_path=None, temperature=1, debug=False):
    
    if 'gpt' in model and '4' in model:
        model =  azure_deployment_model if azure_deployment_model else 'gpt-4'    
    for user_content, assistant_content in zip(user_contents, assistant_contents):
        user_content = user_content.split("\n")
        assistant_content = assistant_content.split("\n")
        
        for u in user_content:
            print(u)
        print("=====================================")
        for a in assistant_content:
            print(a)
        print("=====================================")

    for u in user_contents[-1].split("\n"):
        print(u)

    if debug:
        import pdb; pdb.set_trace()
        return None

    print("=====================================")

    start = time.time()
    
    num_assistant_mes = len(assistant_contents)
    messages = []

    messages.append({"role": "system", "content": "{}".format(system)})
    for idx in range(num_assistant_mes):
        messages.append({"role": "user", "content": user_contents[idx]})
        messages.append({"role": "assistant", "content": assistant_contents[idx]})
    messages.append({"role": "user", "content": user_contents[-1]})

    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = Completion_Obj.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    result = ''
    for choice in response.choices: 
        result += choice.message.content 

    end = time.time()
    used_time = end - start

    print(result)
    if save_path is not None:
        with open(save_path, "w") as f:
            json.dump({"used_time": used_time, "res": result, "system": system, "user": user_contents, "assistant": assistant_contents}, f, indent=4)

    return result

