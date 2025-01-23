"""Utility functions to create a WXR file for Wordpress.
"""

import datetime

from lxml import etree as ET
from lxml.etree import CDATA

# XML namespaces declarations
DC_NS = "http://purl.org/dc/elements/1.1/"
WP_NS = "http://wordpress.org/export/1.2/"
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
EXCERPT_NS = "http://wordpress.org/export/1.2/excerpt/"

NSMAP = {
    "dc": DC_NS,
    "wp": WP_NS,
    "content": CONTENT_NS,
    "excerpt": EXCERPT_NS
}
# To make use of namespaces easier
DC = "{{{0}}}".format(DC_NS)
WP = "{{{0}}}".format(WP_NS)
CONTENT = "{{{0}}}".format(CONTENT_NS)
EXCERPT = "{{{0}}}".format(EXCERPT_NS)


def create_root_node():
    # Passing the namespaces map in order to use tags such as <wp:author>
    root = ET.Element("rss", version="2.0", nsmap=NSMAP)
    return root


def create_text_node(parent, name, content):
    node = ET.SubElement(parent, name)
    node.text = content
    return node


def create_channel_node(root_node, website_title, website_root, language):
    channel_node = ET.SubElement(root_node, "channel")
    create_text_node(channel_node, "title", website_title)
    create_text_node(channel_node, "link", website_root)
    create_text_node(channel_node, "language", language)
    create_text_node(channel_node, WP + "wxr_version", "1.2")
    create_text_node(channel_node, WP + "base_site_url", website_root)
    create_text_node(channel_node, WP + "base_blog_url", website_root)
    create_text_node(channel_node, "generator", "https://wordpress.org/?v=5.2")
    return channel_node


def create_author(channel_node, id_: int, login, email, display_name):
    wp_author = ET.SubElement(channel_node, WP + 'author')
    create_text_node(wp_author, WP + "author_id", str(id_))
    create_text_node(wp_author, WP + "author_login", CDATA(login))
    create_text_node(wp_author, WP + "author_email", CDATA(email))
    create_text_node(wp_author, WP + "author_display_name", CDATA(display_name))

    return channel_node

def create_category(channel_node, id_: int, nicename, name, parent = ""):
    wp_category = ET.SubElement(channel_node, WP + 'category')
    create_text_node(wp_category, WP + "term_id", str(id_))
    create_text_node(wp_category, WP + "category_nicename", CDATA(nicename))
    create_text_node(wp_category, WP + "category_parent", CDATA(parent))
    create_text_node(wp_category, WP + "cat_name", CDATA(name))

    # TODO: Add term if needed

    return channel_node

def create_tag(channel_node, id_: int, slug, name):
    wp_category = ET.SubElement(channel_node, WP + 'category')
    create_text_node(wp_category, WP + "term_id", str(id_))
    create_text_node(wp_category, WP + "tag_slug", CDATA(slug))
    create_text_node(wp_category, WP + "tag_name", CDATA(name))
    
    # TODO: Add term if needed
    
    return channel_node

def add_category(item, slug, text):
    cat_node = ET.SubElement(item, 'category')
    cat_node.set("domain", "category")
    cat_node.set("nicename", slug)
    cat_node.text = CDATA(text)

    return item

def add_tag(item, slug, text):
    cat_node = ET.SubElement(item, 'category')
    cat_node.set("domain", "post_tag")
    cat_node.set("nicename", slug)
    cat_node.text = CDATA(text)

    return item

def create_item_node(*, parent, post_id, title, link, post_name, status, post_type, post_date: datetime.datetime, creator):
    item = ET.SubElement(parent, 'item')
    create_text_node(item, "title", title)
    create_text_node(item, "link", link)
    create_text_node(item, DC + "creator", CDATA(creator))
    create_text_node(item, "description", "")
    create_text_node(item, WP + "post_id", post_id)
    create_text_node(item, WP + "post_date", CDATA('{0:%Y-%m-%d %H:%M:%S}'.format(post_date)))
    create_text_node(item, WP + "post_date_gmt", CDATA('{0:%Y-%m-%d %H:%M:%S}'.format(post_date.astimezone(datetime.timezone.utc))))
    create_text_node(item, WP + "comment_status", CDATA("open"))
    create_text_node(item, WP + "ping_status", CDATA("closed"))
    create_text_node(item, WP + "post_name", CDATA(post_name))
    create_text_node(item, WP + "status", CDATA(status))
    create_text_node(item, WP + "post_parent", "0")
    create_text_node(item, WP + "menu_order", "0")
    create_text_node(item, WP + "post_type", CDATA(post_type))
    create_text_node(item, WP + "post_password", CDATA(""))
    create_text_node(item, WP + "is_sticky", "0")
    return item


def create_post_meta_node(parent, key, value):
    post_meta = ET.SubElement(parent, WP + "postmeta")
    create_text_node(post_meta, WP + "meta_key", CDATA(key))
    create_text_node(post_meta, WP + "meta_value", CDATA(value))

comments_id = 1000
def create_post_comment(parent, author, email, url, IP, date, content, reply = None, reply_author = None, reply_date = None):
    global comments_id

    comment = ET.SubElement(parent, WP + "comment")
    create_text_node(comment, WP + "comment_id", (str(comments_id)))
    create_text_node(comment, WP + "comment_author", CDATA(author))
    create_text_node(comment, WP + "comment_author_email", CDATA(email))
    create_text_node(comment, WP + "comment_author_url", CDATA(url))
    create_text_node(comment, WP + "comment_author_IP", CDATA(IP))
    create_text_node(comment, WP + "comment_date", CDATA('{0:%Y-%m-%d %H:%M:%S}'.format(date)))
    create_text_node(comment, WP + "comment_date_gmt", CDATA('{0:%Y-%m-%d %H:%M:%S}'.format(date.astimezone(datetime.timezone.utc))))
    create_text_node(comment, WP + "comment_content", CDATA(content))
    create_text_node(comment, WP + "comment_approved", CDATA("1"))
    create_text_node(comment, WP + "comment_type", CDATA("comment"))
    create_text_node(comment, WP + "comment_parent", ("0"))
    comments_id += 1
    
    if reply:
        reply_comment = ET.SubElement(parent, WP + "comment")
        create_text_node(reply_comment, WP + "comment_id", (str(comments_id)))
        create_text_node(reply_comment, WP + "comment_author", CDATA(reply_author))
        create_text_node(reply_comment, WP + "comment_date", CDATA('{0:%Y-%m-%d %H:%M:%S}'.format(reply_date)))
        create_text_node(reply_comment, WP + "comment_date_gmt", CDATA('{0:%Y-%m-%d %H:%M:%S}'.format(reply_date.astimezone(datetime.timezone.utc))))
        create_text_node(reply_comment, WP + "comment_content", CDATA(reply))
        create_text_node(reply_comment, WP + "comment_approved", CDATA("1"))
        create_text_node(reply_comment, WP + "comment_type", CDATA("comment"))
        create_text_node(reply_comment, WP + "comment_parent", (str(comments_id - 1)))
        comments_id += 1

    return parent

def serialize_array(array):
    string = 'a:{0}:{{'.format(len(array) // 2)
    for el in array:
        string += 's:{0}:"{1}";'.format(len(el), el)
    string += '}'
    return string


def write_xml(root_node, filename):
    tree = ET.ElementTree(root_node)
    tree.write(filename, pretty_print=True, encoding='utf-8', xml_declaration=True)


WEBSITE_ROOT = "https://domain.tld"
FILENAME = "export.xml"

BLOG = 'kaliuser'
 
root = create_root_node()
channel = create_channel_node(root, BLOG, WEBSITE_ROOT, 'fa_IR')

number_translation = str.maketrans('۱۲۳۴۵۶۷۸۹۰١٢٣٤٥٦٧٨٩٠', '12345678901234567890')
import string

punc_translation = str.maketrans('', '', string.punctuation)

import requests
from bs4 import BeautifulSoup
import jdatetime
from urllib.parse import quote
from http.cookiejar import MozillaCookieJar

# Load cookies from a separate file
def load_cookies(filepath):
    jar = MozillaCookieJar(filepath)
    jar.load(ignore_discard=True, ignore_expires=True)
    return jar

cookies = load_cookies('./cookies.txt')

def parse_mixed_persian_date(persian_date_str):
    persian_date_str = persian_date_str.translate(number_translation)

    persian_months = {
        'فروردین': 1,
        'فروردين': 1,
        'اردیبهشت': 2,
        'ارديبهشت': 2,
        'خرداد': 3,
        'تیر': 4,
        'مرداد': 5,
        'شهریور': 6,
        'مهر': 7,
        'آبان': 8,
        'آذر': 9,
        'دی': 10,
        'بهمن': 11,
        'اسفند': 12,
    }

    date_part, time_part = persian_date_str.split('، ')
    day, month_name, year = date_part.split()
    day = int(day)
    month = persian_months[month_name]

    if year.startswith('0'):
        year = int(year) + 1400
    else:
        year = int(year) + 1300 

    hour, minute = map(int, time_part.split(':'))
    jdate = jdatetime.datetime(year, month, day, hour, minute)
    gregorian_date = jdate.togregorian()

    return gregorian_date

with requests.session() as session:
    session.cookies = cookies

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7,ru;q=0.6',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'referer': f'https://blog.ir/panel/{BLOG}',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    response = session.get(f'https://blog.ir/panel/{BLOG}/categories', headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    def extract_categories(ul,  parent=''):
        categories = {}

        for li in ul.find_all('li', recursive=False):
            cat_id = li.get('catid')
            cat_name = li.a.get_text(strip=True)
            categories[cat_id] = {
                'name': cat_name,
            }

            if parent:
                categories[cat_id]['parent'] = parent

            # Check for nested <ul>
            nested_ul = li.find('ul')
            if nested_ul:
                categories.update(extract_categories(nested_ul, parent=cat_id))

        return categories
    
    all_categories = extract_categories(soup.find('div', id='tree').find('ul'))

    # TODO: Add page enumeration
    params = {
        'page': '1(100)',
    }

    response = requests.get(f'https://blog.ir/panel/{BLOG}/posts', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for edit_url in soup.find_all('a', title='ویرایش'):
        id_ = edit_url['href'].split('/')[-1]
        print(id_)

        response = requests.get(f'https://blog.ir' + edit_url['href'], cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('input', id='txtPostTitle')['value']
        slug = soup.find('input', id='txtUrl')['value']
        
        pub_date = map(int, soup.find('input', {'name': 'publish_date'})['value'].split('/'))
        pub_time = map(int, soup.find('input', {'name': 'publish_date_time'})['value'].split(':'))
        
        post_date = jdatetime.datetime(*pub_date, *pub_time).togregorian()

        try:
            author = soup.find('span', class_='postUser').text.translate(punc_translation).replace(' ', '').strip().lower()
        except:
            author = 'alireza.ahani'#input('Enter your name: ')
        tags = soup.find('input', id='tags')['value'].split(',')
        categories = soup.find('input', id='icategories')['value'].split(',')
        
        content = soup.find('textarea', id='txt0').text.split('<input type="button" id="read_more" style="display:none;" alt="ادامه مطلب">')

        item = create_item_node(
                parent=channel,
                post_id=id_,
                title=title,
                link="{0}/{1}".format(WEBSITE_ROOT, slug),
                post_name=slug,
                status="publish",
                post_type="post",
                post_date=post_date,
                creator=author)
        create_text_node(item, CONTENT + "encoded", CDATA(''.join(content)))
        create_text_node(item, EXCERPT + "encoded", CDATA(content[0]))
        
        # TODO: Add comment enumeration
        params = {
            'page': '1(100)',
            'for_post': id_,
        }

        response = requests.get(f'https://blog.ir/panel/{BLOG}/comments', params=params, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for comment in soup.findAll('div', class_="commentRow"):
            url = comment.find('a', class_='website')
            url = url['href'].strip() if url else ''

            ip = comment.find('a', class_='ip')
            ip = ip.text.strip() if ip else ''

            email = comment.find('a', class_='email')
            email = email.text.strip() if email else ''

            full_comment = comment.find('div', class_='fullComment')
            full_comment = full_comment.decode_contents() if full_comment else ''
            
            empty_reply = comment.find('div', class_='emptyReply')

            reply_text, reply_author, reply_date = None, None, None

            if not empty_reply:
                reply_text = comment.find('div', class_='replyText')
                reply_text = reply_text.decode_contents() if reply_text else ''


            log_date = comment.find('span', class_="logDate").text.strip()
            date = parse_mixed_persian_date(log_date)
                    
            author = comment.find('div', class_='logHeadData').text.split('در مطلب')[0].replace(log_date, '').strip()
            
            if not empty_reply:
                reply_info = comment.find('div', class_='replyInfo').text.split('در')
                reply_author = reply_info[0].replace('پاسخ توسط', '').strip()
                reply_date = parse_mixed_persian_date(reply_info[1].strip())

            create_post_comment(item, author, email, url, ip, date, full_comment, reply_text, reply_author, reply_date)

            

        for tag in tags:
            tag = tag.replace('\r', '').replace('\n', '').replace('\t', ' ').strip()

            add_tag(item, slug=quote(tag.replace(' ', '-').lower()), text=tag)

        for category in categories:
            name = all_categories[category]['name'].strip()

            add_category(item, slug=quote(name), text=name)

write_xml(root, FILENAME)
