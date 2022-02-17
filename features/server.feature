Feature: Check service functionality

    Scenario Outline: Expect process <process> to run
        Given a testserver container
         When I check the process "<process>"
         Then the process arguments are "<args>"

        Examples:
        | process   | args                                |
        | gunicorn  | wsgi:app --bind=0.0.0.0:8080        |

    Scenario: There should be no outdated modules
        Given a testserver container
         When I search the installed modules
         Then I should find no outdated modules

    Scenario Outline: Expect python module <module> to be installed
        Given a sse_mariadb container
         When I check the module "<module>"
         Then the module is installed

        Examples: pip modules packages
            | module          |
            | Flask           |
            | Flask-Bootstrap |
            | gunicorn        |
            | Jinja2          |
            | PyYAML          |
