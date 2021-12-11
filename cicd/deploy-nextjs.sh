#!/usr/bin/env sh

# find root of subproject
export root="$(dirname $0)/../frontend-nextjs"
cd $root
export root=${PWD}
echo $root

# TODO
# unzip assets; emtpy static bucket; sync to static bucket
# - cd path/to/archive
# - rm -rf assets && unzip assets.zip -d assets
# - aws s3 sync ./assets s3://serverless-poc-static-sbx
# - rm -rf assets
# upload default lambda; publish new version
# upload api lambda; publish new version
# update cloudfront lambda@edge integrations
# - have terraform ignore version drift?
# - default lambda -> default behavior (origin request and response)
# - api lambda -> api behavior (origin request only)
# - default lambda -> data behavior (origin request and response)
# create cloudfront invalidation for '/*'
