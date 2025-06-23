from openai import OpenAI
from openai import AzureOpenAI
from rich import print
import os
from dotenv import load_dotenv

# If using_azure, then use the Azure OpenAI API as the model. Else, use ChatGPT API.
using_azure = True


load_dotenv("keys.env")
# API Key here
if(using_azure):
    api_key = os.getenv("AZURE_KEY")
    azure_endpoint = "https://azureapi-test.openai.azure.com/"
else:
    api_key = os.getenv("GPT_KEY")
print("Loaded key:", api_key is not None) 

# model to use (I have gpt-4o and gpt-4o-mini configured)
model = "gpt-4o-mini"

class GPTManager:
    def __init__(self):
        # probably don't need context of other responses outside of a few continuation cases
        self.message_limit = 11 # keep 11-1 unique messages (since system message always kept), prompt and response count as a message each so 5 back and forth scenarios
        self.chat_history = []
        # open API
        try:
            if(using_azure):
                self.client = AzureOpenAI(azure_endpoint=azure_endpoint, api_key=api_key, api_version="2025-04-01-preview")
            else:
                self.client = OpenAI(api_key=api_key)
        except TypeError:
            print("Error, you probably forgot the API key.")

    def chat(self, prompt=""):
        if(not prompt):
            print("Error! No prompt given!")
            return
        
        # Add prompt to history (formatted how gpt wants it)
        self.chat_history.append({"role": "user", "content": prompt})
        
        # Context not as important for this program, pop messages to avoid costs
        while(len(self.chat_history) > self.message_limit):
            self.chat_history.pop(1) # skip the system message
            print("Message removed")


        #print("[yellow]Prompting GPT...")
        response = self.client.chat.completions.create(model=model, messages=self.chat_history)

        # Append response to the chat history
        self.chat_history.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})

        # Display answer to user
        answer = response.choices[0].message.content
        #print(f"[green]\n{answer} \n")
        return answer
    
# Quick debugging test
if __name__ == "__main__":
    gptManager = GPTManager()
    
    # load document
    with open("transcript.txt", "r", encoding="utf-8") as f:
        sys_doc = f.read()
    # load all questions
    with open("questions.txt", "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip()]
    answers = []

    # create sys prompt with document
    sys_prompt = {"role": "system", "content": "Here is a document. Answer the questions about it, in no more than one sentence. Ideally, it should be a 2-4 word answer. Do not access the internet, use only the information in the given document.Based only on the provided transcript, extract the answer to the questions below. As a check for conflicting or uncertain information, include a confidence score (0–100) after each response. Here it is:\n" + sys_doc}
    print(sys_prompt)
    gptManager.chat_history.append(sys_prompt)

    for question in questions:
        answer = gptManager.chat(question)
        answers.append(answer)

    with open("answers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(answers))



