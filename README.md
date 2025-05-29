<img src="https://github.com/codellm-devkit/coco-toolbox/blob/main/docs/assets/logo.png?raw=true" width="900" alt="CoCo Toolbox Logo">

---

**COCO (short for Code Context) Toolbox is a suite of static analysis tools that provides analysis capabilities to LLMs through the Model Context Protocol (MCP).** 

It leverages the [CLDK](https://github.com/codellm-devkit/python-sdk) library to analyze Java projects and expose analysis tools via MCP for AI assistants and other clients.

## Features

- 🔍 Static code analysis built on top of [CLDK](https://github.com/codellm-devkit/python-sdk) for Java projects
- 🔌 MCP server implementation with a number of static analysis tools for easy integration
- 🛠️ Easy command-line interface and invocation

## Installation

COCO uses `uv` as the package manager. To install COCO, run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or 

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

or (for windows users)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Usage

To run the COCO server, use the following command:

```bash
uv run coco serve --project-path <path_to_your_java_project>
```

Replace `<path_to_your_java_project>` with the path to the Java project you want to analyze.

You may also use `uvx` to run the server directly from this Git repository:

```bash
uvx --from git+https://github.com/codellm-devkit/coco-toolbox coco serve --project-path <path_to_your_java_project>
```

## Development

To contribute to COCO, you can clone the repository and install the development dependencies:

```bash
git clone https://github.com/codellm-devkit/coco-toolbox.git
cd coco-toolbox
uv sync --all-groups
```

Start by looking at the test cases in the `tests` directory to understand how to use the tools and the MCP server. You can run the tests using:

```bash
uv run pytest --disable-warnings --pspec
```

Each test case is writen to emulate a MCP client calling the server tool. For example, the [`test_are_we_ready_tool`](https://github.com/codellm-devkit/cldk-coco-toolbox/blob/main/test/test_basic.py#L11) tests to check if the server is ready to accept requests by calling the `are_we_ready` tool.