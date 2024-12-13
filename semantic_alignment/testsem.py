from openai import OpenAI
from prompts import semantic_normalization_prompt, snp, snp2
import ast

client = OpenAI(api_key="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")
ylist = ['Deep Learning', 'DL', 'Deep learning (DL)']
xlist = ['NLP', 'natural language processing', 'natural language processing (NLP)', 'Deep Learning', 'DL', 'Deep learning (DL)', 'activation functions', 'tanh']
# zlist = xlist.append(ylist)
prompt = snp2.format(xlist)





completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]
)

y = completion.choices[0].message.content
z = ast.literal_eval(y)
print(type(z))

# temp = completion.choices[0].text
# print(temp)

# print(a.choices[0].text)