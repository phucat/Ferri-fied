from jinja2 import Environment, FileSystemLoader
import os
import mcp


def build(gadget_directory):
    env = Environment(
        loader=FileSystemLoader([
            os.path.abspath(gadget_directory),
            os.path.abspath(os.path.join(gadget_directory, '..'))
        ]))
    template = env.get_template('template.xml')
    return template.render()


def deploy(project, branch, name, spec):
    return mcp.deploy('gadgets', {
        'project': project,
        'branch': branch,
        'name': name,
        'spec': spec
    }, "/api/%s/%s/%s/%s.xml")
