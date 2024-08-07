import json


def create_html(data, lang, file_name):
    data = json.loads(data)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Translation to {lang}</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .low-score {{
                background-color: #ffcccc;
            }}
        </style>
    </head>
    <body>
        <h1>Translation to {lang}</h1>
        <p><strong>Overall Translation Quality:</strong> {quality}</p>
        <p><strong>Explanation:</strong> {explanation}</p>
        <table>
            <tr>
                <th>Sentence Number</th>
                <th>Original Sentence</th>
                <th>Translated Sentence</th>
                <th>Accuracy</th>
                <th>Meaning Intact</th>
                <th>Well Phrased</th>
                <th>Errors</th>
                <th>Score</th>
                <th>Additional Comments</th>
            </tr>
    """.format(lang=lang, quality=data['overall_translation_quality'], explanation=data['explanation'])

    for sentence in data['evaluations']:
        row_class = "low-score" if sentence['score'] < 5 else ""
        html += """
            <tr class="{row_class}">
                <td>{sentence_number}</td>
                <td>{original_sentence}</td>
                <td>{translated_sentence}</td>
                <td>{accuracy}</td>
                <td>{meaning_intact}</td>
                <td>{well_phrased}</td>
                <td>{errors}</td>
                <td>{score}</td>
                <td>{additional_comments}</td>
            </tr>
        """.format(
            row_class=row_class,
            sentence_number=sentence['sentence_number'],
            original_sentence=sentence['original_sentence'],
            translated_sentence=sentence['translated_sentence'],
            accuracy=sentence['accuracy'],
            meaning_intact=sentence['meaning_intact'],
            well_phrased=sentence['well_phrased'],
            errors=sentence['errors'],
            score=sentence['score'],
            additional_comments=sentence['additional_comments']
        )

    html += """
        </table>
    </body>
    </html>
    """

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html)
