# Rotate Expired Key

## No key given
- If no key is given attempt to create a new key
- If 2 keys already exist, list all
- Ask to remove a key, recommend expired
- Create new key

## Key given
- Key can be 'given' by the access key, friendly name, or credential file containing the key/secret pair in the standard formats (csv, credentials.json, properties files)
    - use overloaded key name mapping to support credentials files that use alternative key names for the access_key
- If key is given, delete and create new key with same attributes
    - Key can be identified by name or access key value
- If key not found, proceed the 'no key given' path

## Key considerations
- do no allow deleting the key used to make the API calls
