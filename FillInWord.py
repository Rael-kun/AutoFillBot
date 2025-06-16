from docx import Document
import re

def fill_in_word(doc_name, output_name, answers):
    """
    Takes in a word doc and an array of answers, filling
    in the responses into the doc. Right now, fills the answers
    into the [Answer X] boxes
    """
    doc = Document(doc_name)

    index = 0

    # cycle through each paragraph, replacing if [Answer X] is in it
    for paragraph in doc.paragraphs:
        placeholder = f'[Answer {index + 1}]'

        if(placeholder in paragraph.text):
            paragraph.text = paragraph.text.replace(placeholder, answers[index])
            index += 1

    # once all finished, save
    doc.save(output_name)


def grab_sections(doc_name):
    """
    Take in a word doc and grabs the sections preceding each answer.
    These sections can be used within prompt to enhance the retrieval.
    """
    doc = Document(doc_name)

    sections = []
    current_section = []

    # matches [Answer X] sections
    answer_pattern = re.compile(r"\[Answer\s*\d+\]", re.IGNORECASE)

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        # if empty paragraph, continue
        if(not text):
            continue

        if(answer_pattern.match(text)):
            # if answer, add current section to list of actual sections
            if(current_section):
                section_text = " ".join(current_section).strip()
                sections.append(section_text)
                current_section = []
        else:
            # if not answer, add text to current section
            current_section.append(text)

    return sections


if __name__ == "__main__":
    print(grab_sections(r"C:\Users\DSU\Research\GPTDOCs\AutoFillBot\AppleDoc.docx"))
