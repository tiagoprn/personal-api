# pylint: disable=too-many-lines,too-many-arguments,unused-argument

from django.contrib.auth import get_user_model

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.django_db
class TestGreetingsEndpoint:
    def test_must_pass_on_existing_user(
        self, real_user, authenticated_api_client
    ):  # pylint: disable=unused-argument
        response = authenticated_api_client.get('/core/greetings/')
        assert response.status_code == 200
        assert response.json() == {'message': 'Hello there, hal_jordan!'}

    @pytest.mark.django_db
    def test_must_fail_on_anonymous_user(self, anonymous_api_client):
        response = anonymous_api_client.get('/core/greetings/')
        assert response.status_code == 401
        assert response.json() == {
            'detail': 'Authentication credentials were not provided.'
        }


@pytest.mark.django_db
class TestLinkViewSet:
    def authenticated_api_client(
        self, user
    ):  # pylint: disable=redefined-outer-name
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client

    def test_access_to_links_get_endpoint_must_fail_for_anonymous_user(
        self, anonymous_api_client
    ):
        response = anonymous_api_client.get('/core/api/links/')
        assert response.status_code == 401
        assert response.json() == {
            'detail': 'Authentication credentials were not provided.'
        }

    def test_links_get_endpoint_for_existing_users(
        self, setup_links_instances
    ):
        all_users = User.objects.all().order_by('username')
        first_user_id = str(all_users.first().id)
        last_user_id = str(all_users.last().id)
        expected_users_links = {
            first_user_id: [
                {
                    'original_link': (
                        'https://www.redhat.com/sysadmin/'
                        'getting-started-socat'
                    )
                },
                {
                    'original_link': (
                        'https://www.django-rest-framew'
                        'ork.org/api-guide/viewsets/'
                    )
                },
                {'original_link': 'https://github.com/curl/curl'},
            ],
            last_user_id: [
                {
                    'original_link': (
                        'https://medium.com/aubergine-solutions'
                        '/viewsets-in-django-rest-framework-25bb0110c210'
                    )
                },
                {
                    'original_link': (
                        'https://harrymoreno.com/2019/0'
                        '6/12/Overriding-Django-Rest-Framework-viewsets.html'
                    )
                },
                {
                    'original_link': (
                        'https://dropbox.tech/infrastructure/atlas'
                        '--our-journey-from-a-python-monolith-'
                        'to-a-managed-platform'
                    )
                },
            ],
        }
        users_links = {}
        for user_id in setup_links_instances.keys():
            users_links[user_id] = []

            for link in setup_links_instances[user_id]:
                users_links[user_id].append(link['original_link'])

            expected_links_set = {
                expected_link['original_link']
                for expected_link in expected_users_links[user_id]
            }
            assert set(users_links[user_id]) == expected_links_set

        for user in all_users:
            client = self.authenticated_api_client(user=user)
            response = client.get('/core/api/links/')
            assert response.status_code == 200

            json_response = response.json()
            assert json_response['count'] == 3

            users = set(result['user'] for result in json_response['results'])
            assert users == {str(user.id)}

            links = [
                result['original_link'] for result in json_response['results']
            ]

            expected_links = [
                link['original_link']
                for link in expected_users_links[str(user.id)]
            ]

            assert set(links) == set(expected_links)

    @pytest.mark.parametrize(
        'username,field_name,field_value,expected_original_link',
        [
            (
                'atrocitus',
                'name',
                'redhat',
                'https://www.redhat.com/sysadmin/getting-started-socat',
            ),
            (
                'atrocitus',
                'name',
                'socat',
                'https://www.redhat.com/sysadmin/getting-started-socat',
            ),
            (
                'haljordan',
                'name',
                'dropbox',
                (
                    'https://dropbox.tech/infrastructure/atlas--our-'
                    'journey-from-a-python-monolith-to-a-managed-platform'
                ),
            ),
            (
                'haljordan',
                'name',
                'monolith',
                (
                    'https://dropbox.tech/infrastructure/atlas--our-journey-'
                    'from-a-python-monolith-to-a-managed-platform'
                ),
            ),
            (
                'atrocitus',
                'slug',
                'django-rest-framework',
                'https://www.django-rest-framework.org/api-guide/viewsets/',
            ),
            (
                'haljordan',
                'original_link',
                (
                    'https://medium.com/aubergine-solutions/viewsets-in-'
                    'django-rest-framework-25bb0110c210'
                ),
                (
                    'https://medium.com/aubergine-solutions/viewsets-in-'
                    'django-rest-framework-25bb0110c210'
                ),
            ),
            (
                'haljordan',
                'sanitized_link',
                (
                    'https://harrymoreno.com/2019/06/12/Overriding-'
                    'Django-Rest-Framework-viewsets.html'
                ),
                (
                    'https://harrymoreno.com/2019/06/12/Overriding-Django-'
                    'Rest-Framework-viewsets.html'
                ),
            ),
            (
                'atrocitus',
                'slug',
                'githubcom-curl',
                'https://github.com/curl/curl',
            ),
            ('atrocitus', 'slug', 'curl', 'https://github.com/curl/curl'),
            ('atrocitus', 'slug', '-curl', 'https://github.com/curl/curl'),
            ('atrocitus', 'slug', 'github', 'https://github.com/curl/curl'),
            (
                'atrocitus',
                'shortened_hash',
                'gWKyugt9UpKs6Ub2YZ3G4F',
                'https://www.django-rest-framework.org/api-guide/viewsets/',
            ),
            (
                'haljordan',
                'shortened_hash',
                'LpVcZWxwx6aAz9WpnriKhP',
                (
                    'https://medium.com/aubergine-solutions/viewsets-'
                    'in-django-rest-framework-25bb0110c210'
                ),
            ),
            (
                'haljordan',
                'shortened_hash',
                'UAziYkWY2LBRfZzQVh92hz',
                (
                    'https://harrymoreno.com/2019/06/12/Overriding-'
                    'Django-Rest-Framework-viewsets.html'
                ),
            ),
            (
                'atrocitus',
                'shortened_hash',
                'gWK',
                'https://www.django-rest-framework.org/api-guide/viewsets/',
            ),
            (
                'haljordan',
                'shortened_hash',
                'LpV',
                (
                    'https://medium.com/aubergine-solutions/viewsets-in-'
                    'django-rest-framework-25bb0110c210'
                ),
            ),
            (
                'haljordan',
                'shortened_hash',
                'UAz',
                (
                    'https://harrymoreno.com/2019/06/12/Overriding-Django-'
                    'Rest-Framework-viewsets.html'
                ),
            ),
            (
                'atrocitus',
                'id',
                'd85eace6-6443-4b0d-9a01-7ec7f7c6c9c8',
                'https://www.django-rest-framework.org/api-guide/viewsets/',
            ),
            (
                'haljordan',
                'id',
                '69c082fe-fa66-4f5e-b784-84be5d5a1817',
                (
                    'https://medium.com/aubergine-solutions/viewsets-in-'
                    'django-rest-framework-25bb0110c210'
                ),
            ),
            (
                'haljordan',
                'id',
                '9304e4a9-93fc-4e97-9177-32e8518782e8',
                (
                    'https://harrymoreno.com/2019/06/12/Overriding-Django-'
                    'Rest-Framework-viewsets.html'
                ),
            ),
            (
                'atrocitus',
                'min_created_at',
                '2021-01-16T00:00:00Z',
                'https://github.com/curl/curl',
            ),
            (
                'atrocitus',
                'min_updated_at',
                '2021-01-16T00:00:00Z',
                'https://github.com/curl/curl',
            ),
        ],
    )
    def test_links_get_single_with_filter_endpoint_for_existing_user(
        self,
        setup_links_instances,
        username,
        field_name,
        field_value,
        expected_original_link,
    ):
        user = User.objects.filter(username=username).first()
        client = self.authenticated_api_client(user=user)

        if field_name == 'id':
            url = f'/core/api/links/{field_value}/'
        else:
            url = f'/core/api/links/?{field_name}={field_value}'

        response = client.get(url)

        assert response.status_code == 200

        json_response = response.json()

        if field_name == 'id':
            assert json_response['id'] == field_value
            original_link = json_response['original_link']
            assert original_link == expected_original_link
        else:
            assert json_response['count'] == 1
            original_link = json_response['results'][0]['original_link']
            assert original_link == expected_original_link

    @pytest.mark.parametrize(
        'username,field_name,field_value,expected_original_link',
        [
            (
                'atrocitus',
                'max_created_at',
                '2021-01-16T00:00:00Z',
                (
                    'https://www.redhat.com/sysadmin/getting-started-socat,'
                    'https://www.django-rest-framework.org/api-guide/viewsets/'
                ),
            ),
            (
                'haljordan',
                'min_created_at,max_created_at',
                '2021-01-13T00:00:00Z,2021-01-19T23:59:59Z',
                (
                    'https://harrymoreno.com/2019/06/12/Overriding-Django-'
                    'Rest-Framework-viewsets.html,https://dropbox.tech/infr'
                    'astructure/atlas--our-journey-from-a-python-monolith-'
                    'to-a-managed-platform'
                ),
            ),
            (
                'atrocitus',
                'max_updated_at',
                '2021-01-16T00:00:00Z',
                (
                    'https://www.redhat.com/sysadmin/getting-started-'
                    'socat,https://www.django-rest-framework.org/'
                    'api-guide/viewsets/'
                ),
            ),
            (
                'haljordan',
                'min_updated_at,max_updated_at',
                '2021-01-13T00:00:00Z,2021-01-19T23:59:59Z',
                (
                    'https://harrymoreno.com/2019/06/12/Overriding-'
                    'Django-Rest-Framework-viewsets.html,https://dropbox.tech'
                    '/infrastructure/atlas--our-journey-from-a-python-'
                    'monolith-to-a-managed-platform'
                ),
            ),
        ],
    )
    def test_links_get_multiple_with_filter_endpoint_for_existing_user(
        self,
        setup_links_instances,
        username,
        field_name,
        field_value,
        expected_original_link,
    ):
        user = User.objects.filter(username=username).first()
        client = self.authenticated_api_client(user=user)

        date_range_field = bool(',' in field_name)

        if date_range_field:
            names = field_name.split(',')
            values = field_value.split(',')
            url = (
                f'/core/api/links/?{names[0]}={values[0]}'
                f'&{names[1]}={values[1]}'
            )
        else:
            url = f'/core/api/links/?{field_name}={field_value}'

        response = client.get(url)
        assert response.status_code == 200

        json_response = response.json()

        expected_links = expected_original_link.split(',')
        assert json_response['count'] == len(expected_links)

        links = [
            result['original_link'] for result in json_response['results']
        ]
        assert set(links) == set(expected_links)

    @pytest.mark.parametrize(
        'username, url',
        [
            ('haljordan', 'https://www.osnews.com'),
            ('atrocitus', 'https://www.gnome.org/'),
            ('haljordan', 'https://tools.suckless.org/'),
        ],
    )
    def test_links_post_endpoint_for_existing_users(
        self, setup_user_instances, username, url
    ):
        user = User.objects.filter(username=username).first()
        client = self.authenticated_api_client(user=user)
        response = client.post(
            '/core/api/links/', data={'original_link': url, 'user': user.id}
        )
        assert response.status_code == 201

        response = client.get('/core/api/links/')
        assert response.status_code == 200

        json_response = response.json()
        assert json_response['count'] == 1
        assert json_response['results'][0]['original_link'] == url

    @pytest.mark.parametrize(
        'username, url, initial_name, changed_name, expected_changed_name',
        [
            (
                'haljordan',
                'https://www.osnews.com',
                'www.osnews.com',
                'name1',
                'name1',
            ),
            (
                'atrocitus',
                'https://www.gnome.org',
                'www.gnome.org',
                'name2',
                'name2',
            ),
            (
                'haljordan',
                'https://tools.suckless.org',
                'tools.suckless.org',
                'name3',
                'name3',
            ),
        ],
    )
    def test_links_put_endpoint_for_existing_users(
        self,
        setup_user_instances,
        username,
        url,
        initial_name,
        changed_name,
        expected_changed_name,
    ):
        user = User.objects.filter(username=username).first()
        client = self.authenticated_api_client(user=user)
        response = client.post(
            '/core/api/links/', data={'original_link': url, 'user': user.id}
        )
        assert response.status_code == 201

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 1

        json_response_record = json_response['results'][0]
        assert json_response_record['original_link'] == url
        assert json_response_record['name'] == initial_name

        record_id = json_response_record['id']

        response = client.put(
            f'/core/api/links/{record_id}/',
            data={'original_link': url, 'user': user.id, 'name': changed_name},
        )
        assert response.status_code == 200

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 1

        json_response_record = json_response['results'][0]
        assert json_response_record['original_link'] == url
        assert json_response_record['name'] == expected_changed_name

    @pytest.mark.parametrize(
        'username, url, initial_name, changed_name, expected_changed_name',
        [
            (
                'haljordan',
                'https://www.osnews.com',
                'www.osnews.com',
                'name1',
                'name1',
            ),
            (
                'atrocitus',
                'https://www.gnome.org',
                'www.gnome.org',
                'name2',
                'name2',
            ),
            (
                'haljordan',
                'https://tools.suckless.org',
                'tools.suckless.org',
                'name3',
                'name3',
            ),
        ],
    )
    def test_links_patch_endpoint_for_existing_users(
        self,
        setup_user_instances,
        username,
        url,
        initial_name,
        changed_name,
        expected_changed_name,
    ):
        user = User.objects.filter(username=username).first()
        client = self.authenticated_api_client(user=user)
        response = client.post(
            '/core/api/links/', data={'original_link': url, 'user': user.id}
        )
        assert response.status_code == 201

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 1

        json_response_record = json_response['results'][0]
        assert json_response_record['original_link'] == url
        assert json_response_record['name'] == initial_name

        record_id = json_response_record['id']

        response = client.patch(
            f'/core/api/links/{record_id}/', data={'name': changed_name}
        )
        assert response.status_code == 200

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 1

        json_response_record = json_response['results'][0]
        assert json_response_record['original_link'] == url
        assert json_response_record['name'] == expected_changed_name

    @pytest.mark.parametrize(
        'username, url, initial_name',
        [
            ('haljordan', 'https://www.osnews.com', 'www.osnews.com'),
            ('atrocitus', 'https://www.gnome.org', 'www.gnome.org'),
            ('haljordan', 'https://tools.suckless.org', 'tools.suckless.org'),
        ],
    )
    def test_links_delete_endpoint_for_existing_user(
        self, setup_user_instances, username, url, initial_name
    ):
        user = User.objects.filter(username=username).first()
        client = self.authenticated_api_client(user=user)
        response = client.post(
            '/core/api/links/', data={'original_link': url, 'user': user.id}
        )
        assert response.status_code == 201

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 1

        json_response_record = json_response['results'][0]
        assert json_response_record['original_link'] == url
        assert json_response_record['name'] == initial_name

        record_id = json_response_record['id']

        response = client.delete(f'/core/api/links/{record_id}/')
        assert response.status_code == 204

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 0

    @pytest.mark.parametrize(
        'records_dict',
        [
            (
                [
                    {
                        'username': 'haljordan',
                        'original_link': 'https://www.osnews.com',
                        'name': 'www.osnews.com',
                    },
                    {
                        'username': 'haljordan',
                        'original_link': 'https://www.gnome.org',
                        'name': 'www.gnome.org',
                    },
                    {
                        'username': 'haljordan',
                        'original_link': 'https://tools.suckless.org',
                        'name': 'tools.suckless.org',
                    },
                ]
            )
        ],
    )
    def test_links_delete_all_for_existing_user(
        self, setup_user_instances, records_dict
    ):
        ids = []
        for record in records_dict:
            user = User.objects.filter(username=record['username']).first()
            client = self.authenticated_api_client(user=user)
            response = client.post(
                '/core/api/links/',
                data={
                    'original_link': record['original_link'],
                    'user': user.id,
                },
            )
            assert response.status_code == 201
            ids.append(response.json()['id'])

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 3

        for link_id in ids:
            response = client.delete(f'/core/api/links/{link_id}/')
            assert response.status_code == 204

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 0

    @pytest.mark.parametrize(
        'records_dict',
        [
            (
                [
                    {
                        'username': 'haljordan',
                        'original_link': 'https://www.osnews.com',
                        'name': 'www.osnews.com',
                    },
                    {
                        'username': 'haljordan',
                        'original_link': 'https://www.gnome.org',
                        'name': 'www.gnome.org',
                    },
                    {
                        'username': 'haljordan',
                        'original_link': 'https://tools.suckless.org',
                        'name': 'tools.suckless.org',
                    },
                ]
            )
        ],
    )
    def test_links_delete_all_endpoint_should_not_be_possible(
        self, setup_user_instances, records_dict
    ):
        for record in records_dict:
            user = User.objects.filter(username=record['username']).first()
            client = self.authenticated_api_client(user=user)
            response = client.post(
                '/core/api/links/',
                data={
                    'original_link': record['original_link'],
                    'user': user.id,
                },
            )
            assert response.status_code == 201

        response = client.get('/core/api/links/')
        json_response = response.json()
        assert json_response['count'] == 3

        response = client.delete('/core/api/links/')
        assert response.status_code == 405
