---
title: Openenv Workflow Agent
emoji: 📈
colorFrom: green
colorTo: green
sdk: docker
pinned: false
license: mit
---
# 🧠 OpenEnv Workflow Agent — Decision-Making Under Uncertainty

## 🚀 Overview

We present a **real-world OpenEnv environment** that simulates workflow management tasks such as email triage, scheduling, and task handling under **partial observability**.

Unlike typical environments, this benchmark focuses on a critical but underexplored capability:

> 🔥 **Cost-aware information gathering in sequential decision-making**

Agents must decide:
- When to act immediately
- When to request additional information
- Whether the cost of uncertainty reduction is justified

---

## 🎯 Why This Matters

Modern AI agents (LLMs, assistants, copilots) operate in **uncertain environments**:
- Emails are ambiguous  
- User intent is hidden  
- Context is incomplete  

Our environment models this realistically by enforcing:

- ❗ Incorrect actions under uncertainty → penalized  
- ❗ Information gathering → beneficial but costly  
- ❗ Multi-step reasoning required for optimal decisions  

---

## 🧠 Core Idea

We introduce a **POMDP-style workflow environment** where:

- The true state is partially hidden
- Agents must **actively reduce uncertainty**
- Information acquisition has a **non-zero cost**

### Key Property:

> An optimal agent follows:
>
> **“Request information only when expected benefit exceeds cost.”**

---

## ⚙️ Environment Design

### 🔹 State

- Emails (observed)
- Tasks & calendar (observed)
- Hidden attributes:
  - true intent
  - urgency
  - missing information

---

### 🔹 Actions

- `classify`
- `reply`
- `schedule`
- `request_info`
- `archive`
- `prioritize`

---

### 🔹 Reward Function

\[
r_t = r_{correct} + r_{progress} - r_{cost} - r_{penalty}
\]

- Correct action → +0.3  
- Task progress → +0.2  
- Step penalty → −0.01  
- Information request cost → −0.05  
- Incorrect action → −0.2  

---

## 🧪 Tasks

### 🟢 Easy
- Clear intent
- Single-step decision

### 🟡 Medium
- Multi-step workflow
- Requires sequencing

### 🔴 Hard
- Ambiguous input
- Requires **information gathering before acting**

---

## 📊 Baseline Results

```

easy:   1.00
medium: 0.50
hard:   0.13

```

### 🔍 Interpretation

- Baseline performs well on simple tasks  
- Fails on ambiguous scenarios  
- Demonstrates need for **information-aware policies**

---

## 🔥 Key Insight

Standard agents fail because they **act too early under uncertainty**.

Agents that act immediately under uncertainty fail.
Agents that strategically gather information succeed.

This environment makes that tradeoff explicit and measurable.

Our environment exposes this failure mode clearly.

---

## 🧩 Novel Contribution

We introduce:

### ✅ Cost-sensitive information gathering
- Asking questions is beneficial but not free

### ✅ Enforced uncertainty
- Actions without information are penalized

### ✅ Sequential dependency
- Early decisions affect future rewards

---

## 🧪 Validation

We verify:

- ✔ Classification fails under missing information  
- ✔ Requesting info enables correct decisions  
- ✔ Tradeoff emerges between cost and accuracy  

---

## 📦 Project Structure

```

app/
tasks/
graders/
baseline/
scripts/
openenv.yaml
Dockerfile
inference.py

````

---

## ▶️ Run Locally

You can pull the pre-built Docker image directly from Docker Hub and run it:

```bash
docker pull imsachin010/openenv-workflow-agent:latest
docker run -d -p 7860:7860 --name openenv-agent imsachin010/openenv-workflow-agent:latest
```

Test endpoint:

```bash
curl -X POST http://localhost:7860/reset
```

---

## 🤖 Inference

Run the inference script inside the environment:

```bash
python -m inference
```

Outputs:

```
[START]
[STEP]
[END]
```

---

## 🧠 Conclusion

This environment highlights a key gap in current agents:

> ❗ They do not reason about **when to gather information**

We provide a benchmark to evaluate and improve:

* decision-making under uncertainty
* information-seeking behavior
* sequential reasoning

---

## 🏁 Submission Notes

* ✔ Fully OpenEnv compliant
* ✔ Deterministic graders
* ✔ Reproducible via Docker
* ✔ HF Space endpoint available


