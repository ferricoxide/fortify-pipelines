# Integrating With Existing Projects

The contents of this project are provided as an `include`able, "stageless" pipeline. When `include`d, it adds the following jobs to the project's existing pipeline:

1. `fortify_vers_prep`: Check SSC for the existence of the target application-version; create if not present
1. `fortify_code-prep`: Process the project's code in preparation for upload to SSC
1. `fortify_push2ssc`: Upload the project's processed-code to SSC
1. `fortify_ssc-export`: Pull the scan-report from SSC and inject it into the GitLab project's security-dashboard (also available under the pipeline's "Security" tab upon completion of the pipeline)

This workflow will be opportunistically-run in parallel to jobs already defined within the `.gitlab-ci.yml` file.

## Adding Fortify Workflow to Existing Pipelines

At the most basic, adding this project's contents to another project's pipelines is as simple as adding a block similar to the following:

~~~
include:
  - project: '${FORTIFY_CI_TEMPLATE_PROJECT}'
    ref: '${FORTIFY_CI_TEMPLATE_BRANCH}'
    file: 'templates/fortify-ssc.yml'
~~~

To your project's `.gitlab-ci.yml` file. Once the templates have been referenced, per the above code-snippet, future pipeline-executions will attempt to interface with the environment's SSC service.

In order for future pipeline-executions to be able to successfully upload scan-artifacts to and import scan-reports from a GitLab project's SSC project-space, it is necessary to add an `SSC_APP_NAME` to each Fortify-enabled GitLab repository's CI/CD variables. The `SSC_APP_NAME` value will be a case-sensitive string forwarded to the repository-owner from the SSC administrator.

Note: It is expected that the above `FORTIFY_CI_TEMPLATE_PROJECT` and `FORTIFY_CI_TEMPLATE_BRANCH` will have been added to the GitLab Runners' global environment variables. If this is not the case &ndash; or if the project-owner or project-user wishes to override the global values &ndash; the values can be set at the project-group or individual repository levels, as well as within a project's `.gitlab-ci.yml` file or within the job-runner web UI.

## Fortify Workflow Initiation-Control

If only the above snippet is added to the project's `.gitlab-ci.yml` file, the Fortify pipeline-jobs will be executed as soon as the GitLab runner begins execution of the pipline's `Test` stage. The `Test` stage is a reserved stage-name that a GitLab runner will always run, even if your pipeline-definitions do not explicitly define one. In order to provide more control of if/when/how the Fortify components are executed, the developer will want to add a stanza similar to:

~~~
fortify_vers-prep:
  needs:
      - <STAGE_NAME_1>
      - <STAGE_NAME_2>
      - [...elided...]
      - <STAGE_NAME_N>
~~~

To their project's `.gitlab-ci.yml` file. The `fortify_vers-prep` job is the first job defined in the included Fortify job-flow. Setting a dependency on one or more of the project's other jobs, will ensure that the Fortify job-flow does not start until after the referenced stage(s) successfully complete.

Note: any job parameters available for controlling the project's other jobs can be injected into the above stanza (e.g. if one wanted to ensure that Fortify jobs only ran for specific branch-names, one could add appropriate `rules:` stanzas).

## Extra Artifacts

For users that wish to generate a PDF-based report, one can also add the `fortify_report-pdf` job to their pipelines by adding:

~~~
  - project: '${FORTIFY_CI_TEMPLATE_PROJECT}'
    ref: '${FORTIFY_CI_TEMPLATE_BRANCH}'
    file: 'templates/fortify-standalone.yml'
~~~

To their `.gitlab-ci.yml` file's `include` section. By default, this job is defined to wait for successful completion of the `fortify_code-prep` job and will upload a PDF-formatted scan-report as `fortify-scan-results.pdf` to GitLab.

## A Note on Branch-Naming

By default, the pipelines will reference the `CI_BUILD_REF_NAME` GitLab pipeline-variable to set the version-name it uses when uploading to and exporting from SSC: whatever your branch-name is is the version-name that will be used in SSC. While SSC is not expected to be directly-used by users, this note is made so that integration-users can be aware of how uploaded artifacts are tracked/referenced within SSC.

This default behavior can be overridden by adding a `SSC_APP_VERS` parameter-value to the project's CI/CD variables. However, setting this variable in other than ad hoc pipeline runs can result in _all_ future jobs re-using the same version-string if pipeline users don't update the parameter-value with each new work-branch.

## Variables Effecting Fortify-Integration

In addition to the `FORTIFY_CI_TEMPLATE_PROJECT` and `FORTIFY_CI_TEMPLATE_BRANCH` variables, it is expected that the GitLab service-owner will also have set:

* `FORTIFY_CONTAINER_DEFAULT`: The container used for basic (non-specialty), container-based GitLab-CI tasks. It's expected that this container will be of a `python:3` type
* `FORTIFY_CONTAINER_EXPORTER`: Name of the Fortify vulnerability-exporter Docker container
* `FORTIFY_CONTAINER_SCA`: Name of the Fortify SCA Docker container
* `FORTIFY_CONTAINER_VERSUTIL`: Name of the Docker-container that contains the Fortify version-utility
* `SSC_URL`: The fully-qualified domain-name of the SSC server
* `SSC_USER_NAME`: The SSC service-user created for the project-space within SSC
* `SSC_USER_PASS`: The cleartext password of the SSC service-user created for the project-space within SSC
* `SSC_TRANSFER_TOKEN`: The API token generated by the SSC service-administrator to access SSC resources delegated to the SSC service-user. The SSC-administrator will create this token as a `CIToken` token-type

As with the `FORTIFY_CI_TEMPLATE_PROJECT` and `FORTIFY_CI_TEMPLATE_BRANCH` variables, these may all be set or overridden at the project-group or individual-repository levels, as well as within a project's `.gitlab-ci.yml` file or, ad hoc, within the job-runner web UI.
