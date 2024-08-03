from lxml import etree

NSPACE = {
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wfw': 'http://wellformedweb.org/CommentAPI/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'wp': 'http://wordpress.org/export/1.2/'
}


def parse_xml(path):
    tree = etree.parse(path)
    root = tree.getroot()

    # todo узнать только ли первый айтем нужен
    first_item = root.find('.//item', namespaces=NSPACE)

    title = first_item.find('title').text
    link = first_item.find('link').text
    pubDate = first_item.find('pubDate').text
    creator = first_item.find('dc:creator', namespaces=NSPACE).text
    guid = first_item.find('guid').text
    # description = ...
    content = first_item.find('content:encoded', namespaces=NSPACE).text
    excerpt = (first_item.find('excerpt:encoded',
                               namespaces=NSPACE)
               .text) if first_item.find('excerpt:encoded', namespaces=NSPACE) is not None else ""
    post_id = first_item.find('wp:post_id', namespaces=NSPACE).text
    post_date = first_item.find('wp:post_date', namespaces=NSPACE).text
    post_date_gmt = first_item.find('wp:post_date_gmt', namespaces=NSPACE).text
    # post_modified = ...
    # post_modified_gmt = ...
    # comment_status = first_item.find('wp:comment_status', namespaces=NSPACE).text
    # ping_status = first_item.find('wp:ping_status', namespaces=NSPACE).text
    post_name = first_item.find('wp:post_name', namespaces=NSPACE).text
    status = first_item.find('wp:status', namespaces=NSPACE).text
    post_parent = first_item.find('wp:post_parent', namespaces=NSPACE).text
    menu_order = first_item.find('wp:menu_order', namespaces=NSPACE).text
    post_type = first_item.find('wp:post_type', namespaces=NSPACE).text
    # post_password = first_item.find('wp:post_password', namespaces=NSPACE).text
    is_sticky = first_item.find('wp:is_sticky', namespaces=NSPACE).text
    # is_sticky для чего?
    # дальше идет категория
    # todo долелать получение ее
    # todo система категорий на разных языках. тут мы ее просто получаем
    category_element = first_item.find('category[@domain="category"]')
    if category_element is not None:
        category_nicename = category_element.get('nicename')
    else:
        category_nicename = None

    return {
        'title': title,
        'link': link,
        'pubDate': pubDate,
        'creator': creator,
        'guid': guid,
        'content': content,
        'excerpt': excerpt,
        'post_id': post_id,
        'post_date': post_date,
        'post_date_gmt': post_date_gmt,
        'post_name': post_name,
        'status': status,
        'post_parent': post_parent,
        'menu_order': menu_order,
        'post_type': post_type,
        'is_sticky': is_sticky,
        'category': category_nicename,
    }
