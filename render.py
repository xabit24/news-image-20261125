#!/usr/bin/env python3
"""Render the 25 Nov 2026 world-news summary image (1024x1024 PNG).

Design: newspaper front page. Masthead, one lead story (the Iowa
lead-azide detonation, scheduled for today) with a drawn warning
visual, then 36 short stories in a two-column grid — 37 verified
stories in all, each one reported on Wednesday 25 November 2026
by Reuters, BBC, The Guardian, Variety, TechCrunch, Mongabay,
Engadget, ABC Australia, The Hindu BusinessLine, SciTechDaily,
Bar and Bench, DW or the outlets' own wires. No story in the grid
is dated 24 November: where an aggregator listed a 24 November
wire under a 25 November headline, the item was left out.

Layout: PIL draws text from the top of the font's em box, which is
about 1.17x the point size, so the vertical rhythm below is sized
from the em box. Grid rows are one headline line plus one summary
line; headlines and summaries are kept short by construction and
the renderer clips anything that still overflows, so no text ever
spills into the next row.

Deterministic: fixed layout, fixed fonts, no timestamps, no
randomness, no network. Pillow writes no metadata into the PNG.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "news.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (22, 21, 19)
GREY = (92, 88, 80)
RED = (179, 39, 30)
NAVY = (29, 78, 137)
TEAL = (14, 107, 92)
AMBER = (178, 118, 12)
RULE = (180, 172, 156)
PANEL = (232, 226, 210)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, face, max_w):
    """Clip text with an ellipsis so it never exceeds max_w."""
    if draw.textlength(text, font=face) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=face) > max_w:
        text = text[:-1]
    return text + "…"


def wrap(draw, text, face, max_w):
    """Greedy word wrap to a pixel width."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=face) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# (kicker, colour, headline, summary)
GRID = [
    ("TARIFFS · UNITED STATES", RED, "US set to unveil new tariffs",
     "Probe into excess factory capacity in 16 trading partners nears release."),
    ("AUSTRALIA · APOLOGY", TEAL, "Australia says sorry to LGBTQ veterans",
     "Canberra apologises for decades of discrimination in the military."),
    ("MARKETS · GOLD", AMBER, "Gold dips before US inflation data",
     "Prices edge lower as traders await October PCE figures due today."),
    ("ENERGY · BRITAIN", RED, "UK households brace for higher bills",
     "Ofgem's new price cap pushes gas prices up sharply from January."),
    ("INDIA · PRICES", AMBER, "Food prices squeeze Indian homes",
     "Rising food costs bite household budgets as inflation stays high."),
    ("AUSTRALIA · COURTS", NAVY, "Killer cop guilty of double murder",
     "Beau Lamarre-Condon convicted of murdering Jesse Baird and Luke Davies."),
    ("OBITUARY · FILM", GREY, "Oscar designer Philip Rosenberg dies at 91",
     "Production designer of 'All That Jazz' and 'Network' dies aged 91."),
    ("BRITAIN · POLICE", NAVY, "Met culture review: little has changed",
     "Latest review finds the force has barely moved since the last inquiry."),
    ("HEALTH · BRITAIN", TEAL, "England's frailty gap widest of 31 nations",
     "Study finds England has the largest frailty gap among 31 countries."),
    ("CLIMATE · UNITED STATES", TEAL, "Scientists urge 'no' to permits bill",
     "120+ climate scientists warn the Baaja bill locks in fossil fuels."),
    ("MARKETS · AI", RED, "Anthropic shares slide below IPO price",
     "Stock falls under $83 as the AI selloff resumes on Wall Street."),
    ("MARKETS · AI", NAVY, "Nvidia, Anthropic end sharply lower",
     "Tech stocks stumble as the AI rally fades; Nasdaq falls again."),
    ("MARKETS · ASIA", AMBER, "Asia's AI rally faces a tougher road",
     "Huang's comeback lifts chip stocks, but analysts warn the rally may fade."),
    ("TECH · NVIDIA", NAVY, "Nvidia a 'detriment' to US industry",
     "Yale's Sonnenfeld says the chip giant hurts American industrial might."),
    ("TECH · NVIDIA", RED, "Trump: pardoning Huang 'an option'",
     "President floats a pardon for Nvidia's CEO amid the federal probe."),
    ("SCIENCE · WILDLIFE", TEAL, "Species down to 50 can still recover",
     "Study: tiny populations can bounce back, but rarely without human help."),
    ("CULTURE · MUSIC", AMBER, "Randy Newman to get lifetime award",
     "Songwriter honoured by the Society of Composers & Lyricists."),
    ("CULTURE · FILM", NAVY, "'One Last Order' streams on Netflix",
     "Viral documentary follows beloved drive-thru worker Sighle Williams."),
    ("TECH · APPLE", GREY, "Apple Watch feature meets CarPlay",
     "A handy Watch feature now works seamlessly with Apple CarPlay."),
    ("RIGHTS · UNITED NATIONS", RED, "UN day against violence on women",
     "Today marks the day for the elimination of violence against women."),
    ("EUROPE · SUMMIT", NAVY, "EU–Western Balkans summit in Brussels",
     "Leaders meet in Brussels as enlargement and security top the agenda."),
    ("ECONOMY · UNITED STATES", AMBER, "US inflation and GDP data due today",
     "October PCE and the second Q3 GDP reading land at 13:30 GMT."),
    ("AUSTRALIA · FINANCE", RED, "Auditors named in 'shameful' ASIC list",
     "Deloitte, EY, PwC and KPMG face sweeping reform calls over complaints."),
    ("CULTURE · MEDIA", NAVY, "Taylor Swift exposé sparks backlash",
     "Vanity Fair's Swift piece draws fire from fans and critics alike."),
    ("AUSTRALIA · MONEY", TEAL, "Is your super safe in a Wall St crash?",
     "ABC asks whether retirement savings would survive a market rout."),
    ("WEATHER · BRITAIN", GREY, "Will it be a white Christmas?",
     "BBC weighs the odds of snow as the festive season approaches."),
    ("INDIA · BUSINESS", AMBER, "Tata Steel in ₹32,266 crore deal",
     "Steel giant proposes buying a 52.38% stake in APL Apollo Tubes."),
    ("TECH · CHIPS", RED, "US blacklists Megaspeed over Nvidia chips",
     "Singapore firm cut off amid fears of AI chip diversion to China."),
    ("INDIA · TELECOM", NAVY, "Jio scraps daily data cap",
     "Reliance Jio drops the 2.5GB daily limit on select plans from Nov 24."),
    ("INDIA · TECH", GREY, "Google Cloud India cuts 30 roles",
     "Firm denies mass layoffs, confirms a small round of job cuts."),
    ("SCIENCE · SPACE", TEAL, "'Star system that should not exist'",
     "Astronomers find a cosmic mystery just 28 light-years away."),
    ("INDIA · COURTS", NAVY, "Collegium picks new Jharkhand chief",
     "Supreme Court collegium recommends Vibhu Bakhru as high court chief."),
    ("EUROPE · SANCTIONS", AMBER, "EU envoys debate Russia sanctions",
     "Ambassadors hold first talks on the 22nd package today in Brussels."),
    ("SPORT · FOOTBALL", NAVY, "Champions League night in Bruges",
     "Club Brugge host Liverpool as the league phase continues tonight."),
    ("AUSTRALIA · POLITICS", TEAL, "Why that Bowen photo captivates",
     "Guardian on the crowded Chris Bowen scowling photo going viral."),
    ("INDIA · DEMOCRACY", RED, "India 'deepens authoritarian slide'",
     "A new report finds democratic decline deepening under Modi. (DW)"),
]


def masthead(d):
    mx = 36
    d.line([(mx, 28), (W - mx, 28)], fill=INK, width=4)
    title = "THE WORLD TODAY"
    face = load(SERIF, 66)
    d.text(((W - d.textlength(title, font=face)) / 2, 32), title,
           font=face, fill=INK)
    meta = load(BOLD, 20)
    d.text((mx, 108), "WEDNESDAY, 25 NOVEMBER 2026", font=meta, fill=INK)
    right = "37 STORIES  ·  ONE IMAGE"
    d.text((W - mx - d.textlength(right, font=meta), 108), right,
           font=meta, fill=RED)
    d.line([(mx, 134), (W - mx, 134)], fill=INK, width=3)


def lead(d, img):
    mx = 36
    y = 148
    kick = load(BOLD, 21)
    d.text((mx, y), "IOWA  ·  UNITED STATES", font=kick, fill=RED)
    h1 = load(BOLD, 56)
    d.text((mx, y + 26), "IOWA BRACES FOR", font=h1, fill=INK)
    d.text((mx, y + 86), "TOXIC BLAST", font=h1, fill=RED)
    dek = ("Army to detonate 68 barrels of unstable lead explosive "
           "today, the day before Thanksgiving.")
    body = load(REG, 21)
    yy = y + 158
    for line in wrap(d, dek, body, 590):
        d.text((mx, yy), line, font=body, fill=INK)
        yy += 26
    side = load(BOLD, 17)
    d.text((mx, yy + 6),
           "FEMA tells residents to stay indoors; courts cleared the blast.",
           font=side, fill=TEAL)

    # warning panel: triangle, barrels, blast burst
    x0, y0, x1, y1 = 668, 148, 988, 384
    d.rounded_rectangle([x0, y0, x1, y1], radius=16,
                        fill=PANEL, outline=INK, width=3)
    cx, cy = 828, 250
    d.polygon([(cx, cy - 62), (cx - 66, cy + 48), (cx + 66, cy + 48)],
              fill=(255, 196, 0), outline=INK, width=4)
    bang = load(BOLD, 64)
    d.text((cx, cy + 8), "!", font=bang, fill=INK, anchor="mm")
    # three barrels below the triangle
    for i, bx in enumerate((716, 796, 876)):
        d.rounded_rectangle([bx, 318, bx + 56, 368], radius=6,
                            fill=NAVY if i != 1 else RED, outline=INK, width=2)
        d.line([(bx, 334), (bx + 56, 334)], fill=(255, 255, 255), width=2)
        d.line([(bx, 352), (bx + 56, 352)], fill=(255, 255, 255), width=2)


def grid(d):
    mx = 36
    gutter = 24
    col_w = (W - 2 * mx - gutter) // 2
    row_h = 32
    top = 402
    head_f = load(BOLD, 15)
    sum_f = load(REG, 12)
    for idx, (kicker, colour, headline, summary) in enumerate(GRID):
        col = idx % 2
        row = idx // 2
        x = mx + col * (col_w + gutter)
        y = top + row * row_h
        tag = kicker.split(" · ")[0] + " — "
        tw = d.textlength(tag, font=head_f)
        d.text((x, y), tag, font=head_f, fill=colour)
        d.text((x + tw, y), fit(d, headline, head_f, col_w - tw),
               font=head_f, fill=INK)
        d.text((x, y + 17), fit(d, summary, sum_f, col_w),
               font=sum_f, fill=GREY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    lead(d, img)
    d = ImageDraw.Draw(img)
    d.line([(36, 392), (W - 36, 392)], fill=INK, width=3)
    grid(d)
    foot = load(REG, 15)
    note = "Sources: Reuters · BBC · The Guardian · Variety · TechCrunch · Mongabay · Engadget · ABC · Hindu BusinessLine · SciTechDaily · DW"
    d.text(((W - d.textlength(note, font=foot)) / 2, 990), note,
           font=foot, fill=GREY)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    print(f"saved {OUT}")


if __name__ == "__main__":
    build()
