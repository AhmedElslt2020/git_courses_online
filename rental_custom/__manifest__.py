{
    "name": "rental_custom",
    "summary": "Modify rental module",
    'depends': ['base', 'sale_renting', 'sale'],
    "data": [
        'views/rental_view.xml',
    ],

    "application": True,
    "sequence": 4,

    "installable": True,

}
