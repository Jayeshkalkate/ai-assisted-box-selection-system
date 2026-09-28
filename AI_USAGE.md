# AI Usage

## 1. Tools used
- **ChatGPT:** research. I used it to understand the assignment in depth:
  what to do, what not to do, and why.
- **Claude:** I used it to generate the project files from the instructions
  I took from ChatGPT's explanation.

## 2. Prompts I gave
- ChatGPT: "With the shared docx, explain me everything about the assignment."
- Claude: "As per the given instructions, give me a zip file of the project."

## 3. Output I accepted
- ChatGPT: the explanation was very detailed. I only used the tech stack,
  the features and the project requirements.
- Claude: the project zip. Building it took a long time and reached the usage
  limit, so I added a prompt asking for the zip before the limit was reached,
  and it answered faster.

## 4. Output I rejected or modified
- ChatGPT gave explanations, code and examples. I filtered them and kept
  only the information I needed.
- Claude: after extracting the zip I found things missing ([.env, .gitignore,
  requirements.txt]). I created them myself. [If you removed anything
  unnecessary from the zip, name the file and what you removed.]
- I renamed the project package to `box_selector` and changed `settings.py`
  to read the secret key, debug flag and allowed hosts from environment
  variables.

## 5. Mistakes the AI made
- Claude sometimes did more than I asked and gave much more output than
  needed.
- The first zip did not include .env, .gitignore or requirements.txt.

## 6. How I verified the final code
- I reviewed the files and functions, using my own notes and documents to
  understand the stack.
- I ran `python manage.py check` and `python manage.py check --deploy`.
- I ran `python manage.py test -v 2`, output in TEST_OUTPUT.md.
