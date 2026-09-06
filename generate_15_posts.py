import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
POSTS_DIR = os.path.join(BASE_DIR, "posts_15_days")
os.makedirs(POSTS_DIR, exist_ok=True)

# Colors
BG_COLOR = (10, 14, 23)        # Obsidian dark
GRID_COLOR = (20, 28, 44)      # Subtle grid
CARD_BG = (16, 22, 36)         # Card surface
CARD_BORDER = (32, 44, 70)     # Border
GREEN = (0, 242, 152)          # Neon emerald
GOLD = (255, 215, 0)           # Gold
RED = (255, 75, 75)            # Warning red
WHITE = (245, 247, 250)        # Pure white
MUTED = (150, 162, 182)        # Muted text
CYAN = (0, 212, 255)           # Cyan

def get_font(size: int, bold: bool = False):
    font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
    try:
        return ImageFont.truetype(font_name, size)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            return ImageFont.load_default()

def draw_card(draw, x, y, w, h, border_color=CARD_BORDER, bg_color=CARD_BG, radius=18):
    """Draws a rounded rectangular card."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color, outline=border_color, width=3)

def draw_base_template(draw, title: str, category: str, day_num: int):
    """Draws the luxury header, branding, grid, and footer for The Wealth Blueprint."""
    # Draw subtle background grid
    for gy in range(160, 1800, 140):
        draw.line([(60, gy), (1020, gy)], fill=GRID_COLOR, width=1)
    for gx in range(60, 1040, 160):
        draw.line([(gx, 160), (gx, 1800)], fill=GRID_COLOR, width=1)
        
    # Top Brand Pill
    pill_text = f"THE WEALTH BLUEPRINT  //  DAY {day_num:02d}"
    pill_font = get_font(26, bold=True)
    draw_card(draw, 100, 90, 480, 56, border_color=GREEN, bg_color=(12, 28, 24), radius=28)
    draw.text((135, 102), pill_text, fill=GREEN, font=pill_font)
    
    # Category Tag
    cat_font = get_font(24, bold=True)
    draw.text((640, 102), f"[{category.upper()}]", fill=GOLD, font=cat_font)
    
    # Main Headline
    title_font = get_font(56, bold=True)
    draw.text((100, 180), title, fill=WHITE, font=title_font)
    
    # Bottom Footer Card
    foot_font = get_font(28, bold=True)
    draw_card(draw, 80, 1750, 920, 90, border_color=GREEN, bg_color=(12, 22, 20), radius=20)
    draw.text((125, 1778), "📌  SAVE THIS REEL  |  FOLLOW @THEWEALTHBLUEPRINT", fill=GREEN, font=foot_font)

# -------------------------------------------------------------
# 15 Specific Infographic Post Renderers
# -------------------------------------------------------------

posts_data = [
    {
        "day": 1,
        "title": "THE 15/3 CREDIT GLITCH",
        "cat": "Credit Hack",
        "script": "If you pay your credit card bill on the due date, you are quietly hurting your credit score. Banks don't report your balance on your due date, they report it on your statement closing date. That means if your limit is 1,000 dollars and you spend 500, your utilization reports as 50 percent, which tanks your score. Instead, use the 15/3 rule: pay half 15 days before your statement, and the rest 3 days before. Save this reel and follow The Wealth Blueprint.",
        "render": "render_day01"
    },
    {
        "day": 2,
        "title": "THE RULE OF 72",
        "cat": "Compound Wealth",
        "script": "Most people have no idea how long it takes to double their money. Billionaires use one simple mental math trick: the Rule of 72. Take the number 72 and divide it by your annual interest rate. If your money sits in an ordinary bank account earning 0.5 percent, it takes 144 years to double. But put that money into the S&P 500 averaging 10 percent, and your wealth doubles every 7.2 years on autopilot. Share this with a friend and follow The Wealth Blueprint.",
        "render": "render_day02"
    },
    {
        "day": 3,
        "title": "BUY, BORROW, DIE",
        "cat": "Tax Loophole",
        "script": "Here is how the ultra-rich legally pay almost zero dollars in income tax. They use a three-step formula called Buy, Borrow, Die. Step 1: They buy appreciating assets like stocks and real estate. Step 2: Instead of selling their assets and paying massive capital gains taxes, they take low-interest loans against their assets to fund their lifestyle. Loans are not taxed as income. Step 3: When they pass away, their assets pass to heirs with a stepped-up tax basis. Save this before it gets deleted.",
        "render": "render_day03"
    },
    {
        "day": 4,
        "title": "3-BANK-ACCOUNT SYSTEM",
        "cat": "Automation",
        "script": "If you keep all your money in one single checking account, you will accidentally spend it every time. Set up the 3-Account System: Account 1 is your Bills Vault, where your paycheck lands and fixed rent and utilities are auto-paid. Account 2 is your Wealth Engine, where 20 percent is auto-transferred into investments. Account 3 is your Guilt-Free Spending card with a strict weekly allowance. Once Account 3 hits zero, you stop spending. Follow The Wealth Blueprint.",
        "render": "render_day04"
    },
    {
        "day": 5,
        "title": "HIGH-YIELD VS BIG BANK",
        "cat": "Banking Glitch",
        "script": "If you have more than 1,000 dollars sitting in a big commercial bank checking account, you are literally losing money to inflation. Traditional banks pay you 0.01 percent interest while they lend your money out at 7 percent. A High-Yield Savings Account pays over 4.5 percent with the exact same FDIC insurance. On a 10,000 dollar emergency fund, that is the difference between making 1 dollar a year versus 450 dollars a year for doing nothing. Move your cash today.",
        "render": "render_day05"
    },
    {
        "day": 6,
        "title": "AUTHORIZED USER HACK",
        "cat": "Credit Secret",
        "script": "If you have a low credit score or zero credit history, here is the fastest legal shortcut. It is called becoming an Authorized User. If a parent or relative has a credit card with an 8-year clean payment history and a high limit, they can add you as an authorized user. Their entire 8-year perfect record instantly copies onto your credit report. You do not even need to touch the physical card. Save this reel and follow for daily finance loopholes.",
        "render": "render_day06"
    },
    {
        "day": 7,
        "title": "THE $700 CAR TRAP",
        "cat": "Wealth Trap",
        "script": "The average monthly car payment in America is now over 700 dollars. That is an absolute wealth killer. If you take that exact same 700 dollars a month and invest it in an S&P 500 index fund for 15 years instead, compound interest turns it into over 300,000 dollars in cash. A car depreciates the second you drive it off the lot, while assets buy your freedom. Stop flexing depreciating metal to impress strangers. Follow The Wealth Blueprint.",
        "render": "render_day07"
    },
    {
        "day": 8,
        "title": "STEALTH WEALTH",
        "cat": "Psychology",
        "script": "There is a massive difference between looking rich and actually being wealthy. People who look rich wear oversized designer logos, lease luxury cars they cannot afford, and live paycheck-to-paycheck to impress people they do not even like. People with stealth wealth wear unbranded clothes, drive reliable 5-year-old paid-off cars, and own cash-flowing assets that pay them while they sleep. Wealth is what you do not see. Save this reel if you prefer freedom.",
        "render": "render_day08"
    },
    {
        "day": 9,
        "title": "48-HR DOPAMINE FREEZE",
        "cat": "Saving Rule",
        "script": "When you see an item you want to buy online, your brain releases a surge of dopamine before you even click checkout. E-commerce websites spend billions weaponizing this biological trigger against your wallet. Here is how you win: enforce a 48-Hour Dopamine Freeze. Add the item to your cart, but close the tab and wait 48 hours. When the dopamine resets, 80 percent of the time you realize you never actually wanted it. Follow for daily money psychology.",
        "render": "render_day09"
    },
    {
        "day": 10,
        "title": "CHARGEBACK SUPERPOWER",
        "cat": "Consumer Law",
        "script": "If an online company refuses to refund you for a damaged product or hits you with an unauthorized recurring fee, never argue with their customer service. Under federal law, you have the legal right to file a Chargeback with your credit card issuer within 60 days. The bank immediately clawbacks the money from the merchant while they investigate. Most merchants will resolve your issue instantly rather than pay a 25 dollar chargeback fee. Share this with someone who shops online.",
        "render": "render_day10"
    },
    {
        "day": 11,
        "title": "GAMMA AI SLIDES",
        "cat": "AI Shortcut",
        "script": "Stop spending your entire Sunday night formatting slide decks in PowerPoint. Go to Gamma.app. Type in a single sentence describing what you need, like Q3 Marketing Plan for a Real Estate Brand, and within 15 seconds, the AI writes the content, designs the layouts, and adds professional imagery across a full 15-slide deck ready to present. You can export directly to PowerPoint for free. Save this reel and follow for daily AI shortcuts.",
        "render": "render_day11"
    },
    {
        "day": 12,
        "title": "NOTEBOOKLM PODCAST",
        "cat": "AI Secret",
        "script": "If you have a 50-page research paper, dense business contract, or textbook chapter to read, stop reading it manually. Upload it to NotebookLM by Google. It is 100 percent free. The AI analyzes the entire document and generates an interactive, two-person conversational podcast explaining every key concept while you drive or workout. You can even ask it questions and it cites the exact page numbers. Follow The Wealth Blueprint for daily productivity hacks.",
        "render": "render_day12"
    },
    {
        "day": 13,
        "title": "SUBSCRIPTION VAMPIRE",
        "cat": "Money Hack",
        "script": "The average person wastes over 100 dollars every month on subscriptions they completely forgot about. Companies design free trials to be easy to start and impossible to remember. Here is the easiest nuclear fix: once every year, report your debit card as damaged and request a replacement card. Your CVV and expiration date change, causing every recurring subscription to instantly fail. You only re-subscribe to the ones you actually use. Follow for daily money shortcuts.",
        "render": "render_day13"
    },
    {
        "day": 14,
        "title": "$10/DAY SNOWBALL",
        "cat": "Compound Math",
        "script": "Most people think you need thousands of dollars to start investing, but 10 dollars a day can change your family's future. If you invest just 10 dollars a day, the cost of two coffees, into a broad index fund averaging a 10 percent annual return, here is what happens: in 10 years you have 65,000 dollars. In 20 years you have 230,000 dollars. In 30 years you have over 680,000 dollars. Time in the market always beats timing the market. Save this reel to stay motivated.",
        "render": "render_day14"
    },
    {
        "day": 15,
        "title": "ASSETS VS LIABILITIES",
        "cat": "Core Foundation",
        "script": "Robert Kiyosaki said it best in Rich Dad Poor Dad: the rich buy assets, while the poor buy liabilities they think are assets. An asset puts money into your pocket whether you work or not: dividend index funds, cash-flowing real estate, automated software. A liability takes money out of your pocket: your car loan, your subscriptions, luxury items. Spend your twenties buying assets that eventually pay for your luxury. Welcome to The Wealth Blueprint. Follow to join the movement.",
        "render": "render_day15"
    }
]

def render_post(item):
    """Renders a high-contrast 1080x1920 infographic poster for the day."""
    img = Image.new("RGB", (1080, 1920), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    day = item["day"]
    draw_base_template(draw, item["title"], item["cat"], day)
    
    # Render custom flowchart cards depending on topic
    h2_font = get_font(38, bold=True)
    body_font = get_font(30, bold=False)
    bold_body = get_font(32, bold=True)
    stat_font = get_font(44, bold=True)
    
    # Generic structured 3-card layout (Problem -> Strategy -> Outcome)
    # Card 1: The Trap
    draw_card(draw, 80, 290, 920, 390, border_color=RED, bg_color=(28, 14, 18))
    draw.text((120, 320), "🛑  THE COSTLY MISTAKE (90% DO THIS)", fill=RED, font=h2_font)
    
    # Card 2: The Loophole / Strategy
    draw_card(draw, 80, 740, 920, 520, border_color=GREEN, bg_color=(12, 28, 22))
    draw.text((120, 770), "⚡  THE BLUEPRINT STRATEGY", fill=GREEN, font=h2_font)
    
    # Connector Arrow down
    draw.line([(540, 680), (540, 735)], fill=CYAN, width=6)
    draw.polygon([(525, 725), (555, 725), (540, 745)], fill=CYAN)
    
    # Card 3: The Result / Math
    draw_card(draw, 80, 1330, 920, 350, border_color=GOLD, bg_color=(28, 25, 12))
    draw.text((120, 1360), "📈  THE FINANCIAL PAYOFF", fill=GOLD, font=h2_font)
    
    draw.line([(540, 1260), (540, 1325)], fill=CYAN, width=6)
    draw.polygon([(525, 1315), (555, 1315), (540, 1335)], fill=CYAN)

    # Populate customized text per day
    if day == 1:
        draw.text((120, 390), "Paying bill on Due Date = Balance reported\non Statement Date. Utilization jumps to 50%,\ntanking your score by 40-70 points.", fill=WHITE, font=body_font)
        draw.text((120, 850), "STEP 1: Pay 50% 15 Days BEFORE statement date.\nSTEP 2: Pay the rest 3 Days BEFORE.\nResult: Bureau sees 2-5% balance utilization.", fill=WHITE, font=bold_body)
        draw.text((120, 1430), "SCORE IMPACT: +40 to +80 Points in 60 Days\n0% Interest Penalties • Unlocks Tier-1 Cards", fill=GREEN, font=stat_font)
        
    elif day == 2:
        draw.text((120, 390), "Leaving savings in a checking account at 0.5%:\nIt will take 144 YEARS to double your money.\nInflation destroys 3% of your purchasing power yearly.", fill=WHITE, font=body_font)
        draw.text((120, 850), "THE FORMULA: 72 / Interest Rate = Years to 2X.\n• High-Yield Savings (5%): Doubles in 14.4 Years\n• S&P 500 Index (10%): Doubles every 7.2 Years!", fill=WHITE, font=bold_body)
        draw.text((120, 1430), "$10,000 invested at age 25 @ 10%:\n= $320,000 at age 60 on complete autopilot.", fill=GOLD, font=stat_font)
        
    elif day == 3:
        draw.text((120, 390), "Selling stocks/real estate triggers 20-37% taxes.\nHigh W2 earners lose nearly half their wealth\nto federal, state, and income taxes.", fill=WHITE, font=body_font)
        draw.text((120, 850), "1. BUY: Hold appreciating stocks & real estate.\n2. BORROW: Take low-interest loan against assets.\n   *Loans are NOT taxed as income!*\n3. DIE: Heirs receive assets with stepped-up basis.", fill=WHITE, font=bold_body)
        draw.text((120, 1430), "LEGAL TAX LIABILITY = 0% INCOME TAX\nAssets stay invested and continue compounding.", fill=GREEN, font=stat_font)

    elif day == 4:
        draw.text((120, 390), "One single checking account = lifestyle creep.\nRent, groceries, and impulsive fun all mix,\nleaving zero savings by the 28th of every month.", fill=WHITE, font=body_font)
        draw.text((120, 850), "ACCOUNT 1: Bills Vault (Rent & Utilities Auto-Paid)\nACCOUNT 2: Wealth Engine (20% Auto-Invested)\nACCOUNT 3: Guilt-Free Spending (Fixed weekly cash).\n*When Account 3 is zero, stop spending!*", fill=WHITE, font=bold_body)
        draw.text((120, 1430), "AUTOMATED SAVINGS RATE = 20% OF INCOME\nZero budgeting willpower required.", fill=GREEN, font=stat_font)

    elif day == 5:
        draw.text((120, 390), "Commercial banks pay 0.01% on checking.\nOn a $10,000 emergency fund, you earn $1/year\nwhile the bank lends your money at 7%.", fill=WHITE, font=body_font)
        draw.text((120, 850), "HIGH-YIELD SAVINGS ACCOUNT (HYSA):\n• Pays 4.50% - 5.00% APY Guaranteed\n• 100% FDIC Insured up to $250,000\n• Takes 5 minutes to set up online.", fill=WHITE, font=bold_body)
        draw.text((120, 1430), "$10,000 EARNS $450 - $500 EVERY YEAR\nRisk-free passive income from your cash reserve.", fill=GOLD, font=stat_font)

    else:
        # Default structured cards for remaining days
        draw.text((120, 390), f"Ignoring the system leads to hidden wealth loss.\nImpulse spending, high interest rates, or missed\nautomation prevents compound wealth accumulation.", fill=WHITE, font=body_font)
        draw.text((120, 850), f"THE WEALTH BLUEPRINT RULE:\nApply the strategic framework outlined in the script.\nAutomate allocation, protect assets, and let time\nwork in your favor rather than against you.", fill=WHITE, font=bold_body)
        draw.text((120, 1430), "RESULT: Accelerated Financial Freedom\nAsset creation beats hourly wages every time.", fill=GREEN, font=stat_font)

    # Save 1080x1920 image
    img_path = os.path.join(POSTS_DIR, f"day{day:02d}_{item['render']}.png")
    img.save(img_path, "PNG")
    
    # Save accompanying voiceover script txt file
    txt_path = os.path.join(POSTS_DIR, f"day{day:02d}_script.txt")
    with open(txt_path, "w", encoding="utf-8") as tf:
        tf.write(item["script"])
        
    return img_path, txt_path

if __name__ == "__main__":
    print(f"Rendering 15 HD Infographic Posters into: {POSTS_DIR}")
    for p in posts_data:
        ip, tp = render_post(p)
        print(f"Generated Day {p['day']:02d}: {os.path.basename(ip)}")
    print("All 15 posts and scripts generated successfully!")
