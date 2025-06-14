from FillInWord import fill_in_word
import GPTManager
from TeamsTranscript import vtt_to_txt

# This uses our questions doc to fill out information. If false, model will use context
# from the text before the answer to generate a response (may perform worse, but will be a
# LOT more hands-off for generation)
use_questions = True

transcript_name = r"C:\Users\DSU\Research\GPTDOCs\Meeting with Weir, Nickolas.vtt"
questions_name = r"C:\Users\DSU\Research\GPTDOCs\AutoFillBot\questions.txt"
word_doc_name = r"C:\Users\DSU\Research\GPTDOCs\AutoFillBot\AppleDoc.docx"
output_name = "AppleFinished.docx"

if __name__ == "__main__" and use_questions:
    # Step 0: Load our GPT and any other variables
    gptManager = GPTManager.GPTManager()

    with open(questions_name, "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip()]
    answers = []

    # Step 1: Save transcript as text
    transcript = vtt_to_txt(transcript_name)

    # Step 2: Configure system prompt
    base_prompt = """Here is a document. Answer the questions about it, in no more than one 
                sentence. Ideally, it should be a 2-4 word answer. The only exception to those rules
                 is if you are asked to do bullet points. Do not access the internet, 
                use only the information in the given document. Based only on the provided 
                transcript, extract the answer to the questions below. Here it is:\n"""
    
    sys_prompt = {"role": "system", "content": base_prompt + transcript}
    gptManager.chat_history.append(sys_prompt)

    # Step 3: Now run GPT and get back answers
    for question in questions:
        answer = gptManager.chat(question)
        answers.append(answer)

#sanity check
    with open("answers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(answers))

    # Step 4: With answers, replace in word document
    fill_in_word(word_doc_name, output_name, answers)

    # Step 5: Profit

elif __name__ == "__main__" and not use_questions:
    # add functionality here
    pass