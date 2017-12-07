from goose3 import Goose
import json

g = Goose({'enable_image_fetching':False})
urls = json.load(open("test_urls.json"))['urls'][:10]

found_n = {
    'title': 0,
    'raw_html': 0,
    'cleaned_text': 0,
    'meta_description': 0,
    'tags': 0,
    'meta_tags': 0
}
extract_failures = 0
body_lens = []

for url in urls:
    try:
        article = g.extract(url=url)
        for key in found_n.keys():
            if key in article.__dict__ and len(article.__dict__[key]) > 0:
                found_n[key] += 1
        body_lens.append(len(article.cleaned_text))
    except:
        extract_failures += 1

print(found_n)
print(body_lens)
