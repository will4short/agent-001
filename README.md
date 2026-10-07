# Agent 001

A simple tool-using AI agent built from first principles in Python.

## What it can do

- Accept a user goal
- Decide when to use tools
- Read files from a restricted workspace
- Perform calculations
- Write results to files
- Chain multiple tool calls autonomously
- Recover from tool errors
- Stop after a maximum number of steps

## What I learned

This project was built without an agent framework to understand the core architecture:

**Goal → Model Decision → Tool Call → Tool Execution → Observation → Next Decision → Completion**

It also includes basic safety controls:

- Workspace-restricted file access
- Iteration limits
- Error handling

## Setup

Create a `.env` file containing:

```text
OPENAI_API_KEY=your_key_here
```

Install dependencies:

```bash
pip install openai python-dotenv
```

Run:

```bash
python agent.py
```