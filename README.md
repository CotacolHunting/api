COTACOL API
===========

[![github-tests-badge]][github-tests]
[![github-mypy-badge]][github-mypy]
[![codecov-badge]][codecov]
[![license-badge]](LICENSE)
[![docs-badge]][docs]


The COTACOL API uses [FastAPI][fastapi].

Application dependencies
------------------------

The application uses [Pipenv][pipenv] to manage Python packages:

    $ pipenv shell
    $ pipenv install --dev

Update dependencies (and manually update `requirements.txt`):

    $ pipenv update --dev && pipenv lock -r

Running the server
------------------

    $ uvicorn cotacol.main:app

Running tests
-------------

    $ pytest --cov=cotacol

Style guide
-----------

Tab size is 4 spaces. Maximum line length is 120. You should run `black` before commiting any change.

    $ black cotacol


[codecov]: https://codecov.io/gh/cotacolhunting/cotacol-api
[codecov-badge]: https://codecov.io/gh/cotacolhunting/cotacol-api/branch/master/graph/badge.svg
[docs]: https://api.cotacol.cc/docs/
[docs-badge]: https://img.shields.io/badge/docs-api.cotacol.cc-blue.svg
[github-mypy]: https://github.com/cotacolhunting/cotacol-api/actions?query=workflow%3A%22mypy%22
[github-mypy-badge]: https://github.com/cotacolhunting/cotacol-api/workflows/mypy/badge.svg
[github-tests]: https://github.com/cotacolhunting/cotacol-api/actions?query=workflow%3A%22tests%22
[github-tests-badge]: https://github.com/cotacolhunting/cotacol-api/workflows/tests/badge.svg
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg

[fastapi]: https://fastapi.tiangolo.com/
[pipenv]: https://docs.pipenv.org/#install-pipenv-today
