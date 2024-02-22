import autogen 

config_list_mistral = [
    {
        'base_url': "http://localhost:8000",
        'api_key': "NULL",
        'model': 'mistral'  # Specify the model name here
    }
]

config_list_codellama = [
    {
        'base_url': "http://localhost:2821",
        'api_key': "NULL",
        'model': 'codellama'  # Specify the model name here
    }
]

llm_config_mistral={
    "config_list": config_list_mistral,
}

llm_config_codellama={
    "config_list": config_list_codellama,
}

assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=llm_config_mistral
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config_mistral,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task="""
write me a snake game in python with a gui and then the user_proxy agent should run the script
"""

user_proxy.initiate_chat(coder, message=task)

groupchat = autogen.GroupChat(agebts=[assistant, coder, user_proxy],message=[],max_rounds=12)
manager = autogen.GroupChatManager(groupchat=groupchat,llm_config_llama=llm_config_mistral)
user_proxy.initiate_chat(manager, message=task)
