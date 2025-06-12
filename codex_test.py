import openai
import os

# Safe way - using environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    model="code-davinci-002",
    prompt="### כתוב פונקציה שמחשבת את סכום המספרים מ־1 עד 100",
    max_tokens=100,
    temperature=0
)

print("💡 תשובה מ־Codex:")
print(response.choices[0].text.strip())