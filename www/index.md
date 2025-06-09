---
title: Home
---
## Our collaborator MakerBox
Makerbox Lao is a collaborative space that fosters the development of technology-driven solutions to various local challenges in Laos. Given that agriculture is a crucial part of Laos' economy that employs around 70% of the population(ASEAN Briefing, 2025), MakerBox is currently building a system to send actionable messages - such as irrigation alerts - to farmers via digital displays in rural areas.


## The Problem
The problem with rendering Lao text on d
### To configure your website:

- The required files to run a basic website are included in the repository. We use here Jekyll to turn markdown files into html that will be automatically updated on the website. The component responsible for this is a GitHub action, which is specified in the folder .github/workflows. There is no need to change this file. However:

- In the settings of your repository, go the section "Pages", and select GitHub Actions in the drop down menu to indicate that this is the way you'd like the webpage to be generated.

- Each time you update the markdown files in the www folder of the repository, it will regenerate the web content. The address of the website will be:

```
https://technology-for-the-poorest-billion.github.io/[your repo name here]
```

- index.md is the root of your website. To link another page from here, located within the www folder, use the following syntax:

```
This is a [link](linkedpage.md) to interesting content.
```

Which results in:

This is a [link](linkedpage.md) to interesting content.

- Pay attention to the header of the markdown files in this section. It contains a title section that you will need to reproduce for each page to render them properly.


