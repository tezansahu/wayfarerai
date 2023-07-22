from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain import HuggingFaceHub
import os
from dotenv import load_dotenv
import prompt
import utils

def setup_model():
    load_dotenv()
    huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']
    repo_id = "tiiuae/falcon-7b-instruct"
    model = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token, repo_id=repo_id, model_kwargs={"temperature":0.1, "max_new_tokens":500, "eos_token_id": 11})
    return model

def chat(llm):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        human_prefix="User",
        ai_prefix="Wayfarer AI"
    )

    llm_chain = LLMChain(
        prompt=prompt.prompt,
        llm=llm,
        verbose=False,
        memory=memory,
    )

    while True:
        human_msg = input("User: ")
        model_response = llm_chain.predict(human_msg=human_msg)
        processed_model_response = utils.process_model_response(model_response)

        llm_chain.memory.chat_memory.messages.pop()
        llm_chain.memory.chat_memory.add_ai_message(processed_model_response)

        print("Wayfarer AI: ", processed_model_response)

def main():
    falcon_model = setup_model()
    chat(falcon_model)

if __name__ == "__main__":
    main()