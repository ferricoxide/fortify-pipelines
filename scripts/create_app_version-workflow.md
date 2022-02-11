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
  
