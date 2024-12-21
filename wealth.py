import feedparser
import os
from datetime import datetime, timedelta
# Base YouTube URL for channels
BASE_YOUTUBE_URL = "https://www.youtube.com/feeds/videos.xml?channel_id="

# Define YouTube channels by categories
youtube_channels = {
    "Wealth Building and Financial Strategy": [
        "UCLXQalldcm6gMYMQfLMliww",  # James Shack
        "UColNfZXzL946wNgxPGWst1A",  # Khe Hy - RadReads
        "UCcefcZRL2oaA_uBNeo5UOWg",  # Y Combinator
        "UCTlYY_YSD1Bh7SZo9bwvv0g",  # Dhande Ki Baat
        "UCwVEhEzsjLym_u1he4XWFkg",  # Finance With Sharan
        "UCFBpVaKCC0ajGps1vf0AgBg",  # Humphrey Yang
        "UC7ZddA__ewP3AtDefjl_tWg",  # I Will Teach You To Be Rich
        "UCxgAuX3XZROujMmGphN_scA",  # Mark Tilbury
        "UC39PLqUmy-AKK5HGYYfwFYw",  # MeaningfulMoney
        "UCb3s91SgcrCcJstffub2Nbw",  # Paisa Vaisa with Anupam Gupta
        "UCRzYN32xtBf3Yxsx5BvJWJw",  # warikoo
        "UCPa0bvFsR1mbBpk5mIPFGLA",  # Vincent Chan
        "UCUUlw3anBIkbW9W44Y-eURw",  # Zero1 by Zerodha
        "UCggPd3Vf9ooG2r4I_ZNWBzA",  # Wint Wealth
        "UCEPWaN-XiZqEQAPiwvBa3ng",  # Tae Kim - Financial Tortoise
        "UCiq1FIgtEK7LRAOB1JXTPig",  # Silicon Valley Girl
        "UCIbslwukNCyVp-XMz_2-gmw",  # Rose Han
        "UCnwHwonddN9cNsIUz6pzeYw",  # Rishabh Dev
        "UCBI57iTXtmJoaI6Ht7MgcfA",  # 1% Club
    ],
    "Finance & Stock Market": [
        "UCZ-MAJzfoLEBUsWprGCFzxw",  # Ashish StockTalk
        "UCqW8jxh4tH1Z1sWPbkGWL4g",  # Akshat Shrivastava
        "UCnHwry_kfr6oJ3W3nMpV6Nw",  # Angel investments
        "UCN5qpJ_OZl53SfMbVPjA6sg",  # Goela School of Finance LLP
        "UCcIvNGMBSQWwo1v3n-ZRBCw",  # Humbled Trader
        "UCiAfu64x7lTXcgzef7Z-PnA",  # Nataraj Malavade - Kannada
        "UCEAAzv2OBqxsSczKJ2QZyGQ",  # Pushkar Raj Thakur: Stock Market Educator
        "UCbqjNSNncLmHIOfoCgSzhoQ",  # Wizard Trader
        "UCir8ZEhgIOLY__2tN1Pi0ig",  # Umar Ashraf
        "UCoi7mlbUebBpQmDtB3L557A",  # SIDDHARTH BHANUSHALI
        "UCTR1Tk8SaMO9qw930kIOMHQ",  # Sagar Sinha

    ],
    "Financial Literacy and Advisory": [
        "UCsNxHPbaCWL1tKw2hxGQD6g",  # Asset Yogi
        "UCvgu3umoosQwH-1LJpu-iEQ",  # Banking Baba
        "UCdvOCtR3a9ICLAw0DD3DpXg",  # bekifaayati
        "UCE43WLnnJlOaC45v3ZFPEDQ",  # Every Paisa Matters
        "UCD3U3VXjTWe27V5XDf2jvJQ",  # ffreedom app - Money (English)
        "UCfMEz1FHN9aQNY2Gtt1BGXw",  # ffreedom app - Money (Kannada)
        "UCVOTBwF0vnSxMRIbfSE_K_g",  # Labour Law Advisor
        "UCqBNPrKu8CZjLzgzf1gbJIA",  # Post Office Pro
        "UC0Fxs5vOGxWQqcuNjB6JZNw",  # Satvinder Narwal
    ]
}

# Function to get videos from an RSS feed
def get_videos_from_rss(rss_url):
    try:
        feed = feedparser.parse(rss_url)
        if feed.bozo:
            raise ValueError(f"Failed to parse feed from {rss_url}. Error: {feed.bozo_exception}")

        today = datetime.now()

        # Calculate the start of the Monday two weeks ago and the end of the last Sunday
        # Monday is weekday 0, Sunday is weekday 6
        last_monday = today - timedelta(days=today.weekday() + 14)  # Start of Monday two weeks ago
        last_sunday = last_monday + timedelta(days=13, hours=23, minutes=59, seconds=59)  # End of Sunday of the second week

        videos = []

        for entry in feed.entries:
            try:
                published = datetime(*entry.published_parsed[:6])
                thumbnail_url = entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else None

                # Check if the video was published between last Monday and last Sunday
                if last_monday <= published <= last_sunday:
                    videos.append({
                        'title': entry.title,
                        'link': entry.link,
                        'published': published,
                        'channel': feed.feed.title,
                        'thumbnail': thumbnail_url
                    })
            except Exception as e:
                print(f"Error processing entry: {e}")

        return videos
    except Exception as e:
        print(f"Error retrieving videos from {rss_url}: {e}")
        return []

# Aggregate videos by categories
all_videos_by_category = {}
for category, channels in youtube_channels.items():
    category_videos = []
    for channel_id in channels:
        rss_url = BASE_YOUTUBE_URL + channel_id
        category_videos.extend(get_videos_from_rss(rss_url))
    all_videos_by_category[category] = sorted(category_videos, key=lambda x: x['published'], reverse=True)

# Create HTML content with navbar and video cards
html_content = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Videos by Category</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Kalam:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }

        h2 {
            text-align: center;
            font-family: 'Kalam', cursive;
            color: #333;
            margin-bottom: 20px;
        }

        .navbar {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        .navbar a {
            margin: 0 15px;
            text-decoration: none;
            font-weight: 600;
            color: #333;
        }

        .navbar a:hover {
            color: #007bff;
        }

        .video-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }

        .card {
            border: 1px solid #ddd;
            border-radius: 8px;  /* Reduced border-radius for a sharper look */
            width: 250px;
            background-color: #fff;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            text-decoration: none;
            color: black;
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .thumbnail {
            width: 100%;
            height: 150px;
            object-fit: cover;
        }

        .video-title {
            font-weight: 600;
            font-size: 1em;  /* Slightly reduced font size for titles */
            margin: 10px 0;
            padding: 0 10px;
        }

        .channel, .published {
            font-size: 0.9em;
            color: gray;
            margin-bottom: 8px;
        }

        .published {
            margin-bottom: 12px;
        }

        .category {
            margin-top: 30px;
        }

        h4{
            text-align: center;
            padding:10px;
            background-color: grey;
            color:white;
        }
    </style>
</head>
<body>

<h2>YouTube Videos by Category</h2>

<div class="navbar">
    <a href="#Wealth_Building_and_Financial_Strategy">Wealth Building and Financial Strategy</a>
    <a href="#Finance_and_Stock_Market">Finance & Stock Market</a>
    <a href="#Financial_Literacy_and_Advisory">Financial Literacy and Advisory</a>
</div>
"""

# Loop through each category and its videos
for category, videos in all_videos_by_category.items():
    category_id = category.replace(" ", "_").replace("&", "and").replace(",", "")
    html_content += f'<div class="category" id="{category_id}"><h2>{category}</h2><div class="video-container">'

    for video in videos:
        html_content += f"""
        <a href="{video['link']}" target="_blank" class="card">
            <img src="{video['thumbnail']}" alt="{video['title']}" class="thumbnail">
            <div class="video-title">{video['title']}</div>
            <div class="channel">{video['channel']}</div>
            <div class="published">{video['published'].strftime('%d %b %Y')}</div>
        </a>
        """

    html_content += "</div></div>"

# Close HTML content
html_content += """
<h4>All content on this webpage, including YouTube videos and other media, belongs to their respective owners and is solely used to showcase user creativity.</h4>
</body>
</html>
"""


script_directory = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_directory, "index.html")

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML file saved to {html_file_path}")

