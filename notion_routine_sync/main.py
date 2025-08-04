from notion_client import Client
import os

notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("DATABASE_ID")

def build_title(props):
    gym = props["Gym"]["checkbox"]
    jawline = props["Jawline"]["checkbox"]
    supp = props["Supplement"]["checkbox"]
    sixpack = props["Sixpack"]["checkbox"]
    unterarm = props["Unterarm"]["checkbox"]

    emoji = ""
    emoji += "🟢" if gym else "⚪️"
    emoji += "🔵" if jawline else "⚪️"
    emoji += "🟡" if supp else "⚪️"
    emoji += "🔴" if sixpack else "⚪️"
    emoji += "🟣" if unterarm else "⚪️"

    date = props["Datum"]["date"]["start"]
    datum = date[8:10] + "." + date[5:7]

    return f"{datum} | {emoji}"

def update_titles():
    entries = notion.databases.query(database_id=database_id)
    for page in entries["results"]:
        props = page["properties"]
        new_title = build_title(props)

        notion.pages.update(
            page_id=page["id"],
            properties={
                "ROUTINE": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": new_title}
                        }
                    ]
                }
            }
        )

if __name__ == "__main__":
    update_titles()
