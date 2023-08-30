from string import Template


class MyTemplate(Template):
    delimiter = '&'


def change_template(patient_name, cirurgia_name, termo_template):

    d = {
        'patient_name': patient_name,
        'cirurgia_name': cirurgia_name
    }

    src = MyTemplate(termo_template)
    termo_result = src.substitute(d)

    return termo_result
