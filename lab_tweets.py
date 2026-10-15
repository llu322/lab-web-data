# Load master_2009.json through master_2018.json, analyze the tweets, and make a bar chart.
# Follow the linked course assignment in README.md.

import json
import matplotlib.pyplot as plt

# Load all ten files, keeping every record.
tweets = []

for year in range(2009, 2019):
    filename = f"master_{year}.json"
    with open(filename, encoding="utf-8") as f:
        tweets.extend(json.load(f))

total = len(tweets)
print("Total tweets:", total)

# Inspect a record to see its fields.
if tweets:
    print("\nFirst record:", tweets[0])

phrases = [
    "obama",
    "trump",
    "mexico",
    "russia",
    "fake news",
    "wall",
    "america",
    "jobs"
]

counts = {}
percentages = {}

for phrase in phrases:
    count = 0

    for tweet in tweets:
        if "full_text" in tweet:
            message = tweet["full_text"]
        else:
            message = tweet["text"]

        if phrase.lower() in message.lower():
            count += 1

    counts[phrase] = count
    percentages[phrase] = count / total * 100 if total else 0

print("\nPhrase counts:")
for phrase in phrases:
    print(f"{phrase}: {counts[phrase]}")

# Print a Markdown table to copy into README.md.
print("\n|            phrase | percent of tweets |")
print("| ----------------: | ----------------- |")

for phrase in phrases:
    print(f"| {phrase:>17} | {percentages[phrase]:05.2f}             |")

# Save a labeled bar chart.
plt.figure(figsize=(9, 6))
plt.barh(phrases, [counts[phrase] for phrase in phrases])
plt.xlabel("Number of tweets")
plt.ylabel("Phrase")
plt.title("Phrase frequency in the 2009–2018 tweet archive")
plt.tight_layout()
plt.savefig("tweets.png")
plt.close()