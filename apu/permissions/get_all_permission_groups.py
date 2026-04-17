#!python

# https://pan.dev/prisma-cloud/api/cspm/get-all/
import json
from dataclasses import dataclass

from dacite import from_dict
import requests

from apu.utils import constants, login


@dataclass
class permission:
    acceptAccountGroups: bool
    acceptCodeRepositories: bool
    acceptResourceLists: bool
    associatedRoles: dict[str, str]
    description: str
    features: list[dict[str, str | dict[str, bool]]]
    lastModifiedBy: str
    lastModifiedTs: int
    name: str
    type: str


def parse_features(features):
    restructured_features = []
    for feat in features:
        if "CREATE" in feat["operations"]:
            create = bool(feat["operations"]["CREATE"])
        else:
            create = False

        if "READ" in feat["operations"]:
            read = bool(feat["operations"]["READ"])
        else:
            read = False

        if "UPDATE" in feat["operations"]:
            update = bool(feat["operations"]["UPDATE"])
        else:
            update = False

        if "DELETE" in feat["operations"]:
            delete = bool(feat["operations"]["DELETE"])
        else:
            delete = False

        anything = create or read or update or delete

        restructured_features.append(
            {
                "featureName": feat["featureName"],
                "create": create,
                "read": read,
                "update": update,
                "delete": delete,
                "any": anything,
            }
        )
    return restructured_features


def parse_permissions(permissions_json):
    permission_list = []
    for permission in permissions_json:
        permission_list.append(
            {
                "features": parse_features(permission),
            }
        )
    return permission_list


def get(includeAssociatedRoles=True, includeFeatures=True):
    params = {
        "includeAssociatedRoles": includeAssociatedRoles,
        "includeFeatures": includeFeatures,
    }
    payload = ""
    url = f"{login.settings['url']}/authz/v1/permission_group"
    response = requests.request(
        method="GET", url=url, headers=login.headers, data=payload, params=params
    )
    response.raise_for_status()
    return json.loads(response.text)


if __name__ == "__main__":
    login.login()
    permission_groups = get()
    for permission_obj in permission_groups:
        print(
            from_dict(
                data_class=permission,
                data=permission_obj,
            )
        )
    filename = f"{constants.script_dir}/permissions.json"
    with open(filename, "w+", newline="", encoding="utf-8") as file:
        json.dump(permission_groups, file, indent=4)
        print(f"Permissions written to {filename}")
