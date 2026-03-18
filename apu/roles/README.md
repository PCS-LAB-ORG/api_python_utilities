# Backup & Restore Procedure

##  Support Backup should be considered

Reach out to the support team for this restoration as they will be able to collect and restore all data for 7 days post-dataloss. As of early 2026, when there are API failures from VCS providers Prisma Cloud may lose access to those repos. This has to be reviewed by the product teams. There is a role table that has to be restored to a good point in time and the repos have to be re-discovered by Prisma.

## Manual Restoration

See accompanying scripts that account for a few extra checks that use logging and a step-wise procedure for review and editing these datasets manually as needed. (For example, if you only wanted to restore repos from a single provider type, you can edit the backup file used in this process.)

The process and script are written to work with definitive identifiers (ID matching). This is the preferred exact process. When partial data or missing data must be accounted for please consider the extra data attributes of each step to help build proper rules for your goal.

The scripts are written to retrieve and update ALL repos and roles.

## Backup Repos

`python get_repos_csv.py`

Call repository api and save to file

API endpoint /repositories has enough data if the repos still exist in Prisma and is faster and has the repo ID needed for restoration..

If you do not have a repo backup then this API will give more data about repos that may help find attributes that identify which repos are grouped together. https://pan.dev/prisma-cloud/api/code/get-vcs-repository/

## Backup Roles

`python get_roles.py`

Call /roles api and save to file.. https://pan.dev/prisma-cloud/api/cspm/get-user-roles/


# If there is a repo provider outage then

Ensure the repositories are reconnected first

## Use this to restore the roles

### Get roles backup

see [Backup Repos](#Backup_Repos)

### Get repos backup

see [Backup Roles](#Backup_Roles)

### Add repos to matching roles

`python add_repos_to_role.py`

use this API to update existing roles API /roles... https://pan.dev/prisma-cloud/api/cspm/update-user-role/

### How the matching works

Key Points:
- a repo is uniquely identified by its owner and repo name
- prisma assigns an ID to each repo

1. take the repo ID list of each role from the backup before the outage
2. match this old repo ID from the roles to the list of repos backed up using /repositories before the outage
3. match this old repo list to the repos reconnected to prisma by owner/repositoryName
4. get the new prisma repo ID of each repo for each role
5. add the new repo IDs to their matched role


# How To Test

1. Create a new role
2. Add some repos to the role
3. Simulate a backup
    1. Get Roles
    2. Get Repos
    3. Discard unrelated data. Only pull the role you just created. You should be able to work with the full list of repos.
4. Simulate an outage by removing repos from the role you created.
5. Run the `add_repos_to_role.py` script with the backup files for roles and repos.
6. Check in the UI to confirm the repos have been added back to your new role.

# Checklist
- [x] Do a backup and recovery test.
- [x] Recover roles that had some repos in them after 'outage' test.
