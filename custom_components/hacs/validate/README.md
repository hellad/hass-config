# Repository validation

This is where the validation rules that run against the various repository categories live.

## Structure

<<<<<<< HEAD
=======
- All validation rules are in the directory for their category.
- Validation rules that aplies to all categories are in the `common` directory.
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
- There is one file pr. rule.
- All rule needs tests to verify every possible outcome for the rule.
- It's better with multiple files than a big rule.
- All rules uses `ValidationBase` or `ActionValidationBase` as the base class.
- The `ActionValidationBase` are for checks that will breaks compatibility with with existing repositories (default), so these are only run in github actions.
<<<<<<< HEAD
=======
- The class name should describe what the check does.
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
- Only use `validate` or `async_validate` methods to define validation rules.
- If a rule should fail, raise `ValidationException` with the failure message.


## Example

```python
<<<<<<< HEAD
from .base import (
=======
from custom_components.hacs.validate.base import (
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    ActionValidationBase,
    ValidationBase,
    ValidationException,
)


class AwesomeRepository(ValidationBase):
    def validate(self):
        if self.repository != "awesome":
            raise ValidationException("The repository is not awesome")

<<<<<<< HEAD
class SuperAwesomeRepository(ActionValidationBase):
    category = "integration"

=======
class SuperAwesomeRepository(ActionValidationBase, category="integration"):
>>>>>>> 6d6a0ed04d4a624e651d2332d2e651b7dbbd95e1
    async def async_validate(self):
        if self.repository != "super-awesome":
            raise ValidationException("The repository is not super-awesome")
```