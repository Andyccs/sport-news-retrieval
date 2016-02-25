# Contributing

We are following [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). To make sure that we adhere to this style guide, we use [YAPF](https://github.com/google/yapf) to reformat our Python codes. 

```Shell
# Install YAPF using pip
pip install yapf

# Run the formatter
# The configuration file is located at ./.style.yapf
yapf -r -i crawler/
```