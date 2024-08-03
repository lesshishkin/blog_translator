from lxml import etree
from lxml.etree import QName


def create_wxr(posts, output_path):
    # Создаем корневой элемент
    rss = etree.Element("rss", version="2.0", nsmap={
        None: "http://purl.org/rss/1.0/modules/content/",
        "excerpt": "http://wordpress.org/export/1.2/excerpt/",
        "wfw": "http://wellformedweb.org/CommentAPI/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "wp": "http://wordpress.org/export/1.2/"
    })

    # Создаем канал
    channel = etree.SubElement(rss, "channel")
    etree.SubElement(channel, "title").text = "Your Blog Title"
    etree.SubElement(channel, "link").text = "http://yourblog.com"
    etree.SubElement(channel, "description").text = "Description of your blog"
    etree.SubElement(channel, "language").text = "en-US"
    etree.SubElement(channel, QName("http://wordpress.org/export/1.2/", "wxr_version")).text = "1.2"

    # Добавляем статьи
    for post in posts:
        item = etree.SubElement(channel, "item")
        etree.SubElement(item, "title").text = post["title"]
        etree.SubElement(item, "link").text = post["link"]
        etree.SubElement(item, "pubDate").text = post["pubDate"]
        etree.SubElement(item, QName("http://purl.org/dc/elements/1.1/", "creator")).text = post["author"]
        content = etree.SubElement(item, QName("http://purl.org/rss/1.0/modules/content/", "encoded"))
        content.text = etree.CDATA(post["content"])
        excerpt = etree.SubElement(item, QName("http://wordpress.org/export/1.2/excerpt/", "encoded"))
        excerpt.text = etree.CDATA(post.get("excerpt", ""))
        etree.SubElement(item, QName("http://wordpress.org/export/1.2/", "post_id")).text = str(post["id"])
        etree.SubElement(item, QName("http://wordpress.org/export/1.2/", "post_date")).text = post["post_date"]
        etree.SubElement(item, QName("http://wordpress.org/export/1.2/", "post_date_gmt")).text = post["post_date_gmt"]
        etree.SubElement(item, QName("http://wordpress.org/export/1.2/", "comment_status")).text = post.get("comment_status", "open")
        etree.SubElement(item, QName("http://wordpress.org/export/1.2/", "ping_status")).text = post.get("ping_status", "open")
        etree.SubElement(item, QName("http://wordpress.org/export/1.2/", "status")).text = post["status"]
        etree.SubElement(item, QName("http://wordpress.org/export/1.2/", "post_type")).text = post.get("post_type", "post")

    # Сохраняем XML в файл
    tree = etree.ElementTree(rss)
    with open("export.xml", "wb") as f:
        tree.write(f, encoding="UTF-8", xml_declaration=True, pretty_print=True)
