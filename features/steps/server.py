import testinfra
import os

from behave import *
from hamcrest import *
from compare import expect

container = testinfra.get_host("docker://%s" % os.environ['IMAGE'])
# host = testinfra.get_host("local://")

@When('I check the process "{proc}"')
@When("I check the process '{proc}'")
def check_proc(context, proc):
    context.workers = container.process.filter(comm=proc)

@Then('the process arguments are "{args}"')
@Then("the process arguments are '{args}'")
def check_proc(context, args):
    expect(context.workers[0].args).to_contain(args)


@When('I check the module "{module}"')
@When("I check the module '{module}'")
def module_check(context, module):
    modules = container.pip_package.get_packages(pip_path='/usr/bin/pip')
    context.module = modules.get(module)
    # context.modules = container.pip_package.get_packages(pip_path='/usr/bin/pip')

@Then('the module is {state}')
def module_state(context, state):
    if state in ('installed', 'present'):
        # modules = json.load(context.modules)
        assert_that(context.module, has_key('version'))


@when('I search the installed modules')
def outdated_modules(context):
    context.outdated_modules = container.pip_package.check(pip_path='/usr/bin/pip')

@then('I should find no outdated modules')
def number_outdated_modules(context):
    assert context.outdated_modules.rc == 0