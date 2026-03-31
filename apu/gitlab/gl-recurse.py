import csv
import os
from pathlib import Path
import gitlab

from dotenv import load_dotenv

# Load variables from the .env file in C:/Users/<username>/.gitlab/.env
dotenv_path = f"{Path.home()}/.gitlab/.env"
load_dotenv(dotenv_path=dotenv_path)


# --- Configuration ---
# Replace with your GitLab instance URL (e.g., 'https://gitlab.com')
GITLAB_URL = os.environ.get("GITLAB_URL")
# Replace with your Personal Access Token
PRIVATE_TOKEN = os.environ.get("PRIVATE_TOKEN")

script_path = os.path.abspath(__file__)  # path to this script
script_dir = os.path.dirname(script_path)  # directory of this script

output_file = f"{script_dir}/output.csv"
BASE_GROUP_ID = "miles-cortex-demos"

gl = gitlab.Gitlab(GITLAB_URL, PRIVATE_TOKEN, ssl_verify=False)

# Set the number of items per page (e.g., 20)
# items_per_page = 20
# Start from the first page

# all_projects = []
all_members = []


def get_projects_recursive(group_id):
    # current_page = 1
    # keep_going = True
    # while keep_going:
    try:
        group = gl.groups.get(group_id)

        # 1. Get projects directly within this group
        # projects = group.projects.list(
        #     iterator=False,
        #     include_subgroups=True,
        #     page=current_page,
        #     per_page=items_per_page,
        # )
        # all_projects.extend(projects)
        for member in group.members.list(all=True):
            all_members.append(
                {
                    "group_url": group.web_url,
                    "username": member.username,
                    "name": member.name,
                    "locked": member.locked,
                    "state": member.state,
                    "group": group.full_name,
                    "group_archived": group.archived,
                    "group_id": member.group_id,
                }
            )

        # 2. Get subgroups of this group and recurse
        subgroups = group.subgroups.list(all=True)
        for subgroup_info in subgroups:
            # Note: subgroup_info is a GroupSubgroup object. Need to use its ID.
            get_projects_recursive(subgroup_info.id)

        # if not len(projects) == 0:
        #     break

        # Move to the next page
        # current_page += 1
        # keep_going = False
    except gitlab.exceptions.GitlabError as e:
        print(f"Error processing group {group_id}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Start the recursion from the base group
get_projects_recursive(BASE_GROUP_ID)

for member in all_members:
    print(f"- {member}")

# Open a new CSV file for writing
with open(f"{script_dir}/output.csv", "w", newline="", encoding="utf-8") as csvfile:
    # Extract the headers (keys) from the first dictionary
    fieldnames = all_members[0].keys()

    # Create a DictWriter object to map dictionaries to output rows
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write all the data rows
    writer.writerows(all_members)
