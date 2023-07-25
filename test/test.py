import html2text

# HTML content to convert
html_content = "<h1>This is a heading</h1><p>This is a paragraph.</p>"

# Convert the HTML to plain text
text_content = html2text.html2text(html_content)

# Print the converted plain text
print(text_content)
