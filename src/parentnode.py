from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        ):
            return True
        else:
            return False

    def to_html(self):
        if self.tag == None:
            raise ValueError
        if self.children == None or len(self.children) == 0:
            raise ValueError("No children given")
        accumulator = ""
        props_string = ""
        if self.props != None:
            props_string = self.props_to_html()
        for child in self.children:
            accumulator += child.to_html()
        return f"<{self.tag}{props_string}>{accumulator}</{self.tag}>"
