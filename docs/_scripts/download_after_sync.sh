# The distribution will return a url that can be used by http clients
echo "Setting DISTRIBUTION_BASE_URL, which is used to retrieve content from the content app."
export DISTRIBUTION_BASE_URL=$(http $BASE_ADDR$DISTRIBUTION_HREF | jq -r '.base_url')

# Next we download a file from the distribution
http -d http://$DISTRIBUTION_BASE_URL/test.iso
