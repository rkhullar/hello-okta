#!/usr/bin/env sh

# find root of subproject
export root
root="$(dirname "$0")/../frontend-nextjs"
cd "$root" || exit
export root=${PWD}
echo "$root"

# TODO
# unzip assets; emtpy static bucket; sync to static bucket
# - cd path/to/archive
# - rm -rf assets && unzip assets.zip -d assets
# - aws s3 sync ./assets s3://serverless-poc-static-sbx
# - rm -rf assets
# upload default lambda; publish new version
# - aws lambda update-function-code --function-name serverless-poc-default-sbx --zip-file fileb://default-lambda.zip --publish
# upload api lambda; publish new version
# - aws lambda update-function-code --function-name serverless-poc-api-sbx --zip-file fileb://api-lambda.zip --publish
# update cloudfront lambda@edge integrations
# - have terraform ignore version drift?
    - no, after updating the lambda function, terraform wants to update the integrations with the correct arns
# - default lambda -> default behavior (origin request and response)
# - api lambda -> api behavior (origin request only)
# - default lambda -> data behavior (origin request and response)
# create cloudfront invalidation for '/*'
