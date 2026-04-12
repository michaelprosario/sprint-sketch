When constructing LLM prompting code, please use the following layers.  Make sure these elements are considered when creating LLM service calls.

Layer 1: The System Layer
This is your agent’s constitution. It defines who the agent is, what it will never do, and how it speaks. It’s written once by your team and never exposed to users.

Layer 2: The Developer Layer
This layer is injected programmatically by your application code on every request. It carries session-specific context: who is the current user, what their account looks like, and how you want the output formatted.

Layer 3: The User Layer
- This layer represents user input for prompt