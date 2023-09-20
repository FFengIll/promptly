# document with embedding

# messages

在用户视角，他们只能看到自己的`指令`和服务的`响应`。[示例](#user-prompt-and-response)

但在服务视角，
1. 所有的`指令`需要经过[转换](#transform-user-messages)
1. 每一个`指令`都会经过embedding分析，获取到相关文档，并附加在整个chat的最前面，作为[相关信息/上下文](#add-to-top)

即如果用户请求如下
```json
{
    "messages": [    
        {
        "role": "user",
        "content": "content",
        "enable": true
        },
    ]
}
```

则服务最后发起的请求是

```json
{
    "messages": [
        {
        "role": "assistant",
        "content": "附加的相关文档，即context",
        "enable": true
        },
        {
        "role": "user",
        "content": "经过转换的指令，包含 latestReply 和 content",
        "enable": true
        },
    ]
}
```

## user prompt and response

> 下例链接：https://www.matterhackers.com/articles/3d-printing-essentials-first-layer

```json
{
  "name": "3d_article",
  "messages": [
    {
      "role": "user",
      "content": "首层的意义？",
      "enable": true
    },
    {
      "role": "assistant",
      "content": "根据你阅读的文章，首层在3D打印中非常重要。它是打印过程中的第一层，对于打印质量和精度至关重要。首层的目的是确保打印物件与打印平台之间有良好的粘附力，以防止打印物件在打印过程中移动或变形。如果首层不正确，可能会导致打印物件无法正常粘附或打印过程中出现问题。因此，正确调整和校准首层是获得成功的3D打印非常重要的一步。",
      "enable": true
    },
    {
      "role": "user",
      "content": "翻译为英文",
      "enable": true
    },
    {
      "role": "assistant",
      "content": "The significance of the first layer?\nAccording to the article you read, the first layer is crucial in 3D printing. It is the initial layer during the printing process and plays a vital role in print quality and accuracy. The purpose of the first layer is to ensure proper adhesion between the printed object and the print bed, preventing the object from shifting or deforming during printing. If the first layer is not set up correctly, it may result in poor adhesion or issues during the printing process. Therefore, adjusting and calibrating the first layer correctly is an essential step for successful 3D printing.",
      "enable": true
    },
    {
      "role": "user",
      "content": "精简成更短的段落",
      "enable": true
    },
    {
      "role": "assistant",
      "content": "The first layer in 3D printing is crucial for ensuring print quality and accuracy. It is responsible for proper adhesion between the object and the print bed, preventing shifting or deformation during printing. Correctly setting up the first layer is essential for successful 3D printing.",
      "enable": true
    },
    {
      "role": "user",
      "content": "西游记作者是？",
      "enable": true
    },
    {
      "role": "assistant",
      "content": "I'm sorry, but I am tuned to answer questions related to the context and provide information based on the articles I have read. I don't have information about the author of \"Journey to the West\" (西游记).",
      "enable": true
    },
    {
      "role": "user",
      "content": "How to use z-offset.",
      "enable": true
    },
    {
      "role": "assistant",
      "content": "根据你阅读的文章，使用Z偏移量（Z-offset）的方法如下：\n\n1. 首先，在你的3D打印机上找到Z偏移量的设置选项。这通常可以在打印机的控制面板、打印机软件或设置文件中找到。\n\n2. 启动你的3D打印机并将打印床预热至适当的温度。确保打印床已经进行了水平调整，以确保平整度和一致性。\n\n3. 选择一个测试模型或创建一个小的测试对象，以便进行Z偏移量的调整。\n\n4. 将测试对象放置在打印床上，启动打印过程。\n\n5. 在打印过程中，观察首层的打印情况。如果首层看起来太高或太低，你可以通过调整Z偏移量来解决这个问题。\n\n6. 如果首层看起来太高，你可以将Z偏移量减小一点，使喷嘴更靠近打印床。如果首层看起来太低，你可以将Z偏移量增加一点，使喷嘴离打印床稍远一些。\n\n7. 通过微调Z偏移量，逐步调整首层的高度，直到你获得理想的打印效果。记住，在调整Z偏移量时要小心，不要调整得太过或太远，以免影响整个打印过程。\n\n请注意，不同的3D打印机和打印材料可能会有不同的Z偏移量设置方法和调整范围。在进行调整之前，建议查阅你的3D打印机的用户手册或相关文档，以了解更多关于Z偏移量的详细信息。",
      "enable": true
    },
    {
      "role": "system",
      "content": "Reponse in `${lang}` if possible.",
      "enable": true
    }
  ]
}
```

## add to top


```json
{
    "role": "assistant",
    "content": "===Related===\n{context}"
}
```


## transform user messages

```json
{
    "role": "user",
    "content": "You are a helpful AI assistant.\n\nIf `Instruction` is a question:\n- Use `Related` to answer the `Question`.\n- If you don't know the answer, just say you don't know. DO NOT try to make up an answer.\n- If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.\n- Answer start with `according to your reading article`.\n\nIf `Instruction` is a task:\n- Try to complete the task with `Last Response`.\n\n===Last Response===\n{latestReply}\n\n===Instruction===\n{content}"
}
```
