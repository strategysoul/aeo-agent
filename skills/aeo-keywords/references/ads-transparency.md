# Competitor ads: Google Ads Transparency Center

Used by the research step (competitor offers and positioning) and the keyword step (keyword ideas from ad copy). Free, public, no login: <https://adstransparency.google.com>.

## What it shows and what it does not

- Shows, per advertiser: each ad's text (headlines, descriptions), images or video, the landing page, format (text, image, video), where it ran (Google Search, YouTube, Shopping, Maps, Play), regions, and the dates it was first and last shown.
- Does not show the keywords an ad targets, bids, spend or impressions (except for political ads in some regions).

So every keyword taken from an ad is `method: inferred`. The ad shows that a competitor pays to say something, not which search it pays for.

## Which competitors

The top 3–5 `direct` competitors in `research/competitors.csv`, by `keywords_in_top10`. Skip competitors listed under `## Not interested` in `decisions.md`. Region: `countries[0]`. Period: the last 30 days. If a competitor shows no ads there, record "no ads in <region>, last 30 days" and move on.

## How to read it, in order

1. **Claude in Chrome** (`chrome` available). Open the site, type the competitor's domain into the search box, and open the matching advertiser. Set the region and the last 30 days. Read the page text; open single ads only to read text that is cut off. At most 30 ads per competitor, text ads first.
2. **DataForSEO** (`dataforseo` available). Search its docs (`docs_search`) for Google Ads Transparency or ads advertiser endpoints. Use them only if the docs list them, read the request fields there, and estimate the cost from the `user_data` price table within the run budget.
3. **Web fetch.** The site needs JavaScript, so a plain fetch usually returns an empty page. Try once; if no ads are in the text, mark the need as not covered.

None worked: say "Competitor ads not checked: needs Claude in Chrome" in the step's output, and continue.

Never click an ad's link from the Transparency Center or from Google results (the advertiser pays for clicks). Open landing pages by typing or fetching the URL. Never log in. If Google shows a CAPTCHA, stop and tell the user; never try to solve it.

## What to save

Reuse a file less than 30 days old from either step instead of reading again. Otherwise save to `<step folder>/raw/<today>/ads-transparency.csv` (`research/` or `keywords/`):

```
competitor_domain,advertiser_name,format,platform,headline,description,landing_url,first_shown,last_shown,region,ad_url,source,method,record_date,run_id
```

`source`: `chrome:adstransparency.google.com`, `dataforseo`, or `https://adstransparency.google.com/…`. `method: measured` for the ad text and dates.

## Using it in research

Add to the brief, under "3. Competitors and alternatives", one line per competitor: number of ads seen, the main offers and claims (price, discount, free shipping, guarantees), and the products or audiences they name, with the ad URL and date. Ads running for more than 90 days with the same message are probably working for that competitor; say so.

## Using it for keywords

From each ad's headlines, descriptions and landing-page path, take the phrases a customer could search for: product and category names, audiences, problems, features, and comparison wording. Leave out slogans, prices and calls to action.

- Normalise as in the skill, and write each phrase in its natural search form ("waterproof trail shoes for wide feet", not "Shop Our Wide Waterproof Range").
- `origin: ads:<competitor domain>`, `method: inferred`, `source` as above. Put `ad_last_shown: <date>` in `notes`.
- Leave `volume`, `difficulty` and `intent` empty; the volume lookup in the plan fills them like any other keyword.
- Phrases with a competitor's brand go to comparison topics, as scoring.md says.
