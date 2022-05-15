# Frontend

Frontend is written in JavaScript, using Vue.js and Node.js. It requires Node.js 14 or newer. We only support LTS releases of Node.js. npm package is currently build using Node.js 16.

## Preparing development environment

Clone Github repo:

    git clone https://github.com/KustoszApp/web-ui

Install dependencies:

    npm install

## Running current development version

Run server:

    npm run serve

Kustosz UI will be available at <http://localhost:8080>.

It's not very useful to run frontend without [API server running](./backend). By default, frontend will assume that backend is available at <http://127.0.0.1:8000/api/v1>. You can specify another URL by setting `VUE_APP_KUSTOSZ_BACKEND_URL` environment variable prior to running `serve` command. Note that variable needs to specify full URL, including path.

    VUE_APP_KUSTOSZ_BACKEND_URL="http://127.0.0.1:9876/api/v2" npm run serve
