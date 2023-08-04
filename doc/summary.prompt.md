# Summary

## first summary

### v1

```json
[
  {
    "role": "system",
    "content": "summary content into `strict one` paragraph, `sort` size, language `chinese`.",
    "id": 90347953623601650,
    "enable": true,
    "order": 0
  },
  {
    "role": "user",
    "content": "1. Introduction\nPretrained language models have become a cornerstone of modern natural language processing\n(NLP) pipelines because they often produce better performance from smaller quantities\nof labeled data. The development of ELMo (Peters et al., 2018), ULMFiT (Howard\nand Ruder, 2018), GPT (Radford et al., 2018), and BERT (Devlin et al., 2019) led to the\nwidespread use of pretrained models as an initialization for finetuning on downstream tasks.\nThe subsequent finding that pretrained language models can perform useful tasks without\nany additional training (Radford et al., 2019; Brown et al., 2020) further demonstrated their\nutility. In addition, the empirical observation that a language model's performance tends to\nincrease as the model is made larger sometimes predictably (Hestness et al., 2017; Kaplan\net al., 2020; Hoffmann et al., 2022) and sometimes suddenly (Wei et al., 2022) has led to a\ntrend of increasing scale (Zeng et al., 2021; Rae et al., 2021; Smith et al., 2022; Chowdhery\net al., 2022). Apart from environmental concerns (Strubell et al., 2019; Lacoste et al., 2019;\nSchwartz et al., 2020), the costs of training large language models (LLMs) are only affordable\nfor well-resourced organizations. Furthermore, until recently, most LLMs were not\npublicly released. As a result, the majority of the research community has been excluded\nfrom the development of LLMs. This exclusion has had concrete consequences; for example,\nmost LLMs are primarily trained on English-language text (with notable exceptions in\nChinese and Korean, e.g. Wang et al., 2021; Zeng et al., 2021; Kim et al., 2021).\nTo address these issues, we present the BigScience Large Open-science Open-access Multilingual\nLanguage Model (BLOOM, BigScience Workshop, 2022). BLOOM is a 176 billion\nparameter language model trained on 46 natural languages and 13 programming languages\nthat was developed and released by a collaboration of hundreds of researchers. The compute\nfor training BLOOM was provided through a French public grant from GENCI and\nIDRIS, leveraging IDRIS' Jean Zay supercomputer. To build BLOOM, we undertook a\nthorough design process for each of its components, including the training dataset (Section\n3.1), model architecture and training objective (Section 3.2), and engineering strategy\nfor distributed learning (Section 3.4). We also performed an analysis of the model's capabilities\n(Section 4). Our overall aim is not only to publicly release a large-scale multilingual\nlanguage model with performance comparable to recently developed systems, but also to\ndocument the coordinated process that went into its development (Section 2.2). The purpose\nof this paper is to provide a high-level overview of these design steps while referencing\nthe individual reports we produced over the course of developing BLOOM.",
    "id": 90349285063463410,
    "enable": true,
    "order": 1
  }
]

```

### v2

```json

[
  {
    "role": "system",
    "content": "Response in `English` and short size.\nSummarize content into strict one paragraph.",
    "id": 16028668458887156000,
    "enable": true,
    "order": 0
  },
  {
    "role": "user",
    "content": "”>“创建配置文件...”下拉菜单选择一个配置文件模板：\n\n选择配置文件模板后，您可以查看设置、扩展和其他数据，如果不想将个别项目包含在其中，则可以将其删除。\n\n在您基于模板创建新配置文件后，对设置、扩展程序或 UI 所做的更改将保留到您的配置文件中。\n\n**拖放选择器**\n\n您可以在放置前按住 Shift 键，将文件和内容放置到文本编辑器中。在此更新中，我们添加了 UI，可让您更改此内容插入文件的方式。例如，在将图像放入 Markdown 文件后，此控件允许您在插入 Markdown 图像、图像的工作区相对路径和图像的完整路径之间切换：\n\n每当您拖放内容并且有不止一种可能的插入方式时，拖放选择器控件就会出现。您可以通过单击或使用 Ctrl+. 打开控件。当您开始键入或将光标移到插入的文本之外，下拉选择器就会消失。您还可以使用\"editor.dropIntoEditor.showDropSelector\": \"never\" 完全禁用拖放选择器控件。\n\nVS Code 包括一些内置的方法来删除常见的内容格式。扩展还可以使用 DocumentDropEditProvider API 添加自己的拖放选项。\n\n**独立的颜色选择器**\n\n现在可以启动独立的颜色选择器来插入和替换颜色。打开颜色选择器，请从命令面板中选择“显示或聚焦独立颜色选择器”。\n\n当扩展没有提供颜色或颜色格式时，颜色选择器会回退到 CSS 格式的颜色。现在还可以在所有文件类型中可视化 CSS 格式颜色的内联颜色装饰器。要显示这些装饰器，请启用“编辑器：默认颜色装饰器” (editor.defaultColorDecorators)设置。\n\n**源代码控制输入中的快速修复**\n\n现在支持在源代码控制消息框中使用代码操作和快速修复：\n\n例如，Code Spell Checker 扩展为源代码控制输入添加了拼写修复。扩展可以提供额外的修复和代码操作。\n\n**将视频拖放到 Markdown 文件中**\n\n想在 Markdown 中插入视频吗？只需将它拖到编辑器中，然后按住 Shift 键将其放入文件中：\n\n这会插入一个指向视频文件的 <video> 标签。您可以从 VS Code 的资源管理器或本地操作系统中拖动视频。\n\n**将图像文件拖放到笔记本中以创建附件**\n\n您现在可以将图像文件拖放到笔记本 Markdown 单元格中以创建附件。放置图像时，使用新的放置选择器控件选择插入图像作为附件：\n\n这会将图像作为附件添加到笔记本中，而不是简单地添加图像链接：\n\n**将文件提交到 Git 大文件存储**\n\nGit 大文件存储 (Git Large File Storage, LFS) 允许您在 Git 存储库中高效地存储大文件。github.dev 和 vscode.dev 现在支持将文件提交到 GitHub 上托管的存储库中的 Git LFS，从而可以从浏览器轻松更新，而无需在本地安装 Git 的 LFS 扩展。\n\ngithub.dev 和 vscode.dev 中的 LFS 提交支持在您的存储库的根目录中已经有一个 .gitattributes 文件时开箱即用，该文件指定应使用 Git LFS 存储哪些文件类型\n",
    "id": 16028671207666225000,
    "enable": true,
    "order": 1
  }
]
```

The latest update of VS Code introduces several new features and improvements. Users can now select a configuration file template from a dropdown menu and customize it by adding or removing individual items. The update also includes a drag and drop selector that allows users to choose how content is inserted into the text editor. Additionally, a standalone color picker has been added, which can be accessed from the command palette. The color picker supports CSS format colors and can be visualized with inline color decorators in all file types. In source code control, quick fixes and code actions are now supported in the message box. Users can also drag and drop videos into Markdown files to insert them as <video> tags. Furthermore, image files can be dropped into Markdown cells to create attachments in notebooks. Lastly, users can now submit files to Git Large File Storage (LFS) directly from github.dev and vscode.dev without the need for the LFS extension.

## combine the summary

### v1

```json

[
  {
    "role": "system",
    "content": "Bellow are all summaries for article chunk.\nCombine these summaries into short size.",
    "id": 14512150759751750000,
    "enable": true,
    "order": 0
  },
  {
    "role": "user",
    "content": "Visual Studio Code 2023 年 4 月版的主要亮点包括辅助功能改进、新颜色主题、配置文件模板、拖放选择器、独立颜色选择器、源代码管理输入的快速修复、Markdown 拖放视频和将图像文件拖放到笔记本中以创建附件。具体改进包括屏幕阅读器的冗余设置、diff 编辑器音频提示的改进、转到行/列功能的改进和新的默认颜色主题。此外，还添加了配置文件模板，可以根据当前项目或任务快速切换编辑器扩展、设置和 UI 布局。拖放选择器可以在放置文件和内容到编辑器中之前，通过按住 Shift 键来选择如何插入文件。\n\n创建配置文件时，可以选择一个配置文件模板。您可以查看设置、扩展和其他数据，并删除不想包含的项目。创建新配置文件后，对设置、扩展程序或UI所做的更改将保留在配置文件中。使用拖放选择器可以将文件和内容放置到文本编辑器中。新版本中添加了UI，可以更改插入文件的方式。内置的颜色选择器可以插入和替换颜色。在源代码控制输入中，支持代码操作和快速修复。可以将视频拖放到Markdown文件中来插入视频。可以将图像文件拖放到笔记本中以创建附件。还可以将文件提交到Git Large File Storage中，以高效地存储大文件。",
    "id": 14512154367524278000,
    "enable": true,
    "order": 0
  }
]
```

### v2

```json

[
  {
    "role": "user",
    "content": "Visual Studio Code 2023 年 4 月版的主要亮点包括辅助功能改进、新颜色主题、配置文件模板、拖放选择器、独立颜色选择器、源代码管理输入的快速修复、Markdown 拖放视频和将图像文件拖放到笔记本中以创建附件。具体改进包括屏幕阅读器的冗余设置、diff 编辑器音频提示的改进、转到行/列功能的改进和新的默认颜色主题。此外，还添加了配置文件模板，可以根据当前项目或任务快速切换编辑器扩展、设置和 UI 布局。拖放选择器可以在放置文件和内容到编辑器中之前，通过按住 Shift 键来选择如何插入文件。\n\n创建配置文件时，可以选择一个配置文件模板。您可以查看设置、扩展和其他数据，并删除不想包含的项目。创建新配置文件后，对设置、扩展程序或UI所做的更改将保留在配置文件中。使用拖放选择器可以将文件和内容放置到文本编辑器中。新版本中添加了UI，可以更改插入文件的方式。内置的颜色选择器可以插入和替换颜色。在源代码控制输入中，支持代码操作和快速修复。可以将视频拖放到Markdown文件中来插入视频。可以将图像文件拖放到笔记本中以创建附件。还可以将文件提交到Git Large File Storage中，以高效地存储大文件。",
    "id": 3325707836586463700,
    "enable": true,
    "order": 0
  },
  {
    "role": "system",
    "content": "Response in Chinese and in short size.\nCombine following summaries, rewrite into a better paragraph.",
    "id": 3325705646153143000,
    "enable": true,
    "order": 1
  }
]
```

Visual Studio Code 2023年4月版的主要亮点包括辅助功能改进、新颜色主题、配置文件模板、拖放选择器、独立颜色选择器、源代码管理输入的快速修复、Markdown拖放视频和将图像文件拖放到笔记本中以创建附件。具体改进包括屏幕阅读器的冗余设置、diff编辑器音频提示的改进、转到行/列功能的改进和新的默认颜色主题。此外，还添加了配置文件模板，可以根据当前项目或任务快速切换编辑器扩展、设置和UI布局。拖放选择器可以在放置文件和内容到编辑器中之前，通过按住Shift键来选择如何插入文件。

# QA

## system - QA via context

```json
[
  {
    "role": "user",
    "content": "You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.\nIf you don't know the answer, just say `you don't know about question from the article`. DO NOT try to make up an answer.\nIf the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.\n\n预训练语言模型已成为现代自然语言处理流程的基石，因为它们通常能在少量标注数据的情况下产生更好的性能。ELMo、ULMFiT、GPT和BERT的发展导致了预训练模型在下游任务微调时的广泛使用。进一步的研究表明，预训练语言模型在不进行任何额外训练的情况下也可以执行有用的任务。此外，观察到语言模型的性能往往随着模型变大而增加，这导致了规模不断增加的趋势。然而，大规模语言模型的训练成本对于资源有限的组织来说是难以承担的。此外，直到最近，大多数大规模语言模型并没有公开发布，使得大部分研究社区无法参与其发展。为了解决这些问题，我们提出了BigScience Large Open-science Open-access Multilingual Language Model（BLOOM）。BLOOM是一个训练了46种自然语言和13种编程语言的1760亿参数的语言模型，由数百名研究人员合作开发和发布。为了构建BLOOM，我们对其各个组成部分进行了详细的设计，包括训练数据集、模型架构和训练目标，以及分布式学习的工程策略。我们还对模型的能力进行了分析。我们的目标不仅是公开发布一个与最近开发的系统性能相当的大规模多语言语言模型，还要记录其开发过程中的协调过程。本文的目的是提供这些设计步骤的高级概述，并引用我们在开发BLOOM过程中产生的各个报告。\n\nQuestion: 如何打铁\nHelpful answer in markdown and  start with `according to your reading article`:\n",
    "id": 5573448931937554000,
    "enable": true,
    "order": 0
  }
]
```

## system & user - QA

```json
[
  {
    "role": "system",
    "content": "You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.\nIf you don't know the answer, just say you don't know. DO NOT try to make up an answer.\nIf the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.",
    "id": 1,
    "enable": true,
    "order": 1
  },
  {
    "role": "user",
    "id": 2,
    "enable": true,
    "content": "Context:\n----------\n预训练语言模型已成为现代自然语言处理流程的基石，因为它们通常能在少量标注数据的情况下产生更好的性能。ELMo、ULMFiT、GPT和BERT的发展导致了预训练模型在下游任务微调时的广泛使用。进一步的研究表明，预训练语言模型在不进行任何额外训练的情况下也可以执行有用的任务。此外，观察到语言模型的性能往往随着模型变大而增加，这导致了规模不断增加的趋势。然而，大规模语言模型的训练成本对于资源有限的组织来说是难以承担的。此外，直到最近，大多数大规模语言模型并没有公开发布，使得大部分研究社区无法参与其发展。为了解决这些问题，我们提出了BigScience Large Open-science Open-access Multilingual Language Model（BLOOM）。BLOOM是一个训练了46种自然语言和13种编程语言的1760亿参数的语言模型，由数百名研究人员合作开发和发布。为了构建BLOOM，我们对其各个组成部分进行了详细的设计，包括训练数据集、模型架构和训练目标，以及分布式学习的工程策略。我们还对模型的能力进行了分析。我们的目标不仅是公开发布一个与最近开发的系统性能相当的大规模多语言语言模型，还要记录其开发过程中的协调过程。本文的目的是提供这些设计步骤的高级概述，并引用我们在开发BLOOM过程中产生的各个报告。\n----------\n\nQuestion: 如何打铁\nHelpful answer in markdown and  start with `according to your reading article`:",
    "order": 2,
    "history": []
  }
]

```

## system & user - QA (better)

### case 1

```json
[
  {
    "role": "system",
    "content": "You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.\nIf you don't know the answer, just say you don't know. DO NOT try to make up an answer.\nIf the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.\n\nHelpful answer in markdown, in language `chinese` and  start with `according to your reading article`.",
    "id": 1,
    "enable": true,
    "order": 1
  },
  {
    "role": "user",
    "id": 2,
    "enable": true,
    "content": "Question: 介绍bloom\nContext:  预训练语言模型已成为现代自然语言处理流程的基石，因为它们通常能在少量标注数据的情况下产生更好的性能。ELMo、ULMFiT、GPT和BERT的发展导致了预训练模型在下游任务微调时的广泛使用。进一步的研究表明，预训练语言模型在不进行任何额外训练的情况下也可以执行有用的任务。此外，观察到语言模型的性能往往随着模型变大而增加，这导致了规模不断增加的趋势。然而，大规模语言模型的训练成本对于资源有限的组织来说是难以承担的。此外，直到最近，大多数大规模语言模型并没有公开发布，使得大部分研究社区无法参与其发展。为了解决这些问题，我们提出了BigScience Large Open-science Open-access Multilingual Language Model（BLOOM）。BLOOM是一个训练了46种自然语言和13种编程语言的1760亿参数的语言模型，由数百名研究人员合作开发和发布。为了构建BLOOM，我们对其各个组成部分进行了详细的设计，包括训练数据集、模型架构和训练目标，以及分布式学习的工程策略。我们还对模型的能力进行了分析。我们的目标不仅是公开发布一个与最近开发的系统性能相当的大规模多语言语言模型，还要记录其开发过程中的协调过程。本文的目的是提供这些设计步骤的高级概述，并引用我们在开发BLOOM过程中产生的各个报告。\n\n",
    "order": 2,
    "history": []
  }
]


```

### case 2

```json

[
  {
    "role": "system",
    "content": "You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.\nIf you don't know the answer, just say you don't know. DO NOT try to make up an answer.\nIf the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.\n\nHelpful answer in markdown, in language `chinese` and  start with `according to your reading article`.",
    "id": 1,
    "enable": true,
    "order": 1
  },
  {
    "role": "user",
    "id": 2,
    "enable": true,
    "content": "Question: 列出所有新特性\nContext:  **点击上方蓝字**\n\n**关注我们**\n\n（本文阅读时间：5分钟)\n\n欢迎使用 Visual Studio Code 2023 年 4 月版。一些主要亮点包括：\n\n*   **辅助功能改进** \\- 更好的屏幕阅读器支持、新的音频提示。\n\n*   **新颜色主题** \\- “现代”浅色和深色主题默认设置。\n\n*   **配置文件模板** \\- Python、Java、数据科学等的内置模板。\n\n*   **拖放选择器** \\- 选择您希望如何将项目链接放置到编辑器中。\n\n*   **独立颜色选择器** \\- 用于插入或修改颜色格式的颜色选择器 UI。\n\n*   **源代码管理输入的快速修复** \\- 直接在输入框中修复拼写和其他错误。\n\n*   **Markdown 拖放视频** \\- 在 Markdown 文件中轻松添加视频标签。\n\n*   **将图像文件拖放到笔记本中以创建附件** \\- 在图像链接、路径或附件之间进行选择。\n\n\n**辅助功能**\n\n**▍****Aria 冗余设置**\n\n屏幕阅读器用户可以通过“accessibility.verbosity.diff-editor”和“accessibility.verbosity.terminal”设置从功能的 aria-label 中排除提示以减少冗余。\n\n**▍****diff 编辑器音频提示改进**\n\nVS Code 现在缓存音频提示，因此它们只需加载一次，从而产生更好的响应能力，并改进了用于 diff 编辑器的音调。\n\n**▍****转到行/列公告**\n\n当调用“转到行/列” (Ctrl+G) 时，屏幕阅读器现在会读取关联的行内容。\n\n**新的默认颜色主题**\n\n新的“深色现代”和“浅色现代”主题取代了“深色”和“浅色”，成为新的默认深色和浅色主题。\n\n**配置文件模板**\n\n配置文件可让您根据当前项目或任务快速切换编辑器扩展、设置和 UI 布局。为了帮助您开始使用配置文件，我们提供了配置文件模板，这些模板是针对不同编程语言和场景的精选配置文件。您可以按原样使用配置文件模板，也可以将其用作起点以进一步自定义您自己的工作流程。\n\n您可以通过“配置文件”>“创建配置文件...”下拉菜单选择一个配置文件模板：\n\n选择配置文件模板后，您可以查看设置、扩展和其他数据，如果不想将个别项目包含在其中，则可以将其删除。\n\n在您基于模板创建新配置文件后，对设置、扩展程序或 UI 所做的更改将保留到您的配置文件中。\n\n**拖放选择器**\n\n您可以在放置前按住 Shift 键，将文件和内容放置到文本编辑器中。在此更新中，我们添加了 UI，可让您更改此内容插入文件\n\n",
    "order": 2,
    "history": []
  }
]
```

## system & user - QA (better) - v0.0804

### case 1

```json
[
  {
    "role": "system",
    "content": "You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.\nIf you don't know the answer, just say you don't know. DO NOT try to make up an answer.\nIf the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.\n\nRespnse in language `chinese`.\nHelpful answer in markdown, and  start with `according to your reading article`.",
    "id": 13188714767125778000,
    "enable": true,
    "order": 1
  },
  {
    "role": "user",
    "content": "Question: 列出所有新特性\nContext:  **点击上方蓝字**\n\n**关注我们**\n\n（本文阅读时间：5分钟)\n\n欢迎使用 Visual Studio Code 2023 年 4 月版。一些主要亮点包括：\n\n*   **辅助功能改进** \\- 更好的屏幕阅读器支持、新的音频提示。\n\n*   **新颜色主题** \\- “现代”浅色和深色主题默认设置。\n\n*   **配置文件模板** \\- Python、Java、数据科学等的内置模板。\n\n*   **拖放选择器** \\- 选择您希望如何将项目链接放置到编辑器中。\n\n*   **独立颜色选择器** \\- 用于插入或修改颜色格式的颜色选择器 UI。\n\n*   **源代码管理输入的快速修复** \\- 直接在输入框中修复拼写和其他错误。\n\n*   **Markdown 拖放视频** \\- 在 Markdown 文件中轻松添加视频标签。\n\n*   **将图像文件拖放到笔记本中以创建附件** \\- 在图像链接、路径或附件之间进行选择。\n\n\n**辅助功能**\n\n**▍****Aria 冗余设置**\n\n屏幕阅读器用户可以通过“accessibility.verbosity.diff-editor”和“accessibility.verbosity.terminal”设置从功能的 aria-label 中排除提示以减少冗余。\n\n**▍****diff 编辑器音频提示改进**\n\nVS Code 现在缓存音频提示，因此它们只需加载一次，从而产生更好的响应能力，并改进了用于 diff 编辑器的音调。\n\n**▍****转到行/列公告**\n\n当调用“转到行/列” (Ctrl+G) 时，屏幕阅读器现在会读取关联的行内容。\n\n**新的默认颜色主题**\n\n新的“深色现代”和“浅色现代”主题取代了“深色”和“浅色”，成为新的默认深色和浅色主题。\n\n**配置文件模板**\n\n配置文件可让您根据当前项目或任务快速切换编辑器扩展、设置和 UI 布局。为了帮助您开始使用配置文件，我们提供了配置文件模板，这些模板是针对不同编程语言和场景的精选配置文件。您可以按原样使用配置文件模板，也可以将其用作起点以进一步自定义您自己的工作流程。\n\n您可以通过“配置文件”>“创建配置文件...”下拉菜单选择一个配置文件模板：\n\n选择配置文件模板后，您可以查看设置、扩展和其他数据，如果不想将个别项目包含在其中，则可以将其删除。\n\n在您基于模板创建新配置文件后，对设置、扩展程序或 UI 所做的更改将保留到您的配置文件中。\n\n**拖放选择器**\n\n您可以在放置前按住 Shift 键，将文件和内容放置到文本编辑器中。在此更新中，我们添加了 UI，可让您更改此内容插入文件\n\n",
    "id": 13188715840867602000,
    "enable": true,
    "order": 2
  }
]
```

根据您的阅读文章，以下是 Visual Studio Code 2023 年 4 月版的新特性：

- 辅助功能改进：更好的屏幕阅读器支持和新的音频提示。
- 新颜色主题：新增了“现代”浅色和深色主题作为默认设置。
- 配置文件模板：内置了 Python、Java、数据科学等的配置文件模板，可以快速切换编辑器扩展、设置和 UI 布局。
- 拖放选择器：可以选择将项目链接放置到编辑器中的方式。
- 独立颜色选择器：用于插入或修改颜色格式的颜色选择器 UI。
- 源代码管理输入的快速修复：可以直接在输入框中修复拼写和其他错误。
- Markdown 拖放视频：可以在 Markdown 文件中轻松添加视频标签。
- 将图像文件拖放到笔记本中以创建附件：可以选择图像链接、路径或附件来创建附件。

希望这些信息对您有所帮助！

### case 2

```json
[
  {
    "role": "system",
    "content": "You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.\nIf you don't know the answer, just say you don't know. DO NOT try to make up an answer.\nIf the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.\n\nRespnse in language `chinese`.\nHelpful answer in markdown, and  start with `according to your reading article`.",
    "id": 13188714767125778000,
    "enable": true,
    "order": 1
  },
  {
    "role": "user",
    "content": "Question: 如何打铁\nContext:  **点击上方蓝字**\n\n**关注我们**\n\n（本文阅读时间：5分钟)\n\n欢迎使用 Visual Studio Code 2023 年 4 月版。一些主要亮点包括：\n\n*   **辅助功能改进** \\- 更好的屏幕阅读器支持、新的音频提示。\n\n*   **新颜色主题** \\- “现代”浅色和深色主题默认设置。\n\n*   **配置文件模板** \\- Python、Java、数据科学等的内置模板。\n\n*   **拖放选择器** \\- 选择您希望如何将项目链接放置到编辑器中。\n\n*   **独立颜色选择器** \\- 用于插入或修改颜色格式的颜色选择器 UI。\n\n*   **源代码管理输入的快速修复** \\- 直接在输入框中修复拼写和其他错误。\n\n*   **Markdown 拖放视频** \\- 在 Markdown 文件中轻松添加视频标签。\n\n*   **将图像文件拖放到笔记本中以创建附件** \\- 在图像链接、路径或附件之间进行选择。\n\n\n**辅助功能**\n\n**▍****Aria 冗余设置**\n\n屏幕阅读器用户可以通过“accessibility.verbosity.diff-editor”和“accessibility.verbosity.terminal”设置从功能的 aria-label 中排除提示以减少冗余。\n\n**▍****diff 编辑器音频提示改进**\n\nVS Code 现在缓存音频提示，因此它们只需加载一次，从而产生更好的响应能力，并改进了用于 diff 编辑器的音调。\n\n**▍****转到行/列公告**\n\n当调用“转到行/列” (Ctrl+G) 时，屏幕阅读器现在会读取关联的行内容。\n\n**新的默认颜色主题**\n\n新的“深色现代”和“浅色现代”主题取代了“深色”和“浅色”，成为新的默认深色和浅色主题。\n\n**配置文件模板**\n\n配置文件可让您根据当前项目或任务快速切换编辑器扩展、设置和 UI 布局。为了帮助您开始使用配置文件，我们提供了配置文件模板，这些模板是针对不同编程语言和场景的精选配置文件。您可以按原样使用配置文件模板，也可以将其用作起点以进一步自定义您自己的工作流程。\n\n您可以通过“配置文件”>“创建配置文件...”下拉菜单选择一个配置文件模板：\n\n选择配置文件模板后，您可以查看设置、扩展和其他数据，如果不想将个别项目包含在其中，则可以将其删除。\n\n在您基于模板创建新配置文件后，对设置、扩展程序或 UI 所做的更改将保留到您的配置文件中。\n\n**拖放选择器**\n\n您可以在放置前按住 Shift 键，将文件和内容放置到文本编辑器中。在此更新中，我们添加了 UI，可让您更改此内容插入文件\n\n",
    "id": 13188715840867602000,
    "enable": true,
    "order": 2
  }
]
```

根据您的阅读文章，没有提到如何打铁的信息。抱歉，我无法回答这个问题。

# RQ

## Generate RQ

```json
[
  {
    "role": "system",
    "content": "Combine bellow summaries into better (as `S`), generate 3 most useful and strict related question (as `RQ`).\nResponse strict in format:\nS:\nRQ:\nRQ:\nRQ:",
    "id": 89973131827679730,
    "enable": true,
    "order": 0
  },
  {
    "role": "user",
    "content": "预训练语言模型已成为现代自然语言处理流程的基石，因为它们通常能在少量标注数据的情况下产生更好的性能。ELMo、ULMFiT、GPT和BERT的发展导致了预训练模型在下游任务微调时的广泛使用。进一步的研究表明，预训练语言模型在不进行任何额外训练的情况下也可以执行有用的任务。此外，观察到语言模型的性能往往随着模型变大而增加，这导致了规模不断增加的趋势。然而，大规模语言模型的训练成本对于资源有限的组织来说是难以承担的。此外，直到最近，大多数大规模语言模型并没有公开发布，使得大部分研究社区无法参与其发展。为了解决这些问题，我们提出了BigScience Large Open-science Open-access Multilingual Language Model（BLOOM）。BLOOM是一个训练了46种自然语言和13种编程语言的1760亿参数的语言模型，由数百名研究人员合作开发和发布。为了构建BLOOM，我们对其各个组成部分进行了详细的设计，包括训练数据集、模型架构和训练目标，以及分布式学习的工程策略。我们还对模型的能力进行了分析。我们的目标不仅是公开发布一个与最近开发的系统性能相当的大规模多语言语言模型，还要记录其开发过程中的协调过程。本文的目的是提供这些设计步骤的高级概述，并引用我们在开发BLOOM过程中产生的各个报告。",
    "id": 89975622908711410,
    "enable": true,
    "order": 1
  }
]
```

## Both Summary and RQ

```json
[
  {
    "role": "system",
    "content": "Combine bellow summaries into better (as `S`), generate 3 most useful and strict related question (as `RQ`).\nResponse strict in format:\n\nS:\nRQ:\nRQ:\nRQ:",
    "id": 14512150759751750000,
    "enable": true,
    "order": 0
  },
  {
    "role": "user",
    "content": "Visual Studio Code 2023 年 4 月版的主要亮点包括辅助功能改进、新颜色主题、配置文件模板、拖放选择器、独立颜色选择器、源代码管理输入的快速修复、Markdown 拖放视频和将图像文件拖放到笔记本中以创建附件。具体改进包括屏幕阅读器的冗余设置、diff 编辑器音频提示的改进、转到行/列功能的改进和新的默认颜色主题。此外，还添加了配置文件模板，可以根据当前项目或任务快速切换编辑器扩展、设置和 UI 布局。拖放选择器可以在放置文件和内容到编辑器中之前，通过按住 Shift 键来选择如何插入文件。\n\n创建配置文件时，可以选择一个配置文件模板。您可以查看设置、扩展和其他数据，并删除不想包含的项目。创建新配置文件后，对设置、扩展程序或UI所做的更改将保留在配置文件中。使用拖放选择器可以将文件和内容放置到文本编辑器中。新版本中添加了UI，可以更改插入文件的方式。内置的颜色选择器可以插入和替换颜色。在源代码控制输入中，支持代码操作和快速修复。可以将视频拖放到Markdown文件中来插入视频。可以将图像文件拖放到笔记本中以创建附件。还可以将文件提交到Git Large File Storage中，以高效地存储大文件。",
    "id": 14512154367524278000,
    "enable": true,
    "order": 0
  }
]
```