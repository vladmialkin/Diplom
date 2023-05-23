import flet


class ResultIssueDialog(flet.AlertDialog):
    def __init__(self):
        super().__init__()
        self.modal = True
        self.database = None
        self.actions = [flet.TextButton("Редактировать", on_click=self.edit_result),
                        flet.TextButton("Закрыть", on_click=self.close_dialog)]
        self.issue_id = None
        self.issue = None
        self.content_text = None
        self.content = flet.Column(height=500, width=700)
        self.content.scroll = 'adaptive'

    def close_dialog(self, event):
        self.page.dialog.open = False
        self.page.update()

    def edit_result(self, event):
        self.content.controls = [
            flet.TextField(value=self.content_text, multiline=True),
            flet.Row([flet.TextButton("Сохранить", on_click=self.save_edit),
                      flet.TextButton("Отменить", on_click=self.cansel_edit)])]
        self.page.update()

    def save_edit(self, event):
        value = self.content.controls[0].value
        self.database.update_result_issue(self.issue_id, value)
        self.content_text = value
        self.cansel_edit(event)

    def cansel_edit(self, event):
        self.content.controls = [flet.Text(value=self.content_text, size=18)]
        self.page.update()

    def show_dialog(self, issue, database):
        self.database = database
        self.issue = issue
        self.issue_id = issue.id
        self.content_text = issue.custom_fields.get(7).value
        self.title = flet.Column(controls=[flet.Text(f"{issue.tracker} #{issue.id}", size=24, weight='bold'),
                                           flet.Text(f"{issue.subject}", size=20, weight='bold'),
                                           flet.Text(f"Результат задачи")])
        self.content.controls = [flet.Text(value=self.content_text, size=18)]
        self.page.dialog.open = True
        self.page.update()


class ExitMenuDialog(flet.AlertDialog):
    def __init__(self):
        super().__init__()
        self.title = flet.Text("Вы действительно хотите выйти?")
        self.actions_alignment = "center"
        self.actions = [flet.TextButton("Да", on_click=self.exit),
                        flet.TextButton("Нет", on_click=self.close_dialog)]

    def exit(self, event):
        self.page.dialog.open = False
        for view in self.page.views:
            if view.route == "auth":
                auth_view = view
                self.page.views.clear()
                self.page.views.append(auth_view)
                self.page.go(auth_view.route)
        self.page.update()

    def close_dialog(self, event):
        self.page.dialog.open = False
        self.page.update()

    def show_dialog(self):
        self.page.dialog.open = True
        self.page.update()


class WorkingHoursDialog(flet.AlertDialog):
    def __init__(self):
        super().__init__()
        self.title = flet.Text("Изменить трудовые часы месяца?")
        self.actions_alignment = "center"
        self.actions = [flet.TextButton("Да", on_click=self.update_working_hours),
                        flet.TextButton("Нет", on_click=self.close_dialog)]
        self.working_hours = None

    def close_dialog(self, event):
        self.page.dialog.open = False
        self.page.update()

    def update_working_hours(self, event):
        pass

    def show_dialog(self, working_hours):
        self.working_hours = working_hours
        self.page.dialog.open = True
        self.page.update()


class DeletePlannedHoursDialog(flet.AlertDialog):
    def __init__(self):
        super().__init__()
        self.database = None
        self.issue_id = None
        self.month = None
        self.actions_alignment = "center"
        self.actions = [flet.TextButton("Да", on_click=self.delete_planned_hours),
                        flet.TextButton("Нет", on_click=self.close_dialog)]
        self.working_hours = None

    def close_dialog(self, event):
        self.page.dialog.open = False
        self.page.update()

    def delete_planned_hours(self, event):
        self.database.delete_month_in_custom_fields(issue_id=self.issue_id, month_plan=self.month)
        self.close_dialog(event)

    def show_dialog(self, database, issue_id, month):
        self.title = flet.Text(f"Удалить {month} из плана месяца?")
        self.database = database
        self.issue_id = issue_id
        self.month = month
        self.page.dialog.open = True
        self.page.update()
