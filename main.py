import os
from dotenv import load_dotenv

import requests
from newspaper import Article

from langchain_classic.schema import (
    HumanMessage
)
from langchain_openai import ChatOpenAI

# =================================================
# This reads the .env file and loads the variables
load_dotenv()

# Get OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
# =================================================

# Set custom headers for web scraping
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

# article source link
article_url = "https://www.artificialintelligence-news.com/2022/01/25/meta-claims-new-ai-supercomputer-will-set-records/"

# Create a session to handle requests
session = requests.Session()

# Fetch and parse the article
try:
    # Fetch the article page
    response = session.get(article_url, headers=headers, timeout=10)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the article using newspaper3k
        article = Article(article_url)
        article.download()
        article.parse()

        # TODO uncomment to see the article title and text without summarization
        # print(f"Title: {article.title}")
        # print(f"Text: {article.text}")

    else:
        print(f"Failed to fetch article at {article_url}")
except Exception as e:
    print(f"Error occurred while fetching article at {article_url}: {e}")

# so far this results in:
# Title: Meta claims its new AI supercomputer will set records
# Text: Meta (formerly Facebook) has unveiled an AI supercomputer that it claims will be the world’s fastest.
# The supercomputer is called the AI Research SuperCluster (RSC) and is yet to be fully complete. However, Meta’s researchers have already begun using it for training large natural language processing (NLP) and computer vision models.
# RSC is set to be fully built in mid-2022. Meta says that it will be the fastest in the world once complete and the aim is for it to be capable of training models with trillions of parameters.
# “We hope RSC will help us build entirely new AI systems that can, for example, power real-time voice translations to large groups of people, each speaking a different language, so they can seamlessly collaborate on a research project or play an AR game together,” wrote Meta in a blog post.
# “Ultimately, the work done with RSC will pave the way toward building technologies for the next major computing platform — the metaverse, where AI-driven applications and products will play an important role.”
# For production, Meta expects RSC will be 20x faster than Meta’s current V100-based clusters. RSC is also estimated to be 9x faster at running the NVIDIA Collective Communication Library (NCCL) and 3x faster at training large-scale NLP workflows.
# A model with tens of billions of parameters can finish training in three weeks compared with nine weeks prior to RSC.
# Meta says that its previous AI research infrastructure only leveraged open source and other publicly-available datasets. RSC was designed with the security and privacy controls in mind to allow Meta to use real-world examples from its production systems in production training.
# What this means in practice is that Meta can use RSC to advance research for vital tasks such as identifying harmful content on its platforms—using real data from them.
# “We believe this is the first time performance, reliability, security, and privacy have been tackled at such a scale,” says Meta.      
# (Image Credit: Meta)
# Want to learn more about AI and big data from industry leaders? Check out AI & Big Data Expo. The next events in the series will be held in Santa Clara on 11-12 May 2022, Amsterdam on 20-21 September 2022, and London on 1-2 December 2022.
# Explore other upcoming enterprise technology events and webinars powered by TechForge here.


# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# *Next steps: Summarize the article text using OpenAI API

# we get the article data from the scraping part
article_title = article.title
article_text = article.text

# prepare template for prompt
template = """You are a very good assistant that summarizes online articles.
Here's the article you want to summarize.
==================
Title: {article_title}
{article_text}
==================
Now, provide a very short summarized version of the article in a bulleted list format.
"""

# use the template in the prompt
prompt = template.format(article_title=article.title, article_text=article.text)
# Create message for the LLM
messages = [HumanMessage(content=prompt)]
# load the model
chat = ChatOpenAI(api_key=openai_api_key, model_name="gpt-4", temperature=0)
# generate summary
summary = chat.invoke(messages)
print(summary.content)

# Example output:
# - Meta (formerly Facebook) has unveiled an AI supercomputer, the AI Research SuperCluster (RSC), which it claims will be the world's fastest once fully built in mid-2022.
# - The RSC is already being used by Meta's researchers for training large natural language processing and computer vision models.
# - The supercomputer is expected to be capable of training models with trillions of parameters and will be 20x faster than Meta’s current V100-based clusters.
# - The RSC will be used to build new AI systems for real-time voice translations and other applications in the metaverse.
# - The supercomputer was designed with security and privacy controls to allow Meta to use real-world examples from its production systems in training.
# - Meta claims that a model with tens of billions of parameters can finish training in three weeks with RSC, compared to nine weeks prior to RSC.