import os
import json
import random

# Built-in High-RPM Viral Scripts (Fallback or instant generation without API key)
VIRAL_TEMPLATES = [
    {
        "niche": "finance",
        "topic": "The 15/3 Credit Card Trick",
        "title": "The Secret Credit Score Hack Nobody Teaches You 💳 #Shorts #Finance",
        "description": "How the 15/3 payment rule keeps your credit utilization below 10% and boosts your credit score.\n\n📌 Free Credit Building Checklist in Bio!\n#creditscore #moneyhacks #personalfinance",
        "pinned_comment": "💳 Grab the free 0% interest card masterlist linked in my bio!",
        "voiceover_text": "If you pay your credit card bill on the due date, you are quietly hurting your credit score. Banks don't report your balance on your due date. They report it on your statement closing date. That means if your limit is one thousand dollars and you spend five hundred, your utilization is reported as fifty percent, which tanks your score. Instead, use the fifteen-three trick. Pay half fifteen days before your statement, and the rest three days before. Your score will skyrocket. Follow for more money secrets.",
        "search_keywords": ["credit card luxury", "counting money", "bank building", "stock market chart", "smartphone banking"]
    },
    {
        "niche": "finance",
        "topic": "The Rule of 72",
        "title": "How to Double Your Money Fast (The Rule of 72) 📈 #Shorts #Investing",
        "description": "The simple mental math trick billionaires use to calculate when their money doubles.\n\n📊 Free Net Worth Tracker in Bio!\n#wealthmindset #compoundinterest #investing101",
        "pinned_comment": "📈 Download the free beginner investing spreadsheet linked in my bio!",
        "voiceover_text": "Most people have no idea how long it takes to double their money. Billionaires use one simple mental math rule. It is called the Rule of 72. Take the number 72 and divide it by your annual interest rate. If your money sits in an ordinary bank account earning half a percent, it will take one hundred and forty-four years to double. But put that money into the S&P 500 averaging ten percent, and your wealth doubles every seven point two years. Let compound interest do the work. Free guide in bio.",
        "search_keywords": ["luxury clock ticking", "skyscrapers city", "vault gold bars", "stock market graph", "success businessman"]
    },
    {
        "niche": "tech_ai",
        "topic": "Secret AI Research Tool",
        "title": "This Free Google AI Feels Illegal to Know 🤖 #Shorts #AITools",
        "description": "Turn any 50-page PDF or textbook into a 2-minute podcast summary with Google NotebookLM.\n\n⚡ 40+ Secret AI Tools in Bio!\n#aitools #productivity #studenthacks #techhacks",
        "pinned_comment": "🤖 Grab the free 40+ AI Tools Cheat Sheet linked in my bio!",
        "voiceover_text": "If you are still reading 50-page PDFs or study guides manually in 2026, stop right now. Go to NotebookLM by Google. It is completely free. Upload any textbook, dense research paper, or business report. With one click, it creates an interactive two-person audio podcast explaining the entire document in plain English. You can even ask it questions and it cites the exact page numbers. Comment the word AI and I will send you twenty more secret tools.",
        "search_keywords": ["typing on laptop", "cyberpunk digital matrix", "artificial intelligence brain", "robot glowing tech", "modern office desk"]
    }
]

def generate_script(niche: str = "finance", api_key: str = None) -> dict:
    """Generates a structured video script via Gemini API or viral templates."""
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            Write an ultra-viral 30-second YouTube Short script in the {niche} niche.
            Must have:
            1. Shocking 3-second hook that stops scrolling immediately.
            2. High-value educational meat with rapid pacing (110-140 words max).
            3. Clear Call to Action for the bio link.
            4. 4-5 visual search keywords for 9:16 stock footage.
            
            Respond strictly in valid JSON format with keys:
            "title", "description", "pinned_comment", "voiceover_text", "search_keywords"
            """
            response = model.generate_content(prompt)
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:-3].strip()
            elif clean_text.startswith("```"):
                clean_text = clean_text[3:-3].strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"[Warning] AI generation fallback triggered: {e}")
            
    # Filter templates by niche or pick random
    filtered = [t for t in VIRAL_TEMPLATES if t["niche"] == niche]
    if not filtered:
        filtered = VIRAL_TEMPLATES
    return random.choice(filtered)

if __name__ == "__main__":
    script = generate_script("finance")
    print(json.dumps(script, indent=2))
