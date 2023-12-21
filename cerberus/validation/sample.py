from datetime import datetime
from string import capwords

from cerberus import Validator


class SampleValidator(Validator):
    """Sample Validator that extends Cerberus `Validator`"""

    def __init__(self, location, *args, **kwargs):
        super(Validator, self).__init__(*args, **kwargs)
        self.location = location
    
    def _check_with_bio_id(self, field: str, value: str):
        """Checks that `bio_id` is valid.
        Valid if:
            - Starts with 'BIO_'
            - Contains `patient_id`
            - Ends with _`location`
        """
        patient_id = self.document.get("patient_id")
        if not patient_id:
            return
        bio_id = f"BIO_{patient_id}_{self.location}"
        if value != bio_id:
            self._error(
                field,
                f"Value must match the format of BIO_{patient_id}_{self.location}"
            )
    
    def _check_with_patient_id(self, field: str, value: str):
        """Checks that `patient_id` is valid.
        Valid if:
            - Starts with 'Patient_'
        """
        if not value.startswith("Patient_"):
            self._error(
                field,
                "Value must start with 'Patient'"
            )
    
    def _check_with_blood_sample_id(self, field: str, value: str):
        """Checks that `blood_sample_id` is valid.
        Valid if:
            - Starts with 'Blood_Sample_'
            - Ends with _`location`
        """
        if not value.startswith("Blood_Sample_") or not value.endswith(f"_{self.location}"):
            self._error(
                field,
                f"Value must start with 'Blood_Sample_' and end with _{self.location}"
            )

    def _check_with_is_integer(self, field: str, value: str):
        """Checks that value is an integer"""
        if not value.isdigit():
            self._error(
                field,
                "Value must be a valid integer"
            )

    def _normalize_coerce_capitalize(self, value: str) -> str:
        """Coerces value to be entirely capitalized"""
        return value.upper() if value else value
    
    def _normalize_coerce_first_letter_capitalize(self, value: str) -> str:
        """Coerces value to have its first letter be capitalized"""
        if value.strip():
            value = value.capitalize()
        return value    
    
    def _normalize_coerce_yyyy_mm_dd(self, value: str) -> str:
        """Coerces value of MM/DD/YYYY to be YYYY_MM_DD"""
        try:
            value = datetime.strftime(datetime.strptime(value, "%Y-%m-%d"), "%Y-%m-%d")
        except ValueError:
            value = datetime.strftime(
                datetime.strptime(value, "%m/%d/%Y"), "%Y-%m-%d"
            )
        return value
    