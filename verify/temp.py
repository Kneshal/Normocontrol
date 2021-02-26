
    '''
    file = check_list[0].docx_file
    urls = settings.MEDIA_ROOT+'fileload/'
    fs = FileSystemStorage(location=urls, base_url=urls)
    filename = fs.save(file.name, file)
    filepath = urls + file.name
    print(filename)
    print(filepath)
    html = ''
    with open(filepath, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value

    context = {'page': page, 'html': html}
    '''
    '''
    filename = 'media/test_docx.docx'
    output = pypandoc.convert(filename, 'html')
    filename, ext = os.path.splitext(filename)
    filename = "{0}.html".format(filename)
    with open(filename, 'w') as f:
        # Python 2 "fix". If this isn't a string, encode it.
        if type(output) is not str:
            output = output.encode('utf-8')
        f.write(output)

    print("Done! Output written to: {}\n".format(filename))
    '''
