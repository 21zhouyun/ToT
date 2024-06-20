import pandas as pd
import heapq
import game24_prompts
import re
import model

class Game24():
    def __init__(self):
        self.client = model.GPT()

    def extract_proposal(self, content):
        proposal = ""
        left = ""

        splitted = content.split("(")
        if len(splitted) < 2:
            return proposal, left
        
        proposal = splitted[0]

        # Extract what's left
        pattern = r'\(left:\s*(.*?)\)'
        match = re.search(pattern, content)
        if match:
            left = match.group(1)
        
        return proposal, left

    def generate_proposals(self, puzzle):
        prompt = game24_prompts.propose_prompt.format(input=puzzle)
        contents = self.client.call(prompt, n=1)
        content = contents[0]

        proposals = []
        next_states = []
        for item in content.split("\n"):
            proposal, left = self.extract_proposal(item)
            if len(proposal) > 0 and len(left) > 0:
                proposals.append(proposal)
                next_states.append(left)

        return proposals, next_states

    def evaluate(self, proposal):
        prompt = game24_prompts.value_prompt.format(input=proposal)

        score = 0 
        score_map = {'impossible': 0.001, 'likely': 1, 'sure': 20} # From official implementation
        contents = self.client.call(prompt, n=3)
        for content in contents:
            name = content.split("\n")[-1]
            if name in score_map:
                score += score_map[name]

        return score

# task = Game24()
# print(task.generate_proposals("3 3 6 10"))
# print(task.extract_proposal("3 + 3 = 6 (left: 6 6 10)"))
# print(task.evaluate("6 6 10"))