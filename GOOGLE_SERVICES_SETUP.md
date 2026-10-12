# Google Search Console and AdSense account setup

The site code is ready for crawling, indexing, and AdSense review. Account-specific values are intentionally not guessed or committed as placeholders.

## Search Console

1. Add `admissiontestbd.online` as a **Domain property** in Google Search Console.
2. Add the TXT record Google supplies to the domain's DNS and complete verification.
3. In **Sitemaps**, submit `https://www.admissiontestbd.online/sitemap.xml`.
4. Inspect `https://www.admissiontestbd.online/` and request indexing once after this release is live.

If a URL-prefix property must be verified with an HTML meta tag instead of DNS, copy only the `content` token from Google and run:

```bash
python3 configure_google_services.py --search-console-token YOUR_REAL_TOKEN
```

Commit and deploy the resulting mirrored `index.html` files.

## AdSense

1. Add `www.admissiontestbd.online` in AdSense and copy the site's real publisher ID. It has the format `ca-pub-` followed by 16 digits.
2. Run the command below with the real value:

```bash
python3 configure_google_services.py --publisher-id ca-pub-1234567890123456
```

3. Commit and deploy the generated changes. The command adds the AdSense account meta tag, the asynchronous Auto ads loader, and valid mirrored `ads.txt` files. It rejects placeholders and malformed IDs.
4. Open `https://www.admissiontestbd.online/ads.txt` after deployment and confirm the publisher number matches the AdSense account.
5. In AdSense **Privacy & messaging**, publish Google's certified consent message for visitors in the EEA, UK, and Switzerland before serving personalized ads there.
6. Request site review. Enable Auto ads only after the account and site are approved.

Do not click live ads, ask visitors to click ads, place ads where they can be mistaken for answer buttons, or add more ads than educational content.
