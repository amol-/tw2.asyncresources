import json
import inspect
from tw2.core.resources import JSLink as TW2JSLink
from tw2.core.resources import CSSLink as TW2CSSLink
from tw2.core.resources import JSSource as TW2JSSource

from . import axel
from . import requirejs

LOADERS = {
    'requirejs': requirejs,
    'axel': axel
}


def enable_async_resources(loader, widget):
    """
    Given a widget ad a preferred loader patches all the
    widget and children resources to be loaded with the
    given loader.
    """
    _replace_resources(loader, widget)

    child = widget
    if hasattr(child, 'child'):
        child = widget.child
        _replace_resources(loader, child)

    for c in child.children_deep():
        _replace_resources(loader, c)


def with_loader(loader):
    """
    Class decorator that patches a tw2 form or widget
    with `enable_async_resources`
    """
    def _decorator(widget):
        enable_async_resources(loader, widget)
        return widget
    return _decorator


class _AsyncResources(list):
    def __init__(self, loader):
        self.loader = loader
        self.dependencies = []
        super(_AsyncResources, self).__init__()

    def __set__(self, instance, value):
        while True:
            try:
                instance.resources.pop()
            except IndexError:
                break

        for v in value:
            instance.resources.append(v)

    @staticmethod
    def _clone_link(res, clone_type):
        if clone_type is not None:
            async_res = clone_type(modname=res.modname,
                                   filename=res.filename,
                                   no_inject=res.no_inject,
                                   whole_dir=res.whole_dir)
            if res.parent is not None:
                async_res.parent = res.parent
            if hasattr(res, 'link'):
                # According to tw2/core/resources.py:163 this is the
                # way to check if a resource has a valid link.
                async_res.link = res.link
            res = async_res

        return res

    def append(self, res):
        already_prepared = False

        if not inspect.isclass(res):
            already_prepared = True
            res = res.__class__

        if issubclass(res, TW2JSSource):
            res = self.loader.JSSource(src=res.src, dependencies=self)
        else:
            if issubclass(res, TW2JSLink):
                res = self._clone_link(res, self.loader.JSLink)
            elif issubclass(res, TW2CSSLink):
                res = self._clone_link(res, self.loader.CSSLink)
            else:
                already_prepared = False

        if already_prepared:
            res = res.req()
            res.prepare()

        return super(_AsyncResources, self).append(res)

    @property
    def js_links(self):
        return [r.link for r in self if isinstance(r, TW2JSLink)]


def _replace_resources(loader, widget):
    if not inspect.isclass(widget):
        # If we replace resources of a widget instance the _AsyncResources descriptor won't work.
        raise ValueError('It is possible to replace resources of widgets only before calling .req()')

    loader = LOADERS[loader]
    resources = _AsyncResources(loader)
    for res in widget.resources:
        resources.append(res)
    widget.resources = resources
