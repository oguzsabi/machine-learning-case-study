import glassdoor_scraper as gs

df = gs.get_jobs('data scientist', 1000, True)

df.to_csv('glassdoor_jobs.csv', index=False)