if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

# Download the schema
curl -o api.json "http://localhost:24817/pulp/api/v3/docs/api.json?bindings&plugin=$1"
# Get the version of the pulpcore or plugin as reported by status API

export VERSION=$(http :24817/pulp/api/v3/status/ | jq --arg plugin $1 -r '.versions[] | select(.component == $plugin) | .version')

podman run -u $(id -u) --rm -v ${PWD}:/local openapitools/openapi-generator-cli:v4.2.3 generate \
    -i /local/api.json \
    -g python \
    -o /local/$1-client \
    --additional-properties=packageName=pulpcore.client.$1,projectName=$1-client,packageVersion=${VERSION} \
    --skip-validate-spec \
    --strict-spec=false

sed -i "s/docs/client/g" $1-client/README.md
find $1-client/docs/* -exec sed -i 's/README/client/g' {} \;
find $1-client/docs/* -exec sed -i 's/\[\[Back to top\]\]//g' {} \;
find $1-client/docs/* -exec sed -i 's/(#)//g' {} \;
find $1-client/docs/* -exec sed -i 's/\[\**object\**\](.md)/**object**/g' {} \;
mv $1-client/docs docs/client
mv $1-client/README.md docs/client.md

cd docs
echo "## Client Documentation" >> client.md
for f in client/*
do
  echo "- [$(basename ${f%.md*})](${f})" >> client.md
done

make html
cd ..

rm api.json
rm -rf $1-client
