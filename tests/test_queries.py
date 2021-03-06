import requests

from common import URL, GRAPHQL_URL, graph_query

def test_query_pastes():
    query = '''
    query {
      pastes {
        id
        ipAddr
        ownerId
        burn
        owner {
            id
            name
        }
        title
        content
        userAgent
      }
    }
    '''
    r = graph_query(GRAPHQL_URL, query)

    assert r.json()['data']['pastes'][0]['id']
    assert r.json()['data']['pastes'][0]['ipAddr'] == '127.0.0.1'
    assert r.json()['data']['pastes'][0]['ownerId'] == 1
    assert r.json()['data']['pastes'][0]['burn'] == False
    assert r.json()['data']['pastes'][0]['owner']['id'] == '1'
    assert r.json()['data']['pastes'][0]['owner']['name'] == 'DVGAUser'
    assert r.json()['data']['pastes'][0]['title']
    assert r.json()['data']['pastes'][0]['userAgent']
    assert r.json()['data']['pastes'][0]['content']

def test_query_paste_by_id():
    query = '''
    query {
      paste (id: 1) {
        id
        ipAddr
        ownerId
        burn
        owner {
            id
            name
        }
        title
        content
        userAgent
      }
    }
    '''
    r = graph_query(GRAPHQL_URL, query)

    assert r.json()['data']['paste']['id'] == '1'
    assert r.json()['data']['paste']['ipAddr'] == '127.0.0.1'
    assert r.json()['data']['paste']['ownerId'] == 1
    assert r.json()['data']['paste']['burn'] == False
    assert r.json()['data']['paste']['owner']['id'] == '1'
    assert r.json()['data']['paste']['owner']['name'] == 'DVGAUser'
    assert r.json()['data']['paste']['title']
    assert r.json()['data']['paste']['userAgent'] == 'User-Agent not set'
    assert r.json()['data']['paste']['content']

def test_query_systemHealth():
    query = '''
        query {
           systemHealth
        }
    '''
    r = graph_query(GRAPHQL_URL, query)
    assert 'System Load' in r.json()['data']['systemHealth']
    assert '.' in r.json()['data']['systemHealth'].split('System Load: ')[1]

def test_query_systemUpdate():
    pass

def test_query_systemDebug():
    query = '''
        query {
           systemDebug
        }
    '''
    r = graph_query(GRAPHQL_URL, query)
    assert r.status_code == 200
    assert 'tty' in r.json()['data']['systemDebug'].lower()

def test_query_users():
    query = '''
        query {
           users {
               id
               username
           }
        }
    '''

    r = graph_query(GRAPHQL_URL, query)
    assert r.status_code == 200
    assert len(r.json()['data']['users']) > 1

def test_query_read_and_burn():
    query = '''
        query {
            readAndBurn(id: 155){
                id
            }
        }
    '''
    r = graph_query(GRAPHQL_URL, query)
    assert r.status_code == 200
    assert r.json()['data']['readAndBurn'] == None

def test_query_search_on_user_object():
    query = '''
        query {
         search(keyword:"operator") {
            ... on UserObject {
                username
                id
              }
          }
        }
    '''

    r = graph_query(GRAPHQL_URL, query)
    assert r.status_code == 200
    assert r.json()['data']['search'][0]['username'] == 'operator'
    assert r.json()['data']['search'][0]['id']


def test_query_search_on_paste_object():
    query = '''
        query {
            search {
                ... on PasteObject {
                owner {
                    name
                    id
                }
                title
                content
                id
                ipAddr
                burn
                ownerId
                }
            }
        }
    '''

    r = graph_query(GRAPHQL_URL, query)
    assert r.status_code == 200
    assert len(r.json()['data']['search']) > 0
    assert r.json()['data']['search'][0]['owner']['id']
    assert r.json()['data']['search'][0]['title']
    assert r.json()['data']['search'][0]['content']
    assert r.json()['data']['search'][0]['id']
    assert r.json()['data']['search'][0]['ipAddr']
    assert r.json()['data']['search'][0]['burn'] == False
    assert r.json()['data']['search'][0]['ownerId']

def test_query_audits():
    query = '''
       query {
            audits {
                id
                gqloperation
                gqlquery
                timestamp
            }
        }
    '''

    r = graph_query(GRAPHQL_URL, query)
    assert r.status_code == 200
    assert len(r.json()['data']['audits']) > 0
    assert r.json()['data']['audits'][0]['id']
    assert r.json()['data']['audits'][0]['gqloperation']
    assert r.json()['data']['audits'][0]['gqlquery']
    assert r.json()['data']['audits'][0]['timestamp']