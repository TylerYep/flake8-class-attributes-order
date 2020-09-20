# flake8-function-order

An extension for flake8 to report on wrong class attributes order and
class level logic.

The validator can extract class attribute type: docstring, property,
nested class, `GLOBAL_VAR`, etc.
If django model fields are detected, the validator can detect,
if the field is link to another table (foreign key, generic key, etc)
or not.

After resolving each attribute type, validator checks attributes order.

Default configuration checks for the following order of attributes:

- `__new__`
- `__init__`
- `__post_init__`
- other magic methods
- `@property`
- `@staticmethod`
- `@classmethod`
- other methods
- private methods

If the order is broken, validator will report on it.

Besides methods, the validator checks other attributes methods:
docstrings, nested classes, constants, attributes, and so on.

Also validator checks, if class has no class level logic and report
if any. Here is an example:

```python
class PhoneForm(forms.Form):
    phone = forms.CharField(17, label='Телефон'.upper())

    # this should happen in __init__!
    phone.widget.attrs.update({'class': 'form-control phone'})

```

## Installation

```
pip install flake8-function-order
```

Configurable options:

| Option                |               Description           | Fallbacks to\* |
|:---------------------:|:-----------------------------------:|:--------------:|
|meta_class             |class Meta: (e.g. in Django projects)| nested_class   |
|nested_class           |Other nested classes                 | None\*         |
|constant               |SOME_CONSTANTS                       | field          |
|outer_field            |some = models.ForeignKey etc.        | field          |
|field                  |Other fields                         | None           |
|`__new__`              |`__new__`                            | magic_method   |
|`__init__`             |`__init__`                           | magic_method   |
|`__post_init__`        |`__post_init__`                      | magic_method   |
|`__str__`              |`__str__`                            | magic_method   |
|magic_method           |Other magic methods                  | method         |
|save                   |def save(...)                        | method         |
|delete                 |def delete(...)                      | method         |
|property_method        |@property/@cached_property etc.      | method         |
|private_property_method|@property/@cached_property with _    | property_method|
|static_method          |@staticmethod                        | method         |
|private_static_method  |@staticmethod beginning with _       | static_method  |
|class_method           |@classmethod                         | method         |
|private_class_method   |@classmethod beginning with _        | class_method   |
|private_method         |other methods beginning with _       | method         |
|method                 |other methods                        | None           |

\* if not provided, will use its supertype order

\*\*  if not defined, such base types and all their subtypes (unless defined)
will be ignored during validation. It's recommended
to set at least `nested_class`, `field` and `method`

You choose how detailed your configuration is.
For example, you can define order of each supported magic method
(`__new__`, `__str__`, etc.), or set `magic_method`
to allow any order among them or even just use `method`

Usage:

```terminal
$ flake8 test.py
test.py:5:5: CCE001 User.fetch_info_from_crm should be after User.LOGIN_FIELD
test.py:15:5: CCE002 Class level expression detected model UserNode, line 15
```

Tested on Python 3.7.x and flake8 3.7.5.

## Error codes

| Error code |                     Description                          |
|:----------:|:--------------------------------------------------------:|
|   CCE001   | Wrong class attributes order (`XXX should be after YYY`) |
|   CCE002   | Class level expression detected                          |
