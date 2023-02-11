{
    "name": "Hospital Management Test",
    "summary": "odoo mates",
    'depends': ['base', 'mail'],
    "data": [

        "security/ir.model.access.csv",
        'views/menu.xml',
        'views/femal_patient_view.xml',
        'views/appointment_view.xml',
    ],

    "application": True,
    "sequence": -100,

    "installable": True,

}
