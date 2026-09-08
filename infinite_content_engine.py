import os
import sys
import json
import random
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def clean_str(val):
    if isinstance(val, str):
        try:
            return val.encode("utf-16", "surrogatepass").decode("utf-16")
        except Exception:
            return val
    elif isinstance(val, list):
        return [clean_str(x) for x in val]
    elif isinstance(val, dict):
        return {k: clean_str(v) for k, v in val.items()}
    return val

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_JSON = os.path.join(BASE_DIR, "dynamic_catalog.json")

# Rich blueprint categories and viral topic formulas for infinite wealth topics
TOPIC_TEMPLATES = [
    {
        "category": "Credit Hack",
        "region": "GLOBAL",
        "title_template": "The {multiplier} Credit Card Glitch Credit Bureaus Hate 💳📉 #Shorts",
        "sub": "How to legally manipulate your credit profile to unlock top-tier cards",
        "c1_t": "THE UTILIZATION REPORTING ERROR",
        "c1_d": "Most people spend 40% of their limit and wonder why their score drops. Bureaus calculate utilization on the STATEMENT DATE, not the due date.",
        "b1": "warning",
        "c2_t": "THE ZERO-BALANCE RESET METHOD",
        "c2_d": "Step 1: Pay 80% of balance 5 days before statement closing.\nStep 2: Let only 1% to 3% report on the statement.\nStep 3: Pay the rest on the actual due date.",
        "b2": "card",
        "c3_t": "THE PAYOFF: +45 TO +85 POINT JUMP",
        "c3_d": "Unlocks 0% APR business lines of credit\nSaves $15,000+ on home mortgage interest.",
        "b3": "growth",
        "voice": "en-US-ChristopherNeural",
        "script": "Here is the credit card glitch that credit bureaus do not want you to know. If you are paying your bill on the due date, you are already too late. Bureaus snapshot your balance on the statement closing date. If you spend forty percent of your limit, your score tanks by fifty points. Instead, pay eighty percent of your card five days before your statement closes. Leave only two percent to report, then pay the rest on the due date. Your score will jump fifty points in thirty days. Subscribe to The Wealth Blueprint for daily banking loopholes."
    },
    {
        "category": "Banking Loophole",
        "region": "INDIA",
        "title_template": "The Auto-Sweep Bank Glitch (Earn {rate}% on Checking) 🏦💸 #Shorts",
        "sub": "How to turn a lazy zero-interest savings account into an automatic money maker",
        "c1_t": "THE 2.5% SAVINGS ACCOUNT TRAP",
        "c1_d": "Commercial banks keep your money in standard savings accounts earning 2.5% while inflation is 6%. You are silently losing purchasing power every month.",
        "b1": "warning",
        "c2_t": "THE AUTO-SWEEP FD CONVERSION",
        "c2_d": "Step 1: Enable Auto-Sweep Facility in your net banking.\nStep 2: Set threshold limit to ₹25,000.\nStep 3: Any surplus auto-converts to 7.2% FD while remaining 100% liquid for UPI.",
        "b2": "vault",
        "c3_t": "THE PAYOFF: ₹12,000+ FREE CASH FLOW",
        "c3_d": "Earn fixed-deposit interest with zero lock-in.\nInstant withdrawal via ATM and UPI without breaking penalties.",
        "b3": "money",
        "voice": "en-IN-PrabhatNeural",
        "script": "If you keep more than twenty five thousand rupees in your bank account, you are losing money to inflation every day. Regular savings accounts only give you two point five percent interest. But if you log into your banking app and enable the auto-sweep facility, every rupee above your threshold automatically converts into a seven percent fixed deposit. When you scan a UPI code or use your debit card, it liquidates instantly with zero penalty. You get high FD returns with complete liquidity. Follow The Wealth Blueprint for more zero BS financial hacks."
    },
    {
        "category": "Tax Shield",
        "region": "GLOBAL",
        "title_template": "How to Write Off Your {asset} as a Business Expense 🏛️💼 #Shorts",
        "sub": "The legal tax loophole self-employed people and creators use to slash taxes",
        "c1_t": "PAYING WITH AFTER-TAX DOLLARS",
        "c1_d": "W2 employees earn, pay 30% taxes first, and spend what remains. Wealthy business owners spend first, deduct expenses, and pay tax only on the net profit.",
        "b1": "warning",
        "c2_t": "THE SECTION 179 WRITE-OFF",
        "c2_d": "Step 1: Form a clean LLC entity with dedicated business bank account.\nStep 2: Purchase equipment, software, or qualifying vehicle used 50%+ for business.\nStep 3: Deduct 100% of purchase price in Year 1.",
        "b2": "card",
        "c3_t": "THE PAYOFF: $6,000 TO $15,000 TAX SAVINGS",
        "c3_d": "Legally lowers your taxable income bracket.\nAccelerates business growth capital.",
        "b3": "bull",
        "voice": "en-US-ChristopherNeural",
        "script": "Here is why the rich legally pay less taxes than the middle class. Most people earn money, pay taxes first, and live on what is left. Business owners earn money, spend on business expenses first, and only pay taxes on what remains. If you create content or run any side hustle, your phone, laptop, home office, and software can be deducted under Section 179. Every dollar written off is thirty cents back in your pocket. Follow The Wealth Blueprint for daily wealth building strategies."
    },
    {
        "category": "Compound Growth",
        "region": "INDIA",
        "title_template": "The ₹{sip_amount}/Month SIP Formula That Creates ₹1 Crore 📈🚀 #WealthShorts",
        "sub": "The exact timeline and return rate needed to build life-changing wealth on autopilot",
        "c1_t": "THE WAITING FOR A WINDFALL TRAP",
        "c1_d": "90% of people delay investing because they think they need lakhs to start. Delaying by just 5 years cuts your final compound corpus in half.",
        "b1": "warning",
        "c2_t": "THE STEP-UP INDEX SIP BLUEPRINT",
        "c2_d": "Step 1: Start ₹5,000/mo in a broad Nifty 50 or Flexi-Cap Index Fund.\nStep 2: Turn on 10% annual Step-Up SIP (increase with your salary raise).\nStep 3: Reinvest all dividends automatically.",
        "b2": "growth",
        "c3_t": "THE PAYOFF: ₹1.28 CRORES CORPUS",
        "c3_d": "Total invested: ₹38 Lakhs.\nWealth created from pure compound interest: ₹90 Lakhs+.",
        "b3": "money",
        "voice": "en-IN-PrabhatNeural",
        "script": "You do not need a huge salary to become a crorepati. If you start an SIP of just five thousand rupees per month in a Nifty index fund and increase it by ten percent every year as your income grows, compound interest will turn your thirty eight lakh investment into one point two eight crores. Over seventy percent of that final wealth comes from pure compound growth, not your pocket. Stop waiting to start. Follow The Wealth Blueprint for daily financial truth."
    },
    {
        "category": "AI Money Workflow",
        "region": "GLOBAL",
        "title_template": "The 3 AI Tools That Replace a $5,000/Month Agency 🤖⚡ #AIProductivity",
        "sub": "How solo operators and small businesses automate content and client delivery",
        "c1_t": "PAYING EXPENSIVE AGENCY RETAINERS",
        "c1_d": "Traditional marketing agencies charge $3,000 to $10,000 monthly for copy, slide decks, and basic research that modern AI models execute in seconds.",
        "b1": "warning",
        "c2_t": "THE TRI-AI STACK FOR SOLO FOUNDERS",
        "c2_d": "Tool 1: Perplexity AI for research with live source citations.\nTool 2: Claude 3.5 Sonnet for high-converting sales copywriting.\nTool 3: Gamma App for interactive 15-slide pitch presentations.",
        "b2": "card",
        "c3_t": "THE PAYOFF: 90% TIME & COST REDUCTION",
        "c3_d": "Produce executive-grade presentations in 5 minutes.\nSave $60,000 annually on freelance and agency fees.",
        "b3": "vault",
        "voice": "en-US-ChristopherNeural",
        "script": "Stop paying agencies thousands of dollars a month for basic work. With three free AI tools, you can replace an entire marketing team. Use Perplexity AI for deep market research with real-time citations. Use Claude for drafting client proposals and persuasive sales emails. And use Gamma to turn any text prompt into a gorgeous fifteen-slide deck in under thirty seconds. Work smarter, not harder. Follow The Wealth Blueprint for daily AI and financial productivity shortcuts."
    }
]

def init_dynamic_catalog():
    """Initializes dynamic_catalog.json from CATALOG_100 if it does not exist."""
    if not os.path.exists(CATALOG_JSON):
        try:
            from content_catalog_100 import CATALOG_100
            cleaned_catalog = clean_str(CATALOG_100)
            with open(CATALOG_JSON, "w", encoding="utf-8") as f:
                json.dump(cleaned_catalog, f, indent=2, ensure_ascii=False)
            print(f">> Initialized dynamic catalog with {len(cleaned_catalog)} posts.")
        except Exception as e:
            print(f"[!] Error loading CATALOG_100: {e}")
            with open(CATALOG_JSON, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

def load_dynamic_catalog():
    init_dynamic_catalog()
    try:
        with open(CATALOG_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_dynamic_catalog(catalog):
    with open(CATALOG_JSON, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

def generate_and_append_new_post():
    """Synthesizes a brand new high-retention post and appends it to dynamic_catalog.json."""
    catalog = load_dynamic_catalog()
    current_count = len(catalog)
    new_id = current_count + 1

    # Calculate day and slot
    new_day = (new_id + 1) // 2
    new_slot = 1 if (new_id % 2 != 0) else 2

    # Pick a creative template
    template = random.choice(TOPIC_TEMPLATES)

    # Contextual dynamic replacements
    multipliers = ["15/3", "10/2", "30-Day", "21-Day", "2-Step"]
    rates = ["7.5", "7.2", "8.1", "7.8"]
    assets = ["MacBook & Phone", "Vehicle & Home Office", "Camera & Studio Setup", "Software & Subscriptions"]
    sips = ["5,000", "10,000", "15,000", "7,500"]

    title = template["title_template"].format(
        multiplier=random.choice(multipliers),
        rate=random.choice(rates),
        asset=random.choice(assets),
        sip_amount=random.choice(sips)
    )

    new_item = {
        "id": new_id,
        "day": new_day,
        "slot": new_slot,
        "region": template["region"],
        "category": template["category"],
        "title": title,
        "sub": template["sub"],
        "c1_t": template["c1_t"],
        "c1_d": template["c1_d"],
        "b1": template["b1"],
        "c2_t": template["c2_t"],
        "c2_d": template["c2_d"],
        "b2": template["b2"],
        "c3_t": template["c3_t"],
        "c3_d": template["c3_d"],
        "b3": template["b3"],
        "voice": template["voice"],
        "script": template["script"],
        "tags": ["wealth", "finance", "moneyhacks", "creditcard", "investing", "banking", "shorts", "reels"],
        "pinned_comment": "Which step in this blueprint was new to you? Comment below and we will send you our 0% Interest Card Masterlist!"
    }

    catalog.append(new_item)
    save_dynamic_catalog(catalog)
    print(f">> [INFINITE ENGINE] Synthesized and queued Post #{new_id:03d}: '{title}' (Day {new_day} Slot {new_slot})")
    return new_item

if __name__ == "__main__":
    init_dynamic_catalog()
    new_post = generate_and_append_new_post()
    print("New post created:", json.dumps(new_post, indent=2))
