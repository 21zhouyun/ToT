# API wrapper to openai models.

from openai import OpenAI

class GPT():
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000):
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def call(self, prompt, n=1):
        rsp = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            n=n
        )

        contents = []
        for choice in rsp.choices:
            contents.append(choice.message.content)
        return contents
    

# # TODO add llama support

# gpt = GPT()
# print(gpt.call("what's your name", n=3))