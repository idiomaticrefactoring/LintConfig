# TODO List – Linter Configuration & Skill System Improvement

## 1. Multi-Platform Deployment
- [ ] Deploy the system to major commercial LLM platforms  
  - [ ] OpenAI  
  - [ ] Claude  
  - [ ] Google (Gemini / PaLM)

- [ ] Deploy to major open-source LLM platforms  
  - [ ] LLaMA-based platforms  
  - [ ] Mistral / Mixtral  
  - [ ] Other popular open-source serving frameworks

- [ ] Validate prompt compatibility and response consistency across platforms

---

## 2. Crawl and Prepare Linter Knowledge Base
- [ ] Select 5 major programming languages  
  - [ ] Finalize language list

- [ ] For each language, select 3–5 popular linters  
  - [ ] Validate popularity and ecosystem support  
  - [ ] Check version compatibility

- [ ] Crawl and collect linter-related data  
  - [ ] Official documentation  
  - [ ] Configuration examples  
  - [ ] Common rules and best practices

- [ ] Normalize and structure crawled data for model usage

---

## 3. Functional Testing with Diverse Prompts
- [ ] Test current functionality using different prompt styles

### 3.1 Task Description Variants
- [ ] "generate linter configuration"  
- [ ] "how to enforce XXXX"  
- [ ] "configure XXXXX"

### 3.2 Linter Specification
- [ ] Prompt explicitly specifies the linter  
- [ ] Prompt does NOT specify the linter

### 3.3 Crawled Data Coverage
- [ ] Linter exists in crawled data  
- [ ] Linter does NOT exist in crawled data

### 3.4 Coding Standard Input Variations
- [ ] Coding standard provided as plain string  
- [ ] Coding standard provided via file path  
- [ ] Coding standard provided via URL

- [ ] Coding standard length variations  
  - [ ] Single sentence  
  - [ ] No explicit coding standard  
  - [ ] One coding rule  
  - [ ] Two coding rules  
  - [ ] Two sentences that represent a single coding rule

### 3.5 Code Input Variations
- [ ] No code provided  
- [ ] Code provided as string  
- [ ] Code provided via file path  
- [ ] Code provided via URL

---

## 4. Skill.md Design Improvements
- [ ] Review current Skill.md design (prompt-driven only)

- [ ] Identify gaps between prompt logic and actual code execution

- [ ] Improve integration between:  
  - [ ] Prompt design  
  - [ ] Code execution flow  
  - [ ] Linter invocation and result handling

- [ ] Redesign Skill.md to better reflect:  
  - [ ] End-to-end workflow  
  - [ ] Prompt + code collaboration  
  - [ ] Extensibility for new linters and languages

- [ ] Validate the new Skill.md with real-world use cases
