# Create File Content from the artifact
 http POST $BASE_ADDR/pulp/api/v3/content/file/files/ \
     relative_path=test_upload.txt \
    _artifact=$ARTIFACT_HREF

export CONTENT_HREF=$(http :24817/pulp/api/v3/content/file/files/ | \
    jq -r '.results[] | select(.relative_path == "test_upload.txt") | ._href')

# Lets inspect our newly created file content
http $BASE_ADDR$CONTENT_HREF
