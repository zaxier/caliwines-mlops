dbx configure -e dev \
    --workspace-dir /Shared/zaxier/packaged-poc/dev/ \
    --artifact-location dbfs:/Shared/zaxier/packaged-poc/dev/dbx/artifacts \
    --profile aws-dev

dbx configure -e staging \
    --workspace-dir /Shared/zaxier/packaged-poc/staging/ \
    --artifact-location dbfs:/Shared/zaxier/packaged-poc/staging/dbx/artifacts \
    --profile aws-staging

dbx configure -e prod \
    --workspace-dir /Shared/zaxier/packaged-poc/prod/ \
    --artifact-location dbfs:/Shared/zaxier/packaged-poc/prod/dbx/artifacts \
    --profile aws-prod