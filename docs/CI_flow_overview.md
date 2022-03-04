# Introduction

Because the templates are architected to allow the used of the `sourceanalyzer` utility with or without involving a Fortify SSC server, the stage-defining files and how their dependencies are declared can seem a little counter-intuitive or redundant.



## How pipeline-files fit together:

1. Inheriting-project adds `include` reference to the relevant `templates/fortify-ssc`
1. The `templates/fortify-ssc` file uses a stageless design to set the execution-order
    1. The `templates/fortify-ssc` file includes the `templates/fortify-ssc-version.yml` and corresponding `templates/fortify-prep.yml` job-definition files
    1. The `templates/fortify-ssc` file referencese the corresponding `fortify_code-prep` job-definition to assert an execution-order. This is done by overriding the `needs:` condition defined in the `templates/fortify-prep.yml` file. This override sets the `fortify_code-prep` job to require successful execution of the `fortify_vers-prep`. This causes the `fortify_vers-prep` job
    1. The `templates/fortify-ssc` file's `fortify_push2ssc` job-definition uses a `needs:` condition to assert a dependency on the successful execution of the `fortify_code-prep` job
    1. The `templates/fortify-ssc` file's `fortify_ssc-export` job-definition uses a `needs:` condition to assert a dependency on the successful execution of the `fortify_push2ssc` job



## Workflow-description for includable-pipeline content

Given the above description of how the various job-definitions use the `needs:` directive to assert jobs' execution-order, the following workflow is created:

1. The `fortify_vers-prep` job (defined in `templates/fortify-ssc-version.yml`) is executed
1. The `fortify_code-prep_<LANG>` job (defined in `templates/fortify-prep.yml`) is executed
1. The `fortify_push2ssc` job (defined in `templates/fortify-ssc.yml`) is executed
1. The `fortify_ssc-export` job (defined in `templates/fortify-ssc`) is executed

Because this workflow is defined "stageless", projects inheriting this workflow do not need to worry about ensuring that the stage-name will neither collide with existing stage-names nor execute in a way that blocks the project's already defined pipeline-activities. This workflow will run at the first opportunity afforded by the inheriting-project's `needs:` referenc to the `fortify_vers-prep` job-definition and will run without blocking already-defined jobs/stages
