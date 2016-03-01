# Contributing

## For Crawler and Classifier

We are following [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). To make sure that we adhere to this style guide, we use [YAPF](https://github.com/google/yapf) to reformat our Python codes. 

```Shell
# Install YAPF using pip
pip install yapf

# Run the formatter
# The configuration file is located at ./.style.yapf
yapf -r -i crawler/
```

## For UI

We are following [Google Javascript Style Guide](https://google.github.io/styleguide/javascriptguide.xml) for Javascript files under the directory `./UI/js`. We use [ESLint](http://eslint.org/) to lint our codes. To use ESLint, we first install the tool by using the following commands:

```Shell
$ cd UI
$ npm install -g eslint eslint-config-defaults
```

Next, we run the tool using the following command:

```Shell
$ eslint js/custom.js
```

Alternatively, if you are using Sublime Text 3, you can install [SublimeLinter](http://www.sublimelinter.com/en/latest/) and [SublimeLinter-eslint](https://github.com/roadhump/SublimeLinter-eslint). 
