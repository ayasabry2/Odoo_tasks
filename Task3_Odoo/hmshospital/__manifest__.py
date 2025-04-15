{
    'name': 'Hospital Managment',
     # "sequence": -101,
    'depends': ['base','crm'],
    'author': 'Aya Sabry',
    'category': 'Management',
    'description': 'A custom module for hospital management',
    'data': [
        'views/hospital_menu.xml',
        'views/res_partner_views.xml',
        'views/patients_views.xml',
        'views/departments_views.xml',
        'views/doctors_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}