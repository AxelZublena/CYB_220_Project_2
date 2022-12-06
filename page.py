from io import BytesIO
from lxml import etree

class Page():
    """
    Object with methods to store a webpage's content and static about it.    
    """

    def __init__(self, content, elapsed_time):
        """
        Initialize a Page with the returned content of an HTTP GET request
        """
        parser = etree.HTMLParser()
        self.html = etree.parse(BytesIO(content), parser=parser)

        self.links = []
        self.divs = []
        self.paragraphs = []
        self.words = []
        self.files = []
        self.images = []
        self.elapsed_time = elapsed_time.total_seconds()

    def get_elapsed_time(self):
        """Returns the time the server to reply"""
        return f"{self.elapsed_time}s" 

    def get_links(self):
        """Returns the <a>s found in the page"""
        self.links = []
        for link in self.html.findall('//a'):
            self.links.append(link)
        return self.links

    def get_formated_links(self):
        """Returns the formated version of the links found in the page"""
        links = self.get_links()
        formatted_links = []
        for link in links:
            formatted_links.append(f"{link.get('href')} -> {link.text}")
        return formatted_links

    def get_divs(self):
        """Returns the <div>s found in the page"""
        self.divs = []
        for div in self.html.findall('//div'):
            self.divs.append(div)
        return self.divs

    def get_paragraphs(self):
        """Returns the <p>s found in the page"""
        self.paragraphs = []
        for paragraph in self.html.findall('//p'):
            self.paragraphs.append(paragraph)
        return self.paragraphs

    def get_images(self):
        """Returns the <img>s found in the page"""
        self.images= []
        for image in self.html.findall('//img'):
            self.images.append(image.attrib['src'])
        return self.images

    def get_words(self):
        """
        Returns the words found in the page.
        Achieves this by using the content of paragraphs
        and links and count words by splitting at " "
        """
        self.words = []
        paragraphs = self.get_paragraphs()
        links = self.get_links()

        self.words = []

        # Paragraph tags
        for paragraph in paragraphs:
            if paragraph.text:
                temp_words = paragraph.text.split(" ")
                for word in temp_words:
                    self.words.append(word)

        # Links
        for link in links:
            if link.text:
                temp_words = link.text.split(" ")
                for word in temp_words:
                    self.words.append(word)

        return self.words

    def get_linked_files(self):
        """
        Returns the paragraphs found in the page
        Achieves this by extracting <link>, <img> and <a src=""> tags
        """
        self.files = []
        # Link tags
        for file in self.html.findall('//link'):
            self.files.append(file.attrib['href'])
        # Image tags
        for image in self.get_images():
            self.files.append(image)
        return self.files

