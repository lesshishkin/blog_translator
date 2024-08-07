import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle


def create_pdf(data, lang, file_name):
    # todo работает плохо, но может и не нужна эта функция, проще html
    data = json.loads(data)

    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Заголовок
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Translation to Spanish")

    # Подзаголовок
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 70, f"Overall Translation Quality: {data['overall_translation_quality']}")
    c.drawString(100, height - 90, f"Explanation: {data['explanation']}")

    # Переход к таблице
    c.translate(inch, height - 150)
    c.setFont("Helvetica", 10)

    # Создание таблицы данных
    table_data = [["Sentence Number", "Original Sentence", "Translated Sentence", "Accuracy", "Meaning Intact", "Well Phrased", "Errors", "Additional Comments"]]

    for eval in data['evaluations']:
        table_data.append([
            eval["sentence_number"],
            eval["original_sentence"],
            eval["translated_sentence"],
            eval["accuracy"],
            eval["meaning_intact"],
            eval["well_phrased"],
            eval["errors"],
            eval["additional_comments"]
        ])

    col_widths = [0.6*inch, 2.5*inch, 2.5*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 2.5*inch]
    table = Table(table_data, colWidths=col_widths)

    # Стиль таблицы
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ])
    table.setStyle(style)

    # Добавление таблицы в PDF
    table.wrapOn(c, width, height)
    table.drawOn(c, 0, -len(table_data) * 15)

    c.save()


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
        html += """
            <tr>
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
