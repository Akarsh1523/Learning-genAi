import tiktoken
encoder = tiktoken.encoding_for_model("gpt-4o")
print(encoder.n_vocab)

text = "The cat sat on the mat"
text2 = "The mat sat on the cat"

tokens = encoder.encode(text)
tokens2 = encoder.encode(text2)

print("Tokens :", tokens)
print("Tokens :", tokens2)



