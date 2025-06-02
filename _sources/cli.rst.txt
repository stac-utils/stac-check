CLI Reference
=============

.. raw:: html

    <embed>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />
    <meta name="generator" content="pdoc 0.9.2" />
    <title>stac_check.cli API documentation</title>
    <meta name="description" content="" />
    <link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/sanitize.min.css" integrity="sha256-PK9q560IAAa6WVRRh76LtCaI8pjTJ2z11v0miyNNjrs=" crossorigin>
    <link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/typography.min.css" integrity="sha256-7l/o7C8jubJiy74VsKTidCy1yBkRtiUGbVkYBylBqUg=" crossorigin>
    <link rel="stylesheet preload" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/styles/github.min.css" crossorigin>
    <style>:root{--highlight-color:#fe9}.flex{display:flex !important}body{line-height:1.5em}#content{padding:20px}#sidebar{padding:30px;overflow:hidden}#sidebar > *:last-child{margin-bottom:2cm}.http-server-breadcrumbs{font-size:130%;margin:0 0 15px 0}#footer{font-size:.75em;padding:5px 30px;border-top:1px solid #ddd;text-align:right}#footer p{margin:0 0 0 1em;display:inline-block}#footer p:last-child{margin-right:30px}h1,h2,h3,h4,h5{font-weight:300}h1{font-size:2.5em;line-height:1.1em}h2{font-size:1.75em;margin:1em 0 .50em 0}h3{font-size:1.4em;margin:25px 0 10px 0}h4{margin:0;font-size:105%}h1:target,h2:target,h3:target,h4:target,h5:target,h6:target{background:var(--highlight-color);padding:.2em 0}a{color:#058;text-decoration:none;transition:color .3s ease-in-out}a:hover{color:#e82}.title code{font-weight:bold}h2[id^="header-"]{margin-top:2em}.ident{color:#900}pre code{background:#f8f8f8;font-size:.8em;line-height:1.4em}code{background:#f2f2f1;padding:1px 4px;overflow-wrap:break-word}h1 code{background:transparent}pre{background:#f8f8f8;border:0;border-top:1px solid #ccc;border-bottom:1px solid #ccc;margin:1em 0;padding:1ex}#http-server-module-list{display:flex;flex-flow:column}#http-server-module-list div{display:flex}#http-server-module-list dt{min-width:10%}#http-server-module-list p{margin-top:0}.toc ul,#index{list-style-type:none;margin:0;padding:0}#index code{background:transparent}#index h3{border-bottom:1px solid #ddd}#index ul{padding:0}#index h4{margin-top:.6em;font-weight:bold}@media (min-width:200ex){#index .two-column{column-count:2}}@media (min-width:300ex){#index .two-column{column-count:3}}dl{margin-bottom:2em}dl dl:last-child{margin-bottom:4em}dd{margin:0 0 1em 3em}#header-classes + dl > dd{margin-bottom:3em}dd dd{margin-left:2em}dd p{margin:10px 0}.name{background:#eee;font-weight:bold;font-size:.85em;padding:5px 10px;display:inline-block;min-width:40%}.name:hover{background:#e0e0e0}dt:target .name{background:var(--highlight-color)}.name > span:first-child{white-space:nowrap}.name.class > span:nth-child(2){margin-left:.4em}.inherited{color:#999;border-left:5px solid #eee;padding-left:1em}.inheritance em{font-style:normal;font-weight:bold}.desc h2{font-weight:400;font-size:1.25em}.desc h3{font-size:1em}.desc dt code{background:inherit}.source summary,.git-link-div{color:#666;text-align:right;font-weight:400;font-size:.8em;text-transform:uppercase}.source summary > *{white-space:nowrap;cursor:pointer}.git-link{color:inherit;margin-left:1em}.source pre{max-height:500px;overflow:auto;margin:0}.source pre code{font-size:12px;overflow:visible}.hlist{list-style:none}.hlist li{display:inline}.hlist li:after{content:',\2002'}.hlist li:last-child:after{content:none}.hlist .hlist{display:inline;padding-left:1em}img{max-width:100%}td{padding:0 .5em}.admonition{padding:.1em .5em;margin-bottom:1em}.admonition-title{font-weight:bold}.admonition.note,.admonition.info,.admonition.important{background:#aef}.admonition.todo,.admonition.versionadded,.admonition.tip,.admonition.hint{background:#dfd}.admonition.warning,.admonition.versionchanged,.admonition.deprecated{background:#fd4}.admonition.error,.admonition.danger,.admonition.caution{background:lightpink}</style>
    <style media="screen and (min-width: 7000px)">@media screen and (min-width:7000px){#sidebar{width:30%;height:100vh;overflow:auto;position:sticky;top:0}#content{width:70%;max-width:100ch;padding:3em 4em;border-left:1px solid #ddd}pre code{font-size:1em}.item .name{font-size:1em}main{display:flex;flex-direction:row-reverse;justify-content:flex-end}.toc ul ul,#index ul{padding-left:1.5em}.toc > ul > li{margin-top:.5em}}</style>
    <style media="print">@media print{#sidebar h1{page-break-before:always}.source{display:none}}@media print{*{background:transparent !important;color:#000 !important;box-shadow:none !important;text-shadow:none !important}a[href]:after{content:" (" attr(href) ")";font-size:90%}a[href][title]:after{content:none}abbr[title]:after{content:" (" attr(title) ")"}.ir a:after,a[href^="javascript:"]:after,a[href^="#"]:after{content:""}pre,blockquote{border:1px solid #999;page-break-inside:avoid}thead{display:table-header-group}tr,img{page-break-inside:avoid}img{max-width:100% !important}@page{margin:0.5cm}p,h2,h3{orphans:3;widows:3}h1,h2,h3,h4,h5,h6{page-break-after:avoid}}</style>
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/highlight.min.js" integrity="sha256-Uv3H6lx7dJmRfRvH8TH6kJD1TSK1aFcwgx+mdg3epi8=" crossorigin></script>
    <script>window.addEventListener('DOMContentLoaded', () => hljs.initHighlighting())</script>
    </head>
    <body>
    <main>
    <article id="content">
    <header>
    <h1 class="title">Module <code>stac_check.cli</code></h1>
    </header>
    <section id="section-intro">
    <details class="source">
    <summary>
    <span>Expand source code</span>
    </summary>
    <pre><code class="python">import click
    from .lint import Linter
    import importlib.matadata

    def link_asset_message(link_list:list, type: str, format: str) -&gt; None:
        &#34;&#34;&#34;Prints a list of links or assets and any errors associated with them.

        Args:
            link_list (list): A list of links or assets.
            type (str): The type of link or asset being processed.
            format (str): The format or request being used.

        Returns:
            None.
        &#34;&#34;&#34;
        if len(link_list) &gt; 0:
            click.secho(f&#34;{type.upper()} {format} errors: &#34;, fg=&#34;red&#34;)
            for asset in link_list:
                click.secho(f&#34;    {asset}&#34;)
        else:
            click.secho(f&#34;No {type.upper()} {format} errors!&#34;, fg=&#34;green&#34;)

    def recursive_message(linter: Linter) -&gt; None:
        &#34;&#34;&#34;Displays messages related to the recursive validation of assets in a collection or catalog.

        Args:
            linter: An instance of the Linter class.

        Returns:
            None.
        &#34;&#34;&#34;
        click.secho()
        click.secho(f&#34;Recursive: Validate all assets in a collection or catalog&#34;, bold=True)
        click.secho(f&#34;Max-depth = {linter.max_depth}&#34;)
        click.secho(&#34;-------------------------&#34;)
        for count, msg in enumerate(linter.validate_all):
            click.secho(f&#34;Asset {count+1} Validated: {msg[&#39;path&#39;]}&#34;, bg=&#34;white&#34;, fg=&#34;black&#34;)
            click.secho()
            if msg[&#39;valid_stac&#39;] == True:
                recursive_linter = Linter(msg[&#34;path&#34;], recursive=0)
                cli_message(recursive_linter)
            else:
                click.secho(f&#34;Valid: {msg[&#39;valid_stac&#39;]}&#34;, fg=&#39;red&#39;)
                click.secho(&#34;Schemas validated: &#34;, fg=&#34;blue&#34;)
                for schema in msg[&#34;schema&#34;]:
                    click.secho(f&#34;    {schema}&#34;)
                click.secho(f&#34;Error Type: {msg[&#39;error_type&#39;]}&#34;, fg=&#39;red&#39;)
                click.secho(f&#34;Error Message: {msg[&#39;error_message&#39;]}&#34;, fg=&#39;red&#39;)
            click.secho(&#34;-------------------------&#34;)

    def intro_message(linter: Linter) -&gt; None:
        &#34;&#34;&#34;Prints an introduction message for the stac-check tool.

        The message includes the stac-check logo, the name of the tool, the version
        of the STAC spec being validated, an update message, and the version of the
        stac-validator being used.

        Args:
            linter (object): An instance of the Linter class, which is used to
                obtain the version of the STAC spec being validated, the update
                message, and the version of the stac-validator being used.

        Returns:
            None.
        &#34;&#34;&#34;
        click.secho(&#34;&#34;&#34;
    ____  ____  __    ___       ___  _  _  ____  ___  __ _ 
    / ___)(_  _)/ _\  / __)___  / __)/ )( \(  __)/ __)(  / )
    \___ \  )( /    \( (__(___)( (__ ) __ ( ) _)( (__  )  ( 
    (____/ (__)\_/\_/ \___)     \___)\_)(_/(____)\___)(__\_)
        &#34;&#34;&#34;)

        click.secho(&#34;stac-check: STAC spec validation and linting tool&#34;, bold=True)

        click.secho()

        if linter.version == &#34;1.0.0&#34;:
            click.secho(linter.set_update_message(), fg=&#39;green&#39;)
        else:
            click.secho(linter.set_update_message(), fg=&#39;red&#39;)

        click.secho()

        click.secho(f&#34;Validator: stac-validator {linter.validator_version}&#34;, bg=&#34;blue&#34;, fg=&#34;white&#34;)

        click.secho()

    def cli_message(linter: Linter) -&gt; None:
        &#34;&#34;&#34;Prints various messages about the STAC object being validated.

        Args:
            linter: The `Linter` object containing information about 
            the STAC object to be validated.

        Returns:
            None
        &#34;&#34;&#34;
        if linter.valid_stac == True:
            click.secho(f&#34;Valid {linter.asset_type}: {linter.valid_stac}&#34;, fg=&#39;green&#39;)
        else:
            click.secho(f&#34;Valid {linter.asset_type}: {linter.valid_stac}&#34;, fg=&#39;red&#39;)

        &#39;&#39;&#39; schemas validated for core object &#39;&#39;&#39;
        click.secho()
        if len(linter.schema) &gt; 0:
            click.secho(&#34;Schemas validated: &#34;, fg=&#34;blue&#34;)
            for schema in linter.schema:
                click.secho(f&#34;    {schema}&#34;)

        &#39;&#39;&#39; best practices message&#39;&#39;&#39;
        click.secho()
        for message in linter.best_practices_msg:
            if message == linter.best_practices_msg[0]:
                click.secho(message, bg=&#39;blue&#39;)
            else:
                click.secho(message, fg=&#39;red&#39;)

        if linter.validate_all == True:
            click.secho()
            click.secho(f&#34;Recursive validation has passed!&#34;, fg=&#39;blue&#39;)
        elif linter.validate_all == False and linter.recursive:
            click.secho()
            click.secho(f&#34;Recursive validation has failed!&#34;, fg=&#39;red&#39;)

        if linter.invalid_asset_format is not None:
            click.secho()
            link_asset_message(linter.invalid_asset_format, &#34;asset&#34;, &#34;format&#34;)

        if linter.invalid_asset_request is not None:
            click.secho()
            link_asset_message(linter.invalid_asset_request, &#34;asset&#34;, &#34;request&#34;)

        if linter.invalid_link_format is not None:
            click.secho()
            link_asset_message(linter.invalid_link_format, &#34;link&#34;, &#34;format&#34;)

        if linter.invalid_link_request is not None:
            click.secho()
            link_asset_message(linter.invalid_link_request, &#34;link&#34;, &#34;request&#34;)

        if linter.error_type != &#34;&#34;:
            click.secho(f&#34;Validation error type: &#34;, fg=&#34;red&#34;)
            click.secho(f&#34;    {linter.error_type}&#34;)

        if linter.error_msg != &#34;&#34;:
            click.secho(f&#34;Validation error message: &#34;, fg=&#39;red&#39;)
            click.secho(f&#34;    {linter.error_msg}&#34;)

        click.secho(f&#34;This object has {len(linter.data[&#39;links&#39;])} links&#34;)

        click.secho()

        ### Stac validator response for reference
        # click.secho(json.dumps(linter.message, indent=4))

    @click.option(
        &#34;--recursive&#34;,
        &#34;-r&#34;,
        is_flag=True,
        help=&#34;Recursively validate all related stac objects.&#34;,
    )
    @click.option(
        &#34;--max-depth&#34;,
        &#34;-m&#34;,
        type=int,
        help=&#34;Maximum depth to traverse when recursing. Omit this argument to get full recursion. Ignored if `recursive == False`.&#34;,
    )
    @click.option(
        &#34;-a&#34;, &#34;--assets&#34;, is_flag=True, help=&#34;Validate assets for format and response.&#34;
    )
    @click.option(
        &#34;-l&#34;, &#34;--links&#34;, is_flag=True, help=&#34;Validate links for format and response.&#34;
    )
    @click.command()
    @click.argument(&#39;file&#39;)
    @click.version_option(version=importlib.metadata.distribution(&#34;stac-check&#34;).version)
    def main(file, recursive, max_depth, assets, links):
        linter = Linter(file, assets=assets, links=links, recursive=recursive, max_depth=max_depth)
        intro_message(linter)
        if recursive &gt; 0:
            recursive_message(linter)
        else:
            cli_message(linter)</code></pre>
    </details>
    </section>
    <section>
    </section>
    <section>
    </section>
    <section>
    <h2 class="section-title" id="header-functions">Functions</h2>
    <dl>
    <dt id="stac_check.cli.cli_message"><code class="name flex">
    <span>def <span class="ident">cli_message</span></span>(<span>linter: <a title="stac_check.lint.Linter" href="lint.html#stac_check.lint.Linter">Linter</a>) ‑> NoneType</span>
    </code></dt>
    <dd>
    <div class="desc"><p>Prints various messages about the STAC object being validated.</p>
    <h2 id="args">Args</h2>
    <dl>
    <dt><strong><code>linter</code></strong></dt>
    <dd>The <code>Linter</code> object containing information about </dd>
    </dl>
    <p>the STAC object to be validated.</p>
    <h2 id="returns">Returns</h2>
    <p>None</p></div>
    <details class="source">
    <summary>
    <span>Expand source code</span>
    </summary>
    <pre><code class="python">def cli_message(linter: Linter) -&gt; None:
        &#34;&#34;&#34;Prints various messages about the STAC object being validated.

        Args:
            linter: The `Linter` object containing information about 
            the STAC object to be validated.

        Returns:
            None
        &#34;&#34;&#34;
        if linter.valid_stac == True:
            click.secho(f&#34;Valid {linter.asset_type}: {linter.valid_stac}&#34;, fg=&#39;green&#39;)
        else:
            click.secho(f&#34;Valid {linter.asset_type}: {linter.valid_stac}&#34;, fg=&#39;red&#39;)

        &#39;&#39;&#39; schemas validated for core object &#39;&#39;&#39;
        click.secho()
        if len(linter.schema) &gt; 0:
            click.secho(&#34;Schemas validated: &#34;, fg=&#34;blue&#34;)
            for schema in linter.schema:
                click.secho(f&#34;    {schema}&#34;)

        &#39;&#39;&#39; best practices message&#39;&#39;&#39;
        click.secho()
        for message in linter.best_practices_msg:
            if message == linter.best_practices_msg[0]:
                click.secho(message, bg=&#39;blue&#39;)
            else:
                click.secho(message, fg=&#39;red&#39;)

        if linter.validate_all == True:
            click.secho()
            click.secho(f&#34;Recursive validation has passed!&#34;, fg=&#39;blue&#39;)
        elif linter.validate_all == False and linter.recursive:
            click.secho()
            click.secho(f&#34;Recursive validation has failed!&#34;, fg=&#39;red&#39;)

        if linter.invalid_asset_format is not None:
            click.secho()
            link_asset_message(linter.invalid_asset_format, &#34;asset&#34;, &#34;format&#34;)

        if linter.invalid_asset_request is not None:
            click.secho()
            link_asset_message(linter.invalid_asset_request, &#34;asset&#34;, &#34;request&#34;)

        if linter.invalid_link_format is not None:
            click.secho()
            link_asset_message(linter.invalid_link_format, &#34;link&#34;, &#34;format&#34;)

        if linter.invalid_link_request is not None:
            click.secho()
            link_asset_message(linter.invalid_link_request, &#34;link&#34;, &#34;request&#34;)

        if linter.error_type != &#34;&#34;:
            click.secho(f&#34;Validation error type: &#34;, fg=&#34;red&#34;)
            click.secho(f&#34;    {linter.error_type}&#34;)

        if linter.error_msg != &#34;&#34;:
            click.secho(f&#34;Validation error message: &#34;, fg=&#39;red&#39;)
            click.secho(f&#34;    {linter.error_msg}&#34;)

        click.secho(f&#34;This object has {len(linter.data[&#39;links&#39;])} links&#34;)

        click.secho()

        ### Stac validator response for reference
        # click.secho(json.dumps(linter.message, indent=4))</code></pre>
    </details>
    </dd>
    <dt id="stac_check.cli.intro_message"><code class="name flex">
    <span>def <span class="ident">intro_message</span></span>(<span>linter: <a title="stac_check.lint.Linter" href="lint.html#stac_check.lint.Linter">Linter</a>) ‑> NoneType</span>
    </code></dt>
    <dd>
    <div class="desc"><p>Prints an introduction message for the stac-check tool.</p>
    <p>The message includes the stac-check logo, the name of the tool, the version
    of the STAC spec being validated, an update message, and the version of the
    stac-validator being used.</p>
    <h2 id="args">Args</h2>
    <dl>
    <dt><strong><code>linter</code></strong> :&ensp;<code>object</code></dt>
    <dd>An instance of the Linter class, which is used to
    obtain the version of the STAC spec being validated, the update
    message, and the version of the stac-validator being used.</dd>
    </dl>
    <h2 id="returns">Returns</h2>
    <p>None.</p></div>
    <details class="source">
    <summary>
    <span>Expand source code</span>
    </summary>
    <pre><code class="python">def intro_message(linter: Linter) -&gt; None:
        &#34;&#34;&#34;Prints an introduction message for the stac-check tool.

        The message includes the stac-check logo, the name of the tool, the version
        of the STAC spec being validated, an update message, and the version of the
        stac-validator being used.

        Args:
            linter (object): An instance of the Linter class, which is used to
                obtain the version of the STAC spec being validated, the update
                message, and the version of the stac-validator being used.

        Returns:
            None.
        &#34;&#34;&#34;
        click.secho(&#34;&#34;&#34;
    ____  ____  __    ___       ___  _  _  ____  ___  __ _ 
    / ___)(_  _)/ _\  / __)___  / __)/ )( \(  __)/ __)(  / )
    \___ \  )( /    \( (__(___)( (__ ) __ ( ) _)( (__  )  ( 
    (____/ (__)\_/\_/ \___)     \___)\_)(_/(____)\___)(__\_)
        &#34;&#34;&#34;)

        click.secho(&#34;stac-check: STAC spec validation and linting tool&#34;, bold=True)

        click.secho()

        if linter.version == &#34;1.0.0&#34;:
            click.secho(linter.set_update_message(), fg=&#39;green&#39;)
        else:
            click.secho(linter.set_update_message(), fg=&#39;red&#39;)

        click.secho()

        click.secho(f&#34;Validator: stac-validator {linter.validator_version}&#34;, bg=&#34;blue&#34;, fg=&#34;white&#34;)

        click.secho()</code></pre>
    </details>
    </dd>
    <dt id="stac_check.cli.link_asset_message"><code class="name flex">
    <span>def <span class="ident">link_asset_message</span></span>(<span>link_list: list, type: str, format: str) ‑> NoneType</span>
    </code></dt>
    <dd>
    <div class="desc"><p>Prints a list of links or assets and any errors associated with them.</p>
    <h2 id="args">Args</h2>
    <dl>
    <dt><strong><code>link_list</code></strong> :&ensp;<code>list</code></dt>
    <dd>A list of links or assets.</dd>
    <dt><strong><code>type</code></strong> :&ensp;<code>str</code></dt>
    <dd>The type of link or asset being processed.</dd>
    <dt><strong><code>format</code></strong> :&ensp;<code>str</code></dt>
    <dd>The format or request being used.</dd>
    </dl>
    <h2 id="returns">Returns</h2>
    <p>None.</p></div>
    <details class="source">
    <summary>
    <span>Expand source code</span>
    </summary>
    <pre><code class="python">def link_asset_message(link_list:list, type: str, format: str) -&gt; None:
        &#34;&#34;&#34;Prints a list of links or assets and any errors associated with them.

        Args:
            link_list (list): A list of links or assets.
            type (str): The type of link or asset being processed.
            format (str): The format or request being used.

        Returns:
            None.
        &#34;&#34;&#34;
        if len(link_list) &gt; 0:
            click.secho(f&#34;{type.upper()} {format} errors: &#34;, fg=&#34;red&#34;)
            for asset in link_list:
                click.secho(f&#34;    {asset}&#34;)
        else:
            click.secho(f&#34;No {type.upper()} {format} errors!&#34;, fg=&#34;green&#34;)</code></pre>
    </details>
    </dd>
    <dt id="stac_check.cli.recursive_message"><code class="name flex">
    <span>def <span class="ident">recursive_message</span></span>(<span>linter: <a title="stac_check.lint.Linter" href="lint.html#stac_check.lint.Linter">Linter</a>) ‑> NoneType</span>
    </code></dt>
    <dd>
    <div class="desc"><p>Displays messages related to the recursive validation of assets in a collection or catalog.</p>
    <h2 id="args">Args</h2>
    <dl>
    <dt><strong><code>linter</code></strong></dt>
    <dd>An instance of the Linter class.</dd>
    </dl>
    <h2 id="returns">Returns</h2>
    <p>None.</p></div>
    <details class="source">
    <summary>
    <span>Expand source code</span>
    </summary>
    <pre><code class="python">def recursive_message(linter: Linter) -&gt; None:
        &#34;&#34;&#34;Displays messages related to the recursive validation of assets in a collection or catalog.

        Args:
            linter: An instance of the Linter class.

        Returns:
            None.
        &#34;&#34;&#34;
        click.secho()
        click.secho(f&#34;Recursive: Validate all assets in a collection or catalog&#34;, bold=True)
        click.secho(f&#34;Max-depth = {linter.max_depth}&#34;)
        click.secho(&#34;-------------------------&#34;)
        for count, msg in enumerate(linter.validate_all):
            click.secho(f&#34;Asset {count+1} Validated: {msg[&#39;path&#39;]}&#34;, bg=&#34;white&#34;, fg=&#34;black&#34;)
            click.secho()
            if msg[&#39;valid_stac&#39;] == True:
                recursive_linter = Linter(msg[&#34;path&#34;], recursive=0)
                cli_message(recursive_linter)
            else:
                click.secho(f&#34;Valid: {msg[&#39;valid_stac&#39;]}&#34;, fg=&#39;red&#39;)
                click.secho(&#34;Schemas validated: &#34;, fg=&#34;blue&#34;)
                for schema in msg[&#34;schema&#34;]:
                    click.secho(f&#34;    {schema}&#34;)
                click.secho(f&#34;Error Type: {msg[&#39;error_type&#39;]}&#34;, fg=&#39;red&#39;)
                click.secho(f&#34;Error Message: {msg[&#39;error_message&#39;]}&#34;, fg=&#39;red&#39;)
            click.secho(&#34;-------------------------&#34;)</code></pre>
    </details>
    </dd>
    </dl>
    </section>
    <section>
    </section>
    </article>
    <nav id="sidebar">
    <h1>Index</h1>
    <div class="toc">
    <ul></ul>
    </div>
    <ul id="index">
    <li><h3>Super-module</h3>
    <ul>
    <li><code><a title="stac_check" href="index.html">stac_check</a></code></li>
    </ul>
    </li>
    <li><h3><a href="#header-functions">Functions</a></h3>
    <ul class="">
    <li><code><a title="stac_check.cli.cli_message" href="#stac_check.cli.cli_message">cli_message</a></code></li>
    <li><code><a title="stac_check.cli.intro_message" href="#stac_check.cli.intro_message">intro_message</a></code></li>
    <li><code><a title="stac_check.cli.link_asset_message" href="#stac_check.cli.link_asset_message">link_asset_message</a></code></li>
    <li><code><a title="stac_check.cli.recursive_message" href="#stac_check.cli.recursive_message">recursive_message</a></code></li>
    </ul>
    </li>
    </ul>
    </nav>
    </main>
    <footer id="footer">
    <p>Generated by <a href="https://pdoc3.github.io/pdoc"><cite>pdoc</cite> 0.9.2</a>.</p>
    </footer>
    </body>

    </embed>