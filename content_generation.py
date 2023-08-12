import datetime
import re
import openai
import os
# Set your OpenAI API key here
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key

# Function to generate blog ideas
def generate_blog_ideas(prompt):
    openai.api_key = api_key

    messages = [
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=1000,
        n=1,
        stop=None,
        presence_penalty=0,
        frequency_penalty=0.1,
    )
    generated_texts = [
        choice.message["content"].strip() for choice in response["choices"]
    ]
    return generated_texts

# Prompt to start the conversation
conversation_prompt = """Act as a Computer Science Journalist with sense of humor of Vir Das. Generate a blog title and 1000 word 
content (with subheadings if needed) on amazing PC fact or information elaborately. 
Also format the content with title, date and draft as false in a Hugo blog Markdown format"""

# Generate blog ideas
blog_idea = generate_blog_ideas(conversation_prompt)
print("Blog Idea:", blog_idea)

# Regular expression pattern to extract the title
title_pattern = r'^title:\s*(.+)$'

# Search for the title using the regular expression
title_match = re.search(title_pattern, blog_idea[0], re.MULTILINE | re.IGNORECASE)

if title_match:
    post_title = title_match.group(1)
    print("Hugo Post Title:", post_title)
else:
    post_title = f"unknown{datetime.datetime.today()}"
    print("Title not found in the Hugo post.")

with open(f"content/posts/{post_title}.md", "w") as post_file:
    post_file.write(blog_idea[0])

