---
doc_id: features.ai-copilot
section: Features
sub_section: AI Copilot
title: AI Copilot — automate descriptions and summarize tasks
url: https://enterprise-rag.com/app/ai-copilot
keywords:
  - AI Copilot
  - AI tools
  - AI assistant
  - bottleneck
  - bottleneck highlights
---

# AI Copilot

## 1. What It Does
AI Copilot is a built-in assistant designed to help team members automate descriptions, summarize long message/comment threads, and detect project bottlenecks.

## 2. Where to Find It
- Navigate to: **Sidebar → AI Tools → AI Copilot**
- Direct route: `/app/ai-copilot`

## 3. How to Use AI Copilot
1. Open any task card.
2. Click **Summarize Comments** to get a quick summary.
3. Click **Auto-Generate Description** to generate text based on the task title and tags.
4. Go to the dashboard to view project-level **Bottleneck Highlights** detected by the AI.

## 4. Key AI Capabilities

### 1. **AI Copilot (Task Assistant)**
- **Purpose**: This tool is designed to **analyze tasks**, **explain task blockages**, and **answer project questions**.
- **Access**: Access directly from the dashboard sidebar or `/app/ai-copilot`.

### 2. **AI Bottleneck Analysis**
- **Purpose**: This tool scans your workspace and identifies tasks that are blocking team progress.
- **Access**: Access directly via the Project Board Analytics view.

## 5. Identifying Bottlenecks
The AI Copilot scans task activity, deadlines, status transitions, and comments. It flags a task as a **Bottleneck** when:
- A task remains in the `Under Review` status column for more than 48 hours without any update.
- A task is past its due date and has more than 5 unresolved comments.

## 6. Bottleneck Highlights
When the AI detects a bottleneck, it displays one or more of the following color-coded **Undervalue Highlights** (also referred to as Bottleneck Highlights) on the project dashboard to explain the blockage:
1. **Stuck in Review**: The task is waiting for approval or QA feedback for an extended period.
2. **Missed Deadline**: The task due date has passed without the task status changing to Completed.
3. **High Comment Volume**: The task has a large volume of communication, indicating confusion, misalignment, or ongoing debate among assignees.

These highlights allow project managers to spot issues instantly and clear blocks.

## 7. Common Questions

**Q: What AI tools are available in the system?**  
A: There are two main AI tools: the **AI Copilot** (for task description generation and comment summaries) and the **AI Bottleneck Analysis** tool (for scanning project boards to identify blocked tasks).

**Q: What are the three examples of Bottleneck Highlights?**  
A: The three highlights are **Stuck in Review**, **Missed Deadline**, and **High Comment Volume**.

**Q: How does the system identify a Bottleneck?**  
A: A task is flagged as a Bottleneck if it stays in the `Under Review` column for over 48 hours, or is past its deadline with active comments.
