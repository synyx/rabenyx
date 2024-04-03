# Rabenyx web application

An expert web application that tries to show things that Nextclouds Poll App
hides due to performance issues. It also performs some tasks in the background
that otherwise needed to be done manually. The web app is based on the
[microframework Flask][1].

## Running the app on your local machine

1. Install Flask
    ````bash
    pip install -U Flask
    ````
2. The configuration for Rabenyx is based on environment variables. See
[the main documentation](../README.md#environment-variables) for
details. If you want to run Flask from the projects root directory, also
set `FLASK_APP=webapp/app.py` as environment variable.
3. Run
    ````bash
    flask run
    ````
4. Open http://127.0.0.1:5000/ in your browser and enjoy Rabenyx.

## How to deploy

To initiate the deployment of a new version of the webapp you need to push a Git
tag with a new version.

````
git tag -a x.y.z -m '<Some nice message or none.>'
git push --tags
````

The deployment only applies the [deployment configuration](../deploy/rabenyx.yaml).
For further details see [GitLabs pipeline configuration](../.gitlab-ci.yml).

[1]: https://github.com/pallets/flask/
