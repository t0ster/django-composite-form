from django import forms


class CompositeForm(forms.Form):
    """
    Helper class to handle form composition.

    Usage::

      class ProfileForm(CompositeForm):
          form_list = [ProfileAddressForm, ProfileBirthDayForm]
    """
    form_list = None  # Form classes
    _form_instances = {}  # Form instances

    def __init__(self, data=None, files=None, *args, **initkwargs):
        if "instance" in initkwargs:
            raise ValueError("use instances instead of instance")
        instances = initkwargs.pop("instances", None)
        if instances is not None:
            if not isinstance(instances, list):
                raise ValueError("instances should be a list the same lenth as form_list")
            if len(instances) != len(self.form_list):
                raise ValueError("instances should be a list the same lenth as form_list")
            for instance, form in zip(instances, self.form_list):
                if instance is not None and not isinstance(instance, form._meta.model):
                    raise ValueError
        self.is_bound = data is not None or files is not None
        self.instances = instances

        for form in self.form_list:
            kwargs = initkwargs.copy()
            if self.get_form_instance(form):
                kwargs.update({"instance": self.get_form_instance(form)})
            self._form_instances[form] = form(data, files, *args, **kwargs)

    def __unicode__(self):
        raise NotImplementedError("Sorry, not implemented yet")

    def get_form_instance(self, form):
        """
        This method only makes sense if form is instance of ModelForm
        """
        if self.instances is not None:
            return self.instances[self.form_list.index(form)]
        return None

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

    @property
    def cleaned_data(self):
        cleaned_data = {}
        for form in self.forms:
            cleaned_data.update(form.cleaned_data)
        return cleaned_data

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
    def initial(self):
        _initial = {}
        for form in self.forms:
            _initial.update(form.initial)
        return _initial

    def non_field_errors(self):
        _errors = forms.util.ErrorList()
        for form in self.forms:
            _errors.extend(form.non_field_errors())
        return _errors

    @property
    def errors(self):
        """
        Returns error dictionary containing all errors from all forms
        """
        _errors = forms.util.ErrorDict()
        for form in self.forms:
            _errors.update(form.errors)

        if not _errors:
            self._clean_fields()
            # This may modify forms' fields so calling _post_clean()
            for form in self.forms:
                form._post_clean()

        return _errors
