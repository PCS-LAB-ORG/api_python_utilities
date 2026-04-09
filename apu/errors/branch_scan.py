#!python

# This will change all strings to UTF-8 and session
# -*- coding: utf-8 -*-

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import csv
import json
import os
import time
from datetime import datetime as dt
from pathlib import Path

import requests

from apu.utils import logger, login, constants

logger = logger.setup_logger()
login.login()

formatted_starttime = dt.now().strftime("%Y-%m-%d_%H-%M-%S")

# Get the full path of the script file
script_path = Path(__file__).resolve()

# Get the directory containing the script
script_dir = (
    f"{script_path.parent}/logs/logs_{formatted_starttime}"  # Default output location
)

if not os.path.exists(script_dir):
    os.makedirs(script_dir)


# https://pan.dev/prisma-cloud/api/code/get-periodic-findings/
# https://pypi.org/project/grequests/
def branch_scan(filename=constants.date_time_format_w_seconds + ".csv", filters=None):
    url = f"{login.settings['url']}/code/api/v2/code-issues/branch_scan"

    # http_logging()
    repository_list = []
    has_next = True
    page = 1
    offset = 0
    limit = 10000  # page size. I have found that 10k is the upper limit for this and it will fail with 10001.
    page_cutoff = 100
    running_total = 0
    running_error_total = 0
    while has_next == True:
        if not filters:
            payload = json.dumps(
                {
                    "filters": {
                        # "ids": ["<my repo ID>"],
                        #     "benchmarks": ["CIS KUBERNETES V1.5"],
                        # "checkStatus": "Error",
                        # "sastLabels": ["CustomPolicy"],
                        #     "secretsRiskFactors": ["PublicRepository"],
                        # "severities": ["LOW", "MEDIUM", "HIGH", "CRITICAL"], # <----------------------- with vulns
                        # "severities": ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"], # <----------------------- includes non vuln
                        #     "vulnerabilityRiskFactors": ["AttackComplexity"],
                        # "codeCategories": ["Vulnerabilities", "IacMisconfigurations"]
                    },
                    # "useSearchAfterPagination": True,
                    # "pageConfig": { # This was tested and does not work. Please use offset and limit instead.
                    #     "page": 0,
                    #     "pageSize": 0
                    # }
                    "offset": offset,
                    "limit": limit,  # default if unspecified is 100
                }
            )
        else:
            payload = json.dumps(filters)
        response = requests.request("POST", url, headers=login.headers, data=payload)
        try:
            response.raise_for_status()
        except Exception as e:
            if e.response.status_code == 401:
                # Refresh token
                logger.info("Reauthenticating.")
                login.refresh_token()
                continue
            if e.response.status_code == 504:
                # Refresh token
                logger.info("Waiting a few seconds beause of timeouts.")
                time.sleep(5)
                login.refresh_token()
                continue
            logger.error("Unhandled error.")
            logger.error(e)
            raise e
        response_text = json.loads(response.text)
        repository_list = response_text["data"]
        if response_text["hasNext"] == True and page <= page_cutoff:
            offset += limit
            page += 1
        else:
            has_next = False
        errors = parse_repo_list(repository_list, filename)
        running_error_total += errors
        running_total += len(repository_list)
        logger.info(
            f"Running total {running_total}. Running errors {running_error_total}. Page {page}"
        )


def parse_repo_list(repository_list, filename):
    with open(filename, "a+", newline="") as csv_file:
        error_count = 0
        finding_count = 0
        for repo in repository_list:
            finding_count += 1
            clean_columns(repo)
            repo_obj = parse_for_category(repo)
            csv_writer = csv.DictWriter(f=csv_file, fieldnames=repo_obj.keys())
            global write_header
            if write_header:
                csv_writer.writeheader()
                write_header = False

            try:
                csv_writer.writerow(repo_obj)
                global total_finding_count
                total_finding_count += 1
            except UnicodeEncodeError:
                write_exception(repo)
                parsed_row = parse_for_category(repo)
                csv_writer.writerow(parsed_row)
                error_count += 1
    return error_count


def clean_columns(repo):
    """
    Some of the data has iternal IDs and raw info that is parsed on the page and this handles those as-needed.
    """
    if repo["codeCategory"] == "Weaknesses" and "dataFlow" in repo:
        data_flow = repo["dataFlow"]
        repo["dataFlow"] = (
            f"{data_flow['source']['path']}:{data_flow['source']['start']['row']}-{data_flow['sink']['end']['row']}"
        )


def write_exception(repo):
    """
    The function to remove non-unicode encoded characters. Notice that if there is any key/value error it will blank the value
    and write to the error file and logs.
    """
    with open(f"{script_dir}/error_{formatted_starttime}.csv", "a+") as err_file:
        for key in repo.keys():
            try:
                err_file.write(f"{repo[key]}, ")
            except Exception:
                value = ""
                for c in str(repo[key]):
                    try:
                        err_file.write(c)
                        value += c
                    except Exception:
                        if c == "́":
                            continue
                        if c == "ą":
                            value += "a"
                            continue
                        if c == "ć":
                            value += "c"
                            continue
                        if c == "ś":  # 'Antoś Bucko'
                            value += "ś"
                            continue
                        value += f" hex {hex(ord(c))} "
                try:
                    err_file.write(f"{value}, ")
                    repo[key] = value

                except Exception:
                    err_file.write(f"<{key} error>, ")
                    repo[key] = f"<{key} error>"
                    global total_error_count
                    total_error_count += 1
        err_file.write("\n")
    # logger.warning(f"Problem writing {repo['codeCategory']} repo {index}: {str(repo)[:100]}...")
    return repo


def parse_for_category(repo):
    category = repo["codeCategory"]

    resource_id = ""
    if "resourceId" in repo:
        resource_id = repo["resourceId"]
    else:
        if "repository" in repo and "codePath" in repo and "causePackageName" in repo:
            resource_id = (
                f"{repo['repository']}:{repo['codePath']}:{repo['causePackageName']}"
            )

    code_path = ""
    if "codePath" in repo:
        code_path = repo["codePath"]
    else:
        code_path = resource_id

    risk_factors = ""
    if "riskFactors" in repo:
        risk_factors = repo["riskFactors"]

    fix_version = ""
    if "fixVersion" in repo:
        fix_version = repo["fixVersion"]
    elif "suggestedFix" in repo:
        fix_version = repo["suggestedFix"]

    custom_policy = ""
    if "customPolicy" in repo:
        custom_policy = repo["customPolicy"]

    license_type = ""
    if "licenseType" in repo:
        license_type = repo["licenseType"]

    compliance = ""
    if "compliance" in repo:
        compliance = repo["compliance"]

    confidence = "-"
    if "confidence" in repo:
        confidence = repo["confidence"]

    language = ""
    if "fileType" in repo:
        language = repo["fileType"]

    repository_source = ""
    if "repositorySource" in repo:
        repository_source = repo["repositorySource"]

    git_user = ""
    if "gitUser" in repo:
        git_user = repo["gitUser"]
    elif "author" in repo:
        git_user = repo["author"]

    cve_uuid = ""
    if "cveUuid" in repo:
        cve_uuid = repo["cveUuid"]
    elif "policy" in repo:
        cve_uuid = repo["policy"]

    cwes = []
    if "cwes" in repo:
        cwes = repo["cwes"]

    lines = ""
    if "dataFlow" in repo:
        lines = repo["dataFlow"]
    elif "codeIssueLine" in repo:
        lines = repo["codeIssueLine"]

    key_map = {
        "Code category": category,
        "Status": repo["checkStatus"],
        "Severity": repo["severity"],
        "IaC Category / Risk factor": risk_factors,
        "Policy ID": repo["violationId"],
        "Policy reference": cve_uuid,
        "Title": repo["policy"],
        "Custom Policy": custom_policy,
        "First Detection Date": repo["firstDetected"],
        "Resource name": resource_id,
        "Source ID": repo["repository"],
        "Suggested fix": fix_version,
        "Code path": code_path,
        "Code issue line": lines,
        "Git user": git_user,
        "Details": (
            f"https://app2.prismacloud.io/projects?viewId=overview&checkStatus=Error&repository={repo['repository']}"
        ),
        "License Type": license_type,
        "CWE": cwes,
        "Compliance": compliance,
        "Confidence": confidence,
        "Repository": repo["repository"],
        "Language": language,
        "Finding Source": repository_source,
    }
    return key_map


write_header = True
total_finding_count = 0
total_error_count = 0

if __name__ == "__main__":
    branch_scan()
    logger.info(
        f"Total findings {total_finding_count}. Total errors {total_error_count}"
    )

    logger.info(
        "Keep in mind that though error files are written with entries that could not be parsed entirely "
        "this is also made to strip out the portions that cannot be written and to print the rest of the data "
        "for that entry to the regular output file for the entry's category. This duplication is a utility "
        "function to help find why this data may not parse correctly and distinguish it from blank data points "
        "that can be parsed."
    )
