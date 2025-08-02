import re

def parse_questions(text):
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    questions = []
    current = {}
    question_text = []

    for line in lines:
        if re.match(r"^\d+\.", line) or ('?' in line and not current):
            if current:
                current['question'] = " ".join(question_text)
                questions.append(current)
                current = {}
                question_text = []
            current['answers'] = []
            question_text.append(line)
        elif re.match(r"^[A-Da-d]\.", line):
            ident = line[0].upper()
            answer = line[2:].strip()
            current['answers'].append((ident, answer))
        else:
            if current and not current.get('answers'):
                question_text.append(line)

    if current and 'answers' in current:
        current['question'] = " ".join(question_text)
        current['correct'] = current['answers'][0][0] if current['answers'] else "A"
        questions.append(current)

    return questions
