# This script demonstrates how to use the OpenAI API to ask a question and get a response.
# BUT unforatunately, it is not working because... "You exceeded your current quota, please check your plan and billing details." :D.

import openai

client = openai.OpenAI(api_key= "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")

def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error communicating with the API: {e}"

if __name__ == "__main__":
    question = input("Ask the AI a question: ")
    answer = ask_openai(question)
    print("\nOpenAI's Response:")
    print(answer)