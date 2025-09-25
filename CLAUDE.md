# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Claude Code Spec Framework** - a specification-driven development system for managing feature specifications and bug reports through AI-assisted workflows. The framework uses a structured approach with validation gates and atomic task execution.

## Commands

This framework provides custom Claude Code commands through the `.claude/commands/` directory:

### Primary Workflow Commands
```bash
# Initialize project guidance documents
/spec-steering-setup

# Create new feature specification
/spec-create <feature-name> [description]

# Execute individual implementation tasks
/spec-execute <feature-name> <task-id>

# Monitor specification progress
/spec-status <feature-name>

# List all specifications
/spec-list
```

### Bug Management Commands
```bash
/bug-create <bug-name> [description]
/bug-analyze <bug-name>
/bug-fix <bug-name>
/bug-verify <bug-name>
/bug-status <bug-name>
```

### Task Command Generation
After creating a specification, generate individual task commands:
```bash
claude-code-spec-workflow generate-task-commands {feature-name}
# Restart Claude Code to see new commands: /feature-name-task-1, /feature-name-task-2, etc.
```

## Architecture

### Core Directories
- `.claude/commands/` - Command definitions for the workflow
- `.claude/agents/` - Validation agents (requirements, design, task, executor)
- `.claude/templates/` - Document templates for consistency
- `.claude/specs/` - Feature specifications storage
- `.claude/bugs/` - Bug tracking and analysis
- `.claude/steering/` - Project context documents (product.md, tech.md, structure.md)

### Development Flow
1. **Requirements Phase** → 2. **Design Phase** → 3. **Tasks Phase** → 4. **Implementation Phase**

Each phase requires validation approval before proceeding. The framework enforces:
- Template compliance through validation agents
- Atomic tasks (15-30 minutes, 1-3 files max)
- Code reuse prioritization over new development
- Requirement traceability throughout implementation

### Validation Pipeline
The framework includes specialized agents that automatically validate:
- **spec-requirements-validator**: User stories and acceptance criteria
- **spec-design-validator**: Architecture and technical design
- **spec-task-validator**: Task breakdown atomicity and implementation clarity
- **spec-task-executor**: Individual task implementation

### Context Management
- Steering documents provide persistent project knowledge
- Templates ensure consistent specification structure
- Hierarchical context loading (steering → templates → specs)

## Key Patterns

### Atomic Task Design
Tasks are designed for optimal AI execution:
- File scope limited to 1-3 related files maximum
- Time-boxed to 15-30 minutes
- Single clear purpose with defined input/output
- Reference to specific requirements and existing code leverage

### Template-Driven Development
- Requirements follow EARS format (Event-Action-Response-State)
- Designs include Mermaid diagrams and code reuse analysis
- User stories in "As a [role], I want [feature], so that [benefit]" format
- Acceptance criteria in WHEN/IF/THEN format

### Quality Gates
- Explicit user approval required between phases
- No phase skipping allowed
- Revision cycles until validation passes
- Steering document alignment verification

## Configuration

The framework uses `.claude/settings.local.json` for permissions:
```json
{
  "permissions": {
    "allow": ["Bash(tree:*)"],
    "deny": [],
    "ask": []
  }
}
```

## Usage Notes

- Always start new projects with `/spec-steering-setup` to establish context
- Use template-driven approach for consistency
- Prioritize code reuse over new development
- Maintain requirement traceability through all phases
- Generate individual task commands for easier parallel execution
- Restart Claude Code after generating new task commands to see them

## Security
- Security best practice from OWASP