from django import forms


class CompositeForm(forms.Form):
    form_list = None
    _form_instances = {}

    def __init__(self, data=None, files=None, *args, **kwargs):
        self.is_bound = data is not None or files is not None
        for form in self.form_list:
            self._form_instances[form] = form(data, files, *args, **kwargs)

    def full_clean(self):
        for form in self._form_instances.values():
            form.full_clean()

    def get_form_instance(self, form):
        return self._form_instances[form]

    @property
    def errors(self):
        _errors = {}
        for form in self._form_instances.values():
            _errors.update(form.errors)
        return _errors
