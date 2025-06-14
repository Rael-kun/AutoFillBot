from docx import Document

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

        if placeholder in paragraph.text:
            paragraph.text = paragraph.text.replace(placeholder, answers[index])
            index += 1

    # once all finished, save
    doc.save(output_name)