
# prompt design
## principle
- 使用尽可能简短但显著有效的prompt
- 提供并控制必要的场外信息，如时间，角色
- 根据使用场景，控制回复量（成本控制）

## system prompt
目前考虑将system prompt拆分为多个。

> 关于这点，社区众说风云，如：合并效率更好；分拆可以让每一句的效果更明确；合并可能模糊作用效果 等。

目前计划仍是拆分为多个，这样可以在后端相对灵活的进行组合使用，也可以随时兜底到合并模式。

关于system prompt的顺序，目前从实验上看没有显著区别，这一点官方也没有明确说明。
但比较多的反馈是，放在后面有效的机会会更大。
另一方面，官方也有表述`system role现在并不能如预期般严格生效`。

> https://community.openai.com/t/the-system-role-how-it-influences-the-chat-behavior/87353/2

## chat
chat过程中，需要结合system prompt进行一系列的控制，包括
- 日期，date
- 角色，act
- 回答篇幅，size limit
  - 目前通过 short，medium，long size 可以显著生效
- 响应语言，lang / locale
  - auto，即 as it is
  - 其他，即指定语言，如chinese

### 遗留问题
- date 的时区可能存在差异，无法固定
- size limit 不适合指定 char number 或 token number，因为有些回答有最低篇幅问题，用模糊的形容词可能更好（如 short size）

## search RQ
即QA并附加related question
建议提供独立的接口，用于RQ模式，并支持参数
- lang
- keyword
- size（limit）
  - 默认是short

这里需要后端拼装system prompt

## search A
即直接answer with keyword。
建议直接使用标准的chat进行，即前端直接拼装user prompt，并包含参数
- lang

也可以开启新的接口（保障prompt不泄露）
并由后端拼装user prompt

这里之所以使用user prompt，是因为需要严格的控制lang（并高准确生效），因此将lang植入prompt肯定是比system prompt辅助效果更好的。