# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waldur_core.server.settings')

from django.core.wsgi import get_wsgi_application
from django.core.files import File

get_wsgi_application()


from waldur_mastermind.marketplace.models import Category, Section, Attribute, AttributeOption, Offering, ServiceProvider
from waldur_core.structure.models import Customer


# attribute types
boolean = 'boolean'
string = 'string'
integer = 'integer'
choice = 'choice'
listattr = 'list'

# Location where images are located
base = ''  # path relative to the cwd or absolute

#### eInfraCentral catalogue ####

## get data
# import json

#import urllib
#url = 'http://beta.einfracentral.eu/api/service/all?quantity=300'
#response = urllib.urlopen(url)
#data = json.loads(response.read())

# with open('/Users/ilja/workspace/waldur-mastermind/all.json') as f:
#     data = json.load(f)


# for c in data['results']:
#     print c['name'], c['category']
#     if c['category']:
#         cat = Category.objects.get_or_create(title=c['category'].split('-')[1])
#
# print data['results'][0]

#### Structure ####

sections = {
    'security': 'Security',
    'performance': 'Performance',
    'support': 'Support',
}

hpc_sections = {
    'system_information': 'System information',
    'node_information': 'Node information',
    'performance': 'Performance',
    'software': 'Software',
    'support': 'Support',
    'security': 'Security',
}

hpc_attributes = {
    'system_information': [
        ('queing_system', 'Queueing system', listattr),
        ('home_space', 'Home space', string),
        ('work_space', 'Work space', string),
        ('linux_distro', 'Linux distribution', listattr),
    ],
    'node_information': [
        ('cpu', 'CPU model', choice),
        ('gpu', 'GPU model', choice),
        ('memory', 'Memory per node (GB)', integer),
        ('local_disk', 'Local disk (GB)', integer),
        ('interconnect', 'Interconnect', choice),
        ('node_count', 'Node count', integer),
    ],
    'performance': [
        ('tflops', 'TFlops', integer),
        ('linpak', 'Linpack TPP', integer)
    ],
    'software': [
        ('applications', 'Applications', listattr),
    ],
    'support': [
        ('email', 'E-mail', string),
        ('phone', 'Phone', string),
        ('portal', 'Support portal', string),
        ('guide', 'User guide', string),
    ],
    'security': [
        ('certification', 'Certification', listattr),
    ]
}

enums = {
    'linux_distro': [
        ('centos7', 'CentOS7'),
        ('ubuntu1604', 'Ubuntu 16.04')
    ],
    'queing_system': [
        ('slurm', 'SLURM'),
        ('torque', 'Torque'),
        ('moab', 'MOAB'),
    ],
    'cpu': [
        ('Intel_Xeon_E5-2650v3', 'Intel Xeon E5-2650v3',),
        ('Intel_Xeon_Gold_6132', 'Intel Xeon Gold 6132'),
        ('Intel_Xeon_E7-8860v4', 'Intel Xeon E7-8860v4'),
        ('Intel_Xeon_E5-2680v3', 'Intel Xeon E5-2680v3'),
    ],
    'gpu': [
        ('NVidia_K80', 'NVidia K80'),
        ('NVidia_P100', 'NVidia V100'),
        ('NVidia_V100', 'NVidia V100'),
    ],
    'interconnect': [
        ('Infiniband_FDR', 'Infiniband FDR'),
        ('Infiniband_EDR', 'Infiniband EDR'),
        ('Ethernet_1G', 'Ethernet 1G'),
        ('Ethernet_10G', 'Ethernet 10G'),
    ],
    'applications': [
        ('Matlab', 'Matlab'),
        ('Gromacs', 'GROMACS'),
    ],
    'certification': [
        ('iskem', 'ISKE M'),
        ('iskeh', 'ISKE H'),
        ('iskel', 'ISKE L'),
        ('iso27001', 'ISO27001'),
        ('vahtiraised', 'VAHTI raised level'),
    ]
}

hpc_configuration = {
        'prefill_name': True,  # If True, name would be pre-filled with label in request creation form
        'order': ['core_hours'],
        'options': {
            'core_hours': {
                'type': 'integer',
                'label': 'Expected core/hours',
                'help_text': 'In thousands',
                'default': 50,
                'min': 1,
                'required': True,  # if field must be provided by a user.
            }
        }
    }

cat, _ = Category.objects.get_or_create(title='HPC', description='High Performance Computing systems')
cat.icon.save('data-center.svg', File(open(base + 'data-center.svg', 'r')))

for section_key in hpc_sections.keys():
    sec, _ = Section.objects.get_or_create(key=section_key, title=hpc_sections[section_key], category=cat)
    sec.is_standalone = True
    sec.save()
    if section_key in hpc_attributes.keys():
        for attribute in hpc_attributes[section_key]:
            key, title, type = attribute
            attr, _ = Attribute.objects.get_or_create(key='%s_%s' % (section_key, key), title=title, type=type, section=sec)
            if key in enums:
                values = enums[key]
                for val_key, val_label in values:
                    AttributeOption.objects.get_or_create(attribute=attr,
                                                          key='%s_%s_%s' % (section_key, key, val_key), title=val_label)


# Offering
customer, _ = Customer.objects.get_or_create(
    name='Lunarc',
    email='support@lunarc.lu.se',
)
ServiceProvider.objects.get_or_create(
    customer=customer,
    enable_notifications=False,
)
aurora, _ = Offering.objects.get_or_create(
    name='Aurora HPC cluster',
    category=cat,
    state=Offering.States.ACTIVE,
    description='Aurora is Lunarc\'s new general purpose HPC cluster',
    full_description='<h2>Overview</h2>Aurora consists out of 180 compute nodes for SNIC use and over 50 compute nodes funded by '
                     'research groups at Lund University.  Each node has two Intel Xeon E5-2650 v3 processors '
                     '(Haswell), offering 20 compute cores per node.  The nodes have 64 GB of DDR4 ram installed.',
    rating=5,
    customer=customer,
    type='Support.OfferingTemplate',
    geolocations=[{"latitude": 55.7119513, "longitude": 13.2013043}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E5-2680v3'],
        u'node_information_gpu': [u'node_information_gpu_NVidia_P100'],
        u'node_information_interconnect': [u'node_information_interconnect_Infiniband_FDR'],
        u'node_information_local_disk': 200,
        u'node_information_memory': 64,
        u'node_information_node_count': 584,
        u'performance_linpak': 462.4,
        u'performance_tflops': 766.6,
        u'software_applications': [u'software_applications_Matlab', u'software_applications_Gromacs'],
        u'system_information_home_space': u'/home/TBA',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queing_system': [u'system_information_queing_system_slurm'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'support@lunarc.lu.se',
        u'support_phone': u'+46 2224454',
        u'support_portal': u'https://supr.snic.se/support/',
        u'support_guide': u'https://lunarc-documentation.readthedocs.io/en/latest/login_howto/',
    },
    options=hpc_configuration,
)
aurora.thumbnail.save('aurora.jpg', File(open(base + 'aurora.jpg', 'r')))

customer, _ = Customer.objects.get_or_create(
    name='CSC',
    email='servicedesk@csc.fi',
)
ServiceProvider.objects.get_or_create(
    customer=customer,
    enable_notifications=False,
)
csc, _ = Offering.objects.get_or_create(
    name='CSC Taito',
    state=Offering.States.ACTIVE,
    category=cat,
    description='The Taito supercluster (taito.csc.fi) is intended for serial (single-core) and small to medium-size parallel jobs.',
    full_description='<h2>Overview</h2>The Taito supercluster (taito.csc.fi) is intended for serial (single-core) and '
                     'small to medium-size parallel jobs. There are also several "fat nodes" for jobs requiring a large '
                     'amount of memory. Taito consists of sixteen cabinets, with a total theoretical peak performance '
                     'of 600 TFLOPS. Taito has been deployed in two phases that presently coexist.',
    rating=5,
    customer=customer,
    type='Support.OfferingTemplate',
    geolocations=[{"latitude": 55.7119513, "longitude": 13.2013043}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E7-8860v4'],
        u'node_information_gpu': [u'node_information_gpu_NVidia_P100', u'node_information_gpu_NVidia_V100'],
        u'node_information_interconnect': [u'node_information_interconnect_Ethernet_10G'],
        u'node_information_local_disk': 0,
        u'node_information_memory': 0,
        u'node_information_node_count': 0,
        u'performance_linpak': 0,
        u'performance_tflops': 0,
        u'software_applications': [u'software_applications_Matlab'],
        u'system_information_home_space': u'/home/smth',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queing_system': [u'system_information_queing_system_slurm'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'servicedesk@csc.fi',
        u'support_phone': u'+358 (0) 94 57 2821',
        u'support_portal': u'https://research.csc.fi/support',
    },
    options=hpc_configuration
)
csc.thumbnail.save('csc.png', File(open(base + 'csc.png', 'r')))

customer, _ = Customer.objects.get_or_create(
    name='DeIC',
    email='sekretariat@deic.dk',
)
ServiceProvider.objects.get_or_create(
    customer=customer,
    enable_notifications=False,
)
computerome, _ = Offering.objects.get_or_create(
    name='Computerome',
    category=cat,
    state=Offering.States.ACTIVE,
    description='Access to Computerome is available to everyone interested in Life Sciences',
    full_description=u'<h2>Overview</h2>The Danish National Life Science Supercomputing Center, Computerome is a HPC '
                     u'Facility specialized for Life Science. Users include Research groups from all Danish Universities '
                     u'and large international research consortiums as well as users from industry and the public Health '
                     u'Care Sector. They all benefit from the fast, flexible and secure infrastructure and the ability '
                     u'to combine different types of sensitive data and perform analysis. Computerome is physically '
                     u'installed at the DTU Risø campus and managed by a strong team of specialists from DTU. ',
    rating=5,
    customer=customer,
    type='Support.OfferingTemplate',
    geolocations=[{"latitude": 55.7119513, "longitude": 13.2013043}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E7-8860v4'],
        u'node_information_gpu': [u'node_information_gpu_NVidia_P100'],
        u'node_information_interconnect': [u'node_information_interconnect_Ethernet_10G'],
        u'node_information_local_disk': 0,
        u'node_information_memory': 0,
        u'node_information_node_count': 0,
        u'performance_linpak': 0,
        u'performance_tflops': 0,
        u'software_applications': [u'software_applications_Matlab'],
        u'system_information_home_space': u'/home/smth',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queing_system': [u'system_information_queing_system_moab'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'hpc@bio.dtu.dk',
        u'support_phone': u'+45 60 90 46 46',
        u'support_guide': u'https://www.computerome.dk/display/CW/Getting+Started+-+new+users',
    },
    options=hpc_configuration
)
computerome.thumbnail.save('computerome.png', File(open(base + 'computerome.png', 'r')))

abacus, _ = Offering.objects.get_or_create(
    name='Abacus 2.0',
    category=cat,
    state=Offering.States.ACTIVE,
    description='The SDU eScience Center is a single point of reference for eScience and research e-infrastructure at SDU.',
    full_description='<h2>Overview</h2>Abacus 2.0 is a supercomputer with 14,016 processor cores. It may be used for a '
                     'broad spectrum of demanding data processing workloads.',
    rating=5,
    customer=customer,
    type='Support.OfferingTemplate',
    geolocations=[{"latitude": 55.3686303, "longitude": 10.4266494}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E5-2680v3'],
        u'node_information_gpu': [u'node_information_gpu_NVidia_P100'],
        u'node_information_interconnect': [u'node_information_interconnect_Infiniband_FDR'],
        u'node_information_local_disk': 200,
        u'node_information_memory': 64,
        u'node_information_node_count': 584,
        u'performance_linpak': 462.4,
        u'performance_tflops': 766.6,
        u'software_applications': [u'software_applications_Matlab', u'software_applications_Gromacs'],
        u'system_information_home_space': u'/home/smth',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queing_system': [u'system_information_queing_system_slurm'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'support@escience.sdu.dk',
        u'support_phone': u'(+45) 6550 2678',
        u'support_guide': u'https://escience.sdu.dk/index.php/slurm-job-scheduler/',
    },
    options=hpc_configuration
)
abacus.thumbnail.save('abacus.jpg', File(open(base + 'abacus.jpg', 'r')))

customer, _ = Customer.objects.get_or_create(
    name='ETAIS',
    email='etais@etais.ee',
)
ServiceProvider.objects.get_or_create(
    customer=customer,
    enable_notifications=False,
)

tartu, _ = Offering.objects.get_or_create(
    name='UT Rocket',
    category=cat,
    state=Offering.States.ACTIVE,
    description='General purpose HPC cluster in UT HPCC',
    full_description='<h2>Overview</h2>The High Performance Computing Center is a consortium of UT and its purpose '
                     'is to maintain and develop the infrastructure for scientific computing. The resources are open '
                     'for use to any research groups from the university and  other Estonian science- and research '
                     'institutions are also welcome.',
    rating=5,
    customer=customer,
    type='Support.OfferingTemplate',
    geolocations=[{"latitude": 58.3796417, "longitude": 26.7157553}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E7-8860v4'],
        u'node_information_interconnect': [u'node_information_interconnect_Ethernet_10G'],
        u'node_information_local_disk': 0,
        u'node_information_memory': 0,
        u'node_information_node_count': 0,
        u'performance_linpak': 0,
        u'performance_tflops': 0,
        u'software_applications': [u'software_applications_Matlab'],
        u'system_information_home_space': u'/home/smth',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queing_system': [u'system_information_queing_system_slurm'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'support@hpc.ut.ee',
        u'support_phone': u'(+372) 566 292 82',
        u'support_guide': u'https://hpc.ut.ee/en/slurm/',
    },
    options=hpc_configuration
)
tartu.thumbnail.save('tartu.png', File(open(base + 'tartu.png', 'r')))

customer, _ = Customer.objects.get_or_create(
    name='University of Iceland',
    email='etais@etais.ee',
)
ServiceProvider.objects.get_or_create(
    customer=customer,
    enable_notifications=False,
)

iceland, _ = Offering.objects.get_or_create(
    name='University of Iceland',
    category=cat,
    description='General purpose HPC cluster',
    state=Offering.States.ACTIVE,
    full_description='<h2>Overview</h2>TBA',
    rating=5,
    customer=Customer.objects.first(),
    type='Support.OfferingTemplate',
    geolocations=[{"latitude": 58.3796417, "longitude": 26.7157553}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E7-8860v4'],
        u'node_information_interconnect': [u'node_information_interconnect_Ethernet_10G'],
        u'node_information_local_disk': 0,
        u'node_information_memory': 0,
        u'node_information_node_count': 0,
        u'performance_linpak': 0,
        u'performance_tflops': 0,
        u'software_applications': [u'software_applications_Matlab'],
        u'system_information_home_space': u'/home/smth',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queing_system': [u'system_information_queing_system_slurm'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'TBA',
        u'support_phone': u'TBA',
        u'support_guide': u'TBA',
    },
    options=hpc_configuration
)
iceland.thumbnail.save('iceland.svg', File(open(base + 'iceland.svg', 'r')))

# http://www.lunarc.lu.se/resources/hardware/aurora/
# https://www.hpc2n.umu.se/resources/hardware/kebnekaise
# https://research.csc.fi/documents/48467/72092/cPouta+Service+Description/6ffbf7fa-ded0-4c2c-acd2-fd97ddd0e3e5
