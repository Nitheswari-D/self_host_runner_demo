def generate_html_report(results,filename):
    
    html_content = """
    <html>
    <head>
        <title>HID Commands Test Report</title>
        <style>
            table { border-collapse: collapse; width: 90%; margin: auto; }
            th, td { border: 2px solid #000; padding: 8px; text-align: center;background-color: white;}
            .pass { background-color: #c8e6c9; }
            .fail { background-color: #ffccbc; }
            .result-pass { color: green; font-weight: bold; }
            .result-fail { color: red; font-weight: bold; }
            .highlight { background-color: yellow; font-weight: bold; }
            pre { margin: 0; 
                font-family: monospace;
                white-space : pre-wrap;
                word-wrap: break-word;
                max-width: 350px;
            }
        </style>
    </head>
    <body>
        <h2 style="text-align:center;">HID Commands Test Report</h2>
        <table>
            <tr>
                <th>Command Label</th>
                <th>Command Bytes</th>
                <th>Expected Response</th>
                <th>Received Response</th>
                <th>Result</th>
            </tr>
    """

    for result in results:
        cls = "pass" if result["passed"] else "fail"
        result_class = "result-pass"if result["passed"]else"result-fail"
        command = result['command']
        expected_hex = result['expected_hex']
        received_hex = result['received_hex']
        start_idx = result['start_idx']

        command_str = ' '.join(f"{b:02X}" for b in command)
        expected_str = ' '.join(expected_hex)

        received_parts = []
        expected_len = len(expected_hex)
        for i, byte in enumerate(received_hex):
            if start_idx != -1 and start_idx <= i < start_idx + expected_len:
                received_parts.append(f'<span class="highlight">{byte}</span>')
            else:
                received_parts.append(byte)
        received_str = ' '.join(received_parts)

        html_content += f"""
            <tr class="{cls}">
                <td>{result['label']}</td>
                <td><pre>{command_str}</pre></td>
                <td><pre>{expected_str}</pre></td>
                <td><pre>{received_str}</pre></td>
                <td class="{result_class}">{'PASS' if result['passed'] else 'FAIL'}</td>
            </tr>
        """
        
    html_content += """
        </table>
    </body>
    </html>
    """

    with open(filename, "w") as f:
        f.write(html_content)
    print(f"Report saved to {filename}")