# -*- coding: utf-8 -*-
{
    'name': 'Education Management System',
    'version': '16.0.0',
    'summary': 'Manage Studens',
    'description': 'This App To Manage Educational Institutions',
    'category': 'Generic Modules/Human Resources',
    'author': "Neoteric Hub",
    'company': 'Neoteric Hub',
    'currency': 'USD',
    'website': "https://www.neoterichub.com",
    'depends': ['base', 'mail', 'web_domain_field'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/multiple_marks_wizard_view.xml',
        'wizard/multiple_academic_records_wizard_view.xml',
        'views/level.xml',
        'views/education_record.xml',
        'views/department.xml',
        'views/sub_department.xml',
        'views/subject.xml',
        'views/marks.xml',
        'views/student_student_view.xml',
        'views/teacher_teacher_view.xml',
        'views/qualification_student_view.xml',
        'views/settings_views.xml',
        'views/menus.xml',
        'reports/student_report.xml',
    ],

    'assets': {
        'web.assets_backend': [
            '/nthub_ems/static/src/js/mark_tree_extend.js',
            '/nthub_ems/static/src/js/academic_records_tree_extend.js',
            '/nthub_ems/static/src/xml/mark_tree_button.xml',
            '/nthub_ems/static/src/xml/academic_records_tree_button.xml',
        ]
    },

    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}


