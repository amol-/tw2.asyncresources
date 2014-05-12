import json
from tw2.core import params as tw2pm
from tw2.core.resources import JSLink as TW2JSLink
from tw2.core.resources import CSSLink as TW2CSSLink
from tw2.core.resources import JSSource as TW2JSSource


class JSLink(TW2JSLink):
    inline_engine_name = 'genshi'
    location = 'headbottom'
    template = '<script type="text/javascript">require(["$w.link"])</script>'


class CSSLink(TW2CSSLink):
    inline_engine_name = 'genshi'
    location = 'headbottom'
    template = '''<script type="text/javascript">
(function(url) {
    var link = document.createElement("link");
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = url;
    document.getElementsByTagName("head")[0].appendChild(link);
})("$w.link");
</script>'''


class JSSource(TW2JSSource):
    dependencies = tw2pm.Param('resources required by this script')
    inline_engine_name = 'genshi'
    template = '<script type="text/javascript">require(${w.js_dependencies}, function() { $w.src })</script>'

    def prepare(self):
        super(TW2JSSource, self).prepare()
        self.js_dependencies = json.dumps(self.dependencies.js_links)