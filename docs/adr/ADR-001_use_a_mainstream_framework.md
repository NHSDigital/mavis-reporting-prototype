# ADR-001: Use a mainstream framework

**Date:** 2025-06-19
**Status:** Proposed

---

- [ADR-001: Use a mainstream framework](#adr-001-use-a-mainstream-framework)
  - [Context](#context)
  - [Decision](#decision)
    - [Options](#options)
      - [Options 1: Flask](#options-1-flask)
      - [Options 2: Django](#options-2-django)
    - [Outcome](#outcome)
    - [Rationale](#rationale)
  - [Consequences](#consequences)
  - [Compliance](#compliance)
  - [Notes](#notes)
  - [Actions](#actions)
  - [Tags](#tags)

## Context

Previous [ADR-00011 on the main Mavis service](https://github.com/nhsuk/manage-vaccinations-in-schools/pull/3780) made the decision to develop this component in Python, on the grounds that [it is a 'MAINSTREAM' language on the NHS Digital Tech Radar](https://github.com/NHSDigital/tech-radar/blob/main/site/data/data.js#L150). Given that decision, we must now decide which framework to use.

## Decision

### Options

#### Options 1: Flask

[Flask homepage](https://flask.palletsprojects.com/)

- Pros
  - Lightweight and simple - comparable to Ruby's [Sinatra](https://sinatrarb.com/) in approach
  - Already [MAINSTREAM](https://github.com/NHSDigital/tech-radar/blob/main/site/data/data.js#L171) on the Tech Radar
  - Easy to get started quickly

- Cons
  - Uses Jinja2 for templating language, meaning the NHS Design System is not immediately compatible
  - Does not provide as many features as Django (e.g. no ORM layer)

#### Options 2: Django

[Django homepage](https://www.djangoproject.com/)

- Pros
  - Fully-featured framework comparable to [Rails](https://rubyonrails.org/) in functionality
  - Provides more features out-of-the-box then Flask
  - Some other teams are already working in Django - opportunity to share libraries, knowledge & approaches
- Cons
  - Not mentioned in the Tech Radar at the time of writing
  - Uses its own template language by default

### Outcome

The decision is to proceed with Flask.

### Rationale

Flask is the only Python framework even mentioned on the Tech Radar at the time of writing, therefore the only choice if we want to use only MAINSTREAM technologies.

Whilst there will need to be some custom integration of the NHS Design System with Jinja2, there is already a [Jinja2 port of the Design System](https://github.com/NHSDigital/nhsuk-frontend-jinja) written by another NHSDigital team, which has been notified back to the Design System maintainers with a view to keeping it regularly updated, and eventually look at rolling Jinja support back in to the main Design System.

It should also be noted that Django does support being configured to use Jinja templates, although this is not the default behaviour.

The architectural approach for this reporting component suits Flasks' "keep-it-simple" philosophy. We will be retrieving all data from the Mavis API rather than a local database, therefore we do not need an ORM.

Should the situation change in future - either Django becomes MAINSTREAM, or the reporting component grows to be more complex than a simple Flask app can reasonably support, we can revisit this decision at that point.

## Consequences

As a result of the above decision, we will:

- proceed with development using Flask
- use the existing port of the NHS Design System to Jinja2
- review the decision in 1 month, once we have done some significant development in Flask

## Compliance

Flask is the only MAINSTREAM Python framework on the Tech Radar, therefore it should not be a contentious choice

## Notes

## Actions

## Tags
