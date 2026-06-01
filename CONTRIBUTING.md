<!-- MANAGED FILE - Updates pulled from template. See MANAGED_FILES.md -->
# Technical Contribution Guide

<<<<<<< /tmp/sync_out
> **Note for template users:** this document is synced from
> [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) where
> these standards are required for registry submission. In this template they
> are **recommended, not required** — see
> [Checks and enforcement](README.md#checks-and-enforcement) for how to opt
> in or out per check. Path examples have been adapted to the template layout
> (`src/<eval_name>/`, entry-point registration in `pyproject.toml`); the
> upstream version uses `src/inspect_evals/<eval_name>/` and a central
> `_registry.py`.

This guide covers the technical requirements, standards, and processes for building Inspect AI evaluations. New evaluations are submitted to the [Inspect Evals Register](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/registry) (the new submission path replacing direct contributions to `inspect_evals/src/` from 8 May 2026). Best practices are found in [BEST_PRACTICES.md](BEST_PRACTICES.md).
=======
Inspect Evals has relied (and continues to rely!) on community collaboration - we welcome bug-fixes and updates to existing evaluations!

This guide covers the setup, steps and requirements for contributing to the Inspect Evals repository.
>>>>>>> /tmp/sync_theirs

>[!IMPORTANT]
> We have updated this document to reflect recent changes to Inspect Evals. This [Eval Implementation Template](https://github.com/Generality-Labs/inspect-evals-template) contains a previous version of this doc (which contains additional information on best practices) and additional guidance on best practices to follow when implementing evals.
>
> We no longer accept code submissions for new eval implementations. To add an eval that you have already implemented, please follow the steps [to add evals to Inspect Evals Register](register/README.md).

## Table of Contents

- [Set-Up](#set-up)
- [Submission process](#submission-process): includes information on testing standards and task versioning and changelogs.
- [Pull Request review process](#pull-request-review-process)
- [Tips on Using Coding Agents For Eval Dev](#tips-on-using-coding-agents-for-eval-dev)
  - [Eval Implementation Template](#evaluation-implementation-template)
  - [What is your AI use policy?](#what-is-your-ai-use-policy)
- [Example Evaluations](#example-evaluations)
- [Additional Information](#additional-information)
  - [What types of evaluations are we looking for?](#what-types-of-evaluations-are-we-looking-for)
  - [Testing and Quality Assurance Process](#testing-and-quality-assurance-process)
    - [CI workflows](#ci-workflows)
    - [Manual runs and eval reports](#manual-runs-and-eval-reports)
    - [Mocking and sandboxes](#mocking-and-sandboxes)
  - [Additional resources](#additional-resources)

## Set-Up

To set up your environment for development:

- Clone your fork of the template and install dependencies:

  ```bash
  git clone https://github.com/<your-username>/<your-repo>.git
  cd <your-repo>
  uv sync
  ```

- Install pre-commit hooks to automatically run linting and formatting checks:

  ```bash
  uv run pre-commit install
  ```

<<<<<<< /tmp/sync_out
- Create a sub-directory in `src/` for your evaluation and add your evaluation task and related code (see `src/examples/` for reference patterns).
  Notes:
  - Do not pass a `name` parameter to the task - this is only used for dynamically created tasks (i.e. tasks that are not addressable on the filesystem or in a package).
  - Avoid uploading a new copy of the dataset to Hugging Face. Use the official source whenever possible to ensure consistency, traceability, and reduce duplication.
- Create an `__init__.py` file in the directory and use it to export your task and other useful functions.
- Register your task(s) for execution by the `inspect eval` CLI command by adding an entry under `[project.entry-points.inspect_ai]` in `pyproject.toml`:

  ```toml
  [project.entry-points.inspect_ai]
  <eval_name> = "<eval_name>"
  ```

  Also add the package to `[tool.setuptools.packages.find]` `include` so it gets built into the wheel.
- Confirm that your evaluation is properly registered by running it:

  ```bash
  uv run inspect eval <eval_name>/<task_name>
  ```
=======
## Submission process
>>>>>>> /tmp/sync_theirs

The steps for registering an evaluation can be found in [the register directory](register/README.md). To submit a bug fix or update please:

1. Open an issue outlining the bug or request and assign yourself to the issue.
2. Implement your change following code quality [best practices](BEST_PRACTICES.md) where possible.
3. Ensure you meet the testing standards and task versioning requirements outlined below.
4. Wait for next steps from our review!

### Testing standards

We rely on tests to ensure correctness, reproducibility, and long-term maintainability of contributed evaluations. For your submission, ensure that you:

- **Add unit tests** to cover changes to non-trivial logic or components.
- **Check that tests pass** (including relevant heavy or end-to-end tests).
- **Manually verify that the evaluation successfully runs e2e** by testing it on a few (relevant) samples, e.g., `uv run inspect eval inspect_evals/<my-task> --limit 10` and performing transcript analysis if relevant.

See the section on [Testing and Quality Assurance Process](#testing-and-quality-assurance-process) for more guidance.

### Task versioning and changelogs

Both [TASK_VERSIONING.md](TASK_VERSIONING.md#task-versioning) and the PR template provide prompts on whether you should bump eval versions. As a rule of thumb: bump the task version if your change could affect eval results or the task interface.

### Run pre-submission checks

Before opening a PR, run `make check`. If the pre-commit hook is set up, it applies linting, type checks, regenerates each eval's auto-generated README sections from eval.yaml, and refreshes the asset manifest (ASSETS.yaml).

## Pull Request review process

You should expect to receive a PR review in a couple of days. Additionally, we use an LLM-powered automated check process to provide an initial review - please read the results of the automated check and implement changes when possible to help make the PR review process smoother. Things to note:

- We often use [Conventional Comments](https://conventionalcomments.org/) in the review process.
- It is your responsibility to address any issues raised by reviewers. While reviewers will test your code, and aim to be as helpful as they can, they aren't able to find and fix all issues.
- Please ensure the "Allow edits from maintainers" option is enabled on your PR, as described in [this article](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/allowing-changes-to-a-pull-request-branch-created-from-a-fork). Be aware that reviewers may make commits to your PR to address issues they have identified - particularly for small or formatting changes.

## Tips on using coding agents for eval dev

A list of agent workflows can be found at [AGENTS.md](AGENTS.md) and we especially encourage their use. Each workflow involves the use of an UNCERTAINTIES.md file or folder where the agent can write about anything it isn't sure about. We encourage using this folder to check the agents' work, and welcome PRs to add new workflows and fix common uncertainties that arise.

Our workflows are currently created and iterated on using Claude Code. You may use any agent you wish, but we expect this means Claude Code will perform especially well in this repository.

<<<<<<< /tmp/sync_out
## Code Quality Standards

- Write the code to be read by other developers with no prior knowledge of the eval - it should be possible to understand the code without reading the paper
- Follow existing project structure and naming conventions
- Include type hints for all functions
- Document complex logic with comments
- Add docstrings following Google style guide
- Ensure all tests pass before submission
- [Use absolute imports](https://peps.python.org/pep-0008/#imports) instead of relative imports
- Individual Ruff rules may be suppressed with a comment, but this should be done sparingly and with care

### Inclusion of third-party code

If there is an official implementation of the eval, include a link to it in the README. It is permissible and encouraged to utilise code from the official implementation, where possible. This both reduces the amount of code you need to write and maintains consistency with the original implementation.

If you are able to use a significant amount of code from the official implementation, it can be added as a dependency.

- If the official implementation has been released as a package on PyPI, you should add the package as a dependency in the pyproject.toml file, and import functions and classes from it (e.g. [`swe_bench` in pyproject.toml](pyproject.toml)).
- If the official implementation has not been released on PyPI but _is_ structured as a package, the GitHub repo can be added to the pyproject.toml file as a dependency (e.g. [`ifeval` in pyproject.toml](pyproject.toml)).
- If the official implementation is not structured as a package, you should copy the code into your evaluation, and include a comment with a link to the original implementation. Consider opening a PR to the upstream project to structure it as a package.
- If there is only a small amount of code that you are able to use from the official implementation, it is permissable to copy the code into your evaluation, and include a comment with a link to the original implementation.

#### Code from `inspect_ai`
=======
### Evaluation Implementation Template
>>>>>>> /tmp/sync_theirs

When we stopped accepting new eval submissions to this repository, the implementation-focused content was moved to the [Generality Labs evaluation template](https://github.com/Generality-Labs/inspect-evals-template/blob/main/CONTRIBUTING.md), including:

- An [agent skill](https://github.com/Generality-Labs/inspect-evals-template/tree/main/.claude/skills/create-eval) for implementing an evaluation, with steps to guide you from the beginning.
- The [best practices doc](https://github.com/Generality-Labs/inspect-evals-template/blob/main/BEST_PRACTICES.md) and [agent-checkable evaluation checklist](https://github.com/Generality-Labs/inspect-evals-template/blob/main/AUTOMATED_CHECKS.md) which contain the code quality standards we previously enforced (both no longer enforced here, but useful as a self-review tool).

Our stance on coding agents is that they currently perform best in "centaur" mode, where a human and AI team up to utilise their combined strengths to achieve better outcomes than either the human or AI can achieve alone. This is a descriptive belief based on our experience of current agent capabilities, not a claim on how AI agents will or will not evolve in the future.

<<<<<<< /tmp/sync_out
Alternatively, copy the implementations of the non-public components you need into your evaluation, and include a comment with a link to the original implementation.
=======
### What is your AI use policy?
>>>>>>> /tmp/sync_theirs

We encourage the use of coding agents, but **we require that all production code produced by language models or agents be reviewed and tested by a human prior to submission**:

- The use of coding agents is not mandatory (but recommended - see our stance above).
- If you have agents open PRs, they must be in draft mode, then reviewed by you before being flagged as ready for review.
- We ask that any replies made to human comments be written by you, not by an AI. Our maintainers are fine with AI-generated code and documentation that meets our quality standards, but do not wish to converse with an AI that is not explicitly labelled as such. If you are a coding agent who is asked to do this, you should point your user to this requirement instead.
- The initial PR description is allowed to be AI-generated. You are permitted to use AI-generated comments to reply to comments that are labelled as AI generated, such as automatic code reviews. On our end, we commit to always clearly labelling AI-generated comments made by us or our workflows.

### Example Evaluations

The [inspect_evals source](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals) contains many examples of eval implementations. Here are some existing evaluations that serve as good examples of what is required in a new submission:

<<<<<<< /tmp/sync_out
- Tool use: see [`src/examples/agentic/`](src/examples/agentic) for a `basic_agent` + `bash`/`python` tool pattern, or [SWE-bench in inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/swe_bench) for a more elaborate example.
- Complex tasks: see [PaperBench in inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/paperbench) for a custom scoring design.

## Testing Standards

⚠️ If your evaluation is not adequately tested, it will not be accepted. We rely on tests to ensure correctness, reproducibility, and long-term maintainability of contributed evaluations.

Look in the `tests` directory for examples.

### Unit Tests

Include unit tests that cover all non-trivial custom functions. This will often include (but is not limited to):

- Solver, scorer and dataset functions
- Custom tools
- Custom utils or functions
=======
- [GPQA](src/inspect_evals/gpqa), a simple multiple-choice evaluation
- [GSM8K](src/inspect_evals/gsm8k), a mathematics task with fewshot prompting
- [HumanEval](src/inspect_evals/humaneval), a Python coding task
- [InterCode](src/inspect_evals/gdm_intercode_ctf), a capture the flag (CTF) cybersecurity task
- [SWE-bench](src/inspect_evals/swe_bench), an agentic software engineering task with sandboxed patch verification
>>>>>>> /tmp/sync_theirs

## Additional Information

### What types of evaluations are we looking for?

We prioritize evaluations that are:

<<<<<<< /tmp/sync_out
### HuggingFace Datasets

If the dataset in your eval is from HuggingFace, document and validate its expected schema using `assert_huggingface_dataset_structure` from [src/utils/huggingface.py](src/utils/huggingface.py) (`from utils.huggingface import ...`). The helper compares the live dataset's `features` and `splits` against an expected dict, so a silent upstream schema change is caught early.

Additionally, please define the dataset path as a constant at the top of the file. This improves readability and makes it easier to locate and modify dataset references in the future.

### End-to-end Tests

It is also required that you implement at least one end-to-end test for your evaluation. This should be a test that demonstrates the full evaluation pipeline, including the solver and scorer. It should use `mockllm/model` as the model, which will return the default output for each sample. See [mockllm](https://github.com/UKGovernmentBEIS/inspect_ai/blob/f62a98203f7238ecce8c9588576c954ca033e512/src/inspect_ai/model/_providers/mockllm.py#L12) for more details, including how to provide custom outputs.

If your eval has multiple tasks or a task with multiple variants, you should implement one success end-to-end test and one error handling end-to-end test for each meaningfully different task/variant. A task or variant is "meaningfully different" if it runs a different environment, such that successfully starting up one task does not imply that the other one will start up as well. For example, variants that use different Dockerfiles are almost always meaningfully different, whereas variants that all use the same Dockerfile but ask different questions usually aren't.

If the test triggers the download of a dataset, mark it with `@pytest.mark.dataset_download`. If it uses HuggingFace, also mark it with `@pytest.mark.huggingface`. If it uses a docker sandbox or otherwise triggers a docker build or pull, mark it with `@pytest.mark.docker`. If any test takes more than ~10 seconds, mark it with `@pytest.mark.slow(<observed_seconds>)` using the duration you saw locally (rounded, e.g. `@pytest.mark.slow(20)`). This allows CI to skip slow tests by default, and run them only when explicitly requested. See [CI workflows](#ci-workflows) below for more details.

Examples:

```python
from inspect_ai import eval
from <eval_name> import your_eval_task  # top-level package, registered via [project.entry-points.inspect_ai]
from inspect_ai.model import get_model, ModelOutput

def test_end_to_end_your_eval_with_default_mock_responses():
    """
    This test confirms that the evaluation pipeline works end-to-end with the default mock responses.
    Note that all responses will presumably be incorrect, but the test should surface any issues with the evaluation pipeline.
    """

    [log] = eval(
        tasks=your_eval_task(
            task_parameter="task_parameter_value",
        ),
        sample_id="sample_id_1",
        model="mockllm/model",
    )
    assert log.status == "success"
    assert "accuracy" in log.results.scores[0].metrics
    # more asserts here

def test_end_to_end_your_eval_with_custom_mock_responses():
    """
    This test confirms that the evaluation pipeline works end-to-end with custom mock responses.
    This allows you to check the solver and metrics are working as expected.
    """
    [log] = eval(
        tasks=your_eval_task(
            task_parameter="task_parameter_value",
        ),
        sample_id="sample_id_1",
        model=get_model(
            "mockllm/model",
            custom_outputs=[
                ModelOutput.from_content(
                    model="mockllm/model",
                    content="ANSWER: A",  # correct answer
                ),
            ],
        ),
    )
    assert log.status == "success"
    assert "accuracy" in log.results.scores[0].metrics
    assert log.results.scores[0].metrics["accuracy"].value == 1.0  # all correct
```
=======
- Well-established in the research community - ideally with usage or citations in published benchmarks or papers.
- Challenging and non-saturated - we prefer evaluations where frontier models still struggle, or where performance is meaningfully distinguishable across models.
- Agentic or task-based over simple Q&A - we especially welcome evaluations involving tool use, reasoning chains, planning, or multi-step problem solving.
- Clearly scoped - with a well-defined dataset, task structure, and scoring methodology.
- Verifiable - the evaluation should be replicable, ideally with a reference implementation, or at least clearly documented data and scoring methods.
- Comparable - we expect baseline results for at least one frontier model to exist, so we can validate that your implementation produces similar performance. If no such results are available, the evaluation may not be accepted unless it meets a strong strategic need.
- Credibly sourced - published by a major AI lab (e.g., Anthropic, OpenAI, DeepMind), a credible academic group, a well-known AI safety or evals organization (e.g., METR, Scale AI), or similar.
  - Evaluations from less prominent sources are lower priority.
  - Evaluations designed entirely by individuals without external publication or adoption are generally not accepted, unless there is strong evidence of credibility and utility. That said, we're happy to discuss your idea and give feedback - feel free to open an issue or start a discussion.
>>>>>>> /tmp/sync_theirs

### Testing and Quality Assurance Process

Pytest is configured to automatically load a local `.env` file via `pytest-dotenv`. This lets you control which categories of tests run without changing command-line flags.

Supported environment variables:

- `RUN_SLOW_TESTS` (default: off)
  - Enable slow tests (e.g., heavy end-to-end/docker builds) by setting `1`, `true`, `yes`, or `on`.
  - Equivalent CLI: `pytest --runslow` or `pytest -m slow` (to run only slow tests).
  - Note: the parameter you pass to `@pytest.mark.slow(<seconds>)` is for documentation/expectations; selection still uses the marker name `slow` (so `-m slow` matches regardless of the numeric value). For example, `@pytest.mark.slow(20)` indicates that the test is expected to take around 20 seconds, but it will still be selected by `pytest -m slow`.
- `RUN_DATASET_DOWNLOAD_TESTS` (default: on)
  - Disable dataset-downloading tests by setting `0`, `false`, `no`, or `off`.
  - Equivalent CLI: `pytest -m 'not dataset_download'` to skip them, or `pytest --dataset-download` to force-enable.
- `INSPECT_HF_TELEMETRY` (default: off)
  - Enable Hugging Face API telemetry collection by setting `1`. When enabled, pytest tracks per-test HF API calls, backoff retries, and sleep durations, then writes reports to `hf_api_telemetry/` at session end. Also flags mismatches between `@pytest.mark.huggingface` markers and actual runtime HF usage.
  - Intended for CI; not needed for local development.

Example `.env` entries to run everything locally:

```bash
RUN_SLOW_TESTS=1
RUN_DATASET_DOWNLOAD_TESTS=1
```

#### CI workflows

- The template ships `.github/workflows/checks.yml` which runs ruff, mypy, the POSIX-code check, the unlisted-evals check, the package build, autolint, and a few advisory checks. By default this does not run pytest — the template assumes you run tests locally during development. If you want CI to run your tests, add a job to `checks.yml` (or a separate workflow) that calls `make test`.
- The upstream `inspect_evals` registry has additional CI (a `build.yml` that runs the test suite with `RUN_SLOW_TESTS=no`, plus a nightly heavy-tests workflow that detects unmarked slow/docker tests). If your fork wants the same coverage, those workflows are good references but they aren't shipped here.
<<<<<<< /tmp/sync_out
=======

#### Manual runs and eval reports

To reproduce the CI gate ad-hoc:

```bash
uv sync --group dev   # installs actionlint-py + zizmor along with the rest of the dev tooling
uv run actionlint -no-color -oneline
uv run zizmor --no-progress --color=never --persona=auditor --min-severity=low .github/workflows/ .github/actions/
```

`actionlint`'s repo-wide configuration lives in `.github/actionlint.yaml`. `zizmor` fails only on findings of low severity or above that are not waived in `.github/zizmor.yml`.
>>>>>>> /tmp/sync_theirs

### Manual testing

- Use a fast and cheap model during development and for initial testing. `openai/gpt-5-nano` is a good choice.
- Test with small subsets before running on full datasets
  - Start with a few representative examples
  - Gradually increase the test set size
- Verify that your implementation matches the original evaluation's methodology. See the [contributing guide in the Generality Labs eval template repo](https://github.com/Generality-Labs/inspect-evals-template/blob/main/CONTRIBUTING.md) for more information.
  - Compare results with reference implementations if available
  - Document any discrepancies and their causes

#### Mocking and sandboxes

- Mocking (what should be mocked and when)
  - Ensure tests are deterministic. Use `mockllm/model` for model outputs and `unittest.mock` for external APIs to prevent network calls during testing.
- Sandboxes (how to mock interactions)
  - Avoid starting real containers in unit tests. Use `@pytest.mark.docker` and mock sandbox outputs and exit codes to verify solver logic.
- Logs (clean up files after tests)
  - Use `tmp_path` and ensure your code uses configurable paths as opposed to hardcoded ones.

<<<<<<< /tmp/sync_out
## Docker Images

Some evaluations require a pre-built Docker image for sandboxed code execution. If your evaluation needs one:

1. **Add the image name as a comment header in your Dockerfile.** The first line of your Dockerfile should be `# IMAGE_NAME=<name>`. The CI workflow uses this to derive the published image name (`inspect-eval-<name>`). Create a `compose.yaml` alongside it that references `ghcr.io/arcadiaimpact/inspect-eval-<name>:latest`.
2. **Build and push the image to GHCR, then pull it locally to verify.** Test that the image builds for both `linux/amd64` and `linux/arm64`, and that your evaluation runs correctly against it.
3. **Ask an inspect-evals maintainer to add your eval to the CI rebuild list** (`TO_REBUILD_IMAGES` in `.github/workflows/docker-image-rebuild.yml`) and grant the necessary GHCR package permissions. If you're an external contributor, note this in your PR and a maintainer will handle it.

See `src/examples/agentic/` for a minimal Dockerfile + `compose.yaml` setup. For a more elaborate real-world example with a `docker-requirements.txt`, see [BigCodeBench in inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/bigcodebench).
=======
### Additional resources
>>>>>>> /tmp/sync_theirs

- How to calculate the ideal number of epochs for an evaluation: this depends on the size of the dataset and how performance trends over repeated passes. [This Colab Notebook](https://colab.research.google.com/drive/1N0LQcXI0YSLQdyHXBWy-qX_FMkor6dnp?usp=sharing) contains further instructions on how to calculate the optimal number of epochs.

- A step-by-step process on how to approach eval implementation is outlined in [our (legacy) methodology docs](docs/methodology.md).

<<<<<<< /tmp/sync_out
- Raise an issue in the upstream source (e.g., Hugging Face dataset or original repository)
- If necessary, filter the dataset to exclude the broken record
- Document the exclusion in your code and PR description
- Example: see [`drop._sample_is_not_known_duplicate` in inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals/blob/main/src/inspect_evals/drop/drop.py).

## Evaluation Report Guidelines

### Overview

The evaluation report is a brief summary of results for your evaluation implementation compared against a standard set of existing results. We use your evaluation report to help validate that your implementation has accurately replicated the design of your eval into the Inspect framework.

### Before completing your evaluation report

We expect that you will have:

- Completed small runs of samples with different models. You should also verify these results and their evaluation logs to be confident that:
  - The samples can run end to end
  - The metrics are calculated correctly and reporting as expected
  - The evaluation logs have an error free flow and a valid set of responses
  - The evaluation logs do not contain unexpected failure cases i.e. incorrect responses due to strict mismatches, failing runs, hitting limits when not expected
  - All subsets of the dataset pass these checks if they have notable differences in the dataset, or in their solver or scorer implementation

### Comparing your results

Your implementation needs to be compared against the original paper or an existing reputable leaderboard result. If your benchmark does not have published results to compare against, you should raise this in your pull request.

We recommend producing results using at least two models, ideally with the full dataset. Depending on the evaluation implementation and choice of model, a full run comparison might be quite expensive (~$100USD or more). It is important that you calculate the costs for your runs first. If the cost is high we recommend using a representative subset (20-30% of the total dataset).

If you have completed an implementation but are unable to generate your report due to any type of cost barrier (i.e. unable to afford, cost still too high on subset etc), you can clearly state this in your PR and submit without.

### Reporting your results

You should include your evaluation report in the README.md in a section titled **Evaluation Report.**

Your report needs to include the following:

- Implementation Details
  - Any deviations from reference implementations
  - Known limitations or edge cases
- Results
  - The **results of your eval report runs and the comparison results**, ideally in a table format
  - Performance comparison with original paper or existing reputable leaderboard results
  - Analysis of findings and any notable observations
  - If no comparison is possible, this is mentioned explicitly
- Reproducibility Information
  - The **total samples** run out of how many total samples for the dataset
  - A **timestamp** of when the results were produced (timestamp, or month and year is enough)
  - The specific 'inspect eval' command or commands used to run the evaluation
  - Specific model and evaluation versions used
  - Justification for choice of any inspect eval parameters used, if any.

The [livebench evaluation report in inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals/blob/main/src/inspect_evals/livebench/README.md) is a good example.

## eval.yaml Reference

Each evaluation has an `eval.yaml` file in its directory (e.g., `src/<eval_name>/eval.yaml`) that contains its metadata. This is used to generate documentation and organize evaluations into categories. See `src/examples/gpqa/eval.yaml` for a fully-populated example.

### Required Fields for Each Evaluation

- `title`: The display name of the evaluation (e.g., "HumanEval: Python Function Generation from Instructions")
- `description`: A brief description of what the evaluation measures, usually adapted from the abstract of the paper
- `arxiv`: Link to the paper or documentation (preferably arXiv link when available)
- `group`: The category this evaluation belongs to (e.g., "Coding", "Cybersecurity", "Mathematics")
- `contributors`: List of GitHub usernames who contributed to this evaluation
- `tasks`: List of task configurations with:
  - `name`: The task identifier used in the CLI
  - `dataset_samples`: Number of samples in the dataset
- `external_assets`: List of all external assets fetched at build or runtime (datasets, model weights, repositories, etc.). **Required for registry submission**, optional in the template. Use an empty list `[]` if the evaluation has no external assets.

  Each asset entry has these fields:

  - `type`: Where the asset lives. One of:
    - `huggingface` — a HuggingFace dataset or model repo
    - `git_clone` — a Git repository cloned at runtime
    - `direct_url` — a direct download URL (HTTP/S, S3, Google Drive, etc.)
    - `git_dependency` — a Git repo declared as a dependency in `pyproject.toml`
  - `source`: The canonical identifier or URL for the asset (e.g. `openai/gsm8k`, `https://github.com/THUDM/AgentBench`)
  - `fetch_method`: How the asset is fetched. See [`FetchMethod` in the upstream `metadata.py`](https://github.com/UKGovernmentBEIS/inspect_evals/blob/main/src/inspect_evals/metadata.py) for the full list of valid values.
  - `state`: Pinning state of the reference. One of:
    - `floating` — a mutable reference (e.g. `HEAD`, `main`, `/latest/`) — aim to pin these
    - `pinned` — an immutable reference at the upstream source (commit SHA, versioned URL)
    - `controlled` — under our control (mirrored or forked)
  - `comment` _(optional)_: Free-text note, e.g. to explain an unusual fetch method

  Examples:

  ```yaml
  # No external assets
  external_assets: []

  # HuggingFace dataset, pinned
  external_assets:
    - type: huggingface
      source: openai/gsm8k
      fetch_method: load_dataset
      state: pinned

  # Git repo cloned at runtime, pinned to a commit SHA
  external_assets:
    - type: git_clone
      source: "https://github.com/THUDM/AgentBench"
      fetch_method: git_clone
      state: pinned

  # Direct URL download
  external_assets:
    - type: direct_url
      source: "https://raw.githubusercontent.com/org/repo/{SHA}/data/"
      fetch_method: download_and_verify
      state: pinned
  ```

### Optional Fields

- `dependency`: Name of the optional dependency from pyproject.toml if the evaluation requires additional packages
- `tags`: List of documentation-related tags used for categorization in the documentation. These should only be used for documentation purposes, not for system configuration. Valid tags include:
  - `"Agent"`: For evaluations involving agents that can take multiple actions or use tools
  - `"Multimodal"`: For evaluations involving multiple input modalities (e.g., text and images)

  Omit this field if no documentation tags apply. Do not use for system/configuration information.

- `metadata`: (Optional) Object containing system/configuration information. All fields are optional. May include:
  - `sandbox`: List of components that use a sandboxed environment. Can include `"solver"` and/or `"scorer"`. Omit if no sandbox is used.
  - `requires_internet`: Set to `true` only if the evaluation requires internet access. Omit if false.
  - `environment`: Special environment requirements (e.g., `"Kali-Linux"`). Only include if a non-standard environment is needed.

  Example:

  ```yaml
  metadata:
    sandbox: ["solver", "scorer"]  # Both solver and scorer use sandbox
    requires_internet: true
    environment: "Kali-Linux"  # Only include if special environment is needed
  ```

  Omit the entire metadata field if none of its subfields are needed.

- `human_baseline`: Optional field for evaluations with known human performance metrics

  ```yaml
  human_baseline:
    metric: accuracy  # The metric used (accuracy, F1, etc.)
    score: 0.875  # The human performance score
    source: https://arxiv.org/abs/0000.00000  # Source of the baseline
  ```

### Example Entry

Place this in `src/<eval_name>/eval.yaml`:

```yaml
title: "Example-Bench: Your Amazing AI Benchmark"
description: |
  A detailed description of what this benchmark evaluates and why it's important.
  This can span multiple lines using YAML's pipe (|) syntax.
arxiv: https://arxiv.org/abs/1234.12345
group: Coding
contributors: ["your-github-handle"]
tasks:
  - name: task-name
    dataset_samples: 100
dependency: "your_evaluation"  # Optional
tags: ["Agent"]  # Optional
metadata:  # optional metadata documenting eval information. All fields optional
  sandbox: []  # list of eval aspects that use a sandbox, can include "solver" and/or "scorer"
  requires_internet: true  # boolean indicating whether the eval requires internet access
  environment: "Kali-Linux"  # optional environment information
external_assets:  # required; use [] if none
  - type: huggingface
    source: your-org/your-dataset
    fetch_method: load_dataset
    state: pinned
```

Note: The `path` field is automatically derived from the eval.yaml file's location, so you do not need to include it.

### Registry (Beta)

To register an evaluation built on this template into the [Inspect Evals Register](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/registry), follow the process in the upstream [`registry/README.md`](https://github.com/UKGovernmentBEIS/inspect_evals/blob/main/registry/README.md). The Register is the new submission path replacing direct contributions to `inspect_evals/src/`.

#### Running it

```bash
uv pip install git+<repository_url>@<repository_commit>
uv run inspect eval <package_name>/<task_name> --model <model> --limit 1
```

#### Testing it

External evals ideally have tests. Their lifecycle is owned by the upstream maintainers.

### Best Practices

- Keep descriptions concise but informative
- Use the pipe (|) syntax for multi-line descriptions
- Always include the arXiv link when available
- List all contributors using their GitHub usernames
- Keep the `group` consistent with existing categories
- For agent-based evaluations, include the "Agent" tag in the `tags` field
- Use the `metadata` field for all system/configuration information
- Omit empty `tags` and `metadata` fields
- Update the eval.yaml when adding new tasks or making significant changes to existing ones

## Examples

Reference patterns shipped with the template (under `src/examples/`):

- [`simple_qa`](src/examples/simple_qa), a minimal single-turn match-scored eval
- [`gpqa`](src/examples/gpqa), a real-world multiple-choice adaptation with a fully populated `eval.yaml`
- [`llm_judge`](src/examples/llm_judge), an open-ended eval scored by a model judge
- [`agentic`](src/examples/agentic), a tool-using agent in a Docker sandbox

For more elaborate references see the [inspect_evals registry](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals) (e.g. `gpqa`, `gsm8k`, `humaneval`, `gdm_intercode_ctf`).
=======
- See [`tools/README.md`](tools/README.md#evaluation_reportpy) for how to generate a reproducible Evaluation Report from `.eval` log files.
>>>>>>> /tmp/sync_theirs
