LangGraph is a library built on top of LangChain that allows you to create complex, "circular" workflows for AI agents.

* Standard LLM chains usually move in a straight line (Input -> Process -> Output)
* LangGraph allows the AI to loop back, correct its own mistakes, and reason through a problem until it reaches a solution.


## 1. Core Concepts
To understand how it works, think of a flow chart made of three parts:

* **Nodes:** These represent the "workers." A node can be a function that calls an LLM, a tool (like a Google Search), or a piece of Python code.

* **Edges:** These are the paths between nodes. They define what happens next.

* **State:** This is a shared memory. Every node can read from and write to this "notebook," ensuring the agent remembers what happened in previous steps.

## 2. Why use it?
Most basic AI setups struggle with tasks that require back-and-forth reasoning. LangGraph is designed for:

* **Cycles (Looping):** If an AI generates a bad answer, you can program a "critic" node to send it back for a rewrite.

* **Persistence:** It can save the state of a conversation automatically, allowing you to "pause" an agent and resume it later.

* **Human-in-the-loop:** You can force the AI to wait for a human to click "Approve" before it executes a specific action (like sending an email or making a purchase).

