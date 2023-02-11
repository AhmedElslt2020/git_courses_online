{
    "name": "Student Registration",
    "summary": "Task by Knowledge bi by ahmed gamal shehataa odoo 15",
    'depends': ['base', 'account'],
    "data": [
        "security/student_registration_security.xml",
        "security/ir.model.access.csv",
        'data/sequence_data.xml',

        'views/student_registration.xml',
        'views/inherit_invoice.xml',
        'views/student_partner_view.xml',

    ],

    # "application": True,
    # "sequence": -1022,
    #
    # "installable": True,

}
