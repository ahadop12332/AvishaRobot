from pyrogram import Client, filters
import requests
from AvishaRobot import pbot as app

def chunk_string(text, chunk_size):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

@app.on_message(filters.command("allrepo"))
async def all_repo_command(client, message):
    try:
        # Check if there is a GitHub username after the /giverepo command
        if len(message.command) > 1:
            github_username = message.command[1]

            # Fetch information about all repositories of the GitHub user
            repo_info = get_all_repository_info(github_username)

            # Split repository info into smaller chunks
            chunked_repo_info = chunk_string(repo_info, 4000)  # Split into chunks of 4000 characters

            # Send the repository information in chunks as separate messages
            for chunk in chunked_repo_info:
                await message.reply_text(chunk)
        else:
            await message.reply_text("⬤ Please enter a GitHub username after the /allrepo command.")
    except Exception as e:
        await message.reply_text(f"⬤ An error occurred ➥ {str(e)}")
#######

def get_all_repository_info(github_username):
    # Set up the GitHub API URL for user repositories
    github_api_url = f"https://api.github.com/users/{github_username}/repos"

    # Perform the request to the GitHub API
    response = requests.get(github_api_url)
    data = response.json()

    # Extract relevant information from the response
    repo_info = "\n\n".join([
        f"𖣐 ʀᴇᴘᴏsɪᴛᴏʀʏ ➥ {repo['full_name']}\n\n"
        f"● ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ➥ {repo['description']}\n"
        f"● sᴛᴀʀs ➥ {repo['stargazers_count']}\n"
        f"● ғᴏʀᴋs ➥ {repo['forks_count']}\n"
        f"𖣐 ᴜʀʟ ➥ {repo['html_url']}"
        for repo in data
    ])

    return repo_info

__mod_name__ = "ʀᴇᴘᴏ"

__help__ = """

 ⬤ /allrepo <github username> ➥ sᴇᴇ ᴀ ɢɪᴛʜᴜʙ ᴜsᴇʀ ᴀʟʟ ʀᴇᴘᴏ.
"""
