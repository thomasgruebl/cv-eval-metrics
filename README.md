# cv-eval-metrics
Collection of my custom implementations of common computer vision evaluation metrics

![GitHub last commit](https://img.shields.io/github/last-commit/thomasgruebl/cv-eval-metrics?style=plastic) ![GitHub](https://img.shields.io/github/license/thomasgruebl/cv-eval-metrics?style=plastic) <a style="text-decoration: none" href="https://github.com/thomasgruebl/cv-eval-metrics/stargazers">
<img src="https://img.shields.io/github/stars/thomasgruebl/cv-eval-metrics.svg?style=plastic" alt="Stars">
</a>
<a style="text-decoration: none" href="https://github.com/thomasgruebl/cv-eval-metrics/fork">
<img src="https://img.shields.io/github/forks/thomasgruebl/cv-eval-metrics.svg?style=plastic" alt="Forks">
</a>
![Github All Releases](https://img.shields.io/github/downloads/thomasgruebl/cv-eval-metrics/total.svg?style=plastic)
<a style="text-decoration: none" href="https://github.com/thomasgruebl/cv-eval-metrics/issues">
<img src="https://img.shields.io/github/issues/thomasgruebl/cv-eval-metrics.svg?style=plastic" alt="Issues">
</a>

### Requirements

- Python 3.10+
- opencv-python>=4.6.0.66 
- numpy>=1.23.5

### Supported Metrics

| Metric | Description                                                                                                     |
|--------|-----------------------------------------------------------------------------------------------------------------|
| MCC    | Matthews Correlation Coefficient. Takes two thresholded, greyscale openCV images as input and computes the MCC. |
| ...    | More methods coming soon...                                                                                     |

### Contributing

1. Fork the repository
2. Create a new feature branch (`git checkout -b my-feature-branch-name`)
3. Commit your new changes (`git commit -m 'commit message' <changed-file>`)
4. Push changes to the branch (`git push origin my-feature-branch-name`)
5. Create a Pull Request
