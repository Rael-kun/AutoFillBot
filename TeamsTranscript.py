import re

def vtt_to_txt(vtt_file, txt_file=None):
    # regex to match <v Name> Spoken words </v>
    speaker_pattern = re.compile('<v\\s+([^>]+)>(.*?)</v>', re.DOTALL)
    # regex to match identifying id's that are hexidecimal and end with a chunk number
    id_pattern = re.compile('^[a-f0-9\\-]+/\\d+-\\d+$', re.IGNORECASE)
    # regex to match timestamp information
    timestamp_pattern = re.compile('^\\d+:\\d+:\\d+\\.\\d+ --> \\d+:\\d+:\\d+\\.\\d+$')

    output = []

    with open(vtt_file, 'r', encoding='utf-8') as f:
        transcript = f.read()

    # grab each block (seperated by two newlines), only grab blocks with timestamps
    blocks = transcript.strip().split('\n\n')

    last_speaker = None

    for block in blocks:
        # remove useless lines within block
        lines = [line for line in block.split('\n') if (not id_pattern.match(line) and not timestamp_pattern.match(line))]
        if(not lines):
            # empty
            continue
        text_block = ' '.join(lines).strip()

        # verify that it is proper speaking pattern
        match = speaker_pattern.search(text_block)

        if(match):
            # grab both parts
            speaker, speech = match.groups()
            speaker = speaker.strip()
            if(',' in speaker):
                parts = [p.strip() for p in speaker.split(',')]
                # first and last name reversed in transcript
                speaker = f'{parts[1]} {parts[0]}'
            # safety check so I don't go insane
            speech = speech.replace('\n', ' ').strip()

            if(speaker == last_speaker):
                # keep going (RAG may want frequent breaks to remind who is speaking, fix this later future me)
                # I totally won't forget to fix this lmao
                output[-1] += ' ' + speech
            else:
                # new speaker, append to later seperate them and update last speaker
                output.append(f'{speaker}: {speech}')
                last_speaker = speaker

    if(txt_file == None):
        # send directly to next step
        return '\n\n'.join(output)
    else:
        # save to file
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(output))

# test case
if __name__ == '__main__':
    transcript_name = r'C:\Users\DSU\Research\GPTDOCs\Meeting with Weir, Nickolas.vtt'
    output_name = 'transcript_clean.txt'
    vtt_to_txt(transcript_name, output_name)