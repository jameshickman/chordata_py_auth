from chordate.events import EventParams
from chordate.tagbuilder import TagBuilder
from chordate.util.form_builder import form_builder


def user_info(e: EventParams) -> dict:
    p = e.get_payload()
    t = p.get('translator')
    widget_id = p.get('widget_id', 'user_info_widget')
    d = TagBuilder().add_attributes(
        {
            'class': 'webbus_container profile__user-information-container',
            'id': widget_id,
            'data-logic': 'user_info_display'
        }
    ).add_child(
        [
            TagBuilder().add_attributes({'class': 'profile__field-label'}).set_text(t.t('User Name')),
            TagBuilder().add_attributes({'class': 'profile__field-value __bind_user_name'}),
            TagBuilder().add_attributes({'class': 'profile__field-label'}).set_text(t.t('Email address')),
            TagBuilder().add_attributes({'class': 'profile__field-value __bind_email'}),
            TagBuilder().add_attributes({'class': 'profile__field-label'}).set_text(t.t('First Name')),
            TagBuilder().add_attributes({'class': 'profile__field-value __bind_first_name'}),
            TagBuilder().add_attributes({'class': 'profile__field-label'}).set_text(t.t('Last Name')),
            TagBuilder().add_attributes({'class': 'profile__field-value __bind_last_name'}),
            TagBuilder().add_attributes({'class': 'profile__section-organization'}).add_child(
                [
                    TagBuilder().add_attributes({'class': 'profile__field-label'}).set_text(t.t('Organization')),
                    TagBuilder().add_attributes({'class': 'profile__field-value __bind_organization'})
                ]
            ),
            TagBuilder().add_attributes({'class': 'profile__section-phone'}).add_child(
                [
                    TagBuilder().add_attributes({'class': 'profile__field-label'}).set_text(t.t('Phone')),
                    TagBuilder().add_attributes({'class': 'profile__field-value __bind_phone'})
                ]
            )
        ]
    )
    return {
        'tags': d,
        'stylesheets': [
            '/authentication/css/styles.css'
        ],
        'scripts': [
            '/authentication/js/user_details.js'
        ]
    }


def user_form(e: EventParams) -> dict:
    p = e.get_payload()
    t = p.get('translator')
    widget_id = p.get('widget_id', 'user_form_widget')
    d = TagBuilder()
    return {
        'tags': d,
        'scripts': [],
        'stylesheets': []
    }
