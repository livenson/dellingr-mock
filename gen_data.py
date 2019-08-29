# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waldur_core.server.settings')

from django.core.wsgi import get_wsgi_application
from django.core.files import File

get_wsgi_application()


from waldur_mastermind.marketplace.models import Category, Section, Attribute, \
    AttributeOption, Offering, ServiceProvider, Plan, PlanComponent, OfferingComponent
from waldur_mastermind.common.mixins import UnitPriceMixin
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
        ('queuing_system', 'Queueing system', listattr),
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
        ('tflops', 'Peak TFlop/s', integer),
        ('linpack', 'Linpack TFlop/s', integer)
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
        ('centos7', 'CentOS Linux 7'),
        ('rhel6', 'Red Hat Enterprise Linux 6')
    ],
    'queuing_system': [
        ('slurm', 'Slurm'),
        ('torque', 'Torque'),
        ('moab', 'Moab'),
    ],
    'cpu': [
        ('Intel_Xeon_E5-2670', 'Intel_Xeon_E5-2670',),
        ('Intel_Xeon_E5-2680v3', 'Intel_Xeon_E5-2680v3'),
        ('Intel_Xeon_E5-2690v3', 'Intel_Xeon_E5-2690v3'),
        ('Intel_Xeon_E7-8860v4', 'Intel Xeon E7-8860v4'),
    ],
    'gpu': [
        ('Nvidia_K80', 'Nvidia K80'),
        ('Nvidia_P100', 'Nvidia P100'),
    ],
    'interconnect': [
        ('Infiniband_FDR', 'Infiniband FDR'),
        ('Infiniband_EDR', 'Infiniband EDR'),
        ('Ethernet_1G', 'Ethernet 1G'),
        ('Ethernet_10G', 'Ethernet 10G'),
    ],
    'applications': [
        ('Matlab', 'Matlab'),
        ('Gromacs', 'Gromacs'),
    ],
    'certification': [
        ('sensitive_data', 'Able to process sensitive data'),
    ]
}

hpc_configuration = {'order': [], 'options': {}}
    # 'prefill_name': True,  # If True, name would be pre-filled with label in request creation form
    # 'order': ['core_hours'],
    # 'options': {
    #     'core_hours': {
    #         'type': 'integer',
    #         'label': 'Expected core/hours',
    #         'help_text': 'In thousands',
    #         'default': 50,
    #         'min': 1,
    #         'required': True,  # if field must be provided by a user.
    #     }
    # }


oecd_science_domain_configuration = {
    'type': 'select_string',
    'label': 'Science Domain',
    'help_text': 'Please select your intended science domain in (OECD 2007 classification)',
    'required': True,
    'choices': [
        '1.1 Mathematics',
        '1.2 Computer and information sciences',
        '1.3 Physical sciences',
        '1.4 Chemical sciences',
        '1.5 Earth and related environmental sciences',
        '1.6 Biological sciences',
        '1.7 Other natural sciences',

        '2.1 Civil engineering',
        '2.2 Electrical engineering, electronic engineering, information engineering',
        '2.3 Mechanical engineering',
        '2.4 Chemical engineering',
        '2.5 Materials engineering',
        '2.6 Medical engineering',
        '2.7 Environmental engineering',
        '2.8 Environmental biotechnology',
        '2.9 Industrial Biotechnology',
        '2.10 Nano-technology',
        '2.11 Other engineering and technologies',

        '3.1 Basic medicine',
        '3.2 Clinical medicine',
        '3.3 Health sciences',
        '3.4 Health biotechnology',
        '3.5 Other medical sciences',

        '4.1 Agriculture, forestry, and fisheries',
        '4.2 Animal and dairy science',
        '4.3 Veterinary science',
        '4.4 Agricultural biotechnology',
        '4.5 Other agricultural sciences',

        '5.1 Psychology',
        '5.2 Economics and business',
        '5.3 Educational sciences',
        '5.3 Sociology',
        '5.5 Law',
        '5.6 Political Science',
        '5.7 Social and economic geography',
        '5.8 Media and communications',
        '5.7 Other social sciences',

        '6.1 History and archaeology',
        '6.2 Languages and literature',
        '6.3 Philosophy, ethics and religion',
        '6.4 Art (arts, history of arts, performing arts, music)',
        '6.5 Other humanities',
    ],
}

nationality_configuraiton = {
    'type': 'string',
    'label': 'Nationalities of users',
    'help_text': 'Due to potential limitations of access to HPC systems and software, '
                 'please provide nationalities of expected users',
    'required': True,
}

extended_configuration = {
    'order': ['oecd_science_domain_configuration', 'nationality'],
    'options': {
        'oecd_science_domain_configuration': oecd_science_domain_configuration,
        'nationality': nationality_configuraiton,
    },
}


# default plan for all
def generate_plan(offering):
    cpu_usage, _ = OfferingComponent.objects.get_or_create(
        offering=offering,
        billing_type=OfferingComponent.BillingTypes.USAGE,
        type='cpu_usage',
        name='CPU usage',
        measured_unit='core-h'
    )
    gpu_usage, _ = OfferingComponent.objects.get_or_create(
        offering=offering,
        billing_type=OfferingComponent.BillingTypes.USAGE,
        type='gpu_usage',
        name='GPU usage',
        measured_unit='core-h'
    )

    plan, _ = Plan.objects.get_or_create(
        name='Dellingr pilot',
        description='Default plan for all resources provided via Dellingr',
        unit=UnitPriceMixin.Units.PER_MONTH,
        offering=offering,
    )

    cpu_usage_plan_component, _ = PlanComponent.objects.get_or_create(
        plan=plan,
        component=cpu_usage,
        price=0.01,
    )

    gpu_usage_plan_component, _ = PlanComponent.objects.get_or_create(
        plan=plan,
        component=gpu_usage,
        price=0.1,
    )

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
    shared=True,
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
        u'node_information_gpu': [u'node_information_gpu_Nvidia_P100'],
        u'node_information_interconnect': [u'node_information_interconnect_Infiniband_FDR'],
        u'node_information_local_disk': 200,
        u'node_information_memory': 64,
        u'node_information_node_count': 584,
        u'performance_linpack': 462.4,
        u'performance_tflops': 766.6,
        u'software_applications': [u'software_applications_Matlab', u'software_applications_Gromacs'],
        u'system_information_home_space': u'/home/TBA',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queuing_system': [u'system_information_queuing_system_slurm'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'support@lunarc.lu.se',
        u'support_phone': u'+46 2224454',
        u'support_portal': u'https://supr.snic.se/support/',
        u'support_guide': u'https://lunarc-documentation.readthedocs.io/en/latest/login_howto/',
    },
    options=hpc_configuration,
)
aurora.thumbnail.save('aurora.jpg', File(open(base + 'aurora.jpg', 'r')))
generate_plan(aurora)


customer, _ = Customer.objects.get_or_create(
    name='CSC',
    email='servicedesk@csc.fi',
)
ServiceProvider.objects.get_or_create(
    customer=customer,
    enable_notifications=False,
)
taito, _ = Offering.objects.get_or_create(
    name='Taito',
    state=Offering.States.ACTIVE,
    category=cat,
    shared=True,
    description='Computing cluster for serial and small-sized parallel jobs.',
    full_description='<h2>Overview</h2>Taito is a computing cluster hosted by CSC - IT Center for Science, Finland. '
                     'It is intended for serial jobs and parallel jobs using up to 672 cores. '
                     'Finland\'s largest collection of scientific software and databases is available for users of Taito. '
                     'Taito is physically located at Kajaani.',
    rating=5,
    customer=customer,
    type='Support.OfferingTemplate',
    geolocations=[{"latitude": 64.231203, "longitude": 27.704096}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E5-2690v3', u'node_information_cpu_Intel_Xeon_E5-2670'],
        u'node_information_gpu': [u'node_information_gpu_Nvidia_P100', u'node_information_gpu_Nvidia_K80'],
        u'node_information_interconnect': [u'node_information_interconnect_Infiniband_FDR'],
        u'node_information_local_disk': 1900,
        u'node_information_memory': 128,
        u'node_information_node_count': 1000,
        u'performance_linpack': 500,
        u'performance_tflops': 600,
        u'software_applications': [u'software_applications_Matlab', u'software_applications_Gromacs'],
        u'system_information_home_space': u'/homeappl/home/username',
        u'system_information_linux_distro': [u'system_information_linux_distro_rhel6'],
        u'system_information_queuing_system': [u'system_information_queuing_system_slurm'],
        u'system_information_work_space': u'/wrk/username',
        u'support_email': u'servicedesk@csc.fi',
        u'support_phone': u'+35894572821',
        u'support_portal': u'https://research.csc.fi/support',
    },
    options=hpc_configuration
)
taito.thumbnail.save('csc.png', File(open(base + 'csc.png', 'r')))
generate_plan(taito)


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
    shared=True,
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
    geolocations=[{"latitude": 55.694998, "longitude": 12.102468}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E5-2683v3'],
        u'node_information_interconnect': [u'node_information_interconnect_Infiniband_FDR'],
        u'node_information_local_disk': 0,
        u'node_information_memory': 128,
        u'node_information_node_count': 540,
        u'performance_linpack': 410.78,
        u'performance_tflops': 483.84,
        u'software_applications': [u'software_applications_Matlab', u'software_applications_Gromacs'],
        u'system_information_home_space': u'/home/TBA',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queuing_system': [u'system_information_queuing_system_moab'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'hpc@bio.dtu.dk',
        u'support_phone': u'+45 60 90 46 46',
        u'support_guide': u'https://www.computerome.dk/display/CW/Getting+Started+-+new+users',
    },
    options=hpc_configuration
)
computerome.thumbnail.save('computerome.png', File(open(base + 'computerome.png', 'r')))
generate_plan(computerome)


abacus, _ = Offering.objects.get_or_create(
    name='Abacus 2.0',
    category=cat,
    shared=True,
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
        u'node_information_gpu': [u'node_information_gpu_Nvidia_P100'],
        u'node_information_interconnect': [u'node_information_interconnect_Infiniband_FDR'],
        u'node_information_local_disk': 200,
        u'node_information_memory': 64,
        u'node_information_node_count': 584,
        u'performance_linpack': 462.4,
        u'performance_tflops': 766.6,
        u'software_applications': [u'software_applications_Matlab', u'software_applications_Gromacs'],
        u'system_information_home_space': u'/home/smth',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queuing_system': [u'system_information_queuing_system_slurm'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'support@escience.sdu.dk',
        u'support_phone': u'(+45) 6550 2678',
        u'support_guide': u'https://escience.sdu.dk/index.php/slurm-job-scheduler/',
    },
    options=hpc_configuration
)
abacus.thumbnail.save('abacus.jpg', File(open(base + 'abacus.jpg', 'r')))
generate_plan(abacus)


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
    shared=True,
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
        u'performance_linpack': 0,
        u'performance_tflops': 0,
        u'software_applications': [u'software_applications_Matlab'],
        u'system_information_home_space': u'/home/smth',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queuing_system': [u'system_information_queuing_system_slurm'],
        u'system_information_work_space': u'/tmp',
        u'support_email': u'support@hpc.ut.ee',
        u'support_phone': u'(+372) 566 292 82',
        u'support_guide': u'https://hpc.ut.ee/en/slurm/',
    },
    options=hpc_configuration
)
tartu.thumbnail.save('tartu.png', File(open(base + 'tartu.png', 'r')))
generate_plan(tartu)


customer, _ = Customer.objects.get_or_create(
    name='University of Iceland',
    email='etais@etais.ee',
)
ServiceProvider.objects.get_or_create(
    customer=customer,
    enable_notifications=False,
)

iceland, _ = Offering.objects.get_or_create(
    name='Garpur HPC cluster',
    category=cat,
    shared=True,
    description='General purpose HPC cluster run by University of Iceland',
    state=Offering.States.ACTIVE,
    full_description='<h2>Overview</h2> Garpur consists of 36 nodes with Intel Xeon E5-2680v3 with 128GB DDR4 and 62 nodes with Intel Xeon Gold 6130 with 192GB DDR4',
    rating=5,
    customer=customer,
    type='Support.OfferingTemplate',
    geolocations=[{"latitude": 64.143315, "longitude":  -21.962558}],
    attributes={
        u'node_information_cpu': [u'node_information_cpu_Intel_Xeon_E5-2680v3'],
        u'node_information_interconnect': [u'node_information_interconnect_Infiniband_FDR'],
        u'node_information_local_disk': 900,
        u'node_information_memory': 128,
        u'node_information_node_count': 36,
        u'performance_linpack': 0,
        u'performance_tflops': 175,
        u'software_applications': [u'software_applications_Matlab'],
        u'system_information_home_space': u'/users/home/TBA',
        u'system_information_linux_distro': [u'system_information_linux_distro_centos7'],
        u'system_information_queuing_system': [u'system_information_queuing_system_slurm'],
        u'system_information_work_space': u'/users/work/TBA',
        u'support_email': u'support-hpc@hi.is',
        u'support_phone': u'525-4745',
        u'support_guide': u'http://ihpc.is/support',
    },
    options=hpc_configuration
)
iceland.thumbnail.save('iceland.svg', File(open(base + 'iceland.svg', 'r')))
generate_plan(iceland)


# http://www.lunarc.lu.se/resources/hardware/aurora/
# https://www.hpc2n.umu.se/resources/hardware/kebnekaise
# https://research.csc.fi/documents/48467/72092/cPouta+Service+Description/6ffbf7fa-ded0-4c2c-acd2-fd97ddd0e3e5
