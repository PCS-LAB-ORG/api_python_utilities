#!python

# This will change all strings to UTF-8 and session
# -*- coding: utf-8 -*-

# https://pan.dev/prisma-cloud/api/code/get-bom-report/
# https://github.com/spyoungtech/grequests

# https://docs.prismacloud.io/en/enterprise-edition/content-collections/application-security/visibility/sbom
# https://docs.prismacloud.io/en/enterprise-edition/content-collections/application-security/visibility/sbom/sbom

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import csv
import json
import os
import sys
import urllib.parse
from datetime import datetime as dt

import grequests
import requests  # Needs to come after 'import grequests'
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from apu.sbom import core
from apu.utils import constants, logger, login

logger = logger.logger

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log_dir = f"{constants.log_dir}/dt.now().strftime('%Y-%m-%d_%H-%M-%S')"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger.info(f"Python version: {sys.version}")


def srcs_by_concrete_id(concrete_id):
    url = f"{login.cspm_session.api_url}/bridgecrew/api/v1/sbom/srcs-by-concreteId"
    # example 'ConcretePackage_javaScript_@angular-devkit/build-optimizer_0.1300.4_https://registry.npmjs.org/'
    payload = json.dumps({"concreteId": concrete_id})
    # headers = login.headers

    return grequests.request("POST", url, headers=login.headers, data=payload)


# def process_source_responses(response):
#     try:
#         response.raise_for_status()
#     except requests.exceptions.HTTPError as err:
#         if response.status_code == 504:
#             logger.error(id, response.status_code)
#         elif response.status_code == 401:
#             logger.warning(f"Code: {response.status_code}: {response.reason} - {response.url}")
#             cspm_session = login.session_manager.create_cspm_session()
#             return
#         else:
#             raise err
# for res_js in json.loads(res.text):
# repos_found.extend(json.loads(res.text))
# return repos_found


#  pylint: disable=unused-argument
def exception_handler(request, exception):
    response = exception.response
    if response.status_code == 504:
        logger.error(id, response.status_code)
    elif response.status_code == 401:
        logger.warning(
            f"Code: {response.status_code}: {response.reason} - {response.url}"
        )
        # cspm_session = session_manager.create_cspm_session()
    elif response.status_code == 403:
        logger.warning(
            f"Code: {response.status_code}: {response.reason} - {response.url}"
        )
        # cspm_session = session_manager.create_cspm_session()
    retry_sources.append(concrete_id)
    return response


login.login(lib="pcpi")
# filters = core.get_filters() # TODO do I need this?
dependencies = core.dependencies()

repos_found = {}
dep_count = len(dependencies)
dependencies = sorted(dependencies, key=lambda x: x["srcCount"], reverse=True)
dependencies_map = {}
for dep in dependencies:
    dependencies_map[dep["id"]] = dep
    for cve in dep["cves"]:
        published_date = cve["publishedDate"]
        try:
            cve["publishedDate"] = dt.fromtimestamp(published_date)
            continue
        except Exception as e:
            pass
        try:
            cve["publishedDate"] = dt.strptime(
                str(published_date), "%Y-%m-%dT%H:%M:%SZ"
            )
            continue
        except ValueError as e:
            pass
        except Exception as e:
            logger.error("This should only be unrecognized errors.")
            raise e

file = f"{constants.log_dir}/merged_file_{constants.now}.csv"
with open(file=file, mode="a", newline="") as merger:
    merged_writer = csv.DictWriter(
        f=merger,
        fieldnames=[
            "Package",
            "Version",
            "Fix Version",
            "Git Org",
            "Git Repository",
            "Line(s)",
            "Path",
            "Registry URL",
            "Root Package",
            "Root Version",
            "Severity",
            "Vulnerability",
            "Licenses",
        ],
    )
    merged_writer.writeheader()

number_of_requests = 0
responses_processed = set()
retry_sources = []
for index, dependency in enumerate(dependencies):
    logger.info(
        f"{dependency['srcCount']} repos ({index}/{dep_count} package-versions) {dependency['id']}"
    )
    concrete_id = urllib.parse.quote(dependency["id"])
    retry_sources.append(concrete_id)

should_retry = True
retry_count = 5
while should_retry and retry_count > 0 and len(retry_sources) > 0:
    retry_count -= 1  # Fail safe against infinite loop
    source_list = []
    for processed_response in responses_processed:
        if processed_response in retry_sources:
            retry_sources.remove(processed_response)

    for src in retry_sources:
        source_list.append(srcs_by_concrete_id(src))
    number_of_requests = len(source_list)
    logger.info(f"Sources to call: {len(source_list)}")
    for index, response in grequests.imap_enumerated(requests=source_list, size=100):
        if index % 5 == 0:  # declutter logs
            logger.info(f"Call Index: {index}/{len(source_list)}")
        try:
            response.raise_for_status()
        except Exception as exception:
            logger.error(exception)
            # retry_count -= 1
            response = exception.response  # pylint: disable=no-member
            if response.status_code == 504:
                logger.error(id, response.status_code)
                continue
            elif response.status_code == 401:
                logger.warning(
                    f"Code: {response.status_code}: {response.reason} - {response.url}"
                )
                # cspm_session = session_manager.create_cspm_session()
            elif response.status_code == 403:
                logger.warning(
                    f"Code: {response.status_code}: {response.reason} - {response.url}"
                )
                # cspm_session = session_manager.create_cspm_session()
            # retry_sources.append(concrete_id)
            else:
                should_retry = False  # If we don't recognize the error then don't risk an endless loop
            break
    reauth = False
    for async_request in source_list:
        concrete_id = json.loads(async_request.kwargs["data"])["concreteId"]
        if None is async_request.response:
            # retry_sources.append(concrete_id)
            continue
        elif (
            async_request.response.status_code == 401
            or async_request.response.status_code == 403
        ):
            reauth = True
            continue
        elif not async_request.response.status_code == 200:
            continue
        res_js = json.loads(async_request.response.text)
        for res in res_js:
            decoded_concrete_id = urllib.parse.unquote(concrete_id)
            package_repo_id = f"{decoded_concrete_id}_{res['id']}"
            if not package_repo_id in repos_found:
                repos_found[package_repo_id] = [res]
            else:
                repos_found[package_repo_id].append(res)
        if concrete_id in retry_sources:
            retry_sources.remove(concrete_id)
        responses_processed.add(concrete_id)
        logger.info(
            f"Res Procd: {len(responses_processed)}, Marked Retry: {len(retry_sources)}, Index: {source_list.index(async_request)}, Adding: {len(res_js)}"
        )
        async_request.session.close()
    if reauth:
        cspm_session = session_manager.create_cspm_session()  # Change to reauth flag
        reauth = False

    sbom_finding_list = []
    for key, package in repos_found.items():
        dependency = dependencies_map[key.rsplit("_", 1)[0]]
        sorted_cves = sorted(
            dependency["cves"], key=lambda cve: cve["publishedDate"], reverse=True
        )
        cve_id = ""
        if len(dependency["cves"]) > 0:
            cve_id = dependency["cves"][0]["id"]

        for repo in package:

            severity = dependency["maxSeverity"] or ""

            root_package = repo["tree"]
            root_package_version = ""
            if root_package:
                if len(root_package) > 0:
                    if "->" in repo["tree"]:
                        root_package = repo["tree"].split("->")[0]
                    if root_package.startswith("@"):
                        root_package = root_package[1:]
                    package_version_split = root_package.split("@")
                    if not len(package_version_split) > 0:
                        root_package = package_version_split[0]
                    else:
                        root_package = ""
                    if not len(package_version_split) > 1:
                        root_package_version = package_version_split[1]
                    else:
                        root_package_version = ""
            else:
                root_package = ""
                root_package_version = ""

            fix_version = ""
            for cve in sorted_cves:
                if "fixedVersion" in cve:
                    fix_version = cve["fixedVersion"]
                    break

            lines = ""
            if "#" in repo["locationUrl"]:
                url_components = repo["locationUrl"].split("#")
                if len(url_components) > 1:
                    lines = repo["locationUrl"].split("#")[1]
                lines = lines.replace("L", "")
                lines = f"[{lines}]"

            registry_url = ""
            if "packageMetadata" in dependency:
                registry_url = dependency["packageMetadata"]["registryUrl"]

            sbom_finding_list.append(
                {
                    "Package": dependency["name"],
                    "Version": dependency["version"],
                    "Fix Version": fix_version,
                    "Git Org": repo["name"].split("/")[0],
                    "Git Repository": repo["name"].split("/")[1],
                    "Line(s)": lines,
                    "Path": repo["filePath"],
                    "Registry URL": registry_url,
                    "Root Package": root_package,
                    "Root Version": root_package_version,
                    "Severity": severity,
                    "Vulnerability": cve_id,
                    "Licenses": dependency["license"],
                }
            )

    print(f"Wrote {len(sbom_finding_list)} packages findings to {file}")
    with open(file=file, mode="a", newline="") as merger:
        merged_writer = csv.DictWriter(
            f=merger,
            fieldnames=[
                "Package",
                "Version",
                "Fix Version",
                "Git Org",
                "Git Repository",
                "Line(s)",
                "Path",
                "Registry URL",
                "Root Package",
                "Root Version",
                "Severity",
                "Vulnerability",
                "Licenses",
            ],
        )
        merged_writer.writerows(sbom_finding_list)

"""
package findings are Code Category: Vulnerabilities
"""
