from io import BytesIO
from lxml import etree

class Page():
    def __init__(self, content):
        parser = etree.HTMLParser()
        self.html = etree.parse(BytesIO(content), parser=parser)

        self.links = []
        self.divs = []
        self.paragraphs = []
        self.words = []
        self.files = []
        self.images = []
        self.language = ""


    def get_links(self):
        self.links = []
        for link in self.html.findall('//a'):
            self.links.append(link)
        return self.links

    def get_divs(self):
        self.divs = []
        for div in self.html.findall('//div'):
            self.divs.append(div)
        return self.divs

    def get_paragraphs(self):
        self.paragraphs = []
        for paragraph in self.html.findall('//p'):
            self.paragraphs.append(paragraph)
        return self.paragraphs

    def get_words(self):
        # Use content of paragraphs and links and count words by splitting at " "
        self.words = []
        paragraphs = self.get_paragraphs()
        links = self.get_links()

        self.words = []

        for paragraph in paragraphs:
            if paragraph.text:
                temp_words = paragraph.text.split(" ")
                for word in temp_words:
                    self.words.append(word)

        for link in links:
            if link.text:
                temp_words = link.text.split(" ")
                for word in temp_words:
                    self.words.append(word)

        return self.words


    # def get_info(self):
    #     return {
    #             "date": self.date,
    #             "title": f"[on {self.color}]{self.title}[/on {self.color}]",
    #             "color": self.color,
    #             "id": self.id
    #             }
