Feature: check container vality

    Scenario: Check container availability
        Given  a testserver container
         When  the testserver container is running
         Then  we can see a docker signature

    Scenario Outline: Expect directory <path> exists
        Given  a testserver container
         When  I check the directory <path>
         Then  the directory is present

        Examples: directories
            | path                       |
            | /home/web                  |
            | /home/web/app              |
            | /home/web/app/templates    |
            | /home/web/log              |

    Scenario Outline: Expect file <path> to exists
        Given a testserver container
        When I check the file <path>
        Then the file is present

        Examples: files
            | path                                            |
            | /home/web/run_gunicorn.sh                       |
            | /home/web/wsgi.py                               |
            | /home/web/app/config.py                         |
            | /home/web/app/routes.py                         |
            | /home/web/app/templates/base.html               |
            | /home/web/app/templates/index.html              |

    Scenario Outline: Expect package <pkg> to be installed
        Given a testserver container
        When I check the package <pkg>
        Then the package is installed

        Examples: alpine packages
            | pkg            |
            | python3        |
            | py3-pip        |