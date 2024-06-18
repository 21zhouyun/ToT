import pandas as pd
import heapq
import game24_prompts
import re
import model
import logging

logging.basicConfig(filename='task24.log', encoding='utf-8', level=logging.DEBUG)

class Game24():
    def __init__(self, data_path):
        self.client = model.GPT()
        self.data = pd.read_csv(data_path)

    def extract_proposal(self, content):
        pattern = r'\(left:\s*(.*?)\)'

        # Using re.search to find the pattern in the text
        match = re.search(pattern, content)

        # Extracting the matched content
        if match:
            result = match.group(1)
            return result
        
        return None

    def generate_one(self, puzzle):
        prompt = game24_prompts.propose_prompt.format(input=puzzle)
        contents = self.client.call(prompt, n=1)
        content = contents[0]

        proposals = []
        for item in content.split("\n"):
            proposal = self.extract_proposal(item)
            if proposal:
                proposals.append(proposal)

        return proposals

    def evaluate_one(self, proposal):
        prompt = game24_prompts.value_prompt.format(input=proposal)

        score = 0 
        score_map = {'impossible': 0.001, 'likely': 1, 'sure': 20} # From official implementation
        contents = self.client.call(prompt, n=3)
        for content in contents:
            name = content.split("\n")[-1]
            if name in score_map:
                score += score_map[name]

        return score

task = Game24("data/24.csv")
print(task.generate_one("6 4"))
# print(task.evaluate_one("6 6 10"))
# print(task.extract_proposal("3 + 3 = 6 (left: 6 6 10)"))