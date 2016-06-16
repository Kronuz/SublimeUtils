import bisect

import sublime
import sublime_plugin


def _find_closest_scope(view, scope, target, max_indent=None):
    matches = view.find_by_selector(scope)
    closest_insrt = bisect.bisect_left(matches, target)
    indent = 0
    while closest_insrt > 0:
        closest_insrt -= 1
        target = matches[closest_insrt]
        line = view.substr(view.full_line(target))
        indent = len(line) - len(line.lstrip())
        if max_indent is None or indent < max_indent:
            break
    if max_indent is not None and indent >= max_indent:
        return '', 0
    return view.substr(target), indent


class SuperComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations='some'):
        if prefix and prefix[0] == 's' and 'source.python' in view.scope_name(locations[0]):
            target = sublime.Region(locations[0], locations[0])

            fn_name, fn_indent = _find_closest_scope(
                view, 'entity.name.function.python', target)

            cls_name, _ = _find_closest_scope(
                view, 'entity.name.type.class.python', target, fn_indent)

            if not cls_name:
                return []

            args, _ = _find_closest_scope(
                view, 'meta.function.parameters.python', target)

            args = args[1:-1]

            all_args = [a.strip() for a in args.split(',')]
            self_name = all_args[0]

            other_args = []
            for arg in all_args[1:]:
                arg, _, val = arg.partition('=')
                other_args.append('%s=%s' % (arg, arg) if val else arg)
            other_args = ', '.join(other_args)

            return [(
                'super(%s, %s)' % (cls_name, self_name),
                'super(%s, %s).%s(${1:%s})' % (cls_name, self_name, fn_name, other_args),
            )]
