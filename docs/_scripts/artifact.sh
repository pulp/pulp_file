# Create a dummy file to upload
echo "Very important content." > test_upload.txt

# Upload the file to Pulp, creating an artifact
export ARTIFACT_HREF=$(http --form POST $BASE_ADDR/pulp/api/v3/artifacts/ file@./test_upload.txt \
    | jq -r '._href')

# Lets inspect our newly created artifact
http $BASE_ADDR$ARTIFACT_HREF
