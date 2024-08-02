import xml.etree.ElementTree as ET
import lxml

# Определение пространств имен
namespaces = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
    'wfw': 'http://wellformedweb.org/CommentAPI/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'wp': 'http://wordpress.org/export/1.2/'
}

# Открытие и парсинг XML файла
tree = ET.parse('getitcom.WordPress.2024-08-01.xml')
root = tree.getroot()

# Регистрация пространств имен
for prefix, uri in namespaces.items():
    ET.register_namespace(prefix, uri)

# Замена содержимого поста
for item in root.findall('./channel/item'):
    title = item.find('title')
    if title is not None and title.text == 'Expanding the Reach: .it.com Domains Can Now Be Listed on the Dan.com Marketplace':
        content = item.find('content:encoded', namespaces)
        if content is not None:
            content.text = '''<![CDATA[<!-- wp:paragraph -->
<p>Сегодня компания it.com Domains с радостью сообщает, что ее домены принимаются для размещения на Dan.com, ведущем маркетплейсе доменов, принадлежащем GoDaddy. Это расширение дополняет начальную <a href="https://get.it.com/blog/godaddy-now-offers-it-com-domains/">доступность доменов .it.com через GoDaddy</a>, предоставляя бизнесу и предпринимателям дополнительные упрощенные возможности доступа к доменам .it.com через безопасную и удобную платформу aftermarket доменов Dan.com.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Dan.com упрощает покупку, продажу и аренду доменных имен, предлагая бесшовный опыт для пользователей. Важность Dan.com на рынке доменов обусловлена его свежим подходом к продаже доменов, акцентом на прозрачности и удобстве использования. Инновационные функции платформы, такие как мгновенные передачи доменов для определенных ccTLD и SEO-оптимизированные целевые страницы, сделали его значимым игроком на вторичном рынке доменов.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Доступность доменов it.com на Dan.com представляет собой значительную возможность для бизнеса всех видов и отраслей создать сильную онлайн-идентичность. С доменами .it.com компании могут расширить свои возможности за пределы традиционных gTLD, выйти на мировые рынки и повысить узнаваемость бренда в IT-сообществе. Более того, поскольку домены .it.com работают в рамках установленной структуры .com, они предлагают первоначальное доверие и бесшовную интеграцию.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Делая домены .it.com доступными через множество платформ, мы позволяем большему числу компаний стимулировать инновации и успех в цифровом пространстве. Это сотрудничество с Dan.com дополняет предложение GoDaddy, создавая еще больше возможностей для бизнеса, стремящегося процветать в современном рыночном пространстве.</p>
<!-- /wp:paragraph -->]]>'''

# Сохранение изменений в новый файл
tree.write('translated_getitcom.WordPress.2024-08-01.xml', encoding='utf-8', xml_declaration=True)