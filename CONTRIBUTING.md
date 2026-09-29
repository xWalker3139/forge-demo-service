# Contributing

## Development Workflow

1. Update the local `main` branch.
2. Create a short-lived branch for the change.
3. Make and test the changes locally.
4. Use Conventional Commits.
5. Push the branch to GitHub.
6. Open a pull request.
7. Merge only after the required checks pass.
8. Delete the branch after merging.

## Branch Naming

Use one of the following prefixes:

- `feat/` for new functionality
- `fix/` for bug fixes
- `docs/` for documentation
- `infra/` for infrastructure changes
- `ci/` for CI/CD changes
- `security/` for security changes
- `test/` for test-related changes
- `refactor/` for internal improvements

Examples:

- `feat/health-endpoints`
- `infra/aws-bootstrap`
- `ci/container-build`
- `docs/architecture-overview`

## Commit Messages

This project uses Conventional Commits:

`type(scope): short description`

Examples:

- `feat(api): add readiness endpoint`
- `fix(helm): correct container port`
- `docs(adr): document repository separation`
- `infra(vpc): add private subnets`
- `ci(build): add container workflow`
- `security(policy): block privileged containers`
- `test(api): add readiness endpoint tests`

Commit messages must:

- use the imperative form;
- start with a lowercase letter after the colon;
- describe one logical change;
- avoid generic messages such as `update`, `changes`, or `fix stuff`.

## Pull Requests

Every pull request should contain:

- a short description of the change;
- the reason for the change;
- instructions for testing it;
- relevant screenshots or logs, when applicable;
- a link to the related issue.