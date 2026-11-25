# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/xabit24/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/xabit24/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

The World Today — a newspaper front page summing up Wednesday 25 November 2026 in 37 verified stories: the Iowa lead-azide detonation leads, followed by 36 short stories from every region — tariffs, markets, science, culture and sport. Drawn in code with Pillow; `main.ts` checks the image against the competition's limits and copies it to `/output/entry.png`.

## Run it

```sh
python3 render.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

Entered on [make.fun](https://make.fun/?ref=d2r4akr8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards

## The stories

**Lead — Iowa, United States:** Iowa braces for toxic blast. The US Army detonates 68 barrels of unstable lead explosive today, the day before Thanksgiving; FEMA tells residents to stay indoors.

**The 36 in the grid:**

- US set to unveil new tariffs
- Australia says sorry to LGBTQ veterans
- Gold dips before US inflation data
- UK households brace for higher bills
- Food prices squeeze Indian homes
- Killer cop guilty of double murder
- Oscar designer Philip Rosenberg dies at 91
- Met culture review: little has changed
- England's frailty gap widest of 31 nations
- Scientists urge 'no' to permits bill
- Anthropic shares slide below IPO price
- Nvidia, Anthropic end sharply lower
- Asia's AI rally faces a tougher road
- Nvidia a 'detriment' to US industry
- Trump: pardoning Huang 'an option'
- Species down to 50 can still recover
- Randy Newman to get lifetime award
- 'One Last Order' streams on Netflix
- Apple Watch feature meets CarPlay
- UN day against violence on women
- EU–Western Balkans summit in Brussels
- US inflation and GDP data due today
- Auditors named in 'shameful' ASIC list
- Taylor Swift exposé sparks backlash
- Is your super safe in a Wall St crash?
- Will it be a white Christmas?
- Tata Steel in ₹32,266 crore deal
- US blacklists Megaspeed over Nvidia chips
- Jio scraps daily data cap
- Google Cloud India cuts 30 roles
- 'Star system that should not exist'
- Collegium picks new Jharkhand chief
- EU envoys debate Russia sanctions
- Champions League night in Bruges
- Why that Bowen photo captivates
- India 'deepens authoritarian slide'

## Sources

Every item was published or first reported on Wednesday 25 November 2026, verified against Reuters, BBC, The Guardian, Variety, TechCrunch, Mongabay, Engadget, ABC Australia, The Hindu BusinessLine, SciTechDaily, Bar and Bench and DW. Nothing is invented, and no 24 November story is presented as a 25 November story: where a wire was dated 24 November it was left out, even when an aggregator listed it under a 25 November headline. The image itself carries the outlet set in its footer.

## How it is made

`render.py` draws the whole page with Pillow at 1024×1024 — masthead, lead story with a drawn warning visual, and the 36-story grid — from fixed text and fixed fonts, so the output is byte-for-byte deterministic. `main.ts` (Node 22, standard library only) validates the PNG signature, size (≤1 MiB) and dimensions (≤1024×1024), then copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`. No network, no timestamps, no randomness.
