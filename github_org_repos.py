import requests
import json
import subprocess
import argparse
from os import path
import time
from multiprocessing import Pool


POOL_SIZE = 4


def cloner(url, dest):
    subprocess.run(["git", "clone", url, dest])


def clone_repos(args):
    # Note this is insufficient if there are more than 100 repos in the org
    response = requests.get(f"https://api.github.com/orgs/{args.org}/repos", auth=(args.username, args.access_token))

    if response.status_code != 200:
        raise Exception("Unable to access Github API.")

    repos = response.json()
    repo_data = [ (repo["clone_url"], path.join(args.destination_dir, repo["name"])) for repo in repos ]
    with Pool(POOL_SIZE) as p:
        p.starmap(cloner, repo_data)


def arguments():
    ap = argparse.ArgumentParser(description="Pull all repos from an org.")
    ap.add_argument("--username", type=str, help="Github username.", required=True)
    ap.add_argument("--access-token", type=str, help="Github access token.", required=True)
    ap.add_argument("--org", type=str, help="Github org.", required=True)
    ap.add_argument("--destination-dir", type=str, help="Directory in which to clone repos.", required=True)
    return ap.parse_args()


def main():
    args = arguments()
    clone_repos(args)


if __name__ == "__main__":
    begin = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Clone time {end - begin}")
