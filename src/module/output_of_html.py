def export_to_html():
    # 画面出力処理
    html_text = f"""
    <p>This is the output of brat visualizer (please wait several seconds until all javascript libraries are loaded):</p>

    <p><br>SVOCの可視化:</p>
    <div id="embedding-entity-example1"></div>
    <script type="text/javascript">
        head.ready(function() {{
            Util.embed('embedding-entity-example1', $.extend({{}}, collData1),
                    $.extend({{}}, docData1), webFontURLs);
        }});
    </script>

    <p><br>品詞の可視化:</p>
    <div id="embedding-entity-example4"></div>
    <script type="text/javascript">
        head.ready(function() {{
            Util.embed('embedding-entity-example4', $.extend({{}}, collData4),
                    $.extend({{}}, docData4), webFontURLs);
        }});
    </script>

    </body>
    </html>
    """
    return html_text
