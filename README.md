# project_index

## What is project_index?
Project index is a small attempt to gather all the information one needs in
order to find instances of a project, common tasks and anything involved in
his workflow.

## Entities

### Projects
Projects can be added, along with their git repos, docs, etc.

#### Dependencies
Project index will automatically discover `requirements.txt` file from your
repository (if there is access), else you can upload a requirements.txt file.
But still it will try to access your repo first.

### Hosts
Hosts, where Projects and Cronjobs belong, can be added. Installed packages
can also be recorded.

### Cronjobs
Cronjobs, used for the needs of the Projects, can be added.
Useful information of each cronjob is also gathered
(command that initiates the cronjob, running period of cronjob, etc.).

### Databases
Databases, used for the needs of the instances of the Projects,
can be added. Useful information of each database is also gathered
(host, username, password, port, engine).

### Notes
Notes can help one to avoid doing the same mistake twice.

### Tags
Tags are used in order to find topic related projects/notes.

## Features

### Deployment status information
A new concept has been introduced named "Deployment Information"

You can now store `DeploymentInfo` objects which associate an `Instance`
with a commit hash (and other information). This allows tracking the 
current state of the `Instance`.  In addition, Project index can
communicate with a repository hosting service via its API
 (currently only `Phabricator`) to retrieve deployment information, such as:

1) Undeployed commits in `master` branch
2) Commits included in each deployment

The information above is presented in the UI in the project's page, where
the list of instances is displayed.

To turn this feature on, simply add `DEPLOYMENT_FEATURES_ENABLED = True`
in your `local_settings.py` and provide `PHABRICATOR_API_TOKEN = <your-token>`

### MoinMoin Pages Generator
Offers support for Wiki sites based on MoinMoin syntax. Pages for Database,
Cronjob, Host, Project entities can be produced, from the details page of each
entity. Clicking Get MoinMoin, redirects to another page, where a MoinMoin
syntaxed page has been generated. From that point, user can be redirected to
wiki site, to add that page.

#### Wiki Url Tree and Categorisation
In order to use MoinMoin feature, user must define a WIKI dictionary to his
`local_settings.py` file. This dictionary must be of the following format:

	WIKI = {
	    'url': 'http://wiki.wiki_example.com',
	    'parent_dir': '/parent_directory',
	    'databases_dir': '/databases_directory/',
	    'hosts_dir': '/hosts_directory/',
	    'cronjobs_dir': '/cronjobs_directory/',
	    'projects_dir': '/projects_directory/',
	    'project_category': 'MyProjects',
	    'host_category': 'MyHosts',
	    'cronjob_category': 'MyCronjobs',
	    'database_category': 'MyDatabases'
	}

Above dictionary helps project_index build links between related entinties'
pages and also categorise MoinMoin Pages for Wiki indexation needs.

##### Example of usage of WIKI
The above dictionary produces the following urls:

	# for database entity with name db_name
	http://wiki.wiki_example.com/parent_directory/databases_directory/db_name

	# for host entity with name host_name
	http://wiki.wiki_example.com/parent_directory/hosts_directory/host_name

	# for cronjob entity with name cronjob_name
	http://wiki.wiki_example.com/parent_directory/cronjobs_directory/cronjob_name

	# for project entity with name project_name
	http://wiki.wiki_example.com/parent_directory/projects_directory/project_name

It also produces the following categories:

	Category-MyProjects
	Category-MyHosts
	Category-MyCronjobs
	Category-MyDatabases

## Testing

To run the tests, you need to install the test requirements. To do so:

    pip install requirements-dev.txt

Then, to run all the tests:

    pytest

To run & produce detailed HTML coverage reports:
    
    pytest --cov='.' --cov-config=.coveragerc --cov-report=html:cov_html
