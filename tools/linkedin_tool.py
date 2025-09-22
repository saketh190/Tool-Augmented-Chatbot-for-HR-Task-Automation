import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

def post_linkedin_update(message, organization_id=None):
    if not LINKEDIN_ACCESS_TOKEN:
        return "LinkedIn access token not set in environment variables."

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # For personal profile posts
    payload = {
        "author": f"urn:li:person:{os.getenv('LINKEDIN_PROFILE_ID')}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # For organization/company posts
    if organization_id:
        payload["author"] = f"urn:li:organization:{organization_id}"

    url = "https://api.linkedin.com/v2/ugcPosts"
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return "LinkedIn post published successfully."
    else:
        return f"Failed to post on LinkedIn: {response.text}"

def register_linkedin_tool(mcp):
    @mcp.tool(
        "post_linkedin_update",
        description="Post a status update or job notification to LinkedIn. Requires LinkedIn API access token."
    )
    def post_linkedin_update_tool(message: str, organization_id: str = None):
        """
        Post a status update or job notification to LinkedIn.
        Args:
            message (str): The content to post.
            organization_id (str, optional): LinkedIn organization ID for company posts.
        Returns:
            str: Status message.
        """
        return post_linkedin_update(message, organization_id)