# Octopus Energy technical challenge

Personal repo to practice interview code challenges

## Quick start

Install the dependencies

    poetry install

### Create superuser

To create a superuser account, use this command:

    poetry run python manage.py createsuperuser

### Running tests

    pytest

## Requirements of the challenge

This document describes a technical challenge that forms part of the Octopus Energy (OE) recruitment process for back-end engineers.
It should take around 3-4 hours. If the project isn’t complete by then, please ensure you leave a list "what you didn't have time to complete" so when the team assesses it, they have more context.

### Background

OE needs to process so-called “flow” files in order to communicate with the energy industry. These are pipe-delimited text files that are sent to us via sFTP. Our systems then import each file into our database.

There are lots of different types of flow files but, for this project, we are only concerned with the “D0010” files which contain information about meter readings.

We need a new service that can import these files and allow their information to be browsed via the web by support staff. For this challenge, files will be imported via the command-line but, later on, a REST interface could be added to allow files to be uploaded via the web.

Some relevant industry terminology:

- **Meter point** - this is the abstract notion of a point of electricity consumption within a property. It is identified by a so-called MPAN. It’s not the same as a physical meter: for instance, a property could replace their analogue meter with a smart-meter but their meter point (and MPAN) will not have changed.
- **Meter** - a physical device installed in someone’s house for measuring electricity consumption. They normally have a serial number. A meter can record different types of electricity consumption using different “registers” (for example, meters in economy7 households have two registers to record day- and night consumption separately; meters in non-economy7 households normally only have one register).
- **Reading** - a decimal value that records the cumulative electricity consumption at a point in time.

### Requirements

#### Deliverable

After the allotted time, a gzipped tarball should be emailed back to talent@octopus.energy or to the person who sent you this challenge. Please make the name of the tarball include your name. This tarball should contain:

- A Django web application (see below for application requirements)
- A .git folder with the commit history for the project
- A README.md that explains how to install and use the project. Include your name somewhere in the README

The project should work on macOS or Linux and run **without Docker**.

Feel free to document any assumptions made, or ideas for improving the project.

Don’t upload the project to a public Github/Bitbucket repo (as this might offer an unfair advantage to future candidates if they stumble across it).

#### Application requirements

The application should be a Django project that runs on Python 3.10 or above.

It should have a management command that can be called with the path to a D0010 file (or files). The relevant data for each meter-point should be extracted and stored in a local database. The specification for these files is included below.

It should provide a version of the Django admin site that allows a user to search for the reading values and dates associated with either:

- An MPAN
- A meter serial number

It should also be possible to see the filename of the flow file that the reading came in.

There should be a test suite and instructions on how to run the tests.

#### Application notes

Use a Postgres or SQLite database. If using SQLite, don’t commit the SQLite database file to source control.

The models and database schema are up to you. Don’t worry about deployment to a remote environment - concentrate on ensuring the project works locally.

#### Flow file specification

The specification of the D0010 (and the other flow files) is publicly available on the Electralink website: [https://www.electralink.co.uk/dtc-catalogue/](https://www.electralink.co.uk/dtc-catalogue/)

In order to see the D0010 specification, please go to the "View Flows" tab and then search for the D0010 flow:

For information on each item's validation, click ‘View Items’ and search for the JXXXX number found in the schema.

Warning: the structure of the documentation is a little hard to understand, we’re not looking for perfection but the ability to understand and solve realistic problems.

A sample D0010 file can be found here:
[https://gist.github.com/codeinthehole/de956088bab2a9168c7647fdf1be7cc5](https://gist.github.com/codeinthehole/de956088bab2a9168c7647fdf1be7cc5)

### Success criteria

When reviewing your submission, we’ll be considering these aspects:

- Correctness - does it meet the requirements? (i.e. can we follow your instructions to set up the project, import a file and see some data in the admin)

- Maintainability - for example, how easy would it be for another developer to take over the project and start adding features
- Robustness - are errors handled gracefully?
