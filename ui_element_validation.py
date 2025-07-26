import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Form Validation using Pydantic
    - This example demonstrates form validation using a pydantic model, which is defined in `models.py`.
    > As at creation date (26.07.2025), I could not find tutorials or examples of marimo form falidation using pydantic and a `validation=` callback, hence this example.
    """
    )
    return


@app.cell
def _():
    from datetime import date

    import marimo as mo
    from pydantic import ValidationError

    from models import Department, Employee

    return Department, Employee, ValidationError, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Define UI elements""")
    return


@app.cell
def _(Department, mo):
    # Define UI elements

    name = mo.ui.text(label="Name")
    email = mo.ui.text(label="Email", kind="email", placeholder="email@example.com")
    birth_date = mo.ui.date(label="Birth Date")
    salary = mo.ui.number(label="Salary", value=0)

    # Get department names from Department Enum
    department = mo.ui.dropdown(
        list(map(lambda dept: dept.name, Department)), label="Department"
    )

    elected_benefits = mo.ui.checkbox(label="Elected Benefits")
    return birth_date, department, elected_benefits, email, name, salary


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Create a form
    - Create the markdown for the form with variables from the batch created for the form.
    - Create the batch. Assign each element to a variable, which should be the same as that used in the markdown.
    - The form data is passed as a dictionary to the `validate=` callback. Therefore, it makes sense to name the batch variables the same as those expected by the `Employee` model, which saves a step in translating the form dictionary into a model readable dictionary.
    - The **Submit** button will not clear the form unless all the inputs are validated completely as per validation rules.
    - The errors returned by the validation callback are displayed in the cell.
    """
    )
    return


@app.cell
def _(
    birth_date,
    department,
    elected_benefits,
    email,
    mo,
    name,
    salary,
    validate_employee_detail_form,
):
    # Define form markdown
    form_markdown = mo.md(
        """## Employee Data
        {name} {birth_date} {email}

        {department} {salary} {elected_benefits}
        """
    )

    # Batch UI elements in the form in the ordedr expected by the Employee model.
    employee_detail_form = form_markdown.batch(
        name=name,
        email=email,
        birth_date=birth_date,
        salary=salary,
        department=department,
        elected_benefits=elected_benefits,
    ).form(
        validate=validate_employee_detail_form,
        show_clear_button=True,
        clear_on_submit=True,
    )
    return (employee_detail_form,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Display the form""")
    return


@app.cell
def _(employee_detail_form):
    employee_detail_form
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Validation""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Method 1
    - This is commented out and provides an option to validate after data has been entered. In this case, the form will not have a `validate=` callback.
    - However, this allows the form to emit data which has not been validated and introduces complexity in the form of further checks required before committing the addition, e.g. to a database. 
    """
    )
    return


@app.cell
def _():
    # This method is less robust, as it allows the form to release an invaid value, which is then checked for validation
    # errors = {}

    # try:
    #     # form.value is a dictionary that can be used directly for model validation
    #     employee = Employee.model_validate(employee_detail_form.value)

    #     mo.output.replace(
    #         mo.md(
    #             f"Employee details validated."
    #         ).callout(kind="success")
    #     )

    #     errors = {}

    # except ValidationError as err:
    #     mo.output.replace(mo.md("Review Input").callout(kind="warn"))
    #     errors = {"__all__": str(err)}
    #     print(errors)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Method 2
    - This is cleaner and more robust, as submission does not complete until all the form data has been validated.
    """
    )
    return


@app.cell
def _(Employee, ValidationError):
    # This method is more robust, as it forces the form to validate before returning a value.

    def validate_employee_detail_form(data: dict) -> str | None:
        data = data.copy()

        # The dropdown returns a list, which interferes with pydantic validation
        department = data.get("department")
        if isinstance(department, list):
            data["department"] = department[0] if department else ""

        try:
            Employee.model_validate(data)
            return None
        except ValidationError as err:
            # Extract field and error msg from each ErrorDetails dict in err.errors()
            error_list = []
            for error_details in err.errors():
                # error_details.get('loc') returns a tuple except for the model_validator error
                field_name = (
                    f"{error_details.get('loc')[0]}: "
                    if error_details.get("loc")
                    else ""
                )
                msg = error_details.get("msg")
                error_list.append(f"{field_name}{msg}")

            err_msg = "\n".join(error_list)

            return str(err_msg)

    return (validate_employee_detail_form,)


if __name__ == "__main__":
    app.run()
