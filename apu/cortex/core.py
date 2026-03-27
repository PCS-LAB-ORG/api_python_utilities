from apu.cortex import jrequest

def get_alerts():
    url = "alerts/get_alerts"

    payload = {
        "request_data": {
            # "filters": {}},
            # "alerts_limit": 1000 # default 1000
        }
    }

    response = jrequest.post(url, payload)
    print(response)
    return response

def issue_search():
    url = "issue/search"

    payload = {
        "request_data": {
            "filters": [{"field": "issue_id", "operator": "in", "value": [0]}],
            "search_from": 0,
            "search_to": 2,
            "sort": {"field": "issue_id", "keyword": "asc"},
        }
    }
    response = jrequest.post(url, payload)
    print(response)
    return response

def get_datasets():
    url = "xql/get_datasets"
    payload = { "request_data": {} }
    response = jrequest.post(url, payload)
    print(response)
    return response

def get_endpoints():
    url = "endpoints/get_endpoints"
    payload = { "request_data": {} }
    response = jrequest.post(url, payload)
    print(response)
    return response

def get_incidents():
    url = "alerts/get_incidents"
    payload = { "request_data": {} }
    response = jrequest.post(url, payload)
    print(response)
    return response

def unified_cli_releases_version():
    url = "unified-cli/releases/version"
    response = jrequest.get(url)
    print(response)
    return response

def case_search():
    url = "case/search"
    payload = {
        "request_data": {
            "filters": [{"field": "severity", "operator": "in", "value": ["HIGH"]}],
            "search_from": 0,
            "search_to": 2,
            "sort": {"field": "case_id", "keyword": "asc"},
        }
    }
    response = jrequest.post(url, payload)
    print(response)
    return response

def xql_lookups_get_data():
    url = "xql/lookups/get_data"
    dataset_name = "asdfsa" # for debugging 'a' is an existing table
    # if dataset_name and not len(sys.argv) > 1:
    #     raise Exception("Table name is required")
    # dataset_name = sys.argv[1]

    limit = 20
    # if len(sys.argv) > 2:
    #     limit = int(sys.argv[2])

    filters = []
    # if len(sys.argv) > 3:
    #     filters = json.loads(sys.argv[3])
    # [
        # {
        #     # "uid": "123",
        #     "user_email": "hiep@abc.com"
        # },
        # {
        #     "department": "dev",
        #     "zipcode": "58674"
        # }
    # ],

    payload = {
        "request": {
            "dataset_name": dataset_name,
            "filters": filters,
            "limit": limit
        }
    }

    response = jrequest.post(url, payload)
    print(response)
    return response

def incidents_extra_data():
    url = "incidents/get_incident_extra_data"
    payload = {
        "request_data": {
            "incident_id": "",
            # "alerts_limit": 1000 # default 1000
        }
    }
    response = jrequest.post(url, payload)
    print(response)
    return response

def asset_groups():
    url = "asset-groups"
    payload = {
        "request_data": {
            #     "AND": [
            #         {
            #             "SEARCH_FIELD": "XDM.ASSET_GROUP.TYPE",
            #             "SEARCH_TYPE": "EQ",
            #             "SEARCH_VALUE": "Dynamic",
            #         }
            #     ]
            # },
            # "sort": [{"FIELD": "XDM.ASSET_GROUP.LAST_UPDATE_TIME", "ORDER": "DESC"}],
            # "search_from": 0,
            # "search_to": 1000,
        }
    }
    response = jrequest.post(url, payload)
    print(response)
    return response
