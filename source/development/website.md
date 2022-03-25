# Website

Kustosz website, available at [www.kustosz.org](https://www.kustosz.org/), is written in Markdown and built using [Hugo](https://gohugo.io/).

Website requires Hugo 0.82.1 or later and Node.js runtime. Production version of website is currently build using Node.js 16.

## Preparing development environment

Clone Github repo along with submodules:

    git clone --recurse-submodules https://github.com/KustoszApp/kustoszapp.github.io.git

Install dependencies:

    npm install

## Running current development version

Run server:

    hugo serve

Kustosz website will be available at <http://localhost:1313/>. Website refreshes automatically as you change documentation source files.
