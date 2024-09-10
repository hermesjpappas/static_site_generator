class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_string = ""
        if self.props != None:
            for prop in self.props:
                props_string += " " + prop + '="' + self.props[prop] + '"'
        return props_string

    def __repr__(self):
        return f"{self.tag}: {self.value} - props: {self.props_to_html()} - children: {self.children}"
