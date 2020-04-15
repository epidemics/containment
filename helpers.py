import pandas as pd
import numpy as np
from notion.client import NotionClient
from notion.collection import NotionDate


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


def df_from_notion_table(table, convert_dates=True):
    rows = table.collection.get_rows()
    df = pd.DataFrame([row.get_all_properties() for row in rows])
    if convert_dates:
        for col in df:
            if df[col].dtype == np.dtype('O'):
                series = df[col].dropna()
                if isinstance(series[0], NotionDate):
                    df[col] = series.apply(lambda d: d.start).astype('M')
    return df


def get_api_metadata(notion_client, comment=None):
    return {'created': pd.Timestamp('now', tz='utc').isoformat(),
            'created_by': notion_client.current_user.full_name,
            'comment': comment}
