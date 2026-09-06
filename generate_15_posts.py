import os
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
POSTS_DIR = os.path.join(BASE_DIR, "posts_15_days")
os.makedirs(POSTS_DIR, exist_ok=True)

# -------------------------------------------------------------
# Color Palette (Dark Luxury & Vibrant Accents)
# -------------------------------------------------------------
BG_COLOR = (9, 12, 20)          # Deep obsidian black
GRID_COLOR = (20, 26, 42)       # Subtle matrix grid
CARD_BG = (15, 20, 32)          # Rich card surface
CARD_BORDER = (35, 46, 72)      # Card outline
GREEN = (0, 242, 152)           # Neon emerald
GOLD = (255, 215, 0)            # Vivid gold
RED = (255, 75, 85)             # Bright crimson
CYAN = (0, 220, 255)            # Cyber cyan
WHITE = (245, 248, 255)         # Crisp white
MUTED = (145, 158, 185)         # Muted subtitle grey

def get_font(size: int, bold: bool = False):
    font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
    try:
        return ImageFont.truetype(font_name, size)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            return ImageFont.load_default()

def wrap_text(text: str, font, max_w: int) -> list:
    """Wraps text so it NEVER overflows max_w pixels."""
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test_line = " ".join(curr + [w])
        bbox = font.getbbox(test_line)
        if bbox[2] - bbox[0] <= max_w:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

def draw_card(draw, x, y, w, h, border_color=CARD_BORDER, bg_color=CARD_BG, radius=20, border_width=3):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color, outline=border_color, width=border_width)

# -------------------------------------------------------------
# Visual Badges & Rich Graphic Illustrators
# -------------------------------------------------------------
def draw_bull_badge(draw, cx, cy, size=48):
    """Draws a powerful geometric Bull Market Emblem."""
    r = size
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 36, 26), outline=GREEN, width=3)
    # Bull Horns
    draw.polygon([(cx - 30, cy - 8), (cx - 48, cy - 35), (cx - 18, cy - 20)], fill=GREEN)
    draw.polygon([(cx + 30, cy - 8), (cx + 48, cy - 35), (cx + 18, cy - 20)], fill=GREEN)
    # Head & Snout
    draw.polygon([(cx - 24, cy - 16), (cx + 24, cy - 16), (cx + 16, cy + 22), (cx, cy + 34), (cx - 16, cy + 22)], fill=GREEN)
    # Eyes
    draw.ellipse([cx - 12, cy - 4, cx - 6, cy + 2], fill=BG_COLOR)
    draw.ellipse([cx + 6, cy - 4, cx + 12, cy + 2], fill=BG_COLOR)
    # Trend Arrow rising through
    draw.line([(cx - 32, cy + 32), (cx + 34, cy - 34)], fill=GOLD, width=4)
    draw.polygon([(cx + 34, cy - 34), (cx + 18, cy - 34), (cx + 34, cy - 18)], fill=GOLD)

def draw_money_stack_badge(draw, cx, cy, size=48):
    """Draws stacked Gold Coins and Cash symbol."""
    r = size
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(36, 30, 10), outline=GOLD, width=3)
    # Base coin
    draw.ellipse([cx - 28, cy - 5, cx + 28, cy + 25], fill=(180, 140, 20), outline=GOLD, width=2)
    # Middle coin
    draw.ellipse([cx - 28, cy - 16, cx + 28, cy + 14], fill=(210, 165, 25), outline=GOLD, width=2)
    # Top coin
    draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 2], fill=(255, 215, 0), outline=(255, 245, 160), width=2)
    # Dollar sign on top coin
    font_s = get_font(26, bold=True)
    draw.text((cx - 8, cy - 26), "$", fill=(120, 80, 0), font=font_s)

def draw_credit_card_badge(draw, cx, cy, size=48):
    """Draws a luxury titanium credit card emblem."""
    r = size
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(22, 28, 44), outline=CYAN, width=3)
    # Mini card body
    draw.rounded_rectangle([cx - 32, cy - 20, cx + 32, cy + 20], radius=6, fill=(10, 14, 24), outline=CYAN, width=2)
    # Gold chip
    draw.rounded_rectangle([cx - 22, cy - 8, cx - 10, cy + 4], radius=2, fill=GOLD)
    # Card lines
    draw.line([(cx - 6, cy - 4), (cx + 22, cy - 4)], fill=(120, 140, 180), width=2)
    draw.line([(cx - 6, cy + 2), (cx + 16, cy + 2)], fill=(120, 140, 180), width=2)

def draw_vault_badge(draw, cx, cy, size=48):
    """Draws a heavy bank vault door emblem."""
    r = size
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(26, 28, 38), outline=GOLD, width=3)
    # Outer vault ring
    draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], outline=WHITE, width=3)
    # 6 Vault Wheel Spokes
    for angle in [0, 60, 120]:
        rad = math.radians(angle)
        dx = int(32 * math.cos(rad))
        dy = int(32 * math.sin(rad))
        draw.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=GOLD, width=3)
    # Central Dial
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=GOLD, outline=WHITE, width=2)

def draw_warning_badge(draw, cx, cy, size=48):
    """Draws a glowing red alert warning badge."""
    r = size
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(42, 16, 20), outline=RED, width=3)
    # Warning triangle
    draw.polygon([(cx, cy - 26), (cx - 26, cy + 22), (cx + 26, cy + 22)], outline=RED, fill=(70, 20, 26), width=2)
    font_ex = get_font(28, bold=True)
    draw.text((cx - 5, cy - 16), "!", fill=WHITE, font=font_ex)

def draw_growth_chart_badge(draw, cx, cy, size=48):
    """Draws ascending green financial chart bars with arrow."""
    r = size
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 34, 28), outline=GREEN, width=3)
    # 4 Bar Columns
    bars = [12, 22, 34, 46]
    for i, h in enumerate(bars):
        bx = cx - 26 + (i * 14)
        draw.rounded_rectangle([bx, cy + 20 - h, bx + 10, cy + 20], radius=2, fill=GREEN)
    # Ascending Trend Line
    draw.line([(cx - 28, cy + 8), (cx + 28, cy - 24)], fill=GOLD, width=3)
    draw.polygon([(cx + 28, cy - 24), (cx + 16, cy - 24), (cx + 28, cy - 12)], fill=GOLD)

# -------------------------------------------------------------
# Base Layout Template
# -------------------------------------------------------------
def draw_base_template(draw, title: str, category: str, subtitle: str, day_num: int):
    # Background Grid
    for gy in range(120, 1850, 130):
        draw.line([(50, gy), (1030, gy)], fill=GRID_COLOR, width=1)
    for gx in range(50, 1050, 140):
        draw.line([(gx, 120), (gx, 1850)], fill=GRID_COLOR, width=1)

    # Top Brand Pill
    pill_text = f"THE WEALTH BLUEPRINT  //  DAY {day_num:02d}"
    pill_font = get_font(24, bold=True)
    draw_card(draw, 70, 75, 470, 52, border_color=GREEN, bg_color=(10, 28, 22), radius=26, border_width=2)
    draw.text((105, 87), pill_text, fill=GREEN, font=pill_font)

    # Category Pill
    cat_font = get_font(22, bold=True)
    cat_w = 400
    draw_card(draw, 560, 75, 450, 52, border_color=GOLD, bg_color=(28, 24, 10), radius=26, border_width=2)
    draw.text((595, 88), f"CATEGORY: {category.upper()}", fill=GOLD, font=cat_font)

    # Main Headline
    title_font = get_font(52, bold=True)
    draw.text((70, 150), title, fill=WHITE, font=title_font)
    
    # Subtitle Hook
    sub_font = get_font(25, bold=False)
    draw.text((70, 218), subtitle, fill=MUTED, font=sub_font)

    # Bottom Call to Action Card
    foot_font = get_font(27, bold=True)
    draw_card(draw, 70, 1750, 940, 90, border_color=GREEN, bg_color=(12, 26, 22), radius=20, border_width=3)
    draw.text((150, 1778), "SAVE THIS REEL   |   FOLLOW @THEWEALTHBLUEPRINT", fill=GREEN, font=foot_font)

# -------------------------------------------------------------
# 15 Specific Infographic Content Definitions
# -------------------------------------------------------------
POSTS_DETAILS = [
    {
        "day": 1,
        "title": "THE 15/3 CREDIT SCORE GLITCH",
        "cat": "Credit Hack",
        "sub": "How the banking system actually calculates your balance utilization",
        "badge1": draw_warning_badge,
        "badge2": draw_credit_card_badge,
        "badge3": draw_bull_badge,
        "card1_title": "THE COMMON MISTAKE (90% DO THIS)",
        "card1_text": "Paying your bill on the Due Date means your balance gets reported on the Statement Closing Date. If your limit is $1,000 and you spent $500, bureaus see a 50% utilization rate, dropping your credit score by 40 to 70 points.",
        "card2_title": "THE 15/3 BLUEPRINT STRATEGY",
        "card2_text": "STEP 1: Pay 50% of your balance 15 Days BEFORE your statement date.\nSTEP 2: Pay the remainder 3 Days BEFORE statement date.\nRESULT: The bureau records a tiny 2% balance utilization.",
        "card3_title": "THE FINANCIAL PAYOFF",
        "card3_text": "+40 to +80 Point Credit Score Jump in 60 Days\nUnlocks 0% APR Cards and saves thousands on mortgages.",
        "script": "If you pay your credit card bill on the due date, you are quietly hurting your credit score. Banks do not report your balance on your due date, they report it on your statement closing date. That means if your limit is 1,000 dollars and you spend 500, your utilization reports as 50 percent, which tanks your score. Instead, use the 15/3 rule: pay half 15 days before your statement, and the rest 3 days before. Save this reel and follow The Wealth Blueprint."
    },
    {
        "day": 2,
        "title": "THE RULE OF 72 (COMPOUND WEALTH)",
        "cat": "Investing Math",
        "sub": "The simple mental math formula billionaires use to calculate when money doubles",
        "badge1": draw_warning_badge,
        "badge2": draw_growth_chart_badge,
        "badge3": draw_money_stack_badge,
        "card1_title": "THE CHECKING ACCOUNT TRAP",
        "card1_text": "Leaving cash in an ordinary checking account earning 0.50% interest: it will take 144 YEARS to double your money. Meanwhile, inflation destroys 3% of your purchasing power every single year.",
        "card2_title": "THE FORMULA: 72 ÷ RETURN RATE = YEARS",
        "card2_text": "Take 72 and divide it by your annual interest return:\n• High-Yield Savings (5.0%): Doubles your money in 14.4 Years\n• S&P 500 Index (10.0%): Doubles your money every 7.2 Years on autopilot!",
        "card3_title": "THE COMPOUND SNOWBALL",
        "card3_text": "$10,000 invested at age 25 @ 10% S&P 500 return\n= $320,000 at age 60 without adding another penny.",
        "script": "Most people have no idea how long it takes to double their money. Billionaires use one simple mental math trick: the Rule of 72. Take the number 72 and divide it by your annual interest rate. If your money sits in an ordinary bank account earning 0.5 percent, it takes 144 years to double. But put that money into the S&P 500 averaging 10 percent, and your wealth doubles every 7.2 years on autopilot. Share this with a friend and follow The Wealth Blueprint."
    },
    {
        "day": 3,
        "title": "BUY, BORROW, DIE (0% TAX LOOPHOLE)",
        "cat": "Tax Loopholes",
        "sub": "How the ultra-wealthy fund private jets & mansions without income tax",
        "badge1": draw_warning_badge,
        "badge2": draw_vault_badge,
        "badge3": draw_bull_badge,
        "card1_title": "THE W2 TAX TRAP",
        "card1_text": "Selling stocks or real estate triggers 20% to 37% capital gains and income taxes. High earners lose up to half their annual income to federal and state tax collectors.",
        "card2_title": "THE 3-STEP BILLIONAIRE STRATEGY",
        "card2_text": "1. BUY: Acquire high-value appreciating stocks & real estate.\n2. BORROW: Take low-interest loans against your asset portfolio.\n   *Crucial Rule: Bank loans are NOT classified as taxable income!*\n3. DIE: Pass assets to heirs with a stepped-up tax basis.",
        "card3_title": "THE RESULT: 0% LEGAL TAX LIABILITY",
        "card3_text": "Assets stay 100% invested, dividends continue compounding,\nand lifestyle is fully funded with low-interest debt.",
        "script": "Here is how the ultra-rich legally pay almost zero dollars in income tax. They use a three-step formula called Buy, Borrow, Die. Step 1: They buy appreciating assets like stocks and real estate. Step 2: Instead of selling their assets and paying massive capital gains taxes, they take low-interest loans against their assets to fund their lifestyle. Loans are not taxed as income. Step 3: When they pass away, their assets pass to heirs with a stepped-up tax basis. Save this before it gets deleted."
    },
    {
        "day": 4,
        "title": "THE 3-BANK-ACCOUNT SYSTEM",
        "cat": "Automation",
        "sub": "Stop budgeting with willpower — let banking architecture build your savings",
        "badge1": draw_warning_badge,
        "badge2": draw_credit_card_badge,
        "badge3": draw_money_stack_badge,
        "card1_title": "THE SINGLE CHECKING ACCOUNT DISASTER",
        "card1_text": "Keeping rent, groceries, and fun in one checking account guarantees lifestyle creep. All your cash bleeds together, leaving you with zero savings by the 28th of every single month.",
        "card2_title": "THE AUTOMATED 3-VAULT ARCHITECTURE",
        "card2_text": "VAULT 1: Bills Account (Paycheck lands here, rent & fixed bills auto-pay)\nVAULT 2: Wealth Engine (20% is auto-transferred to index funds)\nVAULT 3: Guilt-Free Card (Fixed weekly allowance for dining & fun).\n*When Vault 3 hits $0, you stop spending!*",
        "card3_title": "THE PAYOFF: 20% GUARANTEED SAVINGS",
        "card3_text": "Automates $10,000 - $25,000 into wealth assets yearly\nwithout tracking a single receipt or spreadsheet.",
        "script": "If you keep all your money in one single checking account, you will accidentally spend it every time. Set up the 3-Account System: Account 1 is your Bills Vault, where your paycheck lands and fixed rent and utilities are auto-paid. Account 2 is your Wealth Engine, where 20 percent is auto-transferred into investments. Account 3 is your Guilt-Free Spending card with a strict weekly allowance. Once Account 3 hits zero, you stop spending. Follow The Wealth Blueprint."
    },
    {
        "day": 5,
        "title": "HIGH-YIELD VS. BIG COMMERCIAL BANKS",
        "cat": "Banking Glitch",
        "sub": "Why keeping emergency cash in traditional banks is giving away free money",
        "badge1": draw_warning_badge,
        "badge2": draw_growth_chart_badge,
        "badge3": draw_money_stack_badge,
        "card1_title": "THE COMMERCIAL BANK RIP-OFF",
        "card1_text": "Traditional banks pay an insulting 0.01% APY on checking and savings. On a $10,000 emergency fund, you earn $1.00 a year while the bank lends your cash out for mortgages at 7%.",
        "card2_title": "THE HIGH-YIELD SAVINGS ACCOUNT (HYSA)",
        "card2_text": "Switch to an online High-Yield Savings Account (HYSA):\n• Pays 4.50% to 5.00% APY Guaranteed\n• 100% FDIC Insured up to $250,000\n• Full liquidity — withdraw your cash anytime.",
        "card3_title": "ANNUAL CASH GAIN COMPARISON",
        "card3_text": "$10,000 in Big Bank = $1.00 / Year\n$10,000 in HYSA = $450 - $500 / Year (100% Passive)",
        "script": "If you have more than 1,000 dollars sitting in a big commercial bank checking account, you are literally losing money to inflation. Traditional banks pay you 0.01 percent interest while they lend your money out at 7 percent. A High-Yield Savings Account pays over 4.5 percent with the exact same FDIC insurance. On a 10,000 dollar emergency fund, that is the difference between making 1 dollar a year versus 450 dollars a year for doing nothing. Move your cash today."
    },
    {
        "day": 6,
        "title": "THE AUTHORIZED USER CREDIT HACK",
        "cat": "Credit Secret",
        "sub": "The legal credit loophole that copies 8 years of perfect history onto your report",
        "badge1": draw_warning_badge,
        "badge2": draw_credit_card_badge,
        "badge3": draw_bull_badge,
        "card1_title": "THE 'NO CREDIT HISTORY' CATCH-22",
        "card1_text": "Applying for tier-1 credit cards with low or zero credit history gets you instantly rejected. Each rejection adds a hard inquiry, pulling your score down even further.",
        "card2_title": "THE AUTHORIZED USER SHORTCUT",
        "card2_text": "Have a parent or relative add you as an 'Authorized User' to a card with 8+ years of perfect on-time payments and a high credit limit.\n*You do NOT need to spend or touch the physical card!*",
        "card3_title": "INSTANT SCORE ELEVATION",
        "card3_text": "+70 to +110 Credit Score Jump in 30 Days\nTheir 8-year perfect record mirrors onto your credit file.",
        "script": "If you have a low credit score or zero credit history, here is the fastest legal shortcut. It is called becoming an Authorized User. If a parent or relative has a credit card with an 8-year clean payment history and a high limit, they can add you as an authorized user. Their entire 8-year perfect record instantly copies onto your credit report. You do not even need to touch the physical card. Save this reel and follow for daily finance loopholes."
    },
    {
        "day": 7,
        "title": "THE $700 CAR PAYMENT TRAP",
        "cat": "Wealth Destroyer",
        "sub": "How financing a depreciating asset steals decades of retirement freedom",
        "badge1": draw_warning_badge,
        "badge2": draw_growth_chart_badge,
        "badge3": draw_vault_badge,
        "card1_title": "THE $720/MONTH STATUS TRAP",
        "card1_text": "The average American car payment is $720/month. The car loses 20% of its value the minute it leaves the dealership and 60% over 5 years. You are financing a melting ice cube.",
        "card2_title": "THE S&P 500 COMPOUND ALTERNATIVE",
        "card2_text": "Drive a reliable, paid-off car and invest that exact same $720/month into an S&P 500 index fund averaging 10% annual historical returns:\n• In 5 Years: $56,000 in cash\n• In 10 Years: $148,000 in cash\n• In 15 Years: $305,000 in cash!",
        "card3_title": "THE FREEDOM MATH",
        "card3_text": "$305,000 in Cash Assets vs. a Rusted $4,000 Used Car\nChoose long-term wealth over temporary street flexing.",
        "script": "The average monthly car payment in America is now over 700 dollars. That is an absolute wealth killer. If you take that exact same 700 dollars a month and invest it in an S&P 500 index fund for 15 years instead, compound interest turns it into over 300,000 dollars in cash. A car depreciates the second you drive it off the lot, while assets buy your freedom. Stop flexing depreciating metal to impress strangers. Follow The Wealth Blueprint for daily wealth rules."
    },
    {
        "day": 8,
        "title": "STEALTH WEALTH: LOOKING RICH VS. BEING RICH",
        "cat": "Wealth Psychology",
        "sub": "Why the truly wealthy wear plain clothes and drive 6-year-old Toyotas",
        "badge1": draw_warning_badge,
        "badge2": draw_bull_badge,
        "badge3": draw_money_stack_badge,
        "card1_title": "THE FAKE WEALTH TRAP",
        "card1_text": "Oversized luxury designer logos, leased Mercedes, and $300 dinners financed on credit cards to impress strangers you do not even like. Living paycheck-to-paycheck behind a luxury facade.",
        "card2_title": "THE STEALTH WEALTH BLUEPRINT",
        "card2_text": "• Unbranded high-quality clothing (comfort over logos)\n• Reliable paid-off vehicle (zero debt payments)\n• Low overhead lifestyle allowing 40%+ savings rate\n• All capital poured into cash-flowing investments and software.",
        "card3_title": "THE RESULT: ABSOLUTE INDEPENDENCE",
        "card3_text": "Wealth is what you do not see.\nTrue luxury is waking up with 100% control of your time.",
        "script": "There is a massive difference between looking rich and actually being wealthy. People who look rich wear oversized designer logos, lease luxury cars they cannot afford, and live paycheck-to-paycheck to impress people they do not even like. People with stealth wealth wear unbranded clothes, drive reliable 5-year-old paid-off cars, and own cash-flowing assets that pay them while they sleep. Wealth is what you do not see. Save this reel if you prefer freedom."
    },
    {
        "day": 9,
        "title": "THE 48-HOUR DOPAMINE SPENDING FREEZE",
        "cat": "Psychology Hack",
        "sub": "The neuroscience trick that cancels 80% of online impulse purchases",
        "badge1": draw_warning_badge,
        "badge2": draw_vault_badge,
        "badge3": draw_money_stack_badge,
        "card1_title": "THE DOPAMINE WEAPON",
        "card1_text": "E-commerce stores spend billions optimizing one-click checkouts. Seeing an item triggers a dopamine surge in your brain, causing irrational impulse spending before logic kicks in.",
        "card2_title": "THE 48-HOUR FRICTION PROTOCOL",
        "card2_text": "When you want to buy any non-essential item over $50:\n1. Add it to your cart, but do NOT click purchase.\n2. Close the browser tab and set a timer for 48 hours.\n3. After 48 hours, the dopamine spike resets to baseline.",
        "card3_title": "SAVINGS PAYOFF",
        "card3_text": "82% of impulses are voluntarily abandoned.\nSaves an average of $350 - $600 per month automatically.",
        "script": "When you see an item you want to buy online, your brain releases a surge of dopamine before you even click checkout. E-commerce websites spend billions weaponizing this biological trigger against your wallet. Here is how you win: enforce a 48-Hour Dopamine Freeze. Add the item to your cart, but close the tab and wait 48 hours. When the dopamine resets, 80 percent of the time you realize you never actually wanted it. Follow for daily money psychology."
    },
    {
        "day": 10,
        "title": "THE CREDIT CARD CHARGEBACK SUPERPOWER",
        "cat": "Consumer Law",
        "sub": "The secret refund button that forces shady merchants to pay you back",
        "badge1": draw_warning_badge,
        "badge2": draw_credit_card_badge,
        "badge3": draw_bull_badge,
        "card1_title": "THE CUSTOMER SERVICE RUNAROUND",
        "card1_text": "You bought a damaged product or got hit by an unfair recurring charge. The merchant's customer service ignores your emails or refuses a refund, keeping your money.",
        "card2_title": "THE CHARGEBACK NUCLEAR OPTION",
        "card2_text": "Under the federal Fair Credit Billing Act, call your card issuer and request a 'Chargeback' within 60 days.\n• The bank immediately claws back the funds from the merchant\n• The merchant is fined a $25 - $50 bank penalty fee!",
        "card3_title": "THE OUTCOME: 95% REFUND RATE",
        "card3_text": "Merchants almost always settle immediately\nrather than lose merchant processing standing.",
        "script": "If an online company refuses to refund you for a damaged product or hits you with an unauthorized recurring fee, never argue with their customer service. Under federal law, you have the legal right to file a Chargeback with your credit card issuer within 60 days. The bank immediately clawbacks the money from the merchant while they investigate. Most merchants will resolve your issue instantly rather than pay a 25 dollar chargeback fee. Share this with someone who shops online."
    },
    {
        "day": 11,
        "title": "GAMMA AI: 15-SLIDE DECK IN 15 SECONDS",
        "cat": "AI Productivity",
        "sub": "Stop wasting Sunday nights building manual PowerPoint presentations",
        "badge1": draw_warning_badge,
        "badge2": draw_growth_chart_badge,
        "badge3": draw_bull_badge,
        "card1_title": "THE 5-HOUR POWERPOINT SLOG",
        "card1_text": "Formatting bullet points, aligning image boxes, and picking color palettes in PowerPoint burns 4 to 6 hours of your weekend for a simple business or school presentation.",
        "card2_title": "THE 1-CLICK GAMMA.APP WORKFLOW",
        "card2_text": "1. Go to Gamma.app (100% Free).\n2. Type one sentence prompt (e.g. 'Q3 Tech Strategy Deck').\n3. Within 15 seconds, AI writes the entire content, formats visual cards, and embeds relevant graphics.",
        "card3_title": "EXPORT IN SECONDS",
        "card3_text": "Generates 15 polished professional slides in 15 seconds.\nExport directly to PowerPoint or PDF with zero watermarks.",
        "script": "Stop spending your entire Sunday night formatting slide decks in PowerPoint. Go to Gamma.app. Type in a single sentence describing what you need, like Q3 Marketing Plan for a Real Estate Brand, and within 15 seconds, the AI writes the content, designs the layouts, and adds professional imagery across a full 15-slide deck ready to present. You can export directly to PowerPoint for free. Save this reel and follow for daily AI shortcuts."
    },
    {
        "day": 12,
        "title": "NOTEBOOKLM: TURN 100 PAGES INTO A PODCAST",
        "cat": "AI Shortcut",
        "sub": "Google's free AI tool that reads dense PDFs and turns them into audio",
        "badge1": draw_warning_badge,
        "badge2": draw_growth_chart_badge,
        "badge3": draw_vault_badge,
        "card1_title": "THE INFORMATION OVERLOAD PROBLEM",
        "card1_text": "Reading 50-page corporate PDF reports, dense legal contracts, or dry textbook chapters takes hours of eye strain and leads to low retention.",
        "card2_title": "THE GOOGLE NOTEBOOKLM PROTOCOL",
        "card2_text": "1. Go to NotebookLM by Google (Free).\n2. Drag & drop any PDF, textbook, or web article.\n3. Click 'Generate Audio Overview'.\nTwo AI hosts create an interactive conversational podcast breaking down every key insight in plain English!",
        "card3_title": "LEARN WHILE COMMUTING",
        "card3_text": "Listen to 100 pages of dense reading during your 20-minute drive.\nAsk questions and it cites the exact page numbers.",
        "script": "If you have a 50-page research paper, dense business contract, or textbook chapter to read, stop reading it manually. Upload it to NotebookLM by Google. It is 100 percent free. The AI analyzes the entire document and generates an interactive, two-person conversational podcast explaining every key concept while you drive or workout. You can even ask it questions and it cites the exact page numbers. Follow The Wealth Blueprint for daily productivity hacks."
    },
    {
        "day": 13,
        "title": "THE SUBSCRIPTION VAMPIRE KILL-SWITCH",
        "cat": "Money Defense",
        "sub": "The 5-minute nuclear reset that cancels all forgotten subscriptions",
        "badge1": draw_warning_badge,
        "badge2": draw_credit_card_badge,
        "badge3": draw_money_stack_badge,
        "card1_title": "THE HIDDEN $1,200/YEAR CASH BLEED",
        "card1_text": "Free trials make signing up effortless and canceling nearly impossible. The average person wastes over $100 a month on cloud storage, apps, and streaming services they never open.",
        "card2_title": "THE CARD REPLACEMENT KILL-SWITCH",
        "card2_text": "Once every year, log into your banking app and click:\n'Report Debit Card as Damaged / Reissue Card'.\nYour bank sends a new card with a new CVV and expiration date.\n*Every recurring subscription instantly fails!*",
        "card3_title": "EFFORTLESS ANNUAL SAVINGS",
        "card3_text": "You only re-enter card details for the 3 apps you actually use.\nSaves $1,200+ every year with zero awkward cancellation phone calls.",
        "script": "The average person wastes over 100 dollars every month on subscriptions they completely forgot about. Companies design free trials to be easy to start and impossible to remember. Here is the easiest nuclear fix: once every year, report your debit card as damaged and request a replacement card. Your CVV and expiration date change, causing every recurring subscription to instantly fail. You only re-subscribe to the ones you actually use. Follow for daily money shortcuts."
    },
    {
        "day": 14,
        "title": "THE $10 A DAY SNOWBALL ($680,000 COMPOUND)",
        "cat": "Investing Math",
        "sub": "How skipping two fancy coffees builds an empire over time",
        "badge1": draw_warning_badge,
        "badge2": draw_growth_chart_badge,
        "badge3": draw_bull_badge,
        "card1_title": "THE 'I DON'T HAVE CAPITAL' EXCUSE",
        "card1_text": "Believing you need $20,000 before you can invest in the stock market causes young people to lose the single most valuable investing asset: TIME.",
        "card2_title": "THE $10/DAY AUTOMATION FORMULA",
        "card2_text": "Automate $10 a day ($300/mo) into a low-cost S&P 500 index fund averaging 10% annual historical returns:\n• In 10 Years: $65,000 in cash\n• In 20 Years: $230,000 in cash\n• In 30 Years: $680,000 in cash!",
        "card3_title": "THE COMPOUND EFFECT",
        "card3_text": "Your total money contributed = $108,000\nCompound interest added = $572,000 (Pure Profit)",
        "script": "Most people think you need thousands of dollars to start investing, but 10 dollars a day can change your family's future. If you invest just 10 dollars a day, the cost of two coffees, into a broad index fund averaging a 10 percent annual return, here is what happens: in 10 years you have 65,000 dollars. In 20 years you have 230,000 dollars. In 30 years you have over 680,000 dollars. Time in the market always beats timing the market. Save this reel to stay motivated."
    },
    {
        "day": 15,
        "title": "ASSETS VS. LIABILITIES (THE GOLDEN RULE)",
        "cat": "Core Foundation",
        "sub": "The fundamental difference separating the wealthy from the middle class",
        "badge1": draw_warning_badge,
        "badge2": draw_vault_badge,
        "badge3": draw_money_stack_badge,
        "card1_title": "THE MIDDLE CLASS LIABILITIES TRAP",
        "card1_text": "Buying liabilities that take money out of your pocket every month while pretending they are assets: leased luxury cars, depreciating watches, and consumer goods.",
        "card2_title": "THE WEALTH BLUEPRINT ASSET DEFINITION",
        "card2_text": "An Asset puts money into your pocket whether you work or not:\n• Dividend-paying index funds\n• Cash-flowing real estate\n• Automated digital software & media channels.",
        "card3_title": "THE GOLDEN TIMELINE",
        "card3_text": "Spend your 20s buying income-generating assets.\nLet your assets pay for your luxury guilt-free.",
        "script": "Robert Kiyosaki said it best in Rich Dad Poor Dad: the rich buy assets, while the poor buy liabilities they think are assets. An asset puts money into your pocket whether you work or not: dividend index funds, cash-flowing real estate, automated software. A liability takes money out of your pocket: your car loan, your subscriptions, luxury items. Spend your twenties buying assets that eventually pay for your luxury. Welcome to The Wealth Blueprint. Follow to join the movement."
    }
]

def render_post_v2(item):
    """Renders pixel-perfect 1080x1920 poster with contained text & rich graphic emblems."""
    img = Image.new("RGB", (1080, 1920), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    day = item["day"]
    draw_base_template(draw, item["title"], item["cat"], item["sub"], day)

    h2_font = get_font(32, bold=True)
    body_font = get_font(26, bold=False)
    stat_font = get_font(32, bold=True)

    # ---------------------------------------------------------
    # Card 1: The Mistake (Red Warning)
    # ---------------------------------------------------------
    card1_y = 270
    card1_h = 420
    draw_card(draw, 70, card1_y, 940, card1_h, border_color=RED, bg_color=(24, 12, 16))
    draw.text((110, card1_y + 30), f"[!]  {item['card1_title']}", fill=RED, font=h2_font)
    item["badge1"](draw, 920, card1_y + 80, size=46)

    # Text wrapping strictly constrained to 740px width
    lines1 = wrap_text(item["card1_text"], body_font, 740)
    ty = card1_y + 110
    for line in lines1:
        draw.text((110, ty), line, fill=WHITE, font=body_font)
        ty += 44

    # Connector Arrow 1
    draw.line([(540, 695), (540, 740)], fill=CYAN, width=6)
    draw.polygon([(525, 730), (555, 730), (540, 745)], fill=CYAN)

    # ---------------------------------------------------------
    # Card 2: The Blueprint Strategy (Green Solution)
    # ---------------------------------------------------------
    card2_y = 750
    card2_h = 520
    draw_card(draw, 70, card2_y, 940, card2_h, border_color=GREEN, bg_color=(12, 28, 22))
    draw.text((110, card2_y + 30), f"[>]  {item['card2_title']}", fill=GREEN, font=h2_font)
    item["badge2"](draw, 920, card2_y + 80, size=46)

    # Text wrapping with support for multi-line bullet breaks
    ty = card2_y + 110
    raw_lines = item["card2_text"].split("\n")
    for r_line in raw_lines:
        wrapped_sub = wrap_text(r_line, body_font, 740)
        for w_line in wrapped_sub:
            draw.text((110, ty), w_line, fill=WHITE, font=body_font)
            ty += 44
        ty += 8 # Extra padding between bullet blocks

    # Connector Arrow 2
    draw.line([(540, 1275), (540, 1320)], fill=CYAN, width=6)
    draw.polygon([(525, 1310), (555, 1310), (540, 1325)], fill=CYAN)

    # ---------------------------------------------------------
    # Card 3: The Financial Payoff (Gold Result)
    # ---------------------------------------------------------
    card3_y = 1330
    card3_h = 370
    draw_card(draw, 70, card3_y, 940, card3_h, border_color=GOLD, bg_color=(30, 26, 12))
    draw.text((110, card3_y + 30), f"[$]  {item['card3_title']}", fill=GOLD, font=h2_font)
    item["badge3"](draw, 920, card3_y + 80, size=46)

    ty = card3_y + 110
    raw_lines = item["card3_text"].split("\n")
    for r_line in raw_lines:
        wrapped_sub = wrap_text(r_line, stat_font, 740)
        for w_line in wrapped_sub:
            draw.text((110, ty), w_line, fill=GREEN if "PAYOFF" in item["card3_title"] or "$" in w_line else WHITE, font=stat_font)
            ty += 50
        ty += 10

    # Save finalized 1080x1920 HD image
    out_img = os.path.join(POSTS_DIR, f"day{day:02d}_render_day{day:02d}.png")
    img.save(out_img, "PNG")

    # Save matching voiceover script txt
    out_txt = os.path.join(POSTS_DIR, f"day{day:02d}_script.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(item["script"])

    return out_img, out_txt

if __name__ == "__main__":
    print(f">> Rendering All 15 Upgraded Infographic Posters with Custom Emblems & Contained Text...")
    for p in POSTS_DETAILS:
        img_p, txt_p = render_post_v2(p)
        print(f"   [OK] Day {p['day']:02d}: {os.path.basename(img_p)}")
    print(">> All 15 upgraded renders completed successfully!")
