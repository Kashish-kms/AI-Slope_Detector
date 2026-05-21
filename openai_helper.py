from openai import OpenAI

class OpenAIHelper:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def analyze_slop(self, text, scores):
        prompt =prompt = f"""
Act as a world-class linguistic forensic expert. 
Analyze why this text scored {scores['ai']*100}% on an AI detector.
Look specifically for 'AI Slop' markers: 
1. Overuse of transition words (e.g., 'Furthermore', 'In conclusion').
2. Lack of personal anecdotes.
3. Perfect but hollow grammar.
Text: {text[:800]}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except:
            return "OpenAI analysis unavailable."