def export_to_html():
    # 初期設定
    html_text = f"""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>

    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <title>Brat Embedding (minimal example)</title>
        <link rel="stylesheet" type="text/css" href="css/style-vis.css">
        <script type="text/javascript" src="js/head.js"></script>
    </head>

    <body>

    <!-- load all the libraries upfront, which takes forever. -->
    <script type="text/javascript" src="js/brat_loader.js"></script>
    """
    return html_text