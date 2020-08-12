import pyglet.resource

# if an assets directory is above the main.py file's path
# you need to set resource directory manually
def set_resource_directory(path: str):
    pyglet.resource.path = [path]
    pyglet.resource.reindex()