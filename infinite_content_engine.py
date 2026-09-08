import os
import sys
import json
import re
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
PUBLISHED_DIR = os.path.join(BASE_DIR, "published_videos")
HISTORY_FILE = os.path.join(PUBLISHED_DIR, "published_history.json")

# STOPWORDS for deduplication token filtering
STOPWORDS = {
    "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "with",
    "by", "of", "from", "is", "are", "vs", "your", "how", "what", "that",
    "this", "shorts", "reels", "wealth", "secret", "hack", "glitch", "rule"
}

def tokenize_title(title: str) -> set:
    """Extracts meaningful normalized keywords from a title."""
    words = re.findall(r'[a-zA-Z0-9₹$]+', title.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}

def compute_similarity(title1: str, title2: str) -> float:
    """Computes Jaccard word-set similarity between two titles."""
    tokens1 = tokenize_title(title1)
    tokens2 = tokenize_title(title2)
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)

# Curated reservoir of pristine, unique, numbers-backed topics for infinite engine replenishment
RESERVOIR_TOPICS = [
    {
        "category": "Tax Shield",
        "region": "INDIA",
        "voice": "en-IN-PrabhatNeural",
        "title": "Section 80GG: Claim ₹60,000 Rent Deduction Without HRA 🏠🧾",
        "sub": "How freelancers, consultants, and employees without HRA slash rental taxes",
        "c1_t": "NO HRA ON PAYSLIP TRAP",
        "c1_d": "If your company doesn't provide House Rent Allowance (HRA) or you are self-employed, you assume rent cannot be deducted from income tax.",
        "b1": "warning",
        "c2_t": "SECTION 80GG RENT EXEMPTION",
        "c2_d": "Step 1: Verify you or your spouse don't own residential property in the city of work.\nStep 2: File Form 10BA along with your income tax return.\nStep 3: Deduct up to ₹5,000/month (₹60,000/year) directly from total income.",
        "b2": "vault",
        "c3_t": "THE FINANCIAL PAYOFF",
        "c3_d": "Saves Up to ₹18,720 in Hard Cash Tax Annually (in 30% slab)\nValid for all self-employed and non-HRA salaried professionals.",
        "b3": "money",
        "script": "If you pay rent in India but your employer does not give you House Rent Allowance on your salary slip, do not panic. Section 80GG of the Income Tax Act allows any individual who does not receive HRA to deduct rent payments up to 5,000 rupees a month—or 60,000 rupees every financial year. This applies to freelancers, consultants, remote contractors, and small business employees. All you have to do is file a simple declaration called Form 10BA when filing your tax return. In the 30 percent tax slab, that puts nearly 19,000 rupees of hard cash back in your pocket. Save this reel and tell your accountant.",
        "tags": ["section 80gg", "rent deduction no hra", "freelance tax saving", "save rent tax", "indian income tax", "wealth blueprint"]
    },
    {
        "category": "Credit Strategy",
        "region": "GLOBAL",
        "voice": "en-US-ChristopherNeural",
        "title": "The Authorized User Glitch: Boost Credit Score by 100 Points in 30 Days 💳🚀",
        "sub": "How to legally piggyback on a family member's perfect 10-year credit history",
        "c1_t": "THE THIN CREDIT FILE TRAP",
        "c1_d": "Young adults and immigrants get rejected for cards and mortgages because having no credit history is treated just as poorly as having bad credit.",
        "b1": "warning",
        "c2_t": "THE AUTHORIZED USER PIGGYBACK METHOD",
        "c2_d": "Step 1: Ask a parent or spouse with a 750+ score and 10+ year card history.\nStep 2: Add you as an 'Authorized User' on their oldest, pristine card.\nStep 3: You don't even need the physical card; their entire payment history inherits onto your report.",
        "b2": "card",
        "c3_t": "THE FINANCIAL PAYOFF",
        "c3_d": "+70 to +120 Point Credit Score Jump in 30 Days\nInherit 10 years of on-time payment history instantly.",
        "b3": "bull",
        "script": "If you have a low credit score or no credit history at all, do not spend three years waiting to build it. Use a legal credit glitch called the Authorized User Piggyback. Ask a parent or trusted family member with an 800 credit score to add you as an authorized user on their oldest credit card. You do not even need to spend money or touch the physical card. The moment their card issuer reports to the credit bureaus, ten or fifteen years of perfect on-time payment history and high credit limit are instantly copied onto your credit file. Your score can leap eighty to one hundred points in thirty days. Save this reel to fix your credit.",
        "tags": ["authorized user hack", "boost credit score fast", "credit piggybacking", "cibil score jump", "personal finance secrets", "wealth blueprint"]
    },
    {
        "category": "Real Estate Math",
        "region": "GLOBAL",
        "voice": "en-US-ChristopherNeural",
        "title": "The 5% Rule: Why Renting Beats Buying a House Mathematically 🏠📉",
        "sub": "The hidden cost of homeownership that real estate agents never reveal",
        "c1_t": "THE 'RENT IS THROWING MONEY AWAY' LIE",
        "c1_d": "Society convinces you that renting is burning cash, while buying an overpriced house on a 30-year loan is always an asset.",
        "b1": "warning",
        "c2_t": "THE 5% COST OF CAPITAL RULE",
        "c2_d": "Step 1: Calculate 5% of the total property value (1% property tax + 1% maintenance + 3% cost of equity/interest).\nStep 2: Compare that annual 5% number to annual rent on an equivalent home.\nStep 3: If annual rent is LESS than 5% of property value, renting and investing the down payment beats buying.",
        "b2": "growth",
        "c3_t": "THE FINANCIAL PAYOFF",
        "c3_d": "Prevents Illiquid Debt Traps & Cash Bleed\nCompounding down payment in index funds yields 3x more net worth over 20 years.",
        "b3": "money",
        "script": "Stop saying renting is throwing money away. Buying a home has three massive unrecoverable costs that real estate brokers hide: property taxes, home maintenance, and the cost of debt. Add them up and they equal roughly five percent of the home's total value every single year. That means on a 500,000 dollar home, you lose 25,000 dollars a year to unrecoverable non-equity expenses. If you can rent an equivalent home for less than that 25,000 dollars, renting is mathematically cheaper. If you invest the down payment and monthly savings into low-cost index funds, you will build significantly more net worth without being tied to a thirty-year mortgage. Save this before signing a mortgage.",
        "tags": ["rent vs buy", "the 5 percent rule", "real estate math", "mortgage trap", "financial independence", "wealth blueprint"]
    },
    {
        "category": "Tax Arbitrage",
        "region": "INDIA",
        "voice": "en-IN-PrabhatNeural",
        "title": "Form 15G / 15H: Stop Banks from Illegally Deducting 10% TDS 🏦🛑",
        "sub": "How to prevent banks from cutting tax on fixed deposits if your income is below the taxable slab",
        "c1_t": "THE UNNECESSARY 10% TDS DEDUCTION",
        "c1_d": "Banks automatically deduct 10% TDS on FD interest above ₹40,000 (₹50,000 for seniors), even if your total income is below the taxable threshold.",
        "b1": "warning",
        "c2_t": "SUBMIT FORM 15G (OR 15H FOR SENIORS)",
        "c2_d": "Step 1: In the first week of April, log into your net banking portal.\nStep 2: Submit Form 15G (under 60 years) or Form 15H (senior citizens).\nStep 3: It legally certifies that your total tax liability is ZERO, blocking TDS at source.",
        "b2": "vault",
        "c3_t": "THE FINANCIAL PAYOFF",
        "c3_d": "Zero TDS Deducted on Fixed Deposit Interest\nEliminates the headache of filing ITR just to wait 8 months for refunds.",
        "b3": "money",
        "script": "If you or your retired parents have money in bank fixed deposits, banks are likely deducting ten percent TDS from your interest payouts every single quarter. Under Indian tax law, if your fixed deposit interest exceeds forty thousand rupees—or fifty thousand for senior citizens—the bank automatically cuts TDS, even if your total taxable income is below the zero tax slab. To stop this cash drain, submit Form 15G if you are under sixty, or Form 15H if you are a senior citizen. You can submit it in sixty seconds through your mobile banking app in April. It forces the bank to pay one hundred percent of your interest with zero deductions. Save this and help your parents submit it today.",
        "tags": ["form 15g 15h", "stop tds on fd", "fixed deposit tax hack", "senior citizen tax savings", "indian banking rules", "wealth blueprint"]
    },
    {
        "category": "Retirement Shield",
        "region": "INDIA",
        "voice": "en-IN-PrabhatNeural",
        "title": "Senior Citizens Savings Scheme (SCSS): 8.2% Guaranteed Sovereign Yield 🛡️💵",
        "sub": "Why SCSS beats private corporate FDs and mutual funds for retirees seeking safe income",
        "c1_t": "THE RISKY HIGH-YIELD FD TRAP",
        "c1_d": "Retirees chasing 8% returns risk life savings in unrated corporate deposits or volatile debt funds that can default or lose principal.",
        "b1": "warning",
        "c2_t": "CENTRAL GOVT SCSS ALLOCATION",
        "c2_d": "Step 1: Anyone aged 60+ can open an SCSS account at post offices or authorized banks.\nStep 2: Deposit up to ₹30 Lakhs (₹60 Lakhs for couple with joint accounts).\nStep 3: Lock in 8.2% annual interest backed 100% by the sovereign Government of India.",
        "b2": "vault",
        "c3_t": "THE FINANCIAL PAYOFF",
        "c3_d": "Guaranteed ₹2,46,000 Annual Passive Cash Flow (per ₹30 Lakhs)\nQuarterly interest credited automatically with zero market volatility.",
        "b3": "bull",
        "script": "Never let your retired parents gamble their life savings in risky high-yield corporate fixed deposits or volatile debt funds. The Government of India runs the ultimate sovereign retirement vehicle: the Senior Citizens Savings Scheme. Any Indian citizen aged sixty or older can deposit up to thirty lakh rupees into SCSS. A married couple can invest up to sixty lakhs combined. It pays a massive 8.2 percent annual interest rate, backed directly by the sovereign credit of the Central Government. On a thirty lakh deposit, it generates nearly two lakh fifty thousand rupees of guaranteed annual passive income paid out every quarter. Share this with your parents to secure their retirement.",
        "tags": ["senior citizen savings scheme", "scss interest rate", "retirement passive income", "safe investment for seniors", "sovereign guarantee", "wealth blueprint"]
    }
]

def load_dynamic_catalog():
    if not os.path.exists(CATALOG_JSON):
        return []
    try:
        with open(CATALOG_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_dynamic_catalog(catalog):
    with open(CATALOG_JSON, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

def is_duplicate_topic(candidate_title: str, existing_catalog: list) -> bool:
    """Checks if candidate title has semantic keyword collision with existing catalog."""
    cand_norm = candidate_title.lower().strip()
    for item in existing_catalog:
        ex_title = item.get("title", "").lower().strip()
        # Direct substring match
        if cand_norm == ex_title or cand_norm in ex_title or ex_title in cand_norm:
            return True
        # Jaccard word-set similarity check
        sim = compute_similarity(cand_norm, ex_title)
        if sim >= 0.35:
            return True
    return False

def generate_and_append_new_post():
    """Selects a non-duplicate topic from reservoir and appends to dynamic_catalog.json."""
    catalog = load_dynamic_catalog()
    current_count = len(catalog)
    new_id = current_count + 1

    # Find a topic from reservoir that is completely non-duplicate
    chosen_topic = None
    for res_topic in RESERVOIR_TOPICS:
        if not is_duplicate_topic(res_topic["title"], catalog):
            chosen_topic = res_topic
            break

    if not chosen_topic:
        print("[!] All reservoir topics currently exhausted or duplicated in catalog.")
        return None

    new_day = (new_id + 2) // 3
    slot_num = ((new_id - 1) % 3) + 1

    new_item = {
        "id": new_id,
        "day": new_day,
        "slot": slot_num,
        "region": chosen_topic["region"],
        "category": chosen_topic["category"],
        "title": chosen_topic["title"],
        "sub": chosen_topic["sub"],
        "c1_t": chosen_topic["c1_t"],
        "c1_d": chosen_topic["c1_d"],
        "b1": chosen_topic["b1"],
        "c2_t": chosen_topic["c2_t"],
        "c2_d": chosen_topic["c2_d"],
        "b2": chosen_topic["b2"],
        "c3_t": chosen_topic["c3_t"],
        "c3_d": chosen_topic["c3_d"],
        "b3": chosen_topic["b3"],
        "voice": chosen_topic["voice"],
        "script": chosen_topic["script"],
        "tags": chosen_topic.get("tags", ["wealth", "finance", "moneyrules", "smartmoney", "reels", "shorts"]),
        "pinned_comment": "Which part of this blueprint surprised you most? Comment below!"
    }

    catalog.append(new_item)
    save_dynamic_catalog(catalog)
    print(f">> [INFINITE ENGINE] Added verified unique Post #{new_id:02d}: '{chosen_topic['title']}' (Day {new_day} Slot {slot_num})")
    return new_item

if __name__ == "__main__":
    cat = load_dynamic_catalog()
    print(f">> Loaded {len(cat)} items from dynamic catalog.")
    print(">> Deduplication engine verified and ready.")
