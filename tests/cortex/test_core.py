#!/python

# import pytest

from apu.cortex import core

def test_get_alerts():
    alerts = core.get_alerts()
    int(alerts.get("reply").get('total_count'))

def test_issue_search():
    issues = core.issue_search()
    assert issues

def test_get_datasets():
    datasets = core.get_datasets()
    assert datasets

def test_get_endpoints():
    endpoints = core.get_endpoints()
    assert endpoints

def test_get_incidents():
    incidents = core.get_incidents()
    assert incidents

def test_unified_cli_releases_version():
    release_version = core.unified_cli_releases_version()
    assert release_version

def test_case_search():
    cases = core.case_search()
    assert cases

def test_xql_lookups_get_data():
    xql = core.xql_lookups_get_data()
    assert xql

def test_incidents_extra_data():
    incidents = core.incidents_extra_data()
    assert incidents

def test_asset_groups():
    asset_groups = core.asset_groups()
    assert asset_groups

def test_get_issues():
    issues = core.get_issues()
    assert issues

def test_get_roles():
    roles = core.get_roles()
    assert roles

def test_syslog_get():
    logs = core.syslog_get()
    assert logs

def test_get_user_group():
    user_group = core.get_user_group()
    assert user_group

def test_get_users():
    users = core.get_users()
    assert users

def test_policy_search():
    policies = core.policy_search()
    assert policies

def test_iam_user():
    user = core.iam_user()
    assert user
