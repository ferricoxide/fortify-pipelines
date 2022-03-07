#!/usr/bin/env python3
"""
Tool to request creation of a new version-ID for an existing project
("application") tracked in the Fortify Software Security Center Service
"""

import datetime
import json
import os
import sys
import requests

# Suppress certificate warings (while prototyping)
import urllib3
urllib3.disable_warnings()

def token_fetch():
    """
    Fetch an ephemeral, 'UnifiedLoginToken' API-token from SSC
    """
    # Time-info to send as part of request for Unified Login Token
    current_time = datetime.datetime.utcnow()
    expiration =   current_time + datetime.timedelta(days=1)
    expiration =   expiration.isoformat()
    data = {
      "description": "string",
      "terminalDate": expiration,
      "type": "UnifiedLoginToken"
    }

    # use username and password to get unified login token that expires in one day
    headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    }
    unified_token_response = requests.post(
      f'https://{ssc_user_name}:{ssc_user_pass}@{ssc_url}/api/v1/tokens',
      headers=headers,
      json=data,
      verify=False
    )

    # Extract token string from response
    return unified_token_response.json()

def token_nuke(id_to_nuke):
    """
    Erase previously-created 'UnifiedLoginToken' API-tokens
    """

    # use username and password to get unified login token that expires in one day
    headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json'
    }

    unified_token_response = requests.delete(
      f'https://{ssc_user_name}:{ssc_user_pass}@{ssc_url}/api/v1/tokens?ids={id_to_nuke}',
      headers=headers,
      verify=False
    )

    # Check if cleanup worked
    if unified_token_response.json()['responseCode'] == 200:
        print(f"Successfully cleaned up token-ID '{token_id}'")
    else:
        print(f"Failed cleaning up token-ID '{token_id}'")
        sys.exit(1)

def project_exists(ssc_project_name):
    """
    Ensure that the target SSC application/project actually exists
    """
    print('Checking for project named', ssc_project_name)

    api_response = requests.get(
      f'https://{ssc_url}/api/v1/projects?fulltextsearch=true&q=name={ssc_project_name}',
      headers=headers_ulf,
      verify=False
    )

    # Extract token string from response
    return api_response.json()

def get_project_versions():
    """
    Check to see if desired project-version (name) already exists
    """
    # Dump out *all* the project-versions: It'd be really great if could figure
    # out a less-noisy method to do this
    api_response = requests.get(
      f'https://{ssc_url}/api/v1/projectVersions',
      headers=headers_ulf,
      verify=False
    )

    # Create a list of ONLY those project-versions that are part of the desired
    # project
    version_list = []
    for versions in api_response.json()['data']:
        if versions['project']['name'] == ssc_app_name:
            version_list.append(versions['name'])

    # Extract token string from response
    return version_list

def version_create_bare():
    """
    Request creation of the new application/project-version
    """
    # Minimum payload for a version-creation action
    data = {
      "name": f"{ssc_app_vers}",
      "description": "API-created version",
      "active": "true"
    }

    # Submit bare version-creation request
    api_response = requests.post(
      f'https://{ssc_url}/api/v1/projects/{project_id}/versions',
      headers=headers_ulf,
      json=data,
      verify=False
    )

    # Extract token string from response
    return api_response.json()

def version_add_template(new_id):
    """
    Assign an issue-template to the bare project-version
    """
    # Generic issue-template to apply
    data = {
      'issueTemplateId': 'Prioritized-HighRisk-Project-Template'
    }

    # Apply generic issue-template to the bare project-version
    api_response = requests.put(
      f'https://{ssc_url}/api/v1/projectVersions/{new_id}',
      headers=headers_ulf,
      json=data,
      verify=False
    )

    # Extract token string from response
    return api_response.json()

def version_add_attrs(new_id):
    """
    Add set of generic attributes to the bare project-version
    """
    # Generic issue-template to apply
    with open('stubAttrs.json', 'r', encoding="ascii") as file:
        data = json.loads(file.read().replace('\n', ''))


    # Attach attributes to new project-version
    api_response = requests.put(
      f'https://{ssc_url}/api/v1/projectVersions/{new_id}/attributes',
      headers=headers_ulf,
      json=data,
      verify=False
    )

    # Extract token string from response
    return api_response.json()

def kill_processing_rules(new_id):
    """
    Ensure that all processing-rules are disabled
    """
    # Generic issue-template to apply
    with open('processingRules.json', 'r', encoding="ascii") as file:
        data = json.loads(file.read().replace('\n', ''))

    # Disable processing-rules in new project-version
    api_response = requests.put(
      f'https://{ssc_url}/api/v1/projectVersions/{new_id}/resultProcessingRules',
      headers=headers_ulf,
      json=data,
      verify=False
    )

    # Extract token string from response
    return api_response.json()

def version_commit(new_id):
    """
    Activate the new project-version
    """
    # Commit payload
    data = { 'committed': 'true' }

    # Commit new project-version
    api_response = requests.put(
      f'https://{ssc_url}/api/v1/projectVersions/{new_id}',
      headers=headers_ulf,
      json=data,
      verify=False
    )

    # Return the API-response contents
    return api_response.json()


if __name__ == '__main__':
    # Set missing-arguments collector to 0
    MISSING_ARGS = 0

    # Set name of SSC application/project
    if len(os.environ.get('SSC_APP_NAME', [])) != 0:
        ssc_app_name = os.environ.get('SSC_APP_NAME')
    else:
        MISSING_ARGS = 1
        print("SSC_APP_NAME value not set", file=sys.stderr)

    # Set FQDN of SSC server
    if len(os.environ.get('SSC_URL', [])) != 0:
        ssc_url = os.environ.get('SSC_URL')
    else:
        MISSING_ARGS = 1
        print("SSC_URL value not set", file=sys.stderr)

    # Set name of SSC project-user password
    if len(os.environ.get('SSC_USER_PASS', [])) != 0:
        ssc_user_pass = os.environ.get('SSC_USER_PASS')
    else:
        MISSING_ARGS = 1
        print("SSC_USER_PASS value not set", file=sys.stderr)

    # Set name of SSC project-user name
    if len(os.environ.get('SSC_USER_NAME', [])) != 0:
        ssc_user_name = os.environ.get('SSC_USER_NAME')
    else:
        MISSING_ARGS = 1
        print("SSC_USER_NAME value not set", file=sys.stderr)

    # Set name of SSC application/project version
    if len(os.environ.get('SSC_APP_VERS', [])) != 0:
        ssc_app_vers = os.environ.get('SSC_APP_VERS')
    elif len(os.environ.get('CI_COMMIT_BRANCH', [])) != 0:
        ssc_app_vers = os.environ.get('CI_COMMIT_BRANCH')
    else:
        MISSING_ARGS = 1
        print("SSC_APP_VERS value not set", file=sys.stderr)

    if MISSING_ARGS == 1:
        sys.exit(1)

    # Create UnifiedLogin token
    token_response = token_fetch()

    # Check if that worked
    if token_response['responseCode'] == 201:
        token_id = token_response['data']['id']
        token_str = token_response['data']['token']
        status_msg = f"Successfully created token-id '{token_id}' "\
                     f"with UnifiedLoginToken string '{token_str}'"

        # use UnifiedLoginToken from token_str to enable authentciation to other
        # ReST APIs
        headers_ulf = {
          'accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': f'FortifyToken {token_str}'
        }
        print(status_msg)
    else:
        print('Failed generating UnifiedLoginToken. Aborting')
        sys.exit(1)


    # Check if target-project exists
    project_response = project_exists(ssc_app_name)

    if project_response['count'] == 1:
        project_id = project_response['data'][0]['id']
        print(f"Found SSC Group ID '{project_id}' for project-name '{ssc_app_name}'")
    else:
        token_nuke(token_id)
        sys.exit(1)


    # Check if requested project-version already exists
    if ssc_app_vers in get_project_versions():
        print(f"Found '{ssc_app_vers}' version for project-name '{ssc_app_name}'")
        token_nuke(token_id)
        sys.exit()
    else:
        print(f"Version '{ssc_app_vers}' does not exist for project-name '{ssc_app_name}'")


    # Attempt to create requested project-version
    version_response = version_create_bare()
    if version_response['responseCode'] == 201:
        version_id = version_response['data']['id']
        status_msg = f"Created version-string '{ssc_app_vers}' " \
                     f"as ID# '{version_id}' " \
                     f"for project-name '{ssc_app_name}'"
        print(status_msg)
    else:
        token_nuke(token_id)
        sys.exit(1)


    # Attempt to add standard issue-template to new project-version
    if version_add_template(version_id)['responseCode'] == 200:
        print(f"Successfully added standard issue-template to '{ssc_app_name}:{ssc_app_vers}'")
    else:
        print(f"Failed to add standard issue-template to '{ssc_app_name}:{ssc_app_vers}'")
        token_nuke(token_id)
        sys.exit(1)


    # Attempt to add standard attributes to new project-version
    if version_add_attrs(version_id)['responseCode'] == 200:
        print(f"Successfully added standard attributes to '{ssc_app_name}:{ssc_app_vers}'")
    else:
        print(f"Failed to add standard attributes to '{ssc_app_name}:{ssc_app_vers}'")
        token_nuke(token_id)
        sys.exit(1)

    # Attempt to override processing-rule
    if kill_processing_rules(version_id)['responseCode'] == 200:
        print(f"Successfully removed processing rull from '{ssc_app_name}:{ssc_app_vers}'")
    else:
        print(f"Failed removing processing-rules from '{ssc_app_name}:{ssc_app_vers}'")
        token_nuke(token_id)
        sys.exit(1)

    # Attempt to commit the new project-version
    if version_commit(version_id)['responseCode'] == 200:
        print(f"Successfully committed '{ssc_app_name}:{ssc_app_vers}'")
    else:
        print(f"Failed committing '{ssc_app_name}:{ssc_app_vers}'")
        token_nuke(token_id)
        sys.exit(1)

    # Try to clean up any generated tokens before exiting
    token_nuke(token_id)
