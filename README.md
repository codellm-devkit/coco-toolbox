<img src="https://github.com/codellm-devkit/coco-toolbox/blob/main/docs/assets/logo.png?raw=true" width="900" alt="CoCo Toolbox Logo">

CoCo is a toolbox that provides static code analysis capabilities through the Model Context Protocol (MCP). It leverages the [CLDK](https://github.com/codellm-devkit/cldk) library to analyze Java projects and expose analysis tools via MCP for AI assistants and other clients.

## Features

- 🔍 Static code analysis for Java projects
- 🔌 MCP server implementation for easy integration
- 🛠️ Command-line interface with Typer
- 📊 Built on top of CLDK analysis framework

## Installation

Coco uses `uv` as the package manager. To install CoCo, run:

```bash
pipx install uv
```
Note: If you don't have `pipx` installed, you can install it via `pip install pipx`.

## Usage

To run the CoCo server, use the following command:

```bash
uv run coco serve --project-path <path_to_your_java_project>
```

Replace `<path_to_your_java_project>` with the path to the Java project you want to analyze.

You may also use uvx to run the server directly from the Git repository:

```bash
uvx --from git+https://github.com/codellm-devkit/coco-toolbox coco serve --project-path <path_to_your_java_project>
```
