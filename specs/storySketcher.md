4/12/2026

- follow specs/clean_architecture.md
- follow specs/llmPromptDesign.md
- As an agile project manager, I should propose user stories for a scope.
    - create a simple console program for this iteration
    - program should read scope from markdown file
    - user stories should follow coaching in specs/investCoaching.md
    - store proposed user stories in markdown file called output.md
    - program should use the following technology
        - python
        - claude sdk llm
===

Amend sprintSketch/story_sketcher.py
- remove input for the number of user stories
- the program should document a practical number of user stories for the scope

===

Amend /workspaces/sprint-sketch/sprintSketch/story_sketcher.py
- system does not need to parse llm output into user story objects
- the service can return llm output in markdown format
- the parsing logic currently in place is causing bugs
