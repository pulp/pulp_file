export ARTIFACT_RELATIVE_PATH=$(head /dev/urandom | tr -dc a-z | head -c5)

echo 'Create File Content from the artifact and save as environment variable'
export CONTENT_HREF=$(http POST $BASE_ADDR/pulp/api/v3/content/file/files/ \
    relative_path=$ARTIFACT_RELATIVE_PATH \
    _artifact=$ARTIFACT_HREF \
    | jq -r .'_href')

echo "Inspecting new file content"
http $BASE_ADDR$CONTENT_HREF
