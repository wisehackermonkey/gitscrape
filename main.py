
import requests
import csv
from datetime import datetime
import sys

def fetch(base_url,page,token):
    
    headers = {"Authorization":"Bearer " + token}
    r = requests.get(f"{base_url}?since={page}&per_page=100", headers=headers)
    last_user = r.json()[-1]
    return (last_user["id"],last_user["login"], r.json())

def format_row(row):
    return list(map(lambda x: x[1], row.items()))
    

if __name__ == "__main__":
    args = sys.argv
    max_page = 3
    print(args)
    start_id = 0
    if args:
        max_page = int(args[1])
    if len(args) == 3:
        start_id = int(args[2])
    page = 0
    token = open(".env").read()
    base_url = "https://api.github.com/users"
    date = str(datetime.now()).replace(" ","_").replace("-","").replace(":","_")
    output = f'./db.{date}.csv'
    logs = f'./db.logs.{date}.csv'
    print(token)  
    with open(output,"w") as db:
        with open(logs,"a") as logs:
            id = start_id
            csv_writer = csv.writer(db, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["login","id", "node_id",  "type", "site_admin"])
            for x in range(max_page):
                id, username, results = fetch(base_url,id,token)
                logs.write(f"{id},{username}\n")
                logs.flush()
                print(id)
                for row in results:
                    # print(format_row(row))
                    login, _id, node_id, avatar_url, gravatar_id, url, html_url, followers_url, following_url, gists_url, starred_url, subscriptions_url, organizations_url, repos_url, events_url, received_events_url, _type, site_admin = format_row(row)
                    csv_writer.writerow([login,_id, node_id, _type, site_admin])
                db.flush()
