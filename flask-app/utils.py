def convert_poem_to_html(p_num):
    html_poem = ''

    with open(f'../data/poems/{p_num}_poem.txt') as f:
        for line in f:
            html_poem += (line + '<br />')

    return html_poem
