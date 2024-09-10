from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value == None:
            raise ValueError
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
      if(self.tag == other.tag and self.value == other.value and self.props == other.props):
        return True
      else:
        return False

    def to_html(self):
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
