import game24_prompts
import re
import model
import sympy

class Game24():
    def __init__(self):
        self.client = model.GPT()

    def extract_next_state(self, content):
        # Extract what's left
        pattern = r'\(left:\s*(.*?)\)'
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        
        return None

    def generate_proposals(self, puzzle):
        prompt = game24_prompts.propose_prompt.format(input=puzzle)
        contents = self.client.call(prompt, n=1)
        content = contents[0]

        proposals = []
        next_states = []
        for item in content.split("\n"):
            next_state = self.extract_next_state(item)
            if next_state is not None:
                next_states.append(next_state)
                proposals.append(item)

        return proposals, next_states

    def generate_cot_proposal(self, steps, puzzle):
        prompt = game24_prompts.cot_prompt.format(input=puzzle) + "\nSteps:" + steps
        # print(prompt)
        return self.client.call(prompt, n=1)[0]

    def evaluate(self, proposal):
        prompt = game24_prompts.value_prompt.format(input=proposal)

        score = 0 
        score_map = {'impossible': 0.001, 'likely': 1, 'sure': 20} # From official implementation
        contents = self.client.call(prompt, n=3)
        for content in contents:
            # print(content)
            name = content.split("\n")[-1].strip()
            if name in score_map:
                score += score_map[name]

        return score
    
    def test(self, result, problem):
        expression = result.lower().replace('answer: ', '').split("=")[0]

        # Make sure solution contains the right numbers
        numbers = re.findall(r'\d+', expression)
        problem_numbers = re.findall(r'\d+', problem)

        if sorted(numbers) != sorted(problem_numbers):
            return 0

        # Make sure steps are correct
        if (int(sympy.simplify(expression) == 24)):
            return 1
        
        return 0

# task = Game24()
# print(task.generate_proposals("3 3 6 10"))
# print(task.extract_proposal("3 + 3 = 6 (left: 6 6 10)"))
# print(task.evaluate("6 6 10"))
# print(task.test("Answer: (3 + 3) * (10 - 6) = 24", "3 3 6 10"))