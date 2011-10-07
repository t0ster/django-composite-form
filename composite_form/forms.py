from django import forms


class CompositeForm(forms.Form):
    """
    Helper class to handle form composition.

    Usage::

      class ProfileForm(CompositeForm):
          form_list = [ProfileAddressForm, ProfileBirthDayForm]
    """
    form_list = None
    _form_instances = {}

    def __init__(self, data=None, files=None, *args, **kwargs):
        self.is_bound = data is not None or files is not None
        for form in self.form_list:
            self._form_instances[form] = form(data, files, *args, **kwargs)

    @property
    def forms(self):
        """
        Returns list of form instances
        """
        # Preserving forms ordering
        return [self._form_instances[form_class] for form_class in self.form_list]

    def get_form(self, form_class):
        """
        Returns form instance by its class

        ``form_class``: form class from ``forms_list``
        """
        return self._form_instances[form_class]

    def full_clean(self):
        self.errors

    def _clean_fields(self):
        for form in self.forms:
            for name, field in form.fields.items():
                try:
                    value = form.cleaned_data[name]
                    if hasattr(self, 'clean_%s' % name):
                        value = getattr(self, 'clean_%s' % name)()
                        form.cleaned_data[name] = value
                except forms.ValidationError, e:
                    form._errors[name] = self.error_class(e.messages)
                    if name in form.cleaned_data:
                        del form.cleaned_data[name]

    @property
    def errors(self):
        """
        Returns error dictionary containing all errors from all forms
        """
        _errors = {}
        for form in self.forms:
            _errors.update(form.errors)

        if not _errors:
            self._clean_fields()
            # This may modify forms' fields so calling _post_clean()
            for form in self.forms:
                form._post_clean()

        return _errors
