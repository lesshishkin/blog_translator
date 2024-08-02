from lxml import etree


def parse_xml(path):
    # Загрузка и парсинг XML файла
    tree = etree.parse(path)
    root = tree.getroot()

    # Нахождение первого элемента <item>
    namespace = {
        'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wfw': 'http://wellformedweb.org/CommentAPI/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'wp': 'http://wordpress.org/export/1.2/'
    }

    first_item = root.find('.//item', namespaces=namespace)

    # Извлечение данных из первого элемента <item>
    title = first_item.find('title').text
    link = first_item.find('link').text
    pub_date = first_item.find('pubDate').text
    creator = first_item.find('dc:creator', namespaces=namespace).text
    guid = first_item.find('guid').text
    content = first_item.find('content:encoded', namespaces=namespace).text
    excerpt = first_item.find('excerpt:encoded', namespaces=namespace).text if first_item.find('excerpt:encoded', namespaces=namespace) is not None else ""
    post_id = first_item.find('wp:post_id', namespaces=namespace).text
    post_date = first_item.find('wp:post_date', namespaces=namespace).text
    post_date_gmt = first_item.find('wp:post_date_gmt', namespaces=namespace).text
    comment_status = first_item.find('wp:comment_status', namespaces=namespace).text
    ping_status = first_item.find('wp:ping_status', namespaces=namespace).text
    post_name = first_item.find('wp:post_name', namespaces=namespace).text
    status = first_item.find('wp:status', namespaces=namespace).text
    post_parent = first_item.find('wp:post_parent', namespaces=namespace).text
    menu_order = first_item.find('wp:menu_order', namespaces=namespace).text
    post_type = first_item.find('wp:post_type', namespaces=namespace).text
    post_password = first_item.find('wp:post_password', namespaces=namespace).text
    is_sticky = first_item.find('wp:is_sticky', namespaces=namespace).text

    # Вывод извлеченных данных
    print(f"Title: {title}")
    print(f"Link: {link}")
    print(f"Publication Date: {pub_date}")
    print(f"Creator: {creator}")
    print(f"GUID: {guid}")
    print(f"Content: {content}")
    print(f"Excerpt: {excerpt}")
    print(f"Post ID: {post_id}")
    print(f"Post Date: {post_date}")
    print(f"Post Date GMT: {post_date_gmt}")
    print(f"Comment Status: {comment_status}")
    print(f"Ping Status: {ping_status}")
    print(f"Post Name: {post_name}")
    print(f"Status: {status}")
    print(f"Post Parent: {post_parent}")
    print(f"Menu Order: {menu_order}")
    print(f"Post Type: {post_type}")
    print(f"Post Password: {post_password}")
    print(f"Is Sticky: {is_sticky}")
