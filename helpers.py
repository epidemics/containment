import pandas as pd
from notion.client import NotionClient

def get_notion_client(credentials_file='.notion-token'):
    """
    Authenticates with Notion API using stored credentials. You'll need
    to find and store your Notion token for this. When logged into
    Notion, look in the web console for a cookie named "token_v2".
    Copy the contents into a file in this directory named .notion-token
    """
    with open(credentials_file, 'r') as token_file:
        NOTION_TOKEN = token_file.read().strip()

    return NotionClient(token_v2=NOTION_TOKEN)


def get_api_metadata(notion_client, comment=None):
    return {'created': pd.Timestamp('now', tz='utc').isoformat(),
            'created_by': notion_client.current_user.full_name,
            'comment': comment}
