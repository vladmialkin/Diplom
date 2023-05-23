import jinja2
from weasyprint import HTML, CSS
import pathlib


class PdfFormat:
    def __init__(self, path):
        self.site = None
        self.path = path
        self.css = CSS(string="""
            @page{ 
                size: landscape;
                margin: 1cm; 
            }
            body{
                font-size: 10px;
            }
            table{
                width: 100%;
                border-style: solid; 
                border-color: black; 
                border-collapse: collapse;
                margin-left: auto; 
                margin-right: auto;
            }
            """)

    def worker_create_html(self, data, state, sector, user_name, now_date, plan_costs, fact_costs,
                           plan_month, month_year, norm_costs):
        for issue in data:
            if isinstance(issue[6], list):
                issue[6] = '\n'.join(issue[6])

        worker_template = jinja2.Template("""\
        <style>
            TR, TH, TD{
                border: 1px; 
                border-collapse: 
                collapse; border-style: solid; 
                border-color: black;
                margin: auto;
                white-space: pre-line;
            }
        </style>
        <p style="font-size: 20px; text-align: center; font-weight: 700;">{{ state }} за {{ plan_month }}</p>
        <p style="font-size: 18px; font-weight: 700;">{{ sector }}</p>
        <p style="font-size: 16px; font-weight: 700;">{{ user_name }}</p>
        <p>Норма трудозатрат: {{ norm_costs }}</p>
        <p>Плановые трудозатраты: {{ plan_costs }}</p>
        <p>Фактические трудозатраты: {{ fact_costs }}</p>
        <table class="table">
          <tr>
            <th>#</th>
            <th>Тема</th>
            <th>Трекер</th>
            <th>Плановые трудозатраты</th>
            <th>Фактические трудозатраты</th>
            <th>Срок завершения</th>
            <th>План месяца</th>
            <th>Тип задачи</th>
            <th>Результат задачи</th>
          </tr>
          {% for row in data -%}
            <tr>
            {% for value in row -%}
                {% if not value -%}
                    <td>
                        {% else -%}
                    <td>
                        {{ value }}
                    </td>
                {% endif -%}
            {% endfor -%}
            </tr>
          {% endfor -%}
        </table>
        <p>{{ now_date }}</p>
        """)
        worker_site = worker_template.render(data=data, state=state, sector=sector, user_name=user_name,
                                             now_date=now_date,
                                             plan_costs=plan_costs,
                                             fact_costs=fact_costs,
                                             plan_month=plan_month,
                                             norm_costs=norm_costs)
        file_name = f'{user_name}.{state}.{plan_month}.pdf'
        file = pathlib.Path(self.path, file_name)
        HTML(string=worker_site).write_pdf(file, stylesheets=[self.css])
        return file_name

    def supervizor_create_table(self, state, sector, plan_month):
        self.site = None
        supervizor_template = jinja2.Template("""\
            <style>
                TR, TH, TD{
                    border: 1px; 
                    border-collapse: 
                    collapse; border-style: solid; 
                    border-color: black;
                    margin: auto;
                    white-space: pre-line;
                }
            </style>
            <p style="font-size: 20px; text-align: center; font-weight: 700;">{{ state }} за {{ plan_month }}</p>
            <p style="font-size: 18px; font-weight: 700;">{{ sector }}</p>""")
        self.site = supervizor_template.render(state=state, sector=sector, plan_month=plan_month)

    def create_new_row(self, data, user_name, now_date, plan_costs, fact_costs, plan_month, norm_costs):
        for issue in data:
            if isinstance(issue[6], list):
                issue[6] = '\n'.join(issue[6])

        new_worker = jinja2.Template("""\
        <style>
            TR, TH, TD{
                border: 1px; 
                border-collapse: 
                collapse; border-style: solid; 
                border-color: black;
                margin: auto;
                white-space: pre-line;
            }
        </style>
        <p style="font-size: 16px; font-weight: 700;">{{ user_name }}</p>
        <p>Норма трудозатрат: {{ norm_costs }}</p>
        <p>Плановые трудозатраты: {{ plan_costs }}</p>
        <p>Фактические трудозатраты: {{ fact_costs }}</p>
        <table class="table">
          <tr>
            <th>#</th>
            <th>Тема</th>
            <th>Трекер</th>
            <th>Плановые трудозатраты</th>
            <th>Фактические трудозатраты</th>
            <th>Срок завершения</th>
            <th>План месяца</th>
            <th>Тип задачи</th>
            <th>Результат задачи</th>
          </tr>
          {% for row in data -%}
            <tr>
            {% for value in row -%}
                {% if not value -%}
                    <td>
                        {% else -%}
                    <td>
                        {{ value }}
                    </td>
                {% endif -%}
            {% endfor -%}
            </tr>
          {% endfor -%}
        </table>
        <p>{{ now_date }}</p>
        """)
        new_site = new_worker.render(data=data, user_name=user_name, now_date=now_date,
                                     plan_costs=plan_costs,
                                     fact_costs=fact_costs,
                                     plan_month=plan_month,
                                     norm_costs=norm_costs)

        self.site += f"\n{new_site}"

    def supervizor_create_pdf(self, sector, state, date):
        file_name = f'{sector}.{state}.{date}.pdf'
        file = f"{self.path}/assets/{file_name}"
        HTML(string=self.site).write_pdf(file, stylesheets=[self.css])
        return file
