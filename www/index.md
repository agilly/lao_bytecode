## Langing page of the website

This is a test.

[Find out abou the project](about)



### To configure your website:

- The required file to run a basic website are included in the repository. We use Jekyll to turn markdown files into html that will be automatically updated on the website. The component responsible for this is a GitHub action, that is specified in the folder .github/workflows. There is no need to update this file.

- In the settings of your repository, go the section "Pages", and select GitHub Actions to indicate that this is the way you'd like the webpage to be generated.

- Each time you update the repository, it will regenerate the content. The address of the website will be:

```
https://technology-for-the-poorest-billion.github.io/[your repo name here]
```

- index.md is the root of your website. To link another page from here, located within the www folder, use the following syntax:

```
This is a [link](linkedpage.md) to interesting content.
```

Which results in:

This is a [link](linkedpage.md) to interesting content.
