#!/usr/bin/python
"""
Tool to request creation of a new version-ID for an existing project
("application") tracked in the Fortify Software Security Center Service
"""

import argparse
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
    # Set up argument-parsing
    script_opts = argparse.ArgumentParser(
        description='Utility to create new versions for SSC projects'
    )
    script_opts.add_argument(
        "-a",
        "--project-name",
        dest="ssc_app_name",
        help="SSC project/application name"
    )
    script_opts.add_argument(
        "-f",
        "--ssc-fqdn",
        dest="ssc_url",
        help="FQDN of the SSC server"
    )
    script_opts.add_argument(
        "-p",
        "--ssc-userpass",
        dest="ssc_user_pass",
        help="SSC user password"
    )
    script_opts.add_argument(
        "-u",
        "--ssc-username",
        dest="ssc_user_name",
        help="SSC user name"
    )
    script_opts.add_argument(
        "-v",
        "--project-vers",
        dest="ssc_app_vers",
        help="SSC project/application version"
    )

    script_args = script_opts.parse_args()

    # Set name of SSC application/project
    if script_args.ssc_app_name:
        ssc_app_name = script_args.ssc_app_name
    else:
        ssc_app_name = os.environ.get('SSC_APP_NAME', [])

    # Set FQDN of SSC server
    if script_args.ssc_url:
        ssc_url = script_args.ssc_url
    else:
        ssc_url = os.environ.get('SSC_URL', [])

    # Set name of SSC project-user password
    if script_args.ssc_user_pass:
        ssc_user_pass = script_args.ssc_user_pass
    else:
        ssc_user_pass = os.environ.get('SSC_USER_PASS', [])

    # Set name of SSC project-user name
    if script_args.ssc_user_name:
        ssc_user_name = script_args.ssc_user_name
    else:
        ssc_user_name = os.environ.get('SSC_USER_NAME', [])

    # Set name of SSC application/project version
    if script_args.ssc_app_vers:
        ssc_app_vers = script_args.ssc_app_vers
    else:
        ssc_app_vers = os.environ.get('SSC_APP_VERSION', [])

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
        token_nuke(token_id)
        sys.exit(1)


    # Attempt to add standard attributes to new project-version
    if version_add_attrs(version_id)['responseCode'] == 200:
        print(f"Successfully added standard attributes to '{ssc_app_name}:{ssc_app_vers}'")
    else:
        token_nuke(token_id)
        sys.exit(1)

    # Attempt to commit the new project-version
    if version_commit(version_id)['responseCode'] == 200:
        print(f"Successfully committed '{ssc_app_name}:{ssc_app_vers}'")
    else:
        token_nuke(token_id)
        sys.exit(1)

    # Try to clean up any generated tokens before exiting
    token_nuke(token_id)
