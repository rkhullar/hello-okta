#!/usr/bin/env sh

# find root of subproject
export root
root="$(dirname "$0")/../frontend-nextjs"
cd "$root" || exit
export root=${PWD}
echo "$root"

rm -rf .next .serverless .serverless_nextjs
components-v1

rm -rf archive && mkdir -p archive
export archive_path="${root}/archive"
export build_path="${root}/.serverless_nextjs"

cd "${build_path}/assets" && zip -r9 "${archive_path}/assets.zip" *
cd "${build_path}/default-lambda" && zip -r9 "${archive_path}/default-lambda.zip" *
cd "${build_path}/api-lambda" && zip -r9 "${archive_path}/api-lambda.zip" *
cd "${build_path}/regeneration-lambda" && zip -r9 "${archive_path}/regeneration-lambda.zip" *
# cd "${build_path}/image-lambda" && zip -r9 "${archive_path}/image-lambda.zip" *
