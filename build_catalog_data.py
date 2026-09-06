# Generator for all 100 high-retention post definitions
# Alternating Slot 1 (Global High-RPM) and Slot 2 (Indian Personal Finance & Banking Loopholes)

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "content_catalog_100.py")

GLOBAL_TOPICS = [
    # 1
    {
        "title": "The 15/3 Credit Score Glitch Banks Keep Secret 💳📈 #Shorts",
        "cat": "Credit Hack",
        "sub": "How the banking system actually calculates your balance utilization",
        "b1": "warning", "b2": "card", "b3": "bull",
        "c1_t": "THE COMMON MISTAKE (90% DO THIS)",
        "c1_d": "Paying your bill on the Due Date means your balance gets reported on the Statement Closing Date. If your limit is $1,000 and you spent $500, bureaus see a 50% utilization rate, dropping your credit score by 40 to 70 points.",
        "c2_t": "THE 15/3 BLUEPRINT STRATEGY",
        "c2_d": "STEP 1: Pay 50% of your balance 15 Days BEFORE your statement date.\nSTEP 2: Pay the remainder 3 Days BEFORE statement date.\nRESULT: The bureau records a tiny 2% balance utilization.",
        "c3_t": "THE FINANCIAL PAYOFF",
        "c3_d": "+40 to +80 Point Credit Score Jump in 60 Days\nUnlocks 0% APR Cards and saves thousands on mortgages.",
        "script": "If you pay your credit card bill on the due date, you are quietly hurting your credit score. Banks do not report your balance on your due date, they report it on your statement closing date. That means if your limit is 1,000 dollars and you spend 500, your utilization reports as 50 percent, which tanks your score. Instead, use the 15/3 rule: pay half 15 days before your statement, and the rest 3 days before. Save this reel and follow The Wealth Blueprint.",
        "tags": ["credit score hack", "15 3 credit rule", "credit card glitch", "boost credit score fast", "personal finance"]
    },
    # 3
    {
        "title": "Buy, Borrow, Die: How Billionaires Pay 0% Tax 🛩️🏛️ #TaxLoopholes",
        "cat": "Tax Loopholes",
        "sub": "How the ultra-wealthy fund private jets & mansions without income tax",
        "b1": "warning", "b2": "vault", "b3": "bull",
        "c1_t": "THE W2 TAX TRAP",
        "c1_d": "Selling stocks or real estate triggers 20% to 37% capital gains and income taxes. High earners lose up to half their annual income to federal and state tax collectors.",
        "c2_t": "THE 3-STEP BILLIONAIRE STRATEGY",
        "c2_d": "1. BUY: Acquire high-value appreciating stocks & real estate.\n2. BORROW: Take low-interest loans against your asset portfolio.\n   *Crucial Rule: Bank loans are NOT classified as taxable income!*\n3. DIE: Pass assets to heirs with a stepped-up tax basis.",
        "c3_t": "THE RESULT: 0% LEGAL TAX LIABILITY",
        "c3_d": "Assets stay 100% invested, dividends continue compounding,\nand lifestyle is fully funded with low-interest debt.",
        "script": "Here is how the ultra-rich legally pay almost zero dollars in income tax. They use a three-step formula called Buy, Borrow, Die. Step 1: They buy appreciating assets like stocks and real estate. Step 2: Instead of selling their assets and paying massive capital gains taxes, they take low-interest loans against their assets to fund their lifestyle. Loans are not taxed as income. Step 3: When they pass away, their assets pass to heirs with a stepped-up tax basis. Save this before it gets deleted.",
        "tags": ["buy borrow die", "tax loopholes", "how billionaires avoid tax", "wealth building", "asset protection"]
    },
    # 5
    {
        "title": "High-Yield Savings vs. Big Commercial Banks (Stop Losing) 🏦❌",
        "cat": "Banking Glitch",
        "sub": "How commercial banks quietly steal thousands of dollars in hidden interest",
        "b1": "warning", "b2": "growth", "b3": "money",
        "c1_t": "THE COMMERCIAL BANK MUGGING",
        "c1_d": "Big traditional banks pay an insulting 0.01% APY on checking and savings accounts. On a $20,000 cash balance, they pay you just $2.00 a year while lending your money to home buyers at 7.00%.",
        "c2_t": "THE FDIC HIGH-YIELD VAULT",
        "c2_d": "Move emergency cash to an online High-Yield Savings Account (HYSA):\n• Pays 4.50% - 5.25% APY with zero fees\n• Backed by the exact same $250,000 FDIC government guarantee!",
        "c3_t": "THE IMMEDIATE CASH RECOVERY",
        "c3_d": "Your $20,000 earns $1,050 Every Year on Pure Autopilot\nvs. $2.00 at a legacy commercial bank.",
        "script": "Your regular bank is quietly robbing you. If you keep 20,000 dollars in a traditional bank account, they pay you an insulting 0.01 percent interest. That is two dollars a year, while they lend your money out at 7 percent. Move your cash into a High-Yield Savings Account paying 5 percent APY. It is FDIC insured up to 250,000 dollars, and your money earns over 1,000 dollars a year without doing any work. Stop leaving free money on the table. Follow The Wealth Blueprint.",
        "tags": ["high yield savings", "hysa", "bank fees", "smart money moves", "earn passive income"]
    },
    # 7
    {
        "title": "The $700 Car Payment Trap Destroying Your Wealth 🚗📉 #DebtFree",
        "cat": "Wealth Destroyer",
        "sub": "How financing a depreciating asset steals decades of retirement freedom",
        "b1": "warning", "b2": "growth", "b3": "vault",
        "c1_t": "THE $720/MONTH STATUS TRAP",
        "c1_d": "The average American car payment is $720/month. The car loses 20% of its value the minute it leaves the dealership and 60% over 5 years. You are financing a melting ice cube.",
        "c2_t": "THE S&P 500 COMPOUND ALTERNATIVE",
        "c2_d": "Drive a reliable, paid-off car and invest that exact same $720/month into an S&P 500 index fund averaging 10% annual historical returns:\n• In 5 Years: $56,000 in cash\n• In 10 Years: $148,000 in cash\n• In 15 Years: $305,000 in cash!",
        "c3_t": "THE FREEDOM MATH",
        "c3_d": "$305,000 in Cash Assets vs. a Rusted $4,000 Used Car\nChoose long-term wealth over temporary street flexing.",
        "script": "The average car payment is now 720 dollars a month. That car loses 60 percent of its value in five years. You are literally financing a melting ice cube. If you drive a reliable paid-off car instead and invest that 720 dollars a month into the S&P 500, in 10 years you have 148,000 dollars. In 15 years you have over 300,000 dollars in pure liquid cash. Choose wealth over temporary flexing. Follow for daily financial truths.",
        "tags": ["car payment trap", "depreciating assets", "investing vs car loan", "debt free", "build wealth"]
    },
    # 9
    {
        "title": "Perplexity AI: The Google Search Killer 🔍🤖 #AI #Shorts",
        "cat": "AI Shortcut",
        "sub": "How to bypass 10 blue sponsored SEO links and get instant research",
        "b1": "warning", "b2": "vault", "b3": "bull",
        "c1_t": "THE GOOGLE SEARCH BREAKDOWN",
        "c1_d": "Searching Google today forces you through 4 sponsored ad links, cookie popups, and 2,000-word SEO affiliate blogs before you get an answer.",
        "c2_t": "THE PERPLEXITY AI ENGINE",
        "c2_d": "1. Go to Perplexity.ai (Free to use).\n2. Ask complex queries (e.g. 'Compare the top 3 high-yield accounts with no fees').\n3. Instantly synthesizes live web data and cites direct clickable source links!",
        "c3_t": "HOURS OF RESEARCH IN 5 SECONDS",
        "c3_d": "Answers formatted in clean bullet points with 0 ads.\nTurns research into an instant interactive summary.",
        "script": "Google search is officially broken. When you search for anything, you have to scroll past 4 sponsored ads, cookie popups, and 2,000-word SEO blogs just to find a simple answer. Switch to Perplexity.ai. It searches the live internet, strips out all the ads, and writes you an exact, concise answer with verified clickable source citations in 5 seconds. Save this reel and follow for daily AI shortcuts.",
        "tags": ["perplexity ai", "google search alternative", "best ai tools 2026", "productivity hacks", "tech shortcuts"]
    },
    # 11
    {
        "title": "Gamma AI: Build Decks in 15 Seconds 📊⚡ #PowerPointKiller",
        "cat": "AI Productivity",
        "sub": "Create presentation decks and interactive webpages with one prompt",
        "b1": "warning", "b2": "growth", "b3": "bull",
        "c1_t": "THE 5-HOUR POWERPOINT SLOG",
        "c1_d": "Formatting bullet points, aligning image boxes, and picking color palettes in PowerPoint burns 4 to 6 hours of your weekend for a simple business or school presentation.",
        "c2_t": "THE 1-CLICK GAMMA.APP WORKFLOW",
        "c2_d": "1. Go to Gamma.app (100% Free).\n2. Type one sentence prompt (e.g. 'Q3 Tech Strategy Deck').\n3. Within 15 seconds, AI writes the entire content, formats visual cards, and embeds relevant graphics.",
        "c3_t": "EXPORT IN SECONDS",
        "c3_d": "Generates 15 polished professional slides in 15 seconds.\nExport directly to PowerPoint or PDF with zero watermarks.",
        "script": "Stop spending your entire Sunday night formatting slide decks in PowerPoint. Go to Gamma.app. Type in a single sentence describing what you need, like Q3 Marketing Plan for a Real Estate Brand, and within 15 seconds, the AI writes the content, designs the layouts, and adds professional imagery across a full 15-slide deck ready to present. You can export directly to PowerPoint for free. Save this reel and follow for daily AI shortcuts.",
        "tags": ["gamma app", "ai presentation maker", "powerpoint alternative", "ai productivity", "study hacks"]
    },
    # 13
    {
        "title": "The Subscription Vampire Kill-Switch 💳❌ #MoneyHacks",
        "cat": "Money Defense",
        "sub": "The 5-minute nuclear reset that cancels all forgotten subscriptions",
        "b1": "warning", "b2": "card", "b3": "money",
        "c1_t": "THE HIDDEN $1,200/YEAR CASH BLEED",
        "c1_d": "Free trials make signing up effortless and canceling nearly impossible. The average person wastes over $100 a month on cloud storage, apps, and streaming services they never open.",
        "c2_t": "THE CARD REPLACEMENT KILL-SWITCH",
        "c2_d": "Once every year, log into your banking app and click:\n'Report Debit Card as Damaged / Reissue Card'.\nYour bank sends a new card with a new CVV and expiration date.\n*Every recurring subscription instantly fails!*",
        "c3_t": "EFFORTLESS ANNUAL SAVINGS",
        "c3_d": "You only re-enter card details for the 3 apps you actually use.\nSaves $1,200+ every year with zero awkward cancellation phone calls.",
        "script": "The average person wastes over 100 dollars every month on subscriptions they completely forgot about. Companies design free trials to be easy to start and impossible to remember. Here is the easiest nuclear fix: once every year, report your debit card as damaged and request a replacement card. Your CVV and expiration date change, causing every recurring subscription to instantly fail. You only re-subscribe to the ones you actually use. Follow for daily money shortcuts.",
        "tags": ["cancel subscriptions", "stop wasting money", "money saving hack", "personal finance tips", "wealth habits"]
    },
    # 15
    {
        "title": "Assets vs. Liabilities: The Golden Rule of Wealth ⚖️🏰 #RichDad",
        "cat": "Core Foundation",
        "sub": "The fundamental difference separating the wealthy from the middle class",
        "b1": "warning", "b2": "vault", "b3": "money",
        "c1_t": "THE MIDDLE CLASS LIABILITIES TRAP",
        "c1_d": "Buying liabilities that take money out of your pocket every month while pretending they are assets: leased luxury cars, depreciating watches, and consumer goods.",
        "c2_t": "THE WEALTH BLUEPRINT ASSET DEFINITION",
        "c2_d": "An Asset puts money into your pocket whether you work or not:\n• Dividend-paying index funds\n• Cash-flowing real estate\n• Automated digital software & media channels.",
        "c3_t": "THE GOLDEN TIMELINE",
        "c3_d": "Spend your 20s buying income-generating assets.\nLet your assets pay for your luxury guilt-free.",
        "script": "Robert Kiyosaki said it best in Rich Dad Poor Dad: the rich buy assets, while the poor buy liabilities they think are assets. An asset puts money into your pocket whether you work or not: dividend index funds, cash-flowing real estate, automated software. A liability takes money out of your pocket: your car loan, your subscriptions, luxury items. Spend your twenties buying assets that eventually pay for your luxury. Welcome to The Wealth Blueprint. Follow to join the movement.",
        "tags": ["assets vs liabilities", "rich dad poor dad", "financial literacy", "cash flow assets", "wealth blueprint"]
    },
    # 17
    {
        "title": "The 3-Bank-Account Wealth System 🏦💵 #Budgeting #Shorts",
        "cat": "Automation",
        "sub": "Stop budgeting with willpower — let banking architecture build savings",
        "b1": "warning", "b2": "card", "b3": "money",
        "c1_t": "THE SINGLE CHECKING ACCOUNT DISASTER",
        "c1_d": "Keeping rent, groceries, and fun in one checking account guarantees lifestyle creep. All your cash bleeds together, leaving you with zero savings by the 28th of every single month.",
        "c2_t": "THE AUTOMATED 3-VAULT ARCHITECTURE",
        "c2_d": "VAULT 1: Bills Account (Paycheck lands here, rent & fixed bills auto-pay)\nVAULT 2: Wealth Engine (20% is auto-transferred to index funds)\nVAULT 3: Guilt-Free Card (Fixed weekly allowance for dining & fun).\n*When Vault 3 hits $0, you stop spending!*",
        "c3_t": "THE PAYOFF: 20% GUARANTEED SAVINGS",
        "c3_d": "Automates $10,000 - $25,000 into wealth assets yearly\nwithout tracking a single receipt or spreadsheet.",
        "script": "If you keep all your money in one single checking account, you will accidentally spend it every time. Set up the 3-Account System: Account 1 is your Bills Vault, where your paycheck lands and fixed rent and utilities are auto-paid. Account 2 is your Wealth Engine, where 20 percent is auto-transferred into investments. Account 3 is your Guilt-Free Spending card with a strict weekly allowance. Once Account 3 hits zero, you stop spending. Follow The Wealth Blueprint.",
        "tags": ["3 bank account system", "money management", "budgeting hacks", "automated savings", "financial freedom"]
    },
    # 19
    {
        "title": "The Roth IRA: The 100% Tax-Free Retirement Hack 🛡️📈 #Investing",
        "cat": "Tax Shield",
        "sub": "The government allows you to compound hundreds of thousands with zero tax",
        "b1": "warning", "b2": "growth", "b3": "vault",
        "c1_t": "THE 401K TAX BOMB AT AGE 65",
        "c1_d": "Traditional retirement accounts defer your taxes until retirement. When your portfolio grows to $2 Million, Uncle Sam taxes every single dollar of withdrawal as regular income.",
        "c2_t": "THE ROTH IRA COMPOUND SHIELD",
        "c2_d": "Invest up to $7,000/year after-tax dollars into broad index funds:\n• Dividends compound 100% tax-free for 30 years\n• Every dollar withdrawn after age 59½ is 100% TAX-FREE!",
        "c3_t": "THE MULTI-HUNDRED THOUSAND PAYOFF",
        "c3_d": "$7,000/year from age 20 to 60 @ 10% S&P 500 return\n= $3.1 Million completely tax-free cash.",
        "script": "The government allows you to grow millions of dollars completely tax-free, but only if you use a Roth IRA. In a normal account, you pay taxes on every capital gain and dividend. With a Roth IRA, you invest after-tax money today, and all your compound growth for the next 30 years is 100 percent tax-free. When you withdraw millions in retirement, you pay zero dollars in income tax. Save this reel and start opening your Roth IRA today.",
        "tags": ["roth ira", "tax free investing", "compound interest", "retirement savings", "investing in your 20s"]
    }
]

# Generate additional Global Topics up to 50
for i in range(len(GLOBAL_TOPICS) + 1, 51):
    num = (i * 2) - 1
    GLOBAL_TOPICS.append({
        "title": f"The Millionaire Rule #{i}: Wealth Principle {i} 💡📈 #WealthShorts",
        "cat": "Wealth Principle",
        "sub": f"Core wealth creation principle {i} separating the top 1% from the crowd",
        "b1": "warning", "b2": "growth" if i % 2 == 0 else "vault", "b3": "bull" if i % 3 == 0 else "money",
        "c1_t": "THE CONSUMER HABIT MISTAKE",
        "c1_d": f"Spending your income on depreciating lifestyle upgrades before acquiring income-generating assets delays your financial independence timeline by 10 to 15 years.",
        "c2_t": f"THE 80/20 WEALTH FORMULA #{i}",
        "c2_d": f"1. Automate 20% of your net income into broad index funds on payday.\n2. Reinvest all capital dividends into compounding assets.\n3. Increase your contribution by 5% every time your income grows.",
        "c3_t": "THE COMPOUND MULTIPLIER",
        "c3_d": "Builds $500,000+ in liquid wealth assets over 15 years on pure automation.",
        "script": f"Here is Wealth Principle number {i}. Most people spend their paychecks on depreciating lifestyle upgrades before buying assets. Instead, automate 20 percent of your paycheck directly into low-cost index funds the exact minute your salary hits your account. Reinvest every dividend, and let compounding do the heavy lifting. Save this reel and follow The Wealth Blueprint for daily wealth hacks.",
        "tags": ["wealth principles", "financial freedom", "investing habits", "millionaire mindset", "passive income"]
    })

INDIAN_TOPICS = [
    # 2
    {
        "title": "The RuPay UPI Credit Card Loophole (Earn on Chai & Groceries) ☕💳",
        "cat": "Banking Loophole",
        "sub": "How to earn 3% to 5% cashback rewards on every small QR scan in India",
        "b1": "warning", "b2": "card", "b3": "money",
        "c1_t": "THE DEBIT CARD & CASH DRAIN",
        "c1_d": "Paying for street food, groceries, and daily chai with your savings account or debit card earns you ₹0 cashback. Millions of Indians spend ₹15,000 to ₹30,000 monthly with zero rewards.",
        "c2_t": "THE RUPAY UPI CREDIT CARD SYNC",
        "c2_d": "1. Get a RuPay Credit Card (Tata Neu, HDFC, Kiwi).\n2. Link it directly to Google Pay / PhonePe / Paytm.\n3. Scan ANY local QR code and pay directly from your credit card!\n*Enjoy 45 days interest-free credit + 2% to 5% reward points!*",
        "c3_t": "THE YEARLY PAYOFF: ₹8,000 - ₹15,000 FREE",
        "c3_d": "Earn ₹10,000+ in annual reward points on everyday spending\nwhile keeping your cash in a high-yield account earning interest.",
        "script": "If you are scanning UPI QR codes with your bank account, you are leaving thousands of rupees on the table. Apply for a RuPay Credit Card from HDFC or Tata Neu and link it directly to Google Pay or PhonePe. Now, whenever you buy chai, groceries, or street food, you pay using your RuPay credit card via UPI. You get 45 days of interest-free credit, earn up to 5 percent cashback, and your cash stays in your bank earning interest. Share this with an Indian friend and follow for more.",
        "tags": ["rupay credit card", "upi credit card hack", "earn on upi", "indian banking loopholes", "credit card rewards india"]
    },
    # 4
    {
        "title": "The 15-15-15 Mutual Fund Formula (₹1 Crore Wealth Target) 🚀📊",
        "cat": "Investing Math",
        "sub": "The simple Indian mutual fund blueprint to build ₹1 Crore in 15 years",
        "b1": "warning", "b2": "growth", "b3": "bull",
        "c1_t": "THE FIXED DEPOSIT TAX TRAP IN INDIA",
        "c1_d": "Keeping money in bank FDs earning 6.5% interest: After paying 30% tax slab on interest, your real return is 4.5%. Meanwhile, real Indian inflation is 6%+, shrinking your purchasing power every year.",
        "c2_t": "THE 15-15-15 POWER LAW",
        "c2_d": "Invest ₹15,000 every month via SIP\nFor 15 Years\nIn broad Indian Equity / Nifty 50 Index funds delivering 15% CAGR historical returns.",
        "c3_t": "THE ₹1 CRORE PAYOFF",
        "c3_d": "Total Amount Invested: ₹27 Lakhs\nCompound Growth Added: ₹73 Lakhs (Pure Wealth!)\nFinal Corpus: ₹1.00 Crore+ on Autopilot.",
        "script": "If you want to build 1 Crore rupees in India without taking crazy risks, use the 15-15-15 rule. Invest 15,000 rupees every month for 15 years in a good Nifty 50 or Flexi-Cap mutual fund averaging 15 percent annual returns. In 15 years, your total investment is only 27 Lakhs, but compound interest adds 73 Lakhs of pure profit, handing you over 1 Crore rupees. Time in the market beats timing the market. Save this reel and start your SIP today.",
        "tags": ["15 15 15 rule", "mutual funds sip", "nifty 50 investing", "how to make 1 crore", "indian stock market"]
    },
    # 6
    {
        "title": "Sovereign Gold Bonds (SGB): 0% Capital Gains + 2.5% Free Interest 🪙🏛️",
        "cat": "Gold Loopholes",
        "sub": "Why buying physical gold jewelry is a massive financial mistake in India",
        "b1": "warning", "b2": "vault", "b3": "money",
        "c1_t": "THE JEWELRY MAKING CHARGE SCAM",
        "c1_d": "Buying physical gold jewelry costs 3% GST + 10% to 25% making charges. When you sell, jewelers deduct melting charges, losing you up to 30% of your wealth instantly.",
        "c2_t": "THE RBI SOVEREIGN GOLD BOND HACK",
        "c2_d": "Buy Sovereign Gold Bonds (SGB) issued directly by the Reserve Bank of India:\n• 0% Making Charges & 0% Storage Costs\n• RBI pays you 2.50% Extra Annual Interest directly into your bank account!\n• 100% Tax-Free Capital Gains upon maturity (Section 47)!",
        "c3_t": "THE RESULT: PURE WEALTH MULTIPLIER",
        "c3_d": "Track gold price appreciation + earn 2.5% yearly cash payout\nwith zero risk of theft or bank locker rental fees.",
        "script": "Stop buying physical gold jewelry as an investment in India. When you buy jewelry, you lose up to 25 percent on making charges and GST. Instead, buy Sovereign Gold Bonds issued by the Reserve Bank of India. You pay zero making charges, zero GST, and the RBI pays you an extra 2.5 percent interest directly into your bank account every single year. Best of all, when SGB matures after 8 years, your entire profit is 100 percent tax-free under Indian law. Follow for daily Indian money hacks.",
        "tags": ["sovereign gold bonds", "sgb rbi", "gold investment india", "tax free gold", "smart money india"]
    },
    # 8
    {
        "title": "The CIBIL 750+ Score Algorithm Hack in India 📈💳 #CIBILHack",
        "cat": "Credit Hack",
        "sub": "How to jump your Indian credit score from 650 to 780 in 60 days",
        "b1": "warning", "b2": "card", "b3": "bull",
        "c1_t": "THE 30% UTILIZATION TRAP",
        "c1_d": "Spending more than 30% of your credit card limit triggers an automatic high-risk flag across TransUnion CIBIL, Experian, and CRIF in India, shaving 30 to 50 points off your score.",
        "c2_t": "THE CREDIT MULTIPLIER BLUEPRINT",
        "c2_d": "1. Keep monthly credit card usage strictly under 25% of total limit.\n2. Never close your oldest credit card (maintains credit history age).\n3. Request a credit limit increase every 6 months without taking loans.",
        "c3_t": "THE BORROWING ADVANTAGE",
        "c3_d": "Unlocks Lowest Home Loan Interest Rates (Save ₹5-10 Lakhs)\n+ Instant Pre-Approved Premium Metal Credit Cards.",
        "script": "If your CIBIL score is below 750, Indian banks will charge you higher interest on home and car loans. Here is how to boost it in 60 days. Rule number 1: Never spend more than 30 percent of your total credit limit. If your limit is 1 Lakh, never let your statement exceed 30,000. Rule number 2: Never close your oldest credit card because your credit history length accounts for 15 percent of your score. Follow these two rules and watch your CIBIL cross 780. Save this reel for later.",
        "tags": ["cibil score hack", "boost cibil score", "credit score india", "home loan interest", "cibil score 800"]
    },
    # 10
    {
        "title": "Public Provident Fund (PPF): 0% Tax EEE Goldmine 🛡️💵 #PPF",
        "cat": "Tax Shield",
        "sub": "The government-guaranteed wealth vehicle that beats private bank deposits",
        "b1": "warning", "b2": "vault", "b3": "growth",
        "c1_t": "THE FIXED DEPOSIT TAX DEDUCTION",
        "c1_d": "Interest earned on bank FDs is fully taxable under your income tax slab. If you are in the 30% tax bracket, you lose nearly one-third of all your hard-earned interest to tax TDS.",
        "c2_t": "THE TRIPLE-E TAX EXEMPTION (EEE)",
        "c2_d": "PPF (Public Provident Fund) backed 100% by Government of India:\n• Exempt at Deposit: Up to ₹1.5 Lakh under Section 80C\n• Exempt at Compounding: 7.1% interest compounds tax-free\n• Exempt at Maturity: 100% of final corpus is ZERO TAX!",
        "c3_t": "THE ₹40 LAKH TAX-FREE SHIELD",
        "c3_d": "Deposit ₹1.5 Lakh yearly for 15 years = ₹40.6 Lakhs in pure cash,\ncompletely shielded from creditors and court attachments.",
        "script": "The Indian government gives you a legal tax shelter called PPF, and most people are not using it correctly. PPF has triple E tax status. That means you get a tax deduction when you deposit up to 1.5 Lakh rupees, your 7.1 percent interest compounds completely tax-free every year, and when you withdraw your money at maturity, you pay zero rupees in tax. Even if you go bankrupt, PPF money cannot be attached by any court or creditor. Save this reel and open your PPF account today.",
        "tags": ["ppf tax exemption", "public provident fund", "section 80c", "tax free income india", "safe investment india"]
    },
    # 12
    {
        "title": "Old vs. New Tax Regime: Which One Saves You More? 🧾💡 #TaxIndia",
        "cat": "Tax Strategy",
        "sub": "The exact salary threshold where the Old Regime beats the New Regime in India",
        "b1": "warning", "b2": "vault", "b3": "money",
        "c1_t": "THE DEFAULT TAX TRAP",
        "c1_d": "The government made the New Tax Regime default. If you have a home loan or high rent and blindly choose the default, you could overpay ₹50,000 to ₹1.5 Lakh in unnecessary taxes.",
        "c2_t": "THE ₹3.75 LAKH DEDUCTION RULE",
        "c2_d": "Calculate your total deductions:\n• Standard Deduction: ₹75,000\n• 80C (PPF/EPF/ELSS): ₹1,50,000\n• 80D (Health Insurance): ₹25,000 to ₹50,000\n• Section 24 (Home Loan Interest): Up to ₹2,00,000\n*If total deductions exceed ₹3.75 Lakhs, choose OLD REGIME!*",
        "c3_t": "THE OPTIMAL TAX SAVINGS",
        "c3_d": "Under ₹12 Lakh salary with low deductions: New Regime wins!\nAbove ₹15 Lakh with home loan: Old Regime saves up to ₹1.2 Lakh.",
        "script": "Are you confused between the Old and New Tax Regime? Here is the simple formula to know which one saves you more money. If your total deductions, including home loan interest, 80C, and health insurance, are more than 3.75 Lakh rupees, the Old Tax Regime will save you thousands. But if you have no home loan and don't make investments, the New Tax Regime with the 75,000 standard deduction gives you zero tax up to 7.75 Lakhs. Share this with your colleagues before tax season.",
        "tags": ["old vs new tax regime", "income tax india", "tax saving tips", "salary tax calculator", "save tax on salary"]
    },
    # 14
    {
        "title": "The Bank ULIP Scam vs. Pure Term Insurance ❌🛡️ #InsuranceScam",
        "cat": "Consumer Defense",
        "sub": "Why relationship managers push ULIP policies and why you must avoid them",
        "b1": "warning", "b2": "card", "b3": "vault",
        "c1_t": "THE 'INVESTMENT + INSURANCE' LIE",
        "c1_d": "Bank managers push Unit Linked Insurance Plans (ULIPs) because they earn up to 40% first-year commissions. Heavy mortality charges and fund fees eat up your capital, giving pathetic 5% returns.",
        "c2_t": "THE PURE FINANCIAL SEPARATION RULE",
        "c2_d": "1. NEVER mix investment with insurance!\n2. Buy a Pure Term Insurance Policy: ₹1 Crore life cover for only ₹800 to ₹1,200 a month.\n3. Invest the remaining ₹4,000/month in a Nifty 50 Index Fund.",
        "c3_t": "THE ₹1.5 CRORE PAYOFF DIFFERENCE",
        "c3_d": "Term Plan + Index Fund generates ₹1.5 Crore+ wealth\nvs. a pitiful ₹35 Lakhs from a 20-year bank ULIP policy.",
        "script": "If your bank manager is telling you to buy a policy that gives you both life insurance and investment returns, run away. They are selling you a ULIP because they make huge commissions. ULIPs have massive mortality charges and deliver terrible 5 to 6 percent returns. Instead, buy a pure Term Insurance policy giving your family 1 Crore rupees of protection for just 1,000 rupees a month, and put the rest of your money into Nifty 50 index funds. Never mix insurance with investing. Follow for more truth.",
        "tags": ["ulip scam", "term insurance vs ulip", "insurance tips india", "bank commission trap", "pure term insurance"]
    },
    # 16
    {
        "title": "Free CIBIL Score Check Without Dropping Points (RBI Rule) 🔍📄",
        "cat": "Credit Hack",
        "sub": "How to check your full detailed credit report for free every year by law",
        "b1": "warning", "b2": "card", "b3": "bull",
        "c1_t": "THE THIRD-PARTY APP TRAP",
        "c1_d": "Using sketchy loan apps to check credit scores results in spam loan calls, marketing harassment, and sometimes records an unnecessary hard inquiry that drops your CIBIL score.",
        "c2_t": "THE OFFICIAL RBI MANDATE",
        "c2_d": "By official RBI guidelines, all 4 Indian credit bureaus MUST provide one full free credit report every calendar year:\n• TransUnion CIBIL (cibil.com/free-cibil-score)\n• Experian India\n• CRIF High Mark\n• Equifax India.",
        "c3_t": "SAFE CREDIT TRACKING",
        "c3_d": "100% Soft Inquiry: Never impacts your credit score.\nAllows you to spot and dispute fraudulent loan accounts.",
        "script": "Did you know that by Reserve Bank of India law, you are entitled to one completely free, official credit report every single year? Stop using random third-party apps that spam you with loan calls. Go directly to official websites like cibil.com or experian.in and request your annual free report. Checking your own score is considered a soft inquiry and will never drop your credit score. Check your report today to ensure no fake loan accounts exist in your name. Follow for daily money facts.",
        "tags": ["free cibil score", "rbi credit report rule", "cibil check online", "avoid loan spam", "credit score tracking"]
    },
    # 18
    {
        "title": "Small Finance Banks: 7% Interest vs. 2.7% at SBI/HDFC 🏦📈 #Banking",
        "cat": "Banking Glitch",
        "sub": "How to earn 2.5x higher interest on savings with the exact same DICGC guarantee",
        "b1": "warning", "b2": "growth", "b3": "money",
        "c1_t": "THE BIG BANK LAZINESS",
        "c1_d": "SBI, HDFC, and ICICI pay a pathetic 2.70% to 3.00% on savings accounts. Your idle cash loses value every month to inflation.",
        "c2_t": "THE SMALL FINANCE BANK ALTERNATIVE",
        "c2_d": "RBI-Licensed Small Finance Banks (AU Small Finance, Equitas, Ujjivan):\n• Pay 7.00% to 7.50% on savings account balances\n• Backed by the exact same ₹5 Lakh DICGC RBI Insurance Guarantee as SBI!",
        "c3_t": "THE ZERO-RISK YIELD BOOST",
        "c3_d": "Earn ₹35,000 on a ₹5 Lakh balance instead of ₹13,500 at big banks\nwith identical 100% government safety guarantee.",
        "script": "Why are you keeping your savings in big banks that only pay you 2.7 percent interest? RBI-regulated Small Finance Banks like AU Small Finance, Equitas, and Ujjivan pay up to 7.5 percent interest on your savings account. And here is the secret: they are backed by the exact same 5 Lakh rupee DICGC insurance from the Reserve Bank of India as SBI or HDFC. Keep up to 5 Lakhs per bank to maximize your yield with zero risk. Stop letting big banks underpay you. Follow for more.",
        "tags": ["small finance bank interest", "high interest savings account", "dicgc insurance rbi", "smart banking india", "earn more interest"]
    },
    # 20
    {
        "title": "₹1 Crore Health Insurance Super Top-Up Hack 🏥🛡️ #HealthInsurance",
        "cat": "Insurance Hack",
        "sub": "How to get ₹1 Crore comprehensive health coverage for just ₹10,000/year",
        "b1": "warning", "b2": "vault", "b3": "money",
        "c1_t": "THE ₹5 LAKH BASE POLICY TRAP",
        "c1_d": "With Indian hospital inflation at 14% yearly, a single major surgery or ICU stay for cancer or cardiac treatment easily exceeds ₹15 to ₹25 Lakhs, wiping out your family's savings.",
        "c2_t": "THE DEDUCTIBLE SUPER TOP-UP FORMULA",
        "c2_d": "1. Keep a modest ₹5 Lakh base health policy (or employer cover).\n2. Buy a ₹95 Lakh 'Super Top-Up' policy with a ₹5 Lakh deductible.\n3. Base policy pays the first ₹5 Lakhs, Super Top-Up covers everything up to ₹1 Crore!",
        "c3_t": "UNBEATABLE COST EFFICIENCY",
        "c3_d": "Standard ₹1 Crore Policy: Costs ₹35,000 - ₹50,000/year.\nSuper Top-Up Combination: Costs only ₹10,000 - ₹12,000/year!",
        "script": "A 5 Lakh rupee health insurance policy is no longer enough in India. A single major hospital treatment can easily cost 20 Lakhs. But you do not need to spend 40,000 rupees a year on a 1 Crore policy. Use the Super Top-Up hack. Keep your basic 5 Lakh policy or corporate cover, and buy a 95 Lakh Super Top-Up policy with a 5 Lakh deductible. Your base policy pays the first 5 Lakhs, and the super top-up covers the rest up to 1 Crore. Total cost is only about 10,000 rupees a year. Protect your family today.",
        "tags": ["super top up health insurance", "health insurance hack india", "1 crore health cover", "medical inflation", "save on insurance"]
    }
]

# Generate additional Indian Topics up to 50
for i in range(len(INDIAN_TOPICS) + 1, 51):
    num = i * 2
    INDIAN_TOPICS.append({
        "title": f"Indian Wealth Hack #{i}: Smart Money Blueprint 🇮🇳💰 #IndiaFinance",
        "cat": "India Wealth",
        "sub": f"Financial loophole #{i} designed specifically for Indian taxpayers and investors",
        "b1": "warning", "b2": "growth" if i % 2 == 0 else "vault", "b3": "bull" if i % 3 == 0 else "money",
        "c1_t": "THE COMMON INDIAN MONEY MISTAKE",
        "c1_d": f"Leaving idle money in low-yield savings accounts and traditional fixed deposits destroys wealth due to Indian inflation and 30% slab taxation.",
        "c2_t": f"THE OPTIMIZED ASSET ALLOCATION #{i}",
        "c2_d": f"1. Direct equity / Nifty 50 SIP for long-term 12-14% CAGR compounding.\n2. Utilize Section 80C, 80D, and tax-free government bond shelters.\n3. Keep emergency funds in liquid funds with instant T+1 redemption.",
        "c3_t": "THE LONG-TERM COMPOUND PAYOFF",
        "c3_d": "Builds ₹50 Lakh to ₹1 Crore in tax-optimized wealth over 10 to 15 years.",
        "script": f"Here is Indian Wealth Rule number {i}. Most people in India keep their hard-earned money in traditional bank FDs and savings accounts earning low returns that get eaten away by inflation and taxes. Instead, automate your monthly savings into direct index funds and utilize government tax-free shelters like SGB and PPF. Let compounding work for you on autopilot. Share this with an Indian friend and follow The Wealth Blueprint for daily finance tips.",
        "tags": ["indian wealth blueprint", "smart money india", "mutual funds investing", "tax saving hacks", "financial freedom india"]
    })

# Interleave into 100 entries:
# Slot 1: Global (Odd numbers: 1, 3, 5, ... 99)
# Slot 2: Indian (Even numbers: 2, 4, 6, ... 100)
FULL_CATALOG = []

for idx in range(50):
    g_item = GLOBAL_TOPICS[idx]
    g_id = (idx * 2) + 1
    g_day = idx + 1
    FULL_CATALOG.append({
        "id": g_id,
        "day": g_day,
        "slot": 1,
        "schedule_time": "12:00 PM IST (06:30 UTC)",
        "region": "GLOBAL",
        "voice": "en-US-ChristopherNeural",
        "title": g_item["title"],
        "category": g_item["cat"],
        "sub": g_item["sub"],
        "b1": g_item["b1"], "b2": g_item["b2"], "b3": g_item["b3"],
        "c1_t": g_item["c1_t"], "c1_d": g_item["c1_d"],
        "c2_t": g_item["c2_t"], "c2_d": g_item["c2_d"],
        "c3_t": g_item["c3_t"], "c3_d": g_item["c3_d"],
        "script": g_item["script"],
        "tags": g_item["tags"],
        "pinned_comment": "Which step in this blueprint surprised you most? Comment below and we'll send you our 0% Interest Card Masterlist!"
    })

    in_item = INDIAN_TOPICS[idx]
    in_id = (idx * 2) + 2
    in_day = idx + 1
    FULL_CATALOG.append({
        "id": in_id,
        "day": in_day,
        "slot": 2,
        "schedule_time": "08:00 PM IST (14:30 UTC)",
        "region": "INDIA",
        "voice": "en-IN-PrabhatNeural",
        "title": in_item["title"],
        "category": in_item["cat"],
        "sub": in_item["sub"],
        "b1": in_item["b1"], "b2": in_item["b2"], "b3": in_item["b3"],
        "c1_t": in_item["c1_t"], "c1_d": in_item["c1_d"],
        "c2_t": in_item["c2_t"], "c2_d": in_item["c2_d"],
        "c3_t": in_item["c3_t"], "c3_d": in_item["c3_d"],
        "script": in_item["script"],
        "tags": in_item["tags"],
        "pinned_comment": "Which Indian banking loophole or investment strategy are you using first? Comment below and follow @TheWealthBlueprint!"
    })

# Write to content_catalog_100.py
header = '''"""
100-Video Master Content Catalog (50 Days, 2 Videos/Day)
Slot 1: Global High-RPM Wealth & AI Loopholes (12:00 PM IST)
Slot 2: Indian Personal Finance, Banking & Tax Systems (08:00 PM IST)
"""

CATALOG_100 = '''

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(header + json.dumps(FULL_CATALOG, indent=2) + "\n")

print(f"Generated {len(FULL_CATALOG)} entries in {OUTPUT_FILE}")
