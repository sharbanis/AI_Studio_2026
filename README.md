# AI_Studio_2026

## Overview

This repository contains AI-assisted testing learning material, prompt engineering examples, reusable test-generation templates, a local Jira test-case generator, and practical project outputs for the AI Studio 2026 learning track.

## What’s Included

- LLM fundamentals and prompt engineering notes
- Reusable prompt templates for requirements, PRD, API, security, regression, and validation tasks
- A Streamlit application that fetches Jira issues and generates test cases with Ollama or Groq
- Selenium automation examples and TestNG framework references
- VWO login PRD, test case, and test plan practice outputs

## Getting Started

1. Clone the repository to your local machine.
2. Open the project in your editor of choice.
3. Review the markdown notes and prompt files in the chapter and task folders.
4. Use the project folders under `Task_Projects/` and `Prompt_Templates/` as reusable artifacts for testing exercises.

### Run the Local Generator

The local generator is in `LearningAI/chapter_03_LocalTestCaseGenerator/src/`.

```powershell
cd LearningAI/chapter_03_LocalTestCaseGenerator/src
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

Configure Jira and LLM provider settings in the app. The `.env` and runtime `config.json` files are local configuration and should not be committed.

## Project Structure

- `LearningAI/chapter_01_LLMBasics/` - LLM basics and core learning notes
- `LearningAI/chapter_02_PromptEngg/` - Prompt engineering templates and framework guidance
- `LearningAI/chapter_03_LocalTestCaseGenerator/` - Streamlit Jira test-case generator
- `Prompt_Templates/` - Reusable prompt collections for QA and AI-assisted testing
- `Task_Projects/01_Project_PrommptEngg_RICEPOT_Selenium/` - Selenium and TestNG automation project under `Output_Result/SeleniumAdvanceFramework/`
- `Task_Projects/02_Project_PromptEngg/` - VWO login PRD, test plan, and test case outputs
- `AGENTS.md` - Repository-specific guidance for working in this project

## Usage

Use this repository to:

- learn AI-assisted test design workflows
- build structured test plans and requirement-based testing materials
- create prompt-driven QA artifacts
- generate test cases from Jira issues with a configured LLM provider
- explore sample automation and validation workflows

## Repository Status

This repository is intended to store working project files, task outputs, and learning artifacts for the AI Studio 2026 training journey.
