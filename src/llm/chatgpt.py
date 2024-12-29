import openai

class ChatGPT:
    def __init__ (self, api_key):
        openai.api_key = api_key

    def question(self, prompt, model="gpt-4", temperature=0.7, max_tokens=200):
        """
        Calls GPT-4 API with the given prompt.

        :param prompt: The input text you want GPT-4 to respond to.
        :param model: The model to use (default is gpt-4).
        :param temperature: Creativity level of the response (default is 0.7).
        :param max_tokens: Maximum tokens for the response (default is 200).
        :return: The response text from GPT-4.
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a cryptocurrency financial expert specializing in providing reliable advice based on charts and key metrics. Share your insights to guide people in making informed decisions about their investments in the crypto market."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            # Extract the response content
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    prompt = "show hahaha"
    api_key  = ""
    chatgpt = ChatGPT(api_key)
    response = chatgpt.question(prompt)
    print("GPT-4's Response:")
    print(response)

