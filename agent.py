
from langchain import OpenAI, LLMChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.agents import ConversationalAgent, AgentExecutor
import prompt
import tools
import os
import random
from dotenv import load_dotenv


class WayfarerAIAgent():
    def __init__(self, debug=False, memory_window=None):
        print("Initializing Wayfarer AI Agent...")
        load_dotenv()
        self.debug = debug
        self.memory_window = memory_window
        self.agent = self._setup_agent()

    def _setup_agent_memory(self):
        if self.memory_window == None:
            memory = ConversationBufferMemory(memory_key="chat_history", ai_prefix=prompt.AI_PREFIX)
        else:
            memory = ConversationBufferWindowMemory(memory_key="chat_history", ai_prefix=prompt.AI_PREFIX, k=self.memory_window)
        return memory

    def _setup_agent(self):
        agent_prompt = ConversationalAgent.create_prompt(
            prefix=prompt.AGENT_PROMPT_PREFIX, 
            tools=tools.tools, 
            ai_prefix=prompt.AI_PREFIX
        )

        model = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0)
        llm_chain = LLMChain(llm=model, prompt=agent_prompt)

        agent = ConversationalAgent(
            llm_chain=llm_chain,
            tools=tools.tool_names,
            verbose=self.debug,
        )

        memory = self._setup_agent_memory()

        agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools.tools, verbose=self.debug, memory=memory)

        return agent_executor

    def _reply_user(self, user_input):
        return self.agent.run(user_input)
    
    def _format_reply(self, reply):
        return f"{prompt.AI_PREFIX}: {reply}"
    
    def chat(self):
        print(self._format_reply(prompt.GREETING_MSG))
        try:
            while True:
                user_input = input("\nUser: ")
                if user_input == "exit":
                    print(self._format_reply("Exiting..."))
                    break
                elif user_input == "refresh":
                    self.refresh_agent_memory()
                else:
                    print(self._format_reply(self._reply_user(user_input)))
        except KeyboardInterrupt:
            print(f"{prompt.AI_PREFIX}: Exiting...")
        

    def refresh_agent_memory(self):
        self.agent.memory.clear()
        refresh_message = random.choice(prompt.REFRESH_MESSAGES)
        print(self._format_reply(refresh_message))
    
    