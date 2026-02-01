
how to build one claude code skill：

1. https://www.codecademy.com/article/how-to-build-claude-skills
2. https://github.com/anthropics/claude-cookbooks/blob/dd961e43ecb5947df115e8e17067b3b324e5d5e2/skills/notebooks/03_skills_custom_development.ipynb


Activate claude调用skills auto activate

https://github.com/spences10/claude-skills-cli

注册为skills：https://scottspence.com/posts/claude-code-skills-not-recognised

确保prompt的时候，claud 可以调用：skillshttps://scottspence.com/posts/claude-code-skills-dont-auto-activate




SupeRLinting-skills
One lint is enough to recommend linters,

AI linting 一个  idioms
自动的linter配置—> 调用linter进行检查
自动根据coding standards进行linting 简单的prompt


未来AI coding 工具集成


这种ai coding框架都可以集成skills，目前看都没有linting skills
Opencode 类似claude code, 

https://github.com/anomalyco/opencode


code simplifier
claude 内部的一个skill
https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md

https://blog.devgenius.io/inside-claudes-code-simplifier-plugin-how-anthropic-keeps-its-own-codebase-clean-f12254787fa2



可以试一下下面的三个skill和claude插件里的skill的区别—》 我们的lint/refactor工具要不要作为一个skill, 单独作为一个skill or claude 插件里的skill

这个现在也很火，linting可能也可以继承到这样平台作代码审查
集中在code review
https://www.vibekanban.com/

关于AI的一个skill, 集成在了claude code, codex, Cursor, Windsurf, Copilot, Gemini
https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

An agentic skills framework & software development methodology that works.
集中在软件开发， 融合了多个skills，集成在了claude code, open code, Codex
https://github.com/obra/superpowers



Openhands 里支持/集成了很多的skills， skills是其中的一部分
https://github.com/OpenHands/OpenHands



* Perform code compliance checking by applying the generated linter configurations to source code and reporting detected violations.




chatgpt的shared conversation

https://chatgpt.com/share/696b4875-3140-8010-86b0-ceaa78d50682




刚和chatgpt聊了一下

1. AI coding肯定需要linting，但目前没有工具严肃做linting。有需求但没有任何实际支持，蓝海呀，快上站位。

2. 我没有和chatgpt提我们dsl  compiler思想，但它根据需求自己就提出了这个理念。这也说明我们技术路线是正确的。

3. 他提出多tier linting需求，我们也讨论到这点。

4. dsl compile+tdd for coding spec configure是个不错建议，感觉可以在fse上做个扩展。

5. AI coding context下是有很多动态配置和迁移需求的。chatgpt也给了技术路线建议。

我觉得这些建议很有价值，请看一下







Let end users generate dashboards, widgets, apps, and data visualizations from prompts — safely constrained to components you define.
https://github.com/vercel-labs/json-render

这个本质就是做ai coding context下，按照用户定义的UI组件约束和检查UI代码生成，其实也是UI code linting against some standards。

要利用这个工具，需要把design system表述成他的component catalog。如果把component catalog作为linting dsl，那这个其实也是按照设计系统要求做linting dsl configuration。






https://chatgpt.com/share/696c7509-1154-8010-86d7-344a14e72406

Anyway, 尽快把我们已有的linting能力通过skills机制发布一下肯定是有价值的。其他的是后续研究逐步做。