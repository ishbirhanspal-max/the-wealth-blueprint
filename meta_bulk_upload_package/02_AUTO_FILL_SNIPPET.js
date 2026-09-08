// ============================================================
// META BUSINESS SUITE 1-CLICK CAPTION AUTO-FILLER
// 1. Open DevTools on Meta Business Suite (Press F12 -> Console)
// 2. Paste this entire snippet and press Enter!
// ============================================================
(function() {
    const captions = [
        `The CIBIL 750+ Score Algorithm Hack in India 📈💳 #CIBILHack\n\nHow to jump your Indian credit score from 650 to 780 in 60 days\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `Perplexity AI: The Google Search Killer 🔍🤖 #AI #Shorts\n\nHow to bypass 10 blue sponsored SEO links and get instant research\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `Public Provident Fund (PPF): 0% Tax EEE Goldmine 🛡️💵 #PPF\n\nThe government-guaranteed wealth vehicle that beats private bank deposits\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `Gamma AI: Build Decks in 15 Seconds 📊⚡ #PowerPointKiller\n\nCreate presentation decks and interactive webpages with one prompt\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `Old vs. New Tax Regime: Which One Saves You More? 🧾💡 #TaxIndia\n\nThe exact salary threshold where the Old Regime beats the New Regime in India\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `The Subscription Vampire Kill-Switch 💳❌ #MoneyHacks\n\nThe 5-minute nuclear reset that cancels all forgotten subscriptions\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `The Bank ULIP Scam vs. Pure Term Insurance ❌🛡️ #InsuranceScam\n\nWhy relationship managers push ULIP policies and why you must avoid them\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `Assets vs. Liabilities: The Golden Rule of Wealth ⚖️🏰 #RichDad\n\nThe fundamental difference separating the wealthy from the middle class\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `Free CIBIL Score Check Without Dropping Points (RBI Rule) 🔍📄\n\nHow to check your full detailed credit report for free every year by law\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `The 3-Bank-Account Wealth System 🏦💵 #Budgeting #Shorts\n\nStop budgeting with willpower — let banking architecture build savings\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `Small Finance Banks: 7% Interest vs. 2.7% at SBI/HDFC 🏦📈 #Banking\n\nHow to earn 2.5x higher interest on savings with the exact same DICGC guarantee\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `The Roth IRA: The 100% Tax-Free Retirement Hack 🛡️📈 #Investing\n\nThe government allows you to compound hundreds of thousands with zero tax\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `₹1 Crore Health Insurance Super Top-Up Hack 🏥🛡️ #HealthInsurance\n\nHow to get ₹1 Crore comprehensive health coverage for just ₹10,000/year\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `The FDIC $250,000 Loophole (Insure Up to $3 Million) 🏦🛡️ #BankingSecrets\n\nHow high-net-worth individuals insure millions without opening 12 different banks\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`,
        `The HUF Tax Loophole: Save ₹1,50,000+ Every Year 🇮🇳🏛️ #TaxSavings\n\nHow Indian business owners and families legally create a second tax-free identity\n\nFollow @thewealthblueprint10 for daily wealth loopholes!\n\n#wealth #finance #moneyhacks #investing #smartmoney`
    ];

    // Find all caption inputs or contenteditable containers in Meta Bulk Upload table
    const inputs = document.querySelectorAll('div[contenteditable="true"], textarea[placeholder*="caption" i], textarea[aria-label*="caption" i], textarea');
    let filled = 0;

    inputs.forEach((input, index) => {
        if (index < captions.length) {
            const cap = captions[index];
            if (input.tagName.toLowerCase() === 'textarea') {
                input.value = cap;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            } else {
                input.focus();
                input.innerText = cap;
                input.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText' }));
            }
            filled++;
        }
    });

    console.log(`[The Wealth Blueprint] Successfully auto-filled ${filled} reel captions!`);
    alert(`Successfully auto-filled ${filled} reel captions! Now select schedule times and click Schedule.`);
})();
