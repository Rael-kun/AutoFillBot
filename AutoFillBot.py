from FillInWord import fill_in_word
from FillInWord import grab_sections
from FillInWord import grab_n_shot
import GPTManager
from TeamsTranscript import vtt_to_txt

# This uses our questions doc to fill out information. If false, model will use context
# from the text before the answer to generate a response (may perform worse, but will be a
# LOT more hands-off for generation)
use_questions = False
# If this is true, uses num_examples of the n_shot examples defined in FillInWord.py. These
# examples can enhance the performance of this bot substantially, and help the bot figure out
# the format you want it to respond in. If false, no examples will be used, and you can leave
# the n_shot_doc_name as None.
use_n_shot = False
num_examples = 3

transcript_name = r"C:\Users\DSU\Research\GPTDOCs\Meeting with Weir, Nickolas.vtt"
questions_name = r"C:\Users\DSU\Research\GPTDOCs\AutoFillBot\questions.txt"
word_doc_name = r"C:\Users\DSU\Research\GPTDOCs\AutoFillBot\AppleDoc.docx"
n_shot_doc_name = r"C:\Users\DSU\Research\GPTDOCs\AutoFillBot\N_shot_examples.docx"
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
    
    n_shot_examples = ""
    if(use_n_shot):
        n_shot_examples = "Here are some examples of sections you may see and how you should respond:" + grab_n_shot(n_shot_doc_name, num_examples)
    
    sys_prompt = {"role": "system", "content": base_prompt + transcript + n_shot_examples}
    gptManager.chat_history.append(sys_prompt)

    # Step 3: Now run GPT and get back answers
    for question in questions:
        answer = gptManager.chat(question)
        answers.append(answer)


    # Step 4: With answers, replace in word document
    fill_in_word(word_doc_name, output_name, answers)

    # Step 5: Profit

elif __name__ == "__main__" and not use_questions:
    # Step 0: Load our GPT and any other variables
    gptManager = GPTManager.GPTManager()

    questions = grab_sections(word_doc_name)
    answers = []

    # Step 1: Save transcript as text
    transcript = vtt_to_txt(transcript_name)

    # Step 2: Configure system prompt
    base_prompt = """You are an assistant that completes sections of a document using only the 
    provided interview transcript. For each section, use the transcript to fill in missing responses, 
    answer questions, or elaborate naturally on the text. Do not use outside knowledge. Keep 
    responses brief: 1–2 sentences or up to 3 bullet points. Use the tone and language of the 
    transcript. Do not invent information. Only include information clearly found or reasonably 
    inferred from the transcript. If no relevant info is found, respond with: "No relevant 
    information found in transcript. Here is the transcript:\n"""

    n_shot_examples = ""
    if(use_n_shot):
        n_shot_examples = "Here are some examples of sections you may see and how you should respond:" + grab_n_shot(n_shot_doc_name, num_examples)
    
    sys_prompt = {"role": "system", "content": base_prompt + transcript + n_shot_examples}
    gptManager.chat_history.append(sys_prompt)

    # Step 3: Now run GPT and get back answers
    for question in questions:
        answer = gptManager.chat(question)
        answers.append(answer)

    # Step 4: With answers, replace in word document
    fill_in_word(word_doc_name, output_name, answers)

    # Step 5: Wowee look at those profits rise :O