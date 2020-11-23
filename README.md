[![Build Status](https://travis-ci.com/dariober/simulate-parasite-infection.svg?branch=main)](https://travis-ci.com/dariober/simulate-parasite-infection)
[![codecov](https://codecov.io/gh/dariober/simulate-parasite-infection/branch/main/graph/badge.svg)](https://codecov.io/gh/dariober/simulate-parasite-infection)
[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/dariober/simulate-parasite-infection)

<!-- vim-markdown-toc GFM -->

* [Start server locally](#start-server-locally)
* [Run tests](#run-tests)
* [Deploy public](#deploy-public)
    * [Installation](#installation)
    * [Start service](#start-service)
    * [Access](#access)

<!-- vim-markdown-toc -->

We want to simulate the infection of Plasmodium parasites across generations.
Parasites are either resistant or susceptible to a drug.

Start server locally
====================

```
library(shiny)
options(browser= '/usr/bin/google-chrome')
runApp('shiny') # <- Dir containing app.R
```

Run tests
=========

See also `.travis.yml`

```
python3 -m unittest tests.host_test
Rscript tests/testthat.R
```

Deploy public
=============

Installation
------------

For Ubuntu, from https://rstudio.com/products/shiny/download-server/ubuntu/

```
sudo apt-get install r-base
sudo su - \
    -c "R -e \"install.packages('shiny', repos='https://cran.rstudio.com/')\""
sudo apt-get install gdebi-core
wget https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.15.953-amd64.deb
sudo gdebi shiny-server-1.5.15.953-amd64.deb
```

Install R packages as per `requirements.txt`:

```
sudo su -
R
# Assuming you are happy with latest versions
install.packages(c('data.table', 'ggplot2', ...), repos= 'https://cran.rstudio.com/')
```

Copy the application source code to the dir in `site_dir`, file `/etc/shiny-server/shiny-server.conf`:

```
cp -r ~/git_repos/simulate_infection /srv/shiny-server/
```

Start service
-------------

```
sudo systemctl restart shiny-server
```

Access
------

Access application at `http://<ip-address>:<port-no>/<shiny-source-dir>/`

E.g.: [http://192.168.1.8:3838/tmp_simulate_infection/shiny/]

The port is the one given in `/etc/shiny-server/shiny-server.conf`
