import testinfra
import os

from behave import *
from compare import expect
from hamcrest import *

container = testinfra.get_host("docker://%s" % os.environ['IMAGE'])
host = testinfra.get_host("local://")

@given(u'a {container_name} container')
def test_container_name(context, container_name):
    # assert container_name == os.environ['IMAGE']
    containers = host.docker.get_containers(name=container_name)
    assert_that(len(containers), greater_than_or_equal_to(1))

@when('the {container_name} container is running')
def test_docker_container(context, container_name):
    server = host.docker(container_name)
    assert server.is_running

@then(u'we can see a docker signature')
def test_docker_env(context):
    expect(str(host.file('/.dockerenv').exists)).to_be_truthy()


@when('I check the package {package}')
def package(context, package):
    context.package = container.package(package)

@then('the package is {state}')
def package_state(context, state):
    if state in ('installed', 'present'):
        assert context.package.is_installed
    else:
        assert not context.package.is_installed


@step('I check the file {path}')
@step('I check the directory {path}')
def read(context, path):
    context.path = container.file(path)

@step('the {filetype} is {existance}')
def check_file(context, filetype, existance):
    if existance == 'present':
        assert context.path.exists
        if filetype == 'file':
            assert context.path.is_file
        elif filetype == 'directory':
            assert context.path.is_directory
        elif filetype == 'symlink':
            assert context.path.is_symlink
        elif filetype == 'socket':
            assert context.path.is_socket
        else:
            raise NotImplementedError('%s not implemented' % filetype)
    elif existance == 'absent':
        assert not context.path.exists
    elif existance == 'executable':
        mode = context.path.mode
        assert mode & stat.S_IXUSR
    else:
        raise ValueError('%s is not supported' % existance)