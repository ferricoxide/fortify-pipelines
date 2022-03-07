# Create Basic auth-token from credential-pair

~~~
  printf "%s:%s" "${SSC_USER_NAME}" "${SSC_USER_PASS}" | base64
~~~

# List Unified-Login tokens

~~~
   curl -sX GET "https://${SSC_FQDN}/api/v1/tokens?start=0&limit=200" \
     -H "accept: application/json" \
     -H "authorization: Basic ${BASIC_AUTH_STRING}" | \
   jq --exit-status '.data[].id'

~~~

# Request Unified-Login token

~~~
  curl -sX POST "https://${SSC_FQDN}/api/v1/tokens" \
    -H "accept: application/json" \
    -H "authorization: Basic ${BASIC_AUTH_STRING}" | \
    -H "Content-Type: application/json" \
    -d "{ \"description\": \"string\", \"terminalDate\": \"$( date  --date="tomorrow" '+%FT%T.000+0000' )\", \"type\": \"UnifiedLoginToken\"}" | \
  jq -r --exit-status .data.token
~~~

# Delete Unified-Login token

~~~
  curl -sX DELETE "https://${SSC_FQDN}/api/v1/tokens?ids=${TOKEN_ID}" \
    -H "accept: application/json" \
    -H "authorization: Basic ${BASIC_AUTH_STRING}" | \
  jq --exit-status .
~~~

# Get List of Attribute Definitions

~~~
  curl -X GET "https://${SSC_FQDN}/api/v1/attributeDefinitions?start=0&limit=200" \
    -H "accept: application/json" \
    -H "Authorization: FortifyToken ${UNIFIED_LOGIN_TOKEN}"

~~~

# Get Processing Rules for Version

~~~
  curl -sX GET "https://${SSC_FQDN}/api/v1/projectVersions/${VERSION_ID}/resultProcessingRules" \
    -H "accept: application/json" \
    -H "Authorization: FortifyToken ODNiYTY3MjYtODFkYy00N2QzLWE4NzUtMzUxNmVkZGMyZmIx" | \
  jq --exit-status '.data[]'
~~~

or

~~~
  ...
  jq --exit-status '.data[] | {displayName: .displayName, enabled: .enabled}'
~~~

# Create new version:

~~~
  curl -s -X POST "https://${SSC_URL}/api/v1/projects/${SSC_APP_ID}/versions" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -H "authorization: FortifyToken $( jq '.data.token' <<< "${TOKENVAR}" )" \
    -d "{ \"name\": \"${SSC_APP_VERSION}\", \"description\": \"API-created version\", \"active\": true }"
~~~
  

# Attach Issue-template to version:

~~~
  curl -s -X PUT "https://${SSC_URL}/api/v1/projectVersions/${NEW_ID}" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -H "authorization: FortifyToken $( jq '.data.token' <<< "${TOKENVAR}" )" \
    -d '{ "issueTemplateId": "Prioritized-HighRisk-Project-Template" }'
~~~
  

# Attach attributes to version:

~~~
  curl -s -X PUT "https://${SSC_URL}/api/v1/projectVersions/${NEW_ID}/attributes" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -H "authorization: FortifyToken $( jq '.data.token' <<< "${TOKENVAR}" )" \
    -d "$( < "${SSC_ATTR_FILE}" )"
~~~
  

# Commit version:

~~~
  curl -s -X PUT "https://${SSC_URL}/api/v1/projectVersions/${NEW_ID}" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -H "authorization: FortifyToken $( jq '.data.token' <<< "${TOKENVAR}" )" \
    -d "{ \"committed\": true }" && echo
~~~
  
