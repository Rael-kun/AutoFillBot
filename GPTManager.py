from openai import OpenAI
import tiktoken
from rich import print
import os
from dotenv import load_dotenv

load_dotenv("keys.env")
# API Key here
gpt_key = os.getenv("GPT_KEY")
print("Loaded key:", gpt_key is not None) 

class GPTManager:
    def __init__(self):
        # probably don't need context of other responses outside of a few continuation cases
        self.message_limit = 11 # keep 11-1 unique messages (since system message always kept), prompt and response count as a message each so 5 back and forth scenarios
        self.chat_history = []
        # open API
        try:
            self.client = OpenAI(api_key=gpt_key)
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


        print("[yellow]Prompting GPT...")
        response = self.client.chat.completions.create(model="gpt-4o", messages=self.chat_history)

        # Append response to the chat history
        self.chat_history.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})

        # Display answer to user
        answer = response.choices[0].message.content
        print(f"[green]\n{answer} \n")
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



