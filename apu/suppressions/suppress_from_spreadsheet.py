import csv
from pathlib import Path
from datetime import datetime

import pandas as pd

from apu.errors import policies, resources
from apu.repositories import get_repo
from apu.suppressions import core  # TODO may not have to import self


def parse_suppression_file(file_path=""):
    data = []
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path, engine="openpyxl")
        # print(df.head()) # Print the first 5 rows of the DataFrame
        data = df.to_dict(orient="records")

    elif file_path.endswith(".csv"):
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
    else:
        print(f"File extension: {file_path} not supported")
        quit()

    # Commented column names are unused at this time.
    required_column_list = [
        "Code category",
        "Status",
        # "Severity",
        "IaC Category / Risk factor",
        # "Policy ID",
        "Policy reference",
        "Title",
        # "Custom Policy",
        # "First Detection Date",
        "Resource name",
        "Source ID",
        # "Suggested fix",
        "Code path",
        "Code issue line",
        # "Git user",
        # "Details",
        # "License Type",
        # "CWE",
        # "Compliance",
        # "Confidence",
        # "Repository",
        # "Language",
        # "Finding Source"
        "Suppress",  # Manually added to denote if finding should be suppressed. Should be true or false in any casing
        "Comment",  # Comment/Justification for the suppression
        # "Expiration" # Expiration date for the suppression. Unimplemented.. Format needs to be noted
    ]
    required_set = set(required_column_list)
    csv_columns = set(data[0].keys())
    if not required_set.issubset(csv_columns):
        quit(f"Missing columns in file. These are required: {required_set}")

    request_suppress = []
    for row in data:
        # if not row['Code category'] == "Secrets":
        #     print(f"This script is written to only work with Secrets at this time. Discarding this entry from list. {row['Title']}")
        #     continue

        current_suppressed_status = (
            row["Status"] == "SUPPRESSED"
        )  # is already suppressed
        needs_suppressed = (
            "Suppress" in row and row["Suppress"].upper() == "TRUE"
        )  # if manual column Suppress implies I should suppress
        suppress = not current_suppressed_status and needs_suppressed

        """
        !!! Setting this IF statement to 'or True' will cause it to suppress ALL in the spreadsheet !!!
        """
        if suppress:
            request_suppress.append(row)
            # if row['Custom Policy'] == "Yes":
            #     request_suppress.append(row)
            # suppress = True
        print(f"{row['Source ID']}, Request Suppress: {needs_suppressed}, Status: {row['Status']}.. Will Suppress: {suppress}")
    data = request_suppress

    if 0 == len(data):
        print("No findings can be suppressed")

    return data


def name_from_source_id(source_id):
    components = source_id.split("/")
    components.reverse()
    return components[0]


def get_expiration(finding):
    # Valentines Day 2026 at 12:00am PST
    # {
    #     "comment": "asdf",
    #     "expirationTime": 1771056000000,
    #     "suppressionType": "Resources",
    #     "resources": {
    #         "accountId": "jumiles/webgoat",
    #         "id": "BC_GIT_6::jumiles/webgoat::/src/test/java/org/owasp/webgoat/lessons/missingac/MissingFunctionACUsersTest.java:91a33f0e448feb0845cba10cb0d9ac38cf19294d"
    #     },
    #     "origin": "Platform"
    # }
    # expiration_time = 1756278000000
    expiration = -1
    if "Expiration" in finding and not 0 == len(finding["Expiration"]):
        expiration = datetime(finding["Expiration"]).timestamp()
    return expiration


def finding_code_line_to_policy_finding(finding, policy_list):
    derived_file_path_with_commit = ""
    code_lines = ""
    if "," in finding["Code issue line"]:
        code_lines = finding["Code issue line"].split(", ") # '34, 35' is the variable's format
    if "-" in finding["Code issue line"]:
        code_lines = finding["Code issue line"].split("-") # '34, 35' is the variable's format

    for policy in policy_list:
        # print(f"{policy['repository']} {policy['errorLines']} {policy['resourceId']} {policy['violationId']}")
        if not finding["Code category"] == policy["codeCategory"]:
            continue
        if "createdBy" in policy and not finding["Git user"] == policy["createdBy"]:
            continue
        if not finding["Title"] == policy["policy"]:
            continue
        if not finding["Source ID"] == policy["repository"]:
            continue
        if not finding["Severity"] == policy["severity"]:
            continue

        # for secrets
        if (
            "errorLines" in policy
            and str(policy["errorLines"][0]) in code_lines
            and str(policy["errorLines"][1]) in code_lines
        ):
            # error_lines_from_resource = resource_list['data']['errorLines'] # [79, 80]
            derived_file_path_with_commit = policy["resourceId"]  # file path with leading slash and commit sha # 'commitHash' = 'd2a1546df'
            break

        # for weaknesses
        if "locations" in policy:
            for location in policy["locations"]:
                start = str(location["start"]["row"])
                end = str(location["end"]["row"])
                if start in code_lines and end in code_lines:
                    derived_file_path_with_commit = policy["filePath"]  # file path with leading slash and commit sha
                    if "commitHash" in policy:
                        derived_file_path_with_commit += f":{policy['commitHash']}"
                    break
            break
    return derived_file_path_with_commit, code_lines


def suppress(file_path=""):
    """
    The 'data' list are findings thus there are multiple within a single repo
    A repo doesn't have a finding category
    What I need is the reduction of which categories have which repos to narrow
    my search for policies.
    """
    data = parse_suppression_file(file_path)
    repo_list = get_repo.get_repositories(
        includeUnmappedProjects=True, repo_search_list=data
    )
    repo_owner_name_map = {}
    repo_id_list = []
    for repo in repo_list:
        repo_owner_name_map[f"{repo['owner']}/{repo['repository']}"] = repo
        repo_id_list.append(repo["id"])

    category_list = set([finding["Code category"] for finding in data])
    # category_repo_list_map = {}
    # for d in data:
    #     for repo in repo_list:
    #         category = d['Code category']
    #         if f"{repo['owner']}/{repo['repository']}" == d['Source ID']:
    #             if not category in category_repo_list_map:
    #                 category_repo_list_map[category] = set()
    #             category_repo_list_map[category].add(repo['id'])
    #             break

    policies_list = policies.get_policies(category_list, repo_id_list)
    policies_by_title = {policy["title"]: policy for policy in policies_list}
    policies_by_guide = {policy["guideline"]: policy for policy in policies_list}
    policies_by_id = {policy["policyId"]: policy for policy in policies_list}

    # resource_list = get_resources_by_policies(policies_list, category_list, repo_id_list)
    policy_entries = []
    for finding in data:
        policy_id = ""
        if finding["Policy ID"] in policies_by_id:
            policy_id = policies_by_id[finding["Policy ID"]]["policyId"]

        if len(policy_id) == 0 and finding["Title"] in policies_by_title:
            policy_id = policies_by_title[finding["Title"]]["policyId"]

        if len(policy_id) == 0 and finding["Policy reference"] in policies_by_guide:
            policy_id = policies_by_guide[finding["Policy reference"]]["policyId"]

        if len(policy_id) == 0:
            raise Exception(f"Cannot find policy for {finding}")

        repo_id = repo_owner_name_map[finding["Source ID"]]["id"]
        policy_entries.append(
            {
                # "policy_uuid": finding["Policy ID"], # add later
                "policy_id": policy_id,
                "category": finding["Code category"],
                "repo_id_list": repo_id,
            }
        )
    resource_list = resources.get_resources_by_policies(policy_entries)

    # resource_list_checkov = resources.get_resources_by_policies_checkov(policies_list, repo_id_list)

    policy_list = policies.get_policies_by_resource(repo_id_list, resource_list)

    # add policy uuid to poliicy_entries list. I think we have it at this point.

    policies_by_title = {
        policy["policy"]: policy for policy in policy_list
    }  # <-------------- the other uses policies
    policies_by_guide = {}
    for policy in policies_list:
        if policy["guideline"]:
            policies_by_guide[policy["guideline"]] = policy

    for finding in data:
        comment = ""
        if "Comment" in finding:
            comment = finding["Comment"]

        # The docs reference url path bottom level will be like git-secrets-8 vs git_secrets_8 for the real policyId
        # guideline and title will match from findings to policies
        policy_id = ""
        policy_id_by_guide = ""
        uuid = ""

        if finding["Title"] in policies_by_title:
            policy_id = policies_by_title[finding["Title"]]["violationId"]
            uuid = policies_by_title[finding["Title"]].get("uuid")

        if (
            not finding["Policy reference"] == "-"
            and finding["Policy reference"] in policies_by_guide
        ):
            policy_id_by_guide = policies_by_guide[finding["Policy reference"]]["policyId"]
            uuid = policies_by_guide[finding["Policy reference"]].get("uuid")

        if not policy_id_by_guide == policy_id and not 0 == len(policy_id_by_guide):  # I dont think there can be a policy reference for custom policies. If this is untrue then use the title match as the definitive check.
            print(f"Error: {finding}")
            # I found this logic really challenging to determine. Can the policy names be the same?
            continue

        account_id = finding["Source ID"]  # "jumiles-pa/test-cas-app"
        file_path = f"/{finding["Code path"]}"  # "/README.md"
        derived_file_path_with_commit, code_lines = finding_code_line_to_policy_finding(finding, policy_list)
        expiration = get_expiration(finding)

        quit("Not ready for testing")

        if not 0 == len(derived_file_path_with_commit):
            # pass #while testing on some data
            core.create_suppression(
                comment,
                policy_id,
                account_id,
                derived_file_path_with_commit,
                code_lines,
                expiration,
                uuid,
                finding["Code category"],
            )
        else:
            print(f"Resource not found: {finding}")


file_path = f"{Path.home()}/Downloads/csvReport_1773259809905.csv"
suppress(file_path=file_path)

"""
The API submitted the suppression and got a 200 code

I went into the UI and looked up the finding and found it unsupressed

I attempted to suppress it and the UI sent this request and got this response.

curl 'https://api2.prismacloud.io/bridgecrew/api/v2/suppression' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'authorization: eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdW1pbGVzQHBhbG9hbHRvbmV0d29ya3MuY29tIiwiZmlyc3RMb2dpbiI6ZmFsc2UsInByaXNtYUlkIjoiOTAyNTk5MzQ0OTc1NzU5MzYwIiwiaXBBZGRyZXNzIjoiMTM3LjgzLjI0OS4yNDMiLCJpc3MiOiJodHRwczovL2FwaTIucHJpc21hY2xvdWQuaW8iLCJyZXN0cmljdCI6MCwidXNlclJvbGVUeXBlRGV0YWlscyI6eyJoYXNPbmx5UmVhZEFjY2VzcyI6ZmFsc2V9LCJ1c2VyUm9sZVR5cGVOYW1lIjoiU3lzdGVtIEFkbWluIiwiaXNTU09TZXNzaW9uIjp0cnVlLCJsYXN0TG9naW5UaW1lIjoxNzczNDI4NzU5NDQ1LCJhdWQiOiJodHRwczovL2FwaTIucHJpc21hY2xvdWQuaW8iLCJ1c2VyUm9sZVR5cGVJZCI6MSwiYXV0aC1tZXRob2QiOiJTQU1MMiIsInNlbGVjdGVkQ3VzdG9tZXJOYW1lIjoiQVBQMiBQcmlzbWEgQ2xvdWQgQ3VzdG9tZXIgU3VjY2VzcyBMYWItIDU0MTgxNjQxNjcwMTg3OTgwNDgiLCJzZXNzaW9uVGltZW91dCI6NjAsInVzZXJSb2xlSWQiOiJmMzVjOTk4OC0xZmExLTRlNzktYTg1YS00MzFhZTU1YjEyNDgiLCJoYXNEZWZlbmRlclBlcm1pc3Npb25zIjpmYWxzZSwiZXhwIjoxNzczNDM4NTU1LCJpYXQiOjE3NzM0Mzc5NTUsInVzZXJuYW1lIjoianVtaWxlc0BwYWxvYWx0b25ldHdvcmtzLmNvbSIsInVzZXJSb2xlTmFtZSI6IlN5c3RlbSBBZG1pbiJ9.Cs-rHLwcEn1DQAwSd2BZuLzHIx8il4vh8e4BLip6Prs' \
  -H 'content-type: application/json' \
  -H 'origin: https://app2.prismacloud.io' \
  -H 'priority: u=1, i' \
  -H 'referer: https://app2.prismacloud.io/' \
  -H 'sec-ch-ua: "Not-A.Brand";v="24", "Chromium";v="146"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36' \
  --data-raw '{
                    "policyIds": [
                        "BC_SAST_44"
                    ],
                    "justificationComment": "checking myself",
                    "ruleType": "finding",
                    "type": "PERIODIC",
                    "findingIds": [
                        "a9042bd0-cdf9-4f07-803e-19d340bbc48c"
                    ]
                }'
  
  {"message":"Internal Server Error"}


policies/<policies id>/resources response['uuid'] is the finding id
"""
