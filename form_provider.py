from chordataweb.events import EventParams
from chordataweb.tagbuilder import TagBuilder


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
    d = TagBuilder("form").add_attributes({'class': 'user__edit-form', 'id': widget_id}) \
        .add_data({'logic': 'user_form'}).add_child(
        [
            TagBuilder().add_attributes({'class': 'user__form-elements-container'}).add_child([
                TagBuilder('input').add_attributes(
                    {'name': 'username', 'type': 'hidden', 'class': '__bind_username'}
                ),
                TagBuilder().add_attributes({'class': 'user__edit-form-item'}).add_child([
                    TagBuilder('label').add_attributes({'for': 'user-field-email-address'}).set_text(
                        t.t('Email Address')),
                    TagBuilder('input').add_attributes(
                        {
                            'id': 'user-field-email-address',
                            'name': 'email',
                            'class': '__bind_email',
                            'type': 'text'
                        }
                    )
                ]),
                TagBuilder().add_attributes({'class': 'user__edit-form-item'}).add_child([
                    TagBuilder('label').add_attributes({'for': 'user-field-first-name'}).set_text(t.t('First Name')),
                    TagBuilder('input').add_attributes(
                        {
                            'id': 'user-field-first-name',
                            'name': 'first_name',
                            'class': '__bind_firstname',
                            'type': 'text'
                        }
                    )
                ]),
                TagBuilder().add_attributes({'class': 'user__edit-form-item'}).add_child([
                    TagBuilder('label').add_attributes({'for': 'user-field-last-name'}).set_text(t.t('Last Name')),
                    TagBuilder('input').add_attributes({
                        'id': 'user-field-last-name',
                        'name': 'last_name',
                        'class': '__bind_lastname',
                        'type': 'text'
                    })
                ]),
                TagBuilder().add_attributes({'class': 'user__edit-form-item'}).add_child([
                    TagBuilder('label').add_attributes({'for': 'user-field-organization'}).set_text(
                        t.t('Organization')),
                    TagBuilder('input').add_attributes(
                        {
                            'id': 'user-field-organization',
                            'name': 'organization',
                            'class': '__bind_organization',
                            'type': 'text'
                        }
                    )
                ]),
                TagBuilder().add_attributes({'class': 'user__edit-form-item'}).add_child([
                    TagBuilder('label').add_attributes({'for': 'phone-number'}).set_text(t.t('Phone')),
                    TagBuilder('input').add_attributes(
                        {
                            'id': 'phone-number',
                            'name': 'phone',
                            'class': '__bind_phone',
                            'type': 'text'
                        }
                    )
                ])
            ]),
            TagBuilder().add_attributes({'class': 'user__edit-form-password-section'}).add_child([
                TagBuilder().add_attributes({'class': 'user__edit-form-item'}).add_child([
                    TagBuilder('label').add_attributes({'for': 'user-new-password'}).set_text(t.t('New Password')),
                    TagBuilder('input').add_attributes(
                        {
                            'id': 'user-new-password',
                            'name': 'password',
                            'class': '__bind_password',
                            'type': 'password'
                        }
                    )
                ]),
                TagBuilder().add_attributes({'class': 'user__edit-form-item'}).add_child([
                    TagBuilder('label').add_attributes({'for': 'user-new-password-confirmation'}) \
                        .set_text(t.t('Confirm New Password')),
                    TagBuilder('input').add_attributes(
                        {
                            'id': 'user-new-password-confirmation',
                            'name': 'confirmation',
                            'class': '__bind_password_confirmation',
                            'type': 'password'
                        }
                    )
                ])
            ]),
            TagBuilder().add_attributes({'class': 'user__edit-form-action-buttons'}).add_child([
                TagBuilder('button').add_attributes({'class': 'user__edit-form-update'}) \
                    .set_text(t.t('Update Account Information'))
            ])
        ]
    )
    return {
        'tags': d,
        'scripts': [
            '/authentication/js/user_form.js'
        ],
        'stylesheets': [
            '/authentication/css/styles.css'
        ]
    }
