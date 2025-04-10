import google.generativeai as genai


genai.configure(api_key="AIzaSyA4X0YqDg_KUIhLRlryHXaBi9zSW2pUxMI")

def ask_gemini(prompt):
    try:

        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error using the Gemini API: {e}"

if __name__ == "__main__":
    prompt = input("What do you want to ask Gemini? ")
    response = ask_gemini(prompt)
    print("\n Gemini's Response:")
    print(response)
