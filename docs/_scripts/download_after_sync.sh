# The distribution will return a url that can be used by http clients
export DISTRIBUTION_BASE_URL=$(http $BASE_ADDR$DISTRIBUTION_HREF | jq -r '.base_url')

# Next we download a file from the distribution
http -d http://$DISTRIBUTION_BASE_URL/test.iso
