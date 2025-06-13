import requests
import pandas as pd
import numpy as np
import argparse


program_color = '\033[35m' # currently magenta
warning_color = '\033[31m' # currently red
reset_color = '\033[0m' # resets the terminal color and styles

def get_data(url):
    response = requests.get(url)

    if response.status_code != 200:
        if response.status_code == 404:
            print(f"{warning_color}User not found.{reset_color}")
        elif response.status_code == 403:
            print(f"{warning_color}Rate limit exceeded. Try again later.{reset_color}")
        else:
            print(f'{warning_color}Error', response.status_code, f'{reset_color}')
        return None
    else:
        return response.json()

def display_profile(url):
    data = get_data(url)

    if data is None:
        return

    print(f'{program_color}Username{reset_color}: {data['login']}')
    print(f"{program_color}Name{reset_color}: {data['name']}")
    print(f"{program_color}Bio{reset_color}: {data['bio']}")
    print(f"{program_color}Location{reset_color}: {data['location']}")
    print(f"{program_color}Public repos{reset_color}: {data['public_repos']}")
    print(f"{program_color}Followers{reset_color}: {data['followers']}")
    print(f"{program_color}Following{reset_color}: {data['following']}")
    print(f"{program_color}Created at{reset_color}: {data['created_at']}\n")



def display_recent_events(url):
    data = pd.DataFrame(get_data(url))

    if data is None:
        return

    event_types = {
        'PushEvent': 'The user pushed commits to a repository',
        'PullRequestEvent': 'The user opened, closed, or merged a pull request',
        'IssuesEvent': 'The user opened, closed, or reopened an issue',
        'IssueCommentEvent': 'The user commented on an issue',
        'CreateEvent': 'The user created a repository, branch, or tag',
        'DeleteEvent': 'The user deleted a branch or tag',
        'ForkEvent': 'The user forked a repository',
        'WatchEvent': 'The user starred a repository',
        'PublicEvent': 'The user made a repository public',
        'PullRequestReviewEvent': 'The user reviewed a pull request',
        'PullRequestReviewCommentEvent': 'The user commented during a PR review',
        'ReleaseEvent': 'The user published a release',
        'MemberEvent': 'The user added or removed a collaborator',
        'GollumEvent': 'A wiki page was created or updated',
        'CommitCommentEvent': 'The user commented on a commit'
    }

    data['repo_name'] = data['repo'].apply(lambda r: r['name'])
    dfs = {group: d for group, d in data.groupby('repo_name')}

    for group, d in dfs.items():
        print(f'{program_color}repo: ', group, f'{reset_color}')
        ev = d['type'].value_counts()
        for type, count in ev.items():
            print(' - ' + event_types[type], f' {count} times.')


def main():
    parser = argparse.ArgumentParser(description='Fetch GitHub user activity.')
    parser.add_argument('username', help ='GitHub username')

    args = parser.parse_args()
    username = args.username

    link = f'https://api.github.com/users/{username}'
    events_link = link + '/events'

    display_profile(link)
    display_recent_events(events_link)

if __name__ == '__main__':
    main()