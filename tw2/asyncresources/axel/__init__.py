from tw2.core import params as tw2pm
from tw2.core.resources import JSLink as TW2JSLink
from tw2.core.resources import CSSLink as TW2CSSLink
from tw2.core.resources import JSSource as TW2JSSource
import json


def _calc_axel_id(link):
    link_without_extension = link.rsplit('.', 1)[0]
    return link_without_extension.lstrip('/').replace('/', '.')


class JSLink(TW2JSLink):
    inline_engine_name = 'genshi'
    location = 'headbottom'
    template = '<script type="text/javascript">axel.register("${w.axel_id}", "${w.link}").load("${w.axel_id}")</script>'

    def prepare(self):
        super(JSLink, self).prepare()
        self.axel_id = _calc_axel_id(self.link)


class CSSLink(TW2CSSLink):
    inline_engine_name = 'genshi'
    location = 'headbottom'
    template = '<script type="text/javascript">axel.register("${w.axel_id}", "${w.link}").load("${w.axel_id}")</script>'

    def prepare(self):
        super(CSSLink, self).prepare()
        self.axel_id = _calc_axel_id(self.link)


class JSSource(TW2JSSource):
    dependencies = tw2pm.Param('resources required by this script')
    inline_engine_name = 'genshi'
    template = '<script type="text/javascript">axel.ready(${w.axel_dependencies}, function() { $w.src })</script>'

    def prepare(self):
        super(TW2JSSource, self).prepare()
        self.axel_dependencies = json.dumps([_calc_axel_id(l) for l in self.dependencies.links])